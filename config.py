import os
from pymongo import MongoClient
import streamlit as st
import certifi

MONGO_URI = st.secrets["MONGO_URI"]
DB_NAME = 'users'

client = MongoClient(MONGO_URI, 
                    tlsCAFile=certifi.where())
db = client[DB_NAME]
users_collection = db['login']