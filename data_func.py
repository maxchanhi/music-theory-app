from config import users_collection
import streamlit as st
import time
from bson import ObjectId

def login_form():
    st.title("Login")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            is_valid, user_info = verify_user(username, password)
            if is_valid:
                st.session_state['logged_in'] = True
                st.session_state['user_info'] = user_info
                st.success("Login successful!")
                time.sleep(1)
                return True
            else:
                st.error("Invalid username or password")
def load_users():
    return list(users_collection.find())

def verify_user(username, password):
    user = users_collection.find_one({"user_name": username, "user_password": password})
    return (True, user) if user else (False, None)

def record_feedback_list(user_id, text):
    if user_id.startswith('user_'):
        user_id = user_id[5:]
    
    current_date = time.strftime("%m-%d", time.localtime())
    
    # Find the user
    user = users_collection.find_one({"user_id": user_id})
    
    if user and 'Feedback' in user:
        # Check if there's an existing feedback for the current date
        existing_feedback = None
        for feedback in user['Feedback']:
            if current_date in feedback:
                existing_feedback = feedback[current_date]
                break
        
        if existing_feedback:
            # Update existing feedback for the current date
            updated_text = f"{existing_feedback} {text}"
            users_collection.update_one(
                {"user_id": user_id, f"Feedback.{current_date}": {"$exists": True}},
                {"$set": {f"Feedback.$.{current_date}": updated_text}}
            )
        else:
            # Add new feedback entry for the current date
            users_collection.update_one(
                {"user_id": user_id},
                {"$push": {"Feedback": {current_date: text}}}
            )
    else:
        # Create Feedback array and add the first entry
        users_collection.update_one(
            {"user_id": user_id},
            {"$set": {"Feedback": [{current_date: text}]}},
            upsert=True
        )

def get_feedback(userid):
    if userid.startswith('user_'):
        userid = userid[5:]
    user = users_collection.find_one({"user_id": userid})
    return user.get('Feedback', []) if user else []