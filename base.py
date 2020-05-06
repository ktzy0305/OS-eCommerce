from bson import ObjectId
from bson.json_util import dumps, loads
from datetime import datetime, timedelta
from encoder import JSONEncoder
from flask import Flask, jsonify, render_template, redirect, request, Response, session, url_for
from flask_mongoengine import MongoEngine
from flask_cors import CORS
from pymongo import MongoClient
import bson, json, jwt, os, pprint

# Fixed Variables
API_BASE_URL = "/api/v1"
BASE_DIR = os.getcwd()

# Flask Application
app = Flask(__name__)
# Secret Key
app.config["SECRET_KEY"] = "thisisthesecretkey"
# Cross Origin Resource Sharing
CORS(app)
# Read Credentials From Json
MongoDBCredentialsFile = open(os.path.join(BASE_DIR, "MongoDBCredentials.json"))
MongoDBCredentials = json.load(MongoDBCredentialsFile)
# Hosted Mongo Client
DB_URI = "mongodb+srv://{0}:{1}@{2}".format(MongoDBCredentials["username"], MongoDBCredentials["password"], MongoDBCredentials["clusterURL"])
app.config['MONGODB_HOST'] = DB_URI
db = MongoEngine(app)