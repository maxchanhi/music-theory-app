from config import users_collection
import streamlit as st
from datetime import datetime
import uuid

def sign_up():
    st.title("User Registration")

    with st.form("registration_form"):
        user_name = st.text_input("Username")
        user_password = st.text_input("Password", type="password")
        email = st.text_input("Email")
        exam_date = st.date_input("Exam Date")
        
        submitted = st.form_submit_button("Register")

        if submitted:
            if user_name and user_password and email:
                user_id = str(uuid.uuid4())
                user_details = {
                    "user_id": user_id,
                    "user_name": user_name,
                    "user_password": user_password,
                    "create_date": datetime.now().strftime("%Y-%m-%d"),
                    "exam_date": exam_date.strftime("%Y-%m-%d"),
                    "email": email
                }
                users_collection.insert_one(user_details)
                st.success("User registered successfully!")
                return True
            else:
                st.error("All fields are required!")