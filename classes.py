from base import db
from datetime import datetime

class Category(db.Document):
    name = db.StringField(required=True, max_length=200)
    image_url = db.StringField(max_length=1000)

class Product(db.Document):
    title = db.StringField(required=True, max_length=200)
    price = db.FloatField(required=True)
    description = db.StringField(required=True, max_length=1000)
    image_url = db.StringField(default="", max_length=1000)
    category = db.ReferenceField(Category)

class User(db.Document):
    email = db.EmailField(required=True, max_length=100)
    password = db.StringField(required=True, max_length=128)
    name = db.StringField(required=True, max_length=50)
    role = db.StringField(default="USER", required=True, max_length=50)
    registered_on = db.DateTimeField(default=datetime.now())