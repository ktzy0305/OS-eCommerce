from base import *
from classes import *
import re

"""
> Web Page Routes
Contains the routes that define each webpage in the web application.
"""
@app.route('/')
def index():
    return render_template("home.html",
                            featured_products=[1,2,3,4,5],
                            new_products=[1,2,3,4,5], 
                            best_selling_products=[1,2,3,4,5], 
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
            else:
                return render_template("login.html")
    else:
        return redirect(url_for("index"))

@app.route('/logout')
def logout():
    if session.get("user") is not None:
        session.pop("shopping_cart", None)
        session.pop("user", None)
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
    category_name = request.args.get('category_name') 
    category = Category.objects(name=category_name).first()
    products = Product.objects(category=category)
    return render_template('product/search.html', products=products, category=category)

@app.route('/products/<string:product_id>')
def product_info(product_id):
    product = Product.objects(id=product_id).first()
    return render_template("product/details.html", product=product)

@app.route('/shoppingcart')
def shopping_cart():
    if session.get("user") is None:
        return redirect(url_for("index"))
    else:
        if session.get("shopping_cart") is None:
            session["shopping_cart"] = []
            session["total_price"] = 0
        return render_template("shoppingcart.html")

@app.route('/addtocart', methods=['POST'])
def add_to_cart():
    # Check if shopping cart session is empty
    if session.get("shopping_cart") is None:
        session["shopping_cart"] = []
        session["total_price"] = 0

    # Product information to be added into cart
    product_id = request.form["product_id"]
    quantity = request.form["quantity"]
    product = Product.objects(id=product_id).first()

    shopping_cart = session["shopping_cart"]

    existing_product_found = False
    for item in shopping_cart:
        if item[0]['_id']['$oid'] == product_id:
            current_quantity = item[1]
            item[1] = current_quantity + int(quantity)
            existing_product_found = True
            break

    if not existing_product_found:
        shopping_cart.append([product, int(quantity)])
    
    session["shopping_cart"] = shopping_cart
    session["total_price"] = sum([item[0]["price"]*item[1] for item in shopping_cart])
    return redirect(url_for("shopping_cart"))

@app.route('/userprofile')
def user_profile():
    return render_template("profile.html")




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

if __name__ == "__main__":
    app.run()