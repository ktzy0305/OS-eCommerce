from bson.json_util import default
from base import db
from datetime import datetime

class Category(db.Document):
    name = db.StringField(required=True, max_length=200)
    image_url = db.StringField(max_length=1000)

class Product(db.Document):
    title = db.StringField(required=True, max_length=200)
    price = db.FloatField(required=True)
    quantity = db.IntField(required=True)
    description = db.StringField(required=True, max_length=2000)
    image_url = db.StringField(max_length=1000)
    category = db.ReferenceField(Category)
    date_created = db.DateTimeField(default=datetime.now())
    featured_on_homepage = db.BooleanField(default=False)

class CartProduct(db.EmbeddedDocument):
    product = db.ReferenceField(Product)
    title = db.StringField(required=True, max_length=200)
    image_url = db.StringField(max_length=1000)
    price = db.FloatField(required=True)
    quantity = db.IntField(required=True)
    total_amount = db.FloatField(required=True)

class Address(db.EmbeddedDocument):
    country = db.StringField(required=True, max_length=200)
    city = db.StringField(required=True, max_length=200)
    street = db.StringField(required=True, max_length=200)
    unit = db.StringField(required=True, max_length=200)
    postal_code = db.StringField(required=True, max_length=200)

class User(db.Document):
    email = db.EmailField(required=True, max_length=100)
    password = db.StringField(required=True, max_length=128)
    name = db.StringField(required=True, max_length=50)
    gender = db.StringField(default="not specified")
    date_of_birth = db.DateTimeField()
    shopping_cart = db.ListField(db.EmbeddedDocumentField(CartProduct))
    address_list = db.ListField(db.EmbeddedDocumentField(Address))
    role = db.StringField(default="USER", required=True, max_length=50)
    registered_on = db.DateTimeField(default=datetime.now())

class Order(db.Document):
    created_by = db.ReferenceField(User)
    date_created = db.DateTimeField(required=True)
    ordered_products = db.ListField(db.EmbeddedDocumentField(CartProduct))
    total_amount = db.FloatField(required=True)
    delivery_address = db.EmbeddedDocumentField(Address)