import streamlit as st
from data_func import login_form, record_feedback_list

def login():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if not st.session_state['logged_in']:
        loginstage = login_form()
        if loginstage:
            return True, st.session_state['user_info']
    return False, None

def feedback_form():
    if 'user_info' not in st.session_state or st.session_state['user_info'] is None:
        st.error("You are not logged in. Please log in to access this content.")
        return

    st.sidebar.title("Welcome")
    st.sidebar.write(f"User: {st.session_state['user_info']['user_name']}")

    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state['user_info'] = None
        st.rerun()

    st.title("Protected Content")
    st.write("This content is only accessible to logged-in users.")
    user_input = st.text_input("Input", key="input_1")
    if st.button("Submit", key="submit_1"):
        user_id = "user_" + st.session_state['user_info']['user_id']
        record_feedback_list(user_id, text=user_input)
        st.success("Submitted!")