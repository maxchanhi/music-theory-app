import streamlit as st
from duration_equation.time_signature import generate_question
from streamlit_extras.let_it_rain import rain
from urls import fun_emoji_list 
import random
def main_ts():
    if "pressed_ts" not in st.session_state:
        st.session_state.pressed_ts = False
    if "question_data_ts" not in st.session_state:
        st.session_state.question_data_ts = generate_question()
    # Streamlit app
    question_data,correct_answer=st.session_state.question_data_ts
    st.title("Calculation for time signature")
    st.subheader(question_data)
    if st.button("New Question"):
        st.session_state.pressed_ts = False
        st.session_state.question_data_ts = generate_question()
        st.rerun()
    # User input
    user_answer = st.text_input("Your Answer:")
    
    # Check answer
    if st.button("Submit", disabled= st.session_state.pressed_ts) and user_answer:
        st.session_state.pressed_ts = True
        user_answer = str(user_answer)
        if user_answer == str(correct_answer):
            emo = random.choice(fun_emoji_list)
            st.success("Correct!")
            st.balloons()
            rain(emo,animation_length=1)
           
