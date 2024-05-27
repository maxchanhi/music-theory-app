import streamlit as st
from random import randint
from fractions import Fraction
from duration_equation.question import generate_question, correct_ans,question_elements
def duration_cal_main():
    st.title("Music Duration Quiz")
    col1,col2,col3=st.columns(3)
    with col1:
        hard_mode=st.checkbox("Hard mode")    
    with col2:
        simple_dotted=st.checkbox("Dotted",value=True)
    with col3:
        double_dotted=st.checkbox("Double dotted")

    if 'questioncd' not in st.session_state:
        duration,dotted_vartion=question_elements(hard_mode,simple_dotted,double_dotted)
        small_dur, question_dur, question_dotted,dotted_time = generate_question(duration,dotted_vartion)
        st.session_state['questioncd'] = (small_dur, question_dur, question_dotted, dotted_time)
        st.session_state['correctcd'] = correct_ans(small_dur, question_dur, dotted_time)
        st.session_state['pressed_cd']=False
    small_dur, question_dur, question_dotted, dotted_time = st.session_state['questioncd']
    next_question=st.button("Next Question")
    st.subheader(f"How many {small_dur}s equal to a {question_dotted}{question_dur}?")

    user_ans = st.text_input("Enter your answer:",max_chars=2)

    if st.button("Submit",disabled=st.session_state['pressed_cd']):
        correct = st.session_state['correctcd']
        st.session_state['pressed_cd']=True
        if str(user_ans) == str(correct):
            st.success("Correct answer")
        else:
            st.error(f"Wrong answer, the answer is {correct}.")

    if next_question and st.session_state['pressed_cd']:
        st.session_state['pressed_cd']=False
        duration,dotted_vartion=question_elements(hard_mode,simple_dotted,double_dotted)
        small_dur, question_dur, question_dotted,dotted_time = generate_question(duration,dotted_vartion)
        st.session_state['questioncd'] = (small_dur, question_dur, question_dotted, dotted_time)
        st.session_state['correctcd'] = correct_ans(small_dur, question_dur, dotted_time)
        print(st.session_state['questioncd'],st.session_state['correctcd'])
        st.rerun()

if __name__ == "__main__":
    duration_cal_main()
