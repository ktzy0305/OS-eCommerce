from logging import error
from os import name

from mongoengine import errors
from base import *
from classes import *
import re

"""
> Web Page Routes
Contains the routes that define each webpage in the web application.
"""
@app.route('/')
def index():
    if session.get("user"):
        user = User.objects(id=session.get("user")["_id"]["$oid"]).first()
        session["shopping_cart"] = user.shopping_cart

    new_products = Product.objects().order_by('-date_created')[:8]

    return render_template("home.html",
                            featured_products=[1,2,3,4,5,6,7,8,9,10],
                            new_products=new_products, 
                            best_selling_products=[1,2,3,4,5,6,7,8,9,10], 
                            all_products=Product.objects())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get("user") is None:
        if request.method == 'POST':
            email = request.form.get("email")
            password = request.form.get("password")
            if email == "" or password == "":
                return render_template("login.html", error="Please enter your email and/or password.")
            user = User.objects(email=email).first()
            if user is None:
                return render_template("login.html", error="Email and/or password is invalid.")
            else:
                if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                    session["user"] = user
                    return redirect(url_for("index"))
                else:
                    return render_template("login.html", 
                                            error="Email and/or password is invalid.")
        else:
            if 'registration_success' in request.args:
                registration_success = request.args['registration_success']
                return render_template("login.html", registration_success=registration_success)
            elif 'checkout_msg' in request.args:
                checkout_msg = request.args['checkout_msg']
                return render_template("login.html", checkout_msg=checkout_msg)
            else:
                return render_template("login.html")
    else:
        return redirect(url_for("index"))

@app.route('/logout')
def logout():
    if session.get("user") is not None:
        session.pop("user", None)
        session.pop("shopping_cart", None)
        session.pop("total_price", None)
    return redirect(url_for("index"))
        
@app.route('/register', methods=['GET', 'POST'])
def register():
    if session.get("user") is None:
        if request.method == 'POST':
            errors = {}
            name = request.form.get("name")
            email = request.form.get("email")
            password = request.form.get("password")
            confirm_password = request.form.get("password2")
            if name == "":
                errors["name_error"] = "Name cannot be empty!"
            if email == "":
                errors["email_error"] = "Email cannot be empty!"
            else:
                if not re.search('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', email):
                    errors["email_error"] = "Invalid email format!"
                else:
                    existing_user = User.objects(email=email).first()
                    if existing_user:
                        errors["email_error"] = "Email is already taken!"
            if password == "":
                errors["password_error"] = "Password cannot be empty!"
            else:
                if not re.search('^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])[A-z0-9?!@#$%^&*()]{8,}$', password):
                    errors["password_error"] = "Password must contain a minimum of eight characters, with at least one uppercase letter, one lowercase letter and one number. These are the allowable symbols: ?!@#$%^&*()"
            if confirm_password == "":
                errors["confirm_password_error"] = "Confirm Password cannot be empty!"
            else:
                if not (password == confirm_password):
                    errors["confirm_password_error"] = "The password entered does not match the one above."
            if len(errors) == 0:
                password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                new_user = User(email=email, password=password_hash, name=name)
                new_user.save()
                return redirect(url_for("login", registration_success="Account successfully registered!"))
            else:
                return render_template("register.html", errors=errors)
        else:
            return render_template("register.html")
    else:
        return redirect(url_for("index"))

@app.route('/categories')
def category():
    return render_template("category.html",
                           categories=Category.objects())

@app.route('/products/search')
def product_search():
    query = request.args.get('query')
    category_name = request.args.get('category_name') 
    if query:
        products = Product.objects.filter(title__icontains=query)
        return render_template('product/search.html', products=products, query=query)
    else:
        category = Category.objects(name=category_name).first()
        products = Product.objects(category=category)
        return render_template('product/search.html', products=products, category=category)

