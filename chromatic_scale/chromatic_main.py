import streamlit as st
from chromatic_scale.notation import main_chromatic_generator,get_png_files
from chromatic_scale.sync_generation import main
import asyncio
import os
from urls import rain_emoji
from data_func import record_feedback
import random
ss= st.session_state
#st.set_page_config("Chromatic scale identify")
def call_back():
    st.session_state.new_ques_ch = True
def generation_new_ques(clef_list):
    with st.spinner("Generating new question..."):
        chromatic_scale, wrong_options, accending_dir = main_chromatic_generator()
        st.session_state.chromatic_data = chromatic_scale, wrong_options, accending_dir

        st.session_state.problem_info = asyncio.run(main(st.session_state.chromatic_data, clef_list=clef_list))
        png_files = get_png_files()
        random.shuffle(png_files)
        st.session_state.chr_file = png_files
    st.session_state.selected_image = None 
    st.session_state.chr_pressed = False

def select_image(png_file):
    st.session_state.selected_image = png_file
    st.session_state.selected_option = next(i for i, file in enumerate(st.session_state.chr_file) if file == png_file) + 1
    for file in st.session_state.chr_file:
        if file != png_file:
            st.session_state[f"button_{file}"] = False

def chr_main():
    st.title("Chromatic scale identify")

    if "chromatic_data" not in st.session_state:
        st.session_state.chromatic_data = None
        st.session_state.chr_pressed = True
        st.session_state.selected_image = None
        st.session_state.chr_file = None
        st.session_state.new_ques_ch = True
        ss.problem_info = []

    if 'answer_history_cm' not in st.session_state:
        st.session_state.answer_history_cm = []
    clef_list = st.multiselect("Select clef", ["bass","tenor",'alto','treble'],default=['treble'])
    col1,col2=st.columns([4,1])
   
    if st.session_state.chr_file:
        idx=1
        for png_file in st.session_state.chr_file:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.image(png_file)
            with col2:
                if st.session_state.selected_image == png_file:
                    st.button("Selected", disabled=True, key=png_file)
                else:
                    if f"button_{png_file}" not in st.session_state:
                        st.session_state[f"button_{png_file}"] = False
                    if st.button(f"Option {idx}", key=png_file, on_click=select_image, args=(png_file,), disabled=st.session_state[f"button_{png_file}"]):
                        st.session_state[f"button_{png_file}"] = True
            idx+=1
    col1, col2 = st.columns([4, 1])
    with col1:
        if st.button("New question",disabled= not st.session_state.new_ques_ch):
            st.session_state.new_ques_ch = False
            generation_new_ques(clef_list)
            st.rerun()
    with col2:
        chr_check_ans= st.button("Check Answer",disabled=st.session_state.new_ques_ch or st.session_state.selected_image is None, on_click=call_back)
    if chr_check_ans:
        correct_option = next(i for i, file in enumerate(st.session_state.chr_file) if "Correct" in file) + 1
        st.session_state.chr_pressed = True

        selected_file = os.path.basename(st.session_state.selected_image)
        selected_file_name = os.path.splitext(selected_file)[0]
        problem_info = st.session_state.problem_info.get(selected_file_name, "Unknown")

        if "Correct" in st.session_state.selected_image:
            st.success("Correct Answer!")
            rain_emoji()
            result = "Correct"
        else:
            st.warning(f"The correct answer is option {correct_option}. Problem: {problem_info}")
            result = f"Incorrect"
        
        st.session_state.answer_history_cm.append({
            'user result': result,
            'clef tested on': ', '.join(clef_list),
            'problem_info': problem_info
        })
        
        if ss.logged and len(ss.answer_history_cm)>2:
            record_feedback("chrometic scale",str(ss.answer_history_cm))
            ss.update_user_history_cm=[]
            st.write("Feedback recorded successfully!")

