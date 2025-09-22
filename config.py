import pymongo
import streamlit as st
import os
from dotenv import load_dotenv
from pymongo import MongoClient
import certifi

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = 'users'

# User collection
# Connect to MongoDB
client = MongoClient(MONGO_URI, 
                    tlsCAFile=certifi.where())
db = client[DB_NAME]
users_collection = db['login']