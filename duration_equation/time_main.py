import streamlit as st
from duration_equation.time_signature import generate_question
from urls import rain_emoji 
from data_func import record_feedback
ss=st.session_state
def generate_new_question(answer_history):
    max_attempts = 10
    for _ in range(max_attempts):
        new_question = generate_question()
        if len(answer_history) < 2 or new_question[0] not in [q[0] for q in answer_history[-2:]]:
            return new_question
    return new_question  # Return the last generated question if we can't find a unique one

def bn_callback():
    ss.pressed_ts = True

def main_ts():
    if "pressed_ts" not in ss:
        ss.pressed_ts = False
    if "question_data_ts" not in ss:
        ss.question_data_ts = generate_new_question([])
    if "answer_history_ts" not in ss:
        ss.answer_history_ts = []

    question_data, correct_answer = ss.question_data_ts
    st.title("Calculation for time signature")
    st.subheader(question_data)

    if st.button("New Question", disabled=not ss.pressed_ts):
        ss.pressed_ts = False
        ss.question_data_ts = generate_new_question(ss.answer_history_ts)
        st.rerun()

    # User input
    user_answer = st.text_input("Your Answer:")
    
    # Check answer
    if st.button("Submit", disabled=ss.pressed_ts, on_click=bn_callback) and user_answer:
        user_answer = str(user_answer)
        if user_answer == str(correct_answer):
            st.success("Correct!")
            st.balloons()
            rain_emoji()
        else:
            st.error(f"Incorrect. The correct answer is {correct_answer}.")
        
        ss.answer_history_ts.append((question_data, correct_answer, user_answer))


    if ss.logged and len(ss.answer_history_ts) > 2:
        record_feedback("time signature", ss.answer_history_ts)
        st.write("Feedback recorded")
        ss.answer_history_ts = []

if __name__ == "__main__":
    main_ts()