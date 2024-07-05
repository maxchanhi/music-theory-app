import streamlit as st
from inversion.inversion_gen import main_generation
from inversion.notation import roman_numerial, inversion_type
from urls import rain_emoji
ss = st.session_state
def main_inversion():
    
    st.title("Inversion quiz")
    select_clef = st.selectbox("Select the clef that you want to test on:",options=["treble","bass","grand staff"],index=0)
    # Initialize session state variables
    if "question_data_iv" not in st.session_state:
        st.session_state["question_data_iv"] = None
    if "pressed_iv" not in st.session_state:
        st.session_state["pressed_iv"] = True
    if "ans_his_iv" not in ss:
        ss.ans_his_iv = []
    try:
        key_signature = st.session_state["question_data_iv"]["key_sign"]
        st.subheader(f"What is this chord in {key_signature}?")
        st.image("inversion/cropped_score_inversion.png", use_column_width="auto")
    except:
        st.warning("Please generate a New Question")

    col1, col2 = st.columns(2)
    with col1:
        user_nu = st.selectbox("Choose the Roman numeral:", options=roman_numerial)
        if st.button("New Question") and st.session_state["pressed_iv"]:
            st.session_state["pressed_iv"] = False
            st.session_state["question_data_iv"] = main_generation(select_clef)
            st.rerun()
    with col2:
        user_iv = st.selectbox("Choose the inversion type:", options=inversion_type)
        check_ans= st.button("Check Answer", disabled=st.session_state["pressed_iv"])
    if check_ans and st.session_state["question_data_iv"]:
        st.session_state["pressed_iv"] = True
        user_ans = f'{user_nu} {user_iv}'
        correct_ans = st.session_state["question_data_iv"]["triad"] + " " + st.session_state["question_data_iv"]["inversion_type"]
        print("User answer:", user_ans,"Correct answer:", correct_ans)
        if user_ans == correct_ans:
            st.success(f"Correct!")
            rain_emoji()
            st.balloons()
            feedback = "correct"
        elif user_ans != correct_ans:
            st.warning(f"The correct answer is {correct_ans}")
            feedback = "wrong. "
            if user_nu.lower()==st.session_state["question_data_iv"]["triad"].lower():
                st.write("But you can still identify the correct chord.")
                feedback+= "user fail to identify the inversion type"
            elif user_iv.lower()==st.session_state["question_data_iv"]["inversion_type"].lower():
                st.write("But you can still identify the inversion type")
                feedback+= "but user still identify the roman numeral"
            else:
                feedback+= "user both fail to identify the roman numeral and inversion type"
        else:
            st.error("Please try again.")
            feedback=None
        