@app.route('/products/<string:product_id>')
def product_info(product_id):
    product = Product.objects(id=product_id).first()
    if 'error_message' in  request.args:
        error_message = request.args['error_message']
        return render_template("product/details.html", product=product, error_message=error_message)
    else:
        return render_template("product/details.html", product=product)

@app.route('/cart')
def shopping_cart():
    # Initialize shopping cart session variable if it is not initialized
    if session.get("shopping_cart") is None:
        session["shopping_cart"] = []


    # If user is logged in, get their shopping cart stored in DB.
    if session.get("user"):
        user = User.objects(id=session.get("user")["_id"]["$oid"]).first()
        session["shopping_cart"] = user.shopping_cart
    
    session["total_price"] = sum([item["total_amount"] for item in session["shopping_cart"]]) if len(session["shopping_cart"]) > 0 else 0


    # Get remaining stock of products
    items_quantity_remaining = []
    for item in session["shopping_cart"]:
        if session.get("user"):
            items_quantity_remaining.append(item["product"]["quantity"])
        else:
            product = Product.objects(id=item["product"]["$oid"]).first()
            items_quantity_remaining.append(product["quantity"])

    return render_template("shoppingcart.html", items_quantity_remaining = items_quantity_remaining)

@app.route('/cart/add', methods=['POST'])
def add_to_cart():
    # Product information to be added into cart
    product_id = request.form["product_id"]
    quantity = request.form["quantity"]
    product_to_add = Product.objects(id=product_id).first()

    # Check if product has enough stock left
    if product_to_add.quantity < int(quantity):
        error_message = "Sorry, there is insufficient quantity available for this product."
        return redirect(url_for("product_info", product_id=product_id, error_message = error_message))
    
    # Check if user is logged in
    if session.get("user") is None:
        if session.get("shopping_cart") is None:
            session["shopping_cart"] = []

        shopping_cart = session["shopping_cart"]
        
        for item in shopping_cart:
            if item["product"]['$oid'] == product_id:
                current_quantity = item["quantity"]
                new_quantity = current_quantity + int(quantity)
                item["quantity"] = new_quantity
                item["total_amount"] = item["price"] * new_quantity
                session["shopping_cart"] = shopping_cart
                break
      
        else:
            shopping_cart = session["shopping_cart"]
            product_to_add = CartProduct(
                    product=product_to_add, 
                    title=product_to_add["title"], 
                    price=product_to_add["price"],
                    image_url = product_to_add["image_url"],
                    quantity=int(quantity),
                    total_amount = product_to_add["price"] * int(quantity)
            )
            shopping_cart.append(product_to_add)
        session["shopping_cart"] = shopping_cart
        session["total_price"] = sum([item["total_amount"] for item in shopping_cart]) if len(shopping_cart) > 0 else 0
        return redirect(url_for("shopping_cart"))
    
    else:
        # Get User
        user = User.objects(id=session.get("user")["_id"]["$oid"]).first()

        # Check if the product to add already exist in cart, if exists add to current quantity.
        for item in user.shopping_cart:
            if item["product"].id == product_to_add.id:
                current_quantity = item["quantity"]
                new_quantity = current_quantity + int(quantity)
                item["quantity"] = new_quantity
                item["total_amount"] = item["price"] * new_quantity
                user.save()
                break

        else:
            product_to_add = CartProduct(
                    product=product_to_add, 
                    title=product_to_add["title"], 
                    price=product_to_add["price"],
                    image_url = product_to_add["image_url"],
                    quantity=int(quantity),
                    total_amount = product_to_add["price"] * int(quantity)
            )
            user.shopping_cart.append(product_to_add)
            user.save()
        
        session["shopping_cart"] = user.shopping_cart
        session["total_price"] = sum([item["total_amount"] for item in user.shopping_cart]) if len(user.shopping_cart) > 0 else 0
        return redirect(url_for("shopping_cart"))

