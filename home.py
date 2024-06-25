import streamlit as st
from create_ac import sign_up
from app_login import login, feedback_form
import time

def init_session_state():
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = 'login'
    if 'login_stage' not in st.session_state:
        st.session_state['login_stage'] = False
    if 'user_info' not in st.session_state:
        st.session_state['user_info'] = None
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

def main():
    init_session_state()
    
    if st.session_state['current_page'] == 'login' or not st.session_state['logged_in']:
        col1, col2 = st.columns([4,1])
        with col1:
            if st.button("Sign up"):
                st.session_state['current_page'] = 'sign_up'
        with col2:
            if st.button("Login"):
                st.session_state['current_page'] = 'login'
    
    if st.session_state['current_page'] == 'sign_up':
        handle_signup()
    elif st.session_state['current_page'] == 'login':
        handle_login()
    elif st.session_state['current_page'] == 'feedback' and st.session_state['logged_in']:
        feedback_form()
    else:
        st.warning("Please log in to access the content.")
def handle_signup():
    signed = sign_up()
    if signed:
        time.sleep(1)
        st.session_state['login_stage'] = True
        st.session_state['current_page'] = 'feedback'
        st.rerun()

def handle_login():
    login_successful, user_info = login()
    if login_successful:
        st.session_state['login_stage'] = True
        st.session_state['logged_in'] = True
        st.session_state['user_info'] = user_info
        st.session_state['current_page'] = 'feedback'
        st.rerun()
    else:
        st.session_state['login_stage'] = False
        st.session_state['logged_in'] = False
        st.session_state['user_info'] = None

if __name__ == "__main__":
    main()