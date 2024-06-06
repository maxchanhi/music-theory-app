import streamlit as st
from chromatic_scale.notation import main_chromatic_generator,get_png_files
from chromatic_scale.sync_generation import main
import asyncio
import os
import random
#st.set_page_config("Chromatic scale identify")
def chr_main():
    st.title("Chromatic scale identify")

    if "chromatic_data" not in st.session_state:
        st.session_state.chromatic_data = None
        st.session_state.chr_pressed = True
        st.session_state.selected_image = None
        st.session_state.chr_file = None
    clef_list = st.multiselect("Select clef", ["bass","tenor",'alto','treble'],default=['treble'])
    col1,col2=st.columns([4,1])
    with col1:
        chr_new_q = st.button("Generate new question")
    with col2:
        if st.session_state.chr_file ==None:
            disable_chr_check_ans=True
        else:
            disable_chr_check_ans=False
        chr_check_ans= st.button("Check Answer",disabled=disable_chr_check_ans)
    if chr_new_q and st.session_state.chr_pressed:
        with st.spinner("Generating new question..."):
            chromatic_scale,wrong_options,accending_dir = main_chromatic_generator()
            st.session_state.chromatic_data = chromatic_scale,wrong_options,accending_dir
            asyncio.run(main(st.session_state.chromatic_data,clef_list=clef_list))
            png_files = get_png_files()
            random.shuffle(png_files)
            st.session_state.chr_file=png_files

        st.session_state.selected_image = None  # Reset selected image
        st.session_state.chr_pressed = False

    if st.session_state.selected_image:
        if chr_check_ans:
            if "Correct" in st.session_state.selected_image:
                st.success("Correct Answer!")
            else:
                st.error("Wrong Answer!")
            st.session_state.chr_pressed = True


    def select_image(png_file):
        st.session_state.selected_image = png_file
        for file in st.session_state.chr_file:
            if file != png_file:
                st.session_state[f"button_{file}"] = False

    if st.session_state.chr_file:
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
                    if st.button("Select", key=png_file, on_click=select_image, args=(png_file,), disabled=st.session_state[f"button_{png_file}"]):
                        st.session_state[f"button_{png_file}"] = True