@app.route('/cart/update', methods=["POST"])
def update_cart():
    # Information to be updated
    product_id = request.form["product_id"]
    product_to_modify = Product.objects(id=product_id).first()
    new_product_quantity = request.form["product_quantity"]

    if new_product_quantity == "":
        return redirect(url_for("shopping_cart"))

    # Check if user is logged in
    if session.get("user") is None:
        shopping_cart = session["shopping_cart"]

        for item in shopping_cart:
            if item["product"]['$oid'] == product_id:
                item["quantity"] = int(new_product_quantity)
                item["total_amount"] = item["price"] * int(new_product_quantity)
                break
        session["shopping_cart"] = shopping_cart
        session["total_price"] = sum([item["total_amount"] for item in shopping_cart]) if len(shopping_cart) > 0 else 0
    else:
        # Get User
        user = User.objects(id=session.get("user")["_id"]["$oid"]).first()

        # Update the quantity of the product in cart
        for item in user.shopping_cart:
            if item["product"].id == product_to_modify.id:
                item["quantity"] = int(new_product_quantity)
                item["total_amount"] = item["price"] * int(new_product_quantity)
                user.save()
                break
        session["shopping_cart"] = user.shopping_cart
        session["total_price"] = sum([item["total_amount"] for item in user.shopping_cart]) if len(user.shopping_cart) > 0 else 0

    return redirect(url_for("shopping_cart"))


@app.route('/cart/remove/<string:product_id>')
def remove_from_cart(product_id):
    # Check if user is logged in
    if session.get("user") is None:
        shopping_cart = session["shopping_cart"]

        # Find item to remove
        for item in shopping_cart:
            if item["product"]['$oid'] == product_id:
                shopping_cart.remove(item)
                break
    
        session["shopping_cart"] = shopping_cart
        session["total_price"] = sum([item["total_amount"] for item in shopping_cart]) if len(shopping_cart) > 0 else 0

    else:
        # Get User
        user = User.objects(id=session.get("user")["_id"]["$oid"]).first()

        # Product
        product_to_remove = Product.objects(id=product_id).first()

        # Find item to remove
        for item in user.shopping_cart:
            if item["product"].id == product_to_remove.id:
                user.shopping_cart.remove(item)
                user.save()
                break
    
        session["shopping_cart"] = user.shopping_cart
        session["total_price"] = sum([item["total_amount"] for item in user.shopping_cart]) if len(user.shopping_cart) > 0 else 0

    return redirect(url_for("shopping_cart"))

@app.route('/checkout')
def checkout():
    # Check if user is logged in
    if session.get("user") is None:
        checkout_msg = "Please log in or create an account to check out your shopping cart."
        return redirect(url_for("login", checkout_msg=checkout_msg))

    # User
    user = User.objects(id=session.get("user")["_id"]["$oid"]).first()
    checkout_items = user.shopping_cart

    return render_template('checkout.html', checkout_items=checkout_items, user=user)

@app.route('/order/processing')
def place_order():
    # Check if user is logged in
    if session.get("user") is None:
        return redirect(url_for("login"))

    # User
    user = User.objects(id=session.get("user")["_id"]["$oid"]).first()

    # Create Order Object
    order = Order(
        created_by = user,
        date_created = datetime.now(),
        ordered_products = user.shopping_cart,
        total_amount = session.get('total_price'),
        delivery_address = user.address_list[0]
    )

    # Save Order Object
    order.save()

    # Reduce stock of products
    for item in user.shopping_cart:
        product = Product.objects(id=item["product"].id).first()
        product.quantity = product.quantity - item["quantity"]
        product.save()

    # Clear user shopping cart
    del user.shopping_cart

    # Save User State
    user.save()

    # Reset Total Price
    session['total_price'] = 0

    # Pass Order object to order complete page
    return redirect(url_for('order_complete', order_id = order.id))

@app.route('/order/complete')
def order_complete():
    # Check if user is logged in
    if session.get("user") is None:
        return redirect(url_for("login"))

    order_id = request.args['order_id']
    order = Order.objects(id=order_id).first()
    print(order)
    return render_template('ordercomplete.html', order=order)

