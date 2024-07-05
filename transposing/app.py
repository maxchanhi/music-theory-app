import streamlit as st
import os
from transposing.main_generation import picture_generation
from transposing.get_pictures import get_pic_link
from urls import disclaimer, rain_emoji
from data_func import record_feedback

ss=st.session_state
def disable_option_tr(idx):
    st.session_state.dis_option_tr = idx

def check_callback():
    st.session_state.answer_checked_tr = True

def transposing_main():
    st.header("Transposition Quiz")
    
    if "transposed_by" not in st.session_state:
        st.session_state['transposed_by'] = ""
        st.session_state['presses_tran'] = True
        st.session_state['img_link'] = []
        st.session_state['selected_answer_tr'] = None
        st.session_state['answer_checked_tr'] = True
        st.session_state.dis_option_tr = None
        st.session_state['option_problems'] = {}
        st.session_state['student_choices'] = []
    
    if st.session_state.transposed_by:
        st.write("This is the original melody:")
        original_img_path = "transposing/static/question.png"
        if os.path.exists(original_img_path):
            st.image(original_img_path, use_column_width=True)
        else:
            st.error(f"Original melody image not found: {original_img_path}")
        
        st.write(f"Which one is correctly transposed {st.session_state.transposed_by}?")
        st.write("Pick the correct answer:")
        
        for idx, link in enumerate(st.session_state.img_link):
            col1, col2 = st.columns([5, 1])
            with col1:
                img_path = f'transposing/{link}'
                if os.path.exists(img_path):
                    st.image(img_path, use_column_width=True)
                else:
                    st.error(f"Image not found: {img_path}")
            with col2:
                if st.button(f"Option {idx + 1}", key=f"btn_{idx}", on_click=disable_option_tr, args=(idx,),
                             disabled=idx==st.session_state.dis_option_tr):
                    st.session_state.selected_answer_tr = idx
                    st.session_state.answer_checked_tr = False  # Reset check on new selection
        
    col1, col2 = st.columns([4, 1])
    with col1:
        if st.button("Generate question", disabled=not st.session_state.answer_checked_tr):
            st.session_state.transposed_by, st.session_state.option_problems = picture_generation()
            st.session_state.img_link = get_pic_link()
            st.session_state.selected_answer_tr = None
            st.session_state.answer_checked_tr = False
            st.session_state.dis_option_tr = None
            st.rerun()
    with col2:
        check_ans = st.button("Check answer", disabled=st.session_state.answer_checked_tr or st.session_state.dis_option_tr is None,
                                on_click=check_callback)
        
    if check_ans:
        selected_option = st.session_state['img_link'][st.session_state.selected_answer_tr]
        if "correct" in selected_option:
            st.success("Correct!")
            rain_emoji()
            st.session_state.student_choices.append(("correct", "Student answered correctly"))
        else:
            correct_idx = [i for i, link in enumerate(st.session_state.img_link) if "correct" in link][0] + 1
            option_name = selected_option.split('/')[-1].split('.')[0]  # Extract option name from image link
            problem = st.session_state.option_problems.get(option_name, "Unknown problem")
            st.session_state.student_choices.append((option_name, problem))
            st.error(f"Incorrect. Image {correct_idx} is the correct answer. \n Problem: {problem}")

    if len(st.session_state.student_choices) > 5 and ss.logged:
        feedback = str(st.session_state.student_choices)
        record_feedback( subject="transposing", text=feedback)
        st.write("Your results have been logged!")
        st.session_state.student_choices = []

    disclaimer()