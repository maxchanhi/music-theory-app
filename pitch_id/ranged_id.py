import streamlit as st
import random
from pitch_id.element import get_note,levels,accidentals,note_letters
def disable_button():
    st.session_state.pressed_id = True
def pitch_main():
    st.title('Note Identification')
    col1,col2=st.columns([3,1])
    with col1:
        chosen_level = st.select_slider('Select the difficulty level:',options=["basic","intermediate","c clefs","all clefs"])
    with col2:
        st.write("  ")
        st.write("  ")
        ledger=st.checkbox("Use ledger lines",value=False)
    col1,col2=st.columns(2)
    with col1:
        chosen_clefs= st.multiselect('Select the clef:', default=levels[chosen_level][0],options=levels[chosen_level][0])
    with col2:
        chosen_accidental = st.multiselect('Select the accidental:', default=levels[chosen_level][1],options=levels[chosen_level][1])
    if len(chosen_clefs) ==0 or len(chosen_accidental)==0:
        st.warning("Please select at least one clef")
        st.stop()

    if 'current_answer_id' not in st.session_state:
        st.session_state.current_answer_id = None
    if 'pressed_id' not in st.session_state:
        st.session_state.pressed_id = True

    if st.session_state.current_answer_id:
        st.image("score.png") 

    col1, col2 = st.columns(2)
    with col1:
        # The select box for the note letters
        selected_note = st.selectbox('Select the note letter:', note_letters)
        new_quest = st.button("New Question",disabled= not st.session_state.pressed_id)
        if new_quest and st.session_state.pressed_id:
            st.session_state.pressed_id = False
            clef, note,acc = get_note(chosen_clefs,chosen_accidental,ledger)
            st.session_state.current_answer_id = note
            st.rerun()
        
    with col2:
        # The select box for the accidentals
        selected_accidental = st.selectbox('Select the accidental:', accidentals)
        check_ans = st.button("Check Answer", on_click=disable_button,disabled=st.session_state.pressed_id)
    user_ans = f"{selected_note}{selected_accidental}"

    if check_ans:
        if user_ans.lower() == st.session_state.current_answer_id:
            st.success("Correct")
        else:
            st.error(f"The answer should be {st.session_state.current_answer_id}")
       
if __name__ == "__main__":
    pitch_main()
