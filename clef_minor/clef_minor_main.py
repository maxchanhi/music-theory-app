import streamlit as st
from clef_minor.minor_scale import main_generation
from clef_minor.score_gen import display_note
from urls import rain_emoji
from data_func import record_feedback
ss = st.session_state
def click_callback():
    st.session_state.check_anscm = False

def clef_main():
    if "data_cm" not in st.session_state:
        st.session_state.data_cm = None
    if "check_anscm" not in st.session_state:
        st.session_state.check_anscm = False
    if "ans_his_cm" not in ss:
        ss.ans_his_cm = []
    
    col1, col2 = st.columns([4, 1])
    with col1:
        level = st.select_slider(
            "Select your difficulty",
            ["easy", "intermediate", "hard"],
            value="easy"
        )
    with col2:
        hint = st.checkbox("Hint!",value=True)
    selected_option=None
    
    # Display image and radio buttons if data_cm exists
    if st.session_state.data_cm:
        clef, starting_pitch, minor_type, user_options=st.session_state.data_cm
        st.image("score_cm.png",use_column_width=True)
        if hint:
            col1, col2 = st.columns(2)
            with col2:
                display_option = [
                    display_note(op.split()[0]) + " " + ' '.join(op.split()[1:]) for op in user_options
                ]       
                selected_option = st.radio("Select an option", display_option,index=None)
                user_select_idx = display_option.index(selected_option) if selected_option else None
            with col1:
                selected_clef = st.radio("Select the correct clef", ['treble','alto','tenor','bass'],index=None)
        else:
            selected_clef = st.radio("Select the correct clef", ['treble','alto','tenor','bass'],index=None)
    col1, col2 = st.columns([4, 1])
    
    # New Question button
    with col1:
        if st.button("New Question", disabled=st.session_state.check_anscm):
            st.session_state.data_cm = main_generation(level)
            st.session_state.check_anscm = True
            st.rerun()
    
    # Check Answer button
    with col2:
        if hint:
            check_ans = st.button("Check Answer", disabled=not st.session_state.check_anscm or 
                              selected_option is None or selected_clef is None
                              , on_click=click_callback)
        else:
            check_ans = st.button("Check Answer", disabled=not st.session_state.check_anscm 
                                  or selected_clef is None
                              , on_click=click_callback)
        
    if  check_ans:
        minor_type_first = minor_type.split()[0]
        ans = starting_pitch + " " + minor_type_first + " minor"
        correct_answer_idx = user_options.index(ans)
        if hint:
            if correct_answer_idx==user_select_idx and clef == selected_clef:
                st.success("Correct!")
                result = "Correct with hint provided"
                rain_emoji()
            else:
                correct_type = display_option[correct_answer_idx]
                st.error(f"Incorrect. The correct answer is {clef} clef in {correct_type}.")
                result = "Incorrect with hint provided"
        else:
            if clef == selected_clef:
                st.success("Correct!")
                rain_emoji()
                result = "Crrect without hint provided"
            else:
                show_pitch = display_note(starting_pitch)
                st.error(f"Incorrect. The correct answer is {clef} clef in {show_pitch} {minor_type} minor.")
                result = "Incorrect without hint provided"
        if ss.logged :
            ss.ans_his_cm.append(f"{level},{clef},{result}")
            if len(ss.ans_his_cm) > 2:
                record_feedback(subject="Identify clef from minor scale", text =str(ss.ans_his_cm))
                ss.ans_his_cm = []
                st.write("Feedback recorded.")
