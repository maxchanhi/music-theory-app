import streamlit as st
from datetime import datetime
import uuid

ss= st.session_state
def sign_up(users_collection):
    invite_code = st.text_input("Invitation Code")
    invited = True if invite_code in st.secrets["Password"] else False
    if invited:             
        user_name = st.text_input("Username")
        user_password = st.text_input("Password", type="password")
        email = st.text_input("Email")
        exam_date = st.date_input("Exam Date")
    submitted = st.button("Register", disabled= not invited)
    
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
            try:
                result = users_collection.insert_one(user_details)
                if result.inserted_id:
                    ss.user_info=user_details
                    return True
                else:
                    st.error("Failed to insert user details.")
            except Exception as e:
                st.error(f"An error occurred while registering: {e}")
        else:
            st.error("All fields are required!")