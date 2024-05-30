import streamlit as st
from time_signature import generate_question
if "pressed_ts" not in st.session_state:
    st.session_state.pressed_ts = False
if "question_data_ts" not in st.session_state:
    st.session_state.question_data_ts = generate_question()
# Streamlit app
question_data,correct_answer=st.session_state.question_data
st.title("Rhythm Quiz")
st.write(question_data)
if st.button("New Question"):
    st.session_state.pressed_ts = False
    st.session_state.question_data_ts = generate_question()
    st.rerun()
# User input
user_answer = st.text_input("Your Answer:")

# Check answer
if st.button("Submit", disabled= st.session_state.pressed_ts):
    try:
        st.session_state.pressed_ts = True
        user_answer = str(user_answer)
        if user_answer == str(correct_answer):
            st.success("Correct!")
        else:
            st.error(f"Incorrect. The correct answer is {correct_answer}.")
    except:
        st.error("Please enter a valid number.")

# Button to generate a new question
