from bson import ObjectId
from bson.json_util import dumps, loads
from datetime import datetime
from encoder import JSONEncoder
from flask import Flask, jsonify, render_template, request, Response
from flask_cors import CORS
from models import User
from pymongo import MongoClient
import bson, json, os, pprint

# Flask Application
app = Flask(__name__)
# Cross Origin Resource Sharing
CORS(app)
# Read Credentials From Json
base_dir = os.getcwd()
MongoDBCredentialsFile = open(os.path.join(base_dir, "MongoDBCredentials.json"))
MongoDBCredentials = json.load(MongoDBCredentialsFile)
# Hosted Mongo Client
client = MongoClient("mongodb+srv://{0}:{1}@{2}".format(MongoDBCredentials["username"], MongoDBCredentials["password"], MongoDBCredentials["clusterURL"]))
# Using Test Database
db = client["shopify"]
# Current User
CurrentUser = None
# API Base URL
API_BASE_URL = "/api/v1"

def main():
    seed_users()
    user = login_user(email="david@gmail.com", password="password123")
    if user is not None:
        print("Login Successful!")
        CurrentUser = user
        print(user)
    else:
        print("Login Unsuccessful!")

def seed_users():
    users = [
        {
            "name" : "Bob",
            "email" : "bob@gmail.com",
            "password" : "password123",
        },
        {
            "name" : "David",
            "email" : "david@gmail.com",
            "password" : "password123",
        },
        {
            "name" : "Frank",
            "email" : "frank@gmail.com",
            "password" : "password123",
        },
    ]
    users_collection = db["users"]
    if users_collection.count_documents({}) == 0:
        result = users_collection.insert_many(users)
        print(result.inserted_ids)
    else:
        print("User collection has been seeded.")

def login_user(email, password):
    users_collection = db["users"]
    user = users_collection.find_one({"email" : email, "password" : password,})
    return user

def signup_user(user):
    users_collection = db["users"]
    user_id =  users_collection.insert_one(user).inserted_id
    return user_id

def update_user(user_id, data):
    users_collection = db["users"]
    users_collection.update_one({"_id" : ObjectId(user_id)}, { "$set": data })

def delete_user_by_id(user_id):
    users_collection = db["users"]
    users_collection.delete_one({"_id" : ObjectId(user_id)})

# Page Routes
@app.route('/')
def index():
    return render_template("home.html")

@app.route('/login')
def login():
    return render_template("login.html")

# API Routes
@app.route(API_BASE_URL+'/login')
def api_login():
    email = request.args.get("email")
    password = request.args.get("password")
    user = login_user(email=email, password=password)
    if user is None:
        return jsonify("Login Unsuccessful"), 200
    else:
        return json.loads(JSONEncoder().encode(user)), 200

@app.route(API_BASE_URL+'/signup', methods=['POST'])
def api_register():
    data = request.get_json()
    if data is None:
        return Response(400)
    else:
        user_id = signup_user(user=data)
        encoded_user_id = JSONEncoder().encode(user_id)
        return jsonify(str(user_id)), 201

@app.route(API_BASE_URL+'/user/update/<string:user_id>', methods=['PATCH'])
def api_update_user_details(user_id):
    users_collection = db["users"]
    data = request.get_json()
    update_user(user_id=user_id, data=data)
    return '', 204

@app.route(API_BASE_URL+'/user/delete/<string:user_id>', methods=['DELETE'])
def api_delete_user(user_id):
    users_collection = db["users"]
    delete_user_by_id(user_id=user_id)
    return '', 200

if __name__ == "__main__":
    # main()
    app.run()