@app.route('/user/profile')
def user_profile():
    # Check if user is logged in
    if session.get("user") is None:
        return redirect(url_for("login"))

    # User
    user = User.objects(id=session.get("user")["_id"]["$oid"]).first()

    if "pw_change_msg" in request.args:
        pw_change_msg = request.args["pw_change_msg"]
        return render_template("profile.html", user=user, pw_change_msg=pw_change_msg)
    elif "pw_change_errors" in request.args:
        pw_change_errors  = request.args["pw_change_errors"]
        pw_change_errors = pw_change_errors.replace("'", "\"")
        pw_change_errors = json.loads(pw_change_errors)
        return render_template("profile.html", user=user, pw_change_errors=pw_change_errors)
    else:
        return render_template("profile.html", user=user)

@app.route('/user/profile/update', methods=['POST'])
def update_user_profile():
    # Check if user is logged in
    if session.get("user") is None:
        return redirect(url_for("login"))

    # User
    user = User.objects(id=session.get("user")["_id"]["$oid"]).first()

    # Request Form
    name = request.form.get("profile_name")
    gender = request.form.get("gender")
    date_of_birth = request.form.get("date_of_birth")

    # Errors
    errors = {}

    # Checks
    if name == "":
        errors["name_error"] = "Name cannot be empty!"
    if date_of_birth == "":
        errors["date_of_birth_error"] = "Please specify your date of birth!"    

    if len(errors) == 0:
        user.name = name
        user.gender = gender
        user.date_of_birth = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
        user.save()

    return redirect(url_for('user_profile'))

@app.route('/user/address/add', methods=["POST"])
def add_address():
    # Check if user is logged in
    if session.get("user") is None:
        return redirect(url_for("login"))

    # User
    user = User.objects(id=session.get("user")["_id"]["$oid"]).first()
    
    # Address information
    street = request.form["street"]
    unit = request.form["unit"]
    postal_code = request.form["postal_code"]
    country = request.form["country"]
    city = request.form["city"]

    # Create address object
    new_address = Address(
        country = country,
        city = city,
        street = street,
        unit = unit,
        postal_code = postal_code
    )
    # Add to user's address list
    user.address_list.append(new_address)
    user.save()

    return redirect(url_for("user_profile"))

@app.route('/user/address/edit/<string:index>', methods=["POST"])
def edit_address(index):
    # User
    user = User.objects(id=session.get("user")["_id"]["$oid"]).first()

    # Index
    index_to_edit= int(index) - 1

    # Address information
    street = request.form["street"]
    unit = request.form["unit"]
    postal_code = request.form["postal_code"]
    country = request.form["country"]
    city = request.form["city"]

    # Create updated address object
    updated_address = Address(
        country = country,
        city = city,
        street = street,
        unit = unit,
        postal_code = postal_code
    )

    # Update the address
    user.address_list[index_to_edit] = updated_address

    # Save Changes
    user.save()

    return redirect(url_for("user_profile"))

@app.route('/user/address/remove/<string:index>')
def remove_address(index):
    # User
    user = User.objects(id=session.get("user")["_id"]["$oid"]).first()

    # Index
    index_to_remove = int(index) - 1

    # Removal
    del user.address_list[index_to_remove]

    # Save Changes
    user.save()

    return redirect(url_for("user_profile"))

