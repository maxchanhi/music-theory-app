from pymongo import MongoClient
import os
from config import MONGO_URI, DB_NAME, client,db, users_collection
def list_all_users():
    print("List of all users:")
    print("-----------------")
    
    for user in users_collection.find():
        print(f"User document: {user}")
        print("-----------------")



if __name__ == "__main__":
    list_all_users()
    client.close()