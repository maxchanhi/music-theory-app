from grouping_quiz.main import grouping_quiz_main
from instrument_knowledge_quiz.music_quiz import knowledgemain
from compound_simple_time.main import compound_simple_main
from interval.interval_quiz import interval_main
from melody_key.find_key_main import melody_key_main
from pitch_id.id import pitch_main
from melody_key.chord_progression.main import chord_progression_main
from inversion.main_iv import main_inversion
from duration_equation.cal_main import duration_cal_main
from duration_equation.time_main import main_ts
from chromatic_scale.chromatic_main import chr_main
from urls import fun_emoji_list

import streamlit as st

import random

def intro():
    em= random.choice(fun_emoji_list)
    st.title(f"{em}Music Theory App{em}")
    st.write(f"Welcome to my Music Theory App! You can practice your ABRSM grade 5 theory! {random.choice(fun_emoji_list)}")
    st.write("Duration calculation added!")
    st.session_state.demo_name = "—"

    # Rhythm-related container
    with st.expander("Rhythm-related",expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Grouping and beaming"):
                st.session_state.demo_name = "Grouping and beaming"
                st.rerun()
            if st.button("Duration calculation"):
                st.session_state.demo_name = "Duration calculation"
                st.rerun()
        with col2:
            if st.button("Simple-compound Modulation"):
                st.session_state.demo_name = "Simple-compound Modulation"
                st.rerun()
            if st.button("Calculation for time signature"):
                st.session_state.demo_name = "Calculation for time signature"
                st.rerun()

    # Pitch-related container
    with st.expander("Pitch-related",expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Pitch Identification"):
                st.session_state.demo_name = "Pitch Identification"
                st.rerun()
            if st.button("Chromatic scale"):
                st.session_state.demo_name = "Chromatic scale"
                st.rerun()
                
        with col2:
            if st.button("Interval"):
                st.session_state.demo_name = "Interval"
                st.rerun()

    # Key-related container
    with st.expander("Key-related",expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Identifying Key in a Melody"):
                st.session_state.demo_name = "Identifying Key in a Melody"
                st.rerun()
            if st.button("Chord Inversion"):
                st.session_state.demo_name = "Inversion"
                st.rerun()
        with col2:
            if st.button("Chord Progression"):
                st.session_state.demo_name = "Chord Progression"
                st.rerun()

    # Music knowledge container
    with st.expander("Music Knowledge",expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Instrumental Knowledge"):
                st.session_state.demo_name = "Instrumental Knowledge"
                st.rerun()
        with col2:
            if st.button("Music Dictionary"):
                support_url = "https://music-glossary.streamlit.app/"  # Replace with your actual support URL
                st.markdown(f'<meta http-equiv="refresh" content="0; url={support_url}">', unsafe_allow_html=True)

    #https://music-glossary.streamlit.app/
    
    with st.expander("Learn more",expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Support me"):
                support_url = "/support_me"  # Replace with your actual support URL
                st.markdown(f'<meta http-equiv="refresh" content="0; url={support_url}">', unsafe_allow_html=True)
        with col2:
            if st.button("About me"):
                support_url = "/about_me"  # Replace with your actual support URL
                st.markdown(f'<meta http-equiv="refresh" content="0; url={support_url}">', unsafe_allow_html=True)
  
    
def back_home():
    if st.button("Home"):
        st.session_state.demo_name = "—"
        st.rerun()
page_names_to_funcs = {
    "—": intro,
    "Grouping and beaming": grouping_quiz_main,"Simple-compound Modulation": compound_simple_main,"Duration calculation":duration_cal_main,
    "Calculation for time signature":main_ts,"Pitch Identification": pitch_main,"Interval": interval_main,"Chromatic scale":chr_main,
    "Identifying Key in a Melody": melody_key_main,"Chord Progression": chord_progression_main,
    "Inversion":main_inversion, "Instrumental Knowledge": knowledgemain, 
}
def main():
    st.set_page_config(page_title="Music Theory App")
    if 'demo_name' not in st.session_state:
        st.session_state.demo_name = "—"

    page_selected = st.sidebar.radio("Choose a page", page_names_to_funcs.keys(), index=list(page_names_to_funcs.keys()).index(st.session_state.demo_name))
    if page_selected != st.session_state.demo_name:
        st.session_state.demo_name = page_selected
        st.rerun()
    if page_selected  != "—":
        back_home()
        
    page_names_to_funcs[page_selected]()

if __name__ == "__main__":
    main()