@app.route('/user/account/changepassword', methods=["POST"])
def change_password():
    # Check if user is logged in
    if session.get("user") is None:
        return redirect(url_for("login"))

    # User
    user = User.objects(id=session.get("user")["_id"]["$oid"]).first()

    # Form Information
    current_password = request.form.get("current_password")
    new_password = request.form.get("new_password")
    new_password_2 = request.form.get("new_password_2")

    # Check empty
    check_empty = lambda data : True if data == "" else False

    # Check password type same
    check_same = (new_password == new_password_2)

    # Errors
    errors = {}

    if check_empty(current_password):
        errors["current_password_error"] = "Password cannot be empty!"
    if check_empty(new_password):
        errors["new_password_error"] = "New password cannot be empty!"
    if check_empty(new_password):
        errors["new_password_2_error"] = "Field cannot be empty!"

    if not bcrypt.checkpw(current_password.encode('utf-8'), user.password.encode('utf-8')):
        errors["current_password_error"] = "Incorrect Password!"
    if not check_same:
        errors["new_password_2_error"] = "Passwords are not the same."

    if len(errors) == 0:
        new_password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        user.password = new_password_hash.decode("utf-8") 
        user.save()

        return redirect(url_for("user_profile", pw_change_msg="Your password has been successfully changed!"))
    else:
        return redirect(url_for("user_profile", pw_change_errors=errors))



@app.route('/user/orders')
def user_orders():
    # Check if user is logged in
    if session.get("user") is None:
        return redirect(url_for("login"))

    # User
    user = User.objects(id=session.get("user")["_id"]["$oid"]).first()

    # Orders made by user
    user_orders = Order.objects(created_by = user)

    return render_template("orders.html", orders = user_orders)


@app.route('/resetpassword')
def reset_password():
    return render_template("reset_password.html")

@app.route('/privacy')
def privacy_policy():
    return render_template("policies/privacy_policy.html")

@app.route('/terms')
def terms_of_service():
    return render_template("policies/terms_of_service.html")

"""
> REST API Routes
Contains the endpoints for mobile applications to perform user functionality
of this web application.
"""
@app.route(API_BASE_URL+'/login', methods=['POST'])
def api_login():
    email = request.args.get("email")
    password = request.args.get("password")
    user = User.objects(email=email).first()
    if user is None:
        return jsonify("User with email {} does not exist.".format(email)), 200
    else:
        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            token = jwt.encode({'user' : user.email, 'exp': datetime.utcnow() + timedelta(minutes=60)}, app.config["SECRET_KEY"])
            return jsonify({'token' : token.decode('UTF-8')}), 200
        else:
            return jsonify("The entered password was invalid.".format(email)), 200

@app.route(API_BASE_URL+'/signup', methods=['POST'])
def api_register():
    data = request.get_json()
    if data is None:
        return jsonify('No data received'), 400
    else:
        existing_user = User.objects(email=data["email"]).first()
        if existing_user is None:
            password_hash = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt())
            new_user = User(email=data["email"], password=password_hash, name=data["name"])
            new_user.save()
            token = jwt.encode({'user' : new_user.email, 'exp': datetime.utcnow() + timedelta(minutes=60)}, app.config["SECRET_KEY"])
            return jsonify({'token' : token.decode('UTF-8')}), 201
        else:
            return jsonify("A user with the email {0} already exists.".format(data["email"])), 200

@app.route(API_BASE_URL+'/user/update/<string:user_id>', methods=['PATCH'])
def api_update_user_details(user_id):
    data = request.get_json()
    user = User.objects.get(id=user_id)
    user.update(__raw__={"$set": data })
    return 'Update Successful!', 204

@app.route(API_BASE_URL+'/user/delete/<string:user_id>', methods=['DELETE'])
def api_delete_user(user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return 'Delete Successful!'.format(), 200

@app.route(API_BASE_URL+'/products', methods=['GET'])
def api_products():
    products = Product.objects
    return jsonify(products), 200

@app.route(API_BASE_URL+'/shoppingcart/<string:user_id>', methods=['GET'])
def api_get_shopping_cart(user_id):
    data = request.get_json()
    user = User.objects.get(id=user_id)
    return jsonify(user.shopping_cart)

"""
Error Handling
"""

# Error 404 - Page Not Found
@app.errorhandler(404)
def page_not_found(e):
    return render_template(
        "errors/page_not_found.html", 
        message="The page you're trying to find does not exist.", 
        page_url=url_for("index"), 
        page_name="Home"
    ), 404

if __name__ == "__main__":
    app.run()