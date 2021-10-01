from bson import ObjectId
from bson.json_util import dumps, loads
from datetime import datetime, timedelta
from encoder import JSONEncoder
from flask import Flask, jsonify, render_template, redirect, request, Response, session, url_for
from flask_mongoengine import MongoEngine
from flask_cors import CORS
from pymongo import MongoClient
import bcrypt, bson, json, jwt, os, pprint

# Fixed Variables
API_BASE_URL = "/api/v1"
BASE_DIR = os.getcwd()
DB_URI = None

# Flask Application
app = Flask(__name__)

# Secret Key
if "SECRET_KEY" in os.environ:
    app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
else:
    AppCredentialsFile = open(os.path.join(BASE_DIR, "credentials", "AppCredentials.json"))
    AppCredentials = json.load(AppCredentialsFile)
    app.config["SECRET_KEY"] = AppCredentials["secret_key"]

# Cross Origin Resource Sharing
CORS(app)

# Read Credentials From Json
if ("MONGODB_USERNAME" in os.environ) and ("MONGODB_PASSWORD" in os.environ) and ("MONGODB_CLUSTER_URL" in os.environ):
    # Hosted Mongo Client
    DB_URI = "mongodb+srv://{0}:{1}@{2}".format(os.environ["MONGODB_USERNAME"], os.environ["MONGODB_PASSWORD"], os.environ["MONGODB_CLUSTER_URL"])
else:
    MongoDBCredentialsFile = open(os.path.join(BASE_DIR, "credentials", "MongoDBCredentials.json"))
    MongoDBCredentials = json.load(MongoDBCredentialsFile)
    # Hosted Mongo Client
    DB_URI = "mongodb+srv://{0}:{1}@{2}".format(MongoDBCredentials["username"], MongoDBCredentials["password"], MongoDBCredentials["clusterURL"])

app.config['MONGODB_HOST'] = DB_URI
db = MongoEngine(app)