from config import users_collection
import streamlit as st
import time
from bson import ObjectId
ss= st.session_state

def login_form():
    if "user_info" not in ss:
        ss.user_info = None
    username = st.text_input("Username",key="form_userName")
    password = st.text_input("Password", type="password",key="form_pass")
    submitted = st.button("Login")

    if submitted:
        is_valid, user_info = verify_user(username, password)
        if is_valid:
            ss.login = True
            st.session_state['user_info'] = user_info
            return True
        else:
            return False

def load_users():
    try:
        return list(users_collection.find())
    except Exception as e:
        print(f"load_users failed: {e}")
        return []


def verify_user(username, password):
    try:
        user = users_collection.find_one({"user_name": username, "user_password": password})
        return (True, user) if user else (False, None)
    except Exception as e:
        print(f"verify_user failed: {e}")
        return (False, None)

from datetime import datetime
from bson import ObjectId


def get_feedback(userid):
    try:
        if userid.startswith('user_'):
            userid = userid[5:]
        
        feedback_collection = users_collection.database.feedback
        feedback = feedback_collection.find({"user_id": userid}).sort("date", -1)
        
        feedback_list = list(feedback)
        print(f"Retrieved {len(feedback_list)} feedback entries for user {userid}")
        return feedback_list
    except Exception as e:
        print(f"get_feedback failed: {e}")
        return []

def setup_database():
    try:
        feedback_collection = users_collection.database.feedback
        feedback_collection.create_index([("user_id", 1), ("date", -1)])
    except Exception as e:
        print(f"setup_database failed: {e}")


def record_feedback(subject, text):
    try:
        user_id = ss.user_info['user_id']
        text = str(text)
        if user_id.startswith('user_'):
            user_id = user_id[5:]

        current_date = datetime.now()

        feedback_entry = {
            "user_id": user_id,
            "date": current_date,
            "subject": subject,
            "details": text
        }

        feedback_collection = users_collection.database.feedback
        result = feedback_collection.insert_one(feedback_entry)
        if result.inserted_id:
            # Update the user document with a reference to the feedback
            users_collection.update_one(
                {"user_id": user_id},
                {"$push": {"feedback_refs": result.inserted_id}}
            )
            return True
        else:
            return False
    except Exception as e:
        print(f"record_feedback failed: {e}")
        return False