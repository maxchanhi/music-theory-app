from init_import import * 

def intro():
    # Get database connection
    db = get_database()
    users_collection = db['login']
            
    col1, col2 = st.columns([5,1])
    with col1:
        with st.popover("Sign Up"):
            if not ss.logged:
                register = sign_up(users_collection)
                if register:
                    ss.logged = True
                    st.rerun()
            elif ss.logged:
                st.success("You are already logged in")

    with col2:
        if not ss.logged:
            with st.popover("Log In"):
                login = login_form()
                if login:
                    ss.logged = True
                    st.rerun()
                elif login==False:
                    st.error("Incorrect username or password")
        else:
            if st.button("Log Out"):
                ss.logged = False
                st.rerun()
            
    em = random.choice(fun_emoji_list)
    st.title(f"{em}Music Theory App{em}")
    st.write(f"Welcome to my Music Theory App! You can practice your ABRSM grade 5 theory! {random.choice(fun_emoji_list)}")
    st.write("Transposing and dictionary added!")
    
    login_greeting()
    ss.demo_name = "—"

    # Rhythm-related container
    with st.expander("Rhythm-related", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Grouping and beaming"): ss.demo_name = "Grouping and beaming"
            if st.button("Duration calculation"): ss.demo_name = "Duration calculation"
        with col2:
            if st.button("Simple-compound Modulation"): ss.demo_name = "Simple-compound Modulation"
            if st.button("Calculation for time signature"): ss.demo_name = "Calculation for time signature"

    # Pitch-related container
    with st.expander("Pitch-related", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Pitch Identification"): ss.demo_name = "Pitch Identification"
            if st.button("Chromatic scale"): ss.demo_name = "Chromatic scale"
            if st.button("Same pitches with different clefs"): ss.demo_name = "Same pitches with different clefs"
        with col2:
            if st.button("Interval"): ss.demo_name = "Interval"
            if st.button("Transposing"): ss.demo_name = "Transposing"

    # Key-related container
    with st.expander("Key-related", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Identifying Key in a Melody"): ss.demo_name = "Identifying Key in a Melody"
            if st.button("Chord Inversion"): ss.demo_name = "Inversion"
        with col2:
            if st.button("Chord Progression"): ss.demo_name = "Chord Progression"
            if st.button("Identify clef from minor scale"): ss.demo_name = "Identify clef from minor scale"

    # Music knowledge container
    with st.expander("Music Knowledge", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.write("  ")
            if st.button("Instrumental Knowledge"): ss.demo_name = "Instrumental Knowledge"
        with col2:
            st.markdown(button_style, unsafe_allow_html=True)
            st.markdown('<a href="https://music-glossary.streamlit.app" class="button" target="_blank">Music Dictionary</a>', unsafe_allow_html=True)
    with st.expander("Music Supplement", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Note Reading Exercise Generator"): ss.demo_name = "Note Reading Exercise Generator"
        with col2:
            pass
    with st.expander("Learn more", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Support me"):
                st.markdown('<meta http-equiv="refresh" content="0; url=/support_me">', unsafe_allow_html=True)
        with col2:
            if st.button("About me"):
                st.markdown('<meta http-equiv="refresh" content="0; url=/about_me">', unsafe_allow_html=True)

    if ss.demo_name != "—":
        st.rerun()

page_names_to_funcs = {
    "—": intro,
    "Grouping and beaming": grouping_quiz_main,
    "Simple-compound Modulation": compound_simple_main,
    "Duration calculation": duration_cal_main,
    "Calculation for time signature": main_ts,
    "Pitch Identification": pitch_main,
    "Interval": interval_main,
    "Chromatic scale": chr_main,
    "Transposing": transposing_main,
    "Same pitches with different clefs": main_sp,
    "Identifying Key in a Melody": melody_key_main,
    "Chord Progression": chord_progression_main,
    "Identify clef from minor scale": clef_main,
    "Inversion": main_inversion,
    "Instrumental Knowledge": knowledgemain,
    "Note Reading Exercise Generator":story_main
}

def main():
    st.set_page_config(page_title="Music Theory App", page_icon="🎵")
    if 'demo_name' not in ss:
        ss.demo_name = "—"
    if "logged" not in ss:
        ss.logged = None
        ss.last_ai_greeting = None
    
    page_selected = st.sidebar.radio("Choose a page", page_names_to_funcs.keys(), index=list(page_names_to_funcs.keys()).index(ss.demo_name))
    if page_selected != ss.demo_name:
        ss.demo_name = page_selected
        st.rerun()
    if page_selected != "—":
        if ss.logged:
            st.success("You are logged in")
        else:
            st.warning("You are not logged in")
        back_home()
        
    page_names_to_funcs[page_selected]()

if __name__ == "__main__":
    main()
