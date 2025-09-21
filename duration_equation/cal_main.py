import streamlit as st
from random import randint
from fractions import Fraction
from duration_equation.question import generate_question, correct_ans, question_elements
from urls import rain_emoji
from data_func import record_feedback

def bn_callback():
    st.session_state.pressed_cd = True

def generate_new_question(hard_mode, simple_dotted, double_dotted, previous_question):
    duration, dotted_variation = question_elements(hard_mode, simple_dotted, double_dotted)
    small_dur, question_dur, question_dotted, dotted_time, new_question_tuple = generate_question(duration, dotted_variation, previous_question)
    correct = correct_ans(small_dur, question_dur, dotted_time)
    new_question = (small_dur, question_dur, question_dotted, dotted_time, correct)
    return new_question, new_question_tuple

def duration_cal_main():
    st.title("Music Duration Quiz")

    if 'question_history_cd' not in st.session_state:
        st.session_state.question_history_cd = []
    
    if 'previous_question_cd' not in st.session_state:
        st.session_state.previous_question_cd = None

    col1, col2, col3 = st.columns(3)
    with col1:
        hard_mode = st.checkbox("Hard mode")    
    with col2:
        simple_dotted = st.checkbox("Dotted", value=True)
    with col3:
        double_dotted = st.checkbox("Double dotted")

    if 'questioncd' not in st.session_state:
        new_question, new_prev_q_tuple = generate_new_question(hard_mode, simple_dotted, double_dotted, st.session_state.previous_question_cd)
        st.session_state['questioncd'] = new_question[:4]
        st.session_state['correctcd'] = new_question[4]
        st.session_state.previous_question_cd = new_prev_q_tuple
        st.session_state['pressed_cd'] = False

    small_dur, question_dur, question_dotted, dotted_time = st.session_state['questioncd']
    next_question = st.button("Next Question",disabled= not st.session_state['pressed_cd'])
    question = f"How many {small_dur}s equal to a {question_dotted}{question_dur}?"
    st.subheader(question)

    user_ans = st.text_input("Enter your answer:", max_chars=2)

    if st.button("Submit", disabled=st.session_state['pressed_cd'],on_click=bn_callback):
        correct = st.session_state['correctcd']
        if str(user_ans) == str(correct):
            st.success("Correct answer")
            rain_emoji()
        else:
            st.error(f"Wrong answer, the correct answer is {correct}.")
        st.session_state.question_history_cd.append(
            [f"hard mode{hard_mode}",f"Single dotted:{simple_dotted},Double dotted:{double_dotted}",
            question,"user answer:",str(user_ans),"correct answer:",str(correct)]
        )

    if next_question and st.session_state['pressed_cd']:
        st.session_state['pressed_cd'] = False
        new_question, new_prev_q_tuple = generate_new_question(hard_mode, simple_dotted, double_dotted, st.session_state.previous_question_cd)
        st.session_state['questioncd'] = new_question[:4]
        st.session_state['correctcd'] = new_question[4]
        st.session_state.previous_question_cd = new_prev_q_tuple
        st.rerun()

    # Display question history
    if len(st.session_state.question_history_cd)>2 and st.session_state.logged:
        record_feedback("duration calculation",str(st.session_state.question_history_cd))
        st.write("Feedback recorded")
        st.session_state.question_history_cd=[]

if __name__ == "__main__":
    duration_cal_main()