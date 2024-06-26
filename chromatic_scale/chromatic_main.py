import streamlit as st
from chromatic_scale.notation import main_chromatic_generator,get_png_files
from chromatic_scale.sync_generation import main
import asyncio
import os
from urls import rain_emoji
from streamlit_extras.let_it_rain import rain
import random
#st.set_page_config("Chromatic scale identify")
def generation_new_ques(clef_list):
    with st.spinner("Generating new question..."):
        chromatic_scale,wrong_options,accending_dir = main_chromatic_generator()
        st.session_state.chromatic_data = chromatic_scale,wrong_options,accending_dir
        asyncio.run(main(st.session_state.chromatic_data,clef_list=clef_list))
        png_files = get_png_files()
        random.shuffle(png_files)
        st.session_state.chr_file=png_files
    st.session_state.selected_image = None 
    st.session_state.chr_pressed = False
def select_image(png_file):
    st.session_state.selected_image = png_file
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
        st.session_state.new_ques_ch = False
    
    clef_list = st.multiselect("Select clef", ["bass","tenor",'alto','treble'],default=['treble'])
    col1,col2=st.columns([4,1])
    if st.session_state.new_ques_ch:
        generation_new_ques(clef_list)
        st.session_state.new_ques_ch=False
    
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
        if st.button("Generate new question",disabled= st.session_state.new_ques_ch):
            st.session_state.new_ques_ch = True
            st.rerun()
    with col2:
        chr_check_ans= st.button("Check Answer",disabled=st.session_state.new_ques_ch and not st.session_state.chr_file)
    if st.session_state.selected_image:
        if chr_check_ans:
            if "Correct" in st.session_state.selected_image:
                st.success("Correct Answer!")
                rain_emoji()
            else:
                idxx=1
                for img in st.session_state.chr_file:
                    if "Correct" in img:
                        correct_idx=idxx
                        break
                    idxx+=1
                st.error(f"The correct answer is option {correct_idx}")
            st.session_state.chr_pressed = True


    

    


