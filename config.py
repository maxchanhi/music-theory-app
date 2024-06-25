import os
from pymongo import MongoClient

MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017')
DB_NAME = 'users'

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
users_collection = db['login']