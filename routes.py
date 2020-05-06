from base import *
from classes import *

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
                           all_products=[1,2,3,4,5,6,7,8,9,10,11,12])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html", error=False)
    else:
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.objects(email=email, password=password).first()
        if user is not None:
            session["user"] = user
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error=True)

@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for('index'))
        
@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/shoppingcart')
def shopping_cart():
    return render_template("shoppingcart.html")

@app.route('/userprofile')
def user_profile():
    return render_template("profile.html")




"""
> REST API Routes
Contains the endpoints for mobile applications to perform user functionality
of this web application.
"""
@app.route(API_BASE_URL+'/login')
def api_login():
    email = request.args.get("email")
    password = request.args.get("password")
    user = User.objects(email=email, password=password).first()
    if user is None:
        return jsonify("Login Unsuccessful"), 200
    else:
        token = jwt.encode({'user' : user.email, 'exp': datetime.utcnow() + timedelta(minutes=60)}, app.config["SECRET_KEY"])
        return jsonify({'token' : token.decode('UTF-8')}), 200

@app.route(API_BASE_URL+'/signup', methods=['POST'])
def api_register():
    data = request.get_json()
    if data is None:
        return Response(400)
    else:
        new_user = User(email=data["email"], password=data["password"], name=data["name"])
        new_user.save()
        token = jwt.encode({'user' : new_user.email, 'exp': datetime.utcnow() + timedelta(minutes=60)}, app.config["SECRET_KEY"])
        return jsonify({'token' : token.decode('UTF-8')}), 201

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

if __name__ == "__main__":
    app.run()