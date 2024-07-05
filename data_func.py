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
    return list(users_collection.find())

def verify_user(username, password):
    user = users_collection.find_one({"user_name": username, "user_password": password})
    return (True, user) if user else (False, None)

from datetime import datetime
from bson import ObjectId


def get_feedback(userid):
    if userid.startswith('user_'):
        userid = userid[5:]
    
    feedback_collection = users_collection.database.feedback
    feedback = feedback_collection.find({"user_id": userid}).sort("date", -1)
    
    feedback_list = list(feedback)
    print(f"Retrieved {len(feedback_list)} feedback entries for user {userid}")
    return feedback_list
def setup_database():
    feedback_collection = users_collection.database.feedback
    feedback_collection.create_index([("user_id", 1), ("date", -1)])

def record_feedback(subject, text):
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