import streamlit as st
from urls import *
#from urls import page_names_to_funcs
def intro():
    st.title("Music Theory App")
    st.write("Welcome to the Music Theory App!")
    st.session_state.demo_name = "—"

    # Rhythm-related container
    with st.expander("Rhythm-related",expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Grouping and beaming"):
                st.session_state.demo_name = "Grouping and beaming"
                st.rerun()
        with col2:
            if st.button("Simple-compound Modulation"):
                st.session_state.demo_name = "Simple-compound Modulation"
                st.rerun()

    # Pitch-related container
    with st.expander("Pitch-related",expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Pitch Identification"):
                st.session_state.demo_name = "Pitch Identification"
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
        with col2:
            if st.button("Chord Progression"):
                st.session_state.demo_name = "Chord Progression"
                st.rerun()

    # Music knowledge container
    with st.expander("Music Knowledge",expanded=True):
        if st.button("Instrumental Knowledge"):
            st.session_state.demo_name = "Instrumental Knowledge"
            st.rerun()
def back_home():
    if st.button("Home"):
        st.session_state.demo_name = "—"
        st.rerun()

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
    try: 
        main()
    except:
        st.warning("🚧Sorry, this page is under construction🚧")
