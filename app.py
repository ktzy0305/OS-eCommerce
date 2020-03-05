from datetime import datetime
from encoder import JSONEncoder
from flask import Flask, jsonify, request
from pymongo import MongoClient
import json, os, pprint

# Flask Application
app = Flask(__name__)
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

def Main():
    SeedUsers()
    user = AuthenticateUser(username="bobbyboi", password="password123")
    if user is not None:
        print("Login Successful!")
        CurrentUser = user
        print(user)
    else:
        print("Login Unsuccessful!")

def SeedUsers():
    users = [
        {
            "email" : "bob@gmail.com",
            "username" : "bobbyboi",
            "password" : "password123",
        },
        {
            "email" : "david@gmail.com",
            "username" : "beckhamDee",
            "password" : "password123",
        },
        {
            "email" : "frank@gmail.com",
            "username" : "frankenGG",
            "password" : "password123",
        },
    ]
    users_collection = db["users"]
    if users_collection.count_documents({}) == 0:
        result = users_collection.insert_many(users)
        print(result.inserted_ids)
    else:
        print("User collection has been seeded.")

def AuthenticateUser(username, password):
    users_collection = db["users"]
    user = users_collection.find_one({"username" : username, "password" : password,})
    return user

@app.route('/')
def Index():
    return jsonify("Welcome to Shopify API")

@app.route('/login')
def Login():
    username = request.args.get("username")
    password = request.args.get("password")
    user = AuthenticateUser(username=username, password=password)
    return json.loads(JSONEncoder().encode(user))

@app.route('/register')
def Register():
    return
    

if __name__ == "__main__":
    app.run()
    # Main()