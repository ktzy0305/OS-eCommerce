from pymongo import MongoClient
import json, os, pprint

# Create a DB Handler class in future to handle collections and documents 
# in MongoDB

class MongoDBHandler:
    
    def __init__(self, client):
        self.client = client
        super().__init__()
    