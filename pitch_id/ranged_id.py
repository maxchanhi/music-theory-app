import streamlit as st
import random
from pitch_id.element import get_note,levels,accidentals,note_letters,ranged_score_generation
from urls import rain_emoji
from data_func import record_feedback
import os
ss = st.session_state
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
    if "ans_history_id" not in ss:
        ss.ans_history_id = []

    if st.session_state.pressed_id:
        st.image("score.png")
        

    col1, col2 = st.columns(2)
    with col1:
        # The select box for the note letters
        selected_note = st.selectbox('Select the note letter:', note_letters)
        new_quest = st.button("New Question",disabled= not st.session_state.pressed_id)
        if new_quest and st.session_state.pressed_id:
            st.session_state.pressed_id = False
            clef, note,acc = get_note(chosen_clefs,chosen_accidental,ledger)
            ranged_score_generation(chosen_clef, picked_note, clef_data['pitch_range'])
            st.session_state.current_answer_id = note
            st.rerun()
        
    with col2:
        # The select box for the accidentals
        selected_accidental = st.selectbox('Select the accidental:', accidentals)
        check_ans = st.button("Check Answer", on_click=disable_button,disabled=st.session_state.pressed_id)
    user_ans = f"{selected_note} {selected_accidental}"

    if check_ans:
        if user_ans.lower() == st.session_state.current_answer_id.lower():
            st.success("Correct")
            result = "User is Correct"
            ans = ""
            rain_emoji()
        else:
            st.error(f"The answer should be {st.session_state.current_answer_id}")
            print(selected_note, selected_accidental, st.session_state.current_answer_id.split()[1].lower())
            ans = f"User answer: {user_ans}. The correct answer: {st.session_state.current_answer_id}."
            if st.session_state.current_answer_id.split()[0].lower() == selected_note.lower():
                result =f"The note is correct, but the accidental is wrong. The correct accidental is {st.session_state.current_answer_id.split()[1]}"
            elif st.session_state.current_answer_id.split()[1].lower() == selected_accidental.split()[0].lower():
                result =f"The accidental is correct, but the note is wrong. The correct note is {st.session_state.current_answer_id.split()[0]}"
            else:
                result =f"The note and accidental are both wrong. The correct answer is {st.session_state.current_answer_id}"
            st.write(result)
        if ss.logged:
            ss.ans_history_id.append(f"""{result}.{ans}.Level difficulty:{chosen_level}. Ledger line used:{ledger}""")
            if len(ss.ans_history_id) > 2:
                record_feedback("pitch identification",text=str(ss.ans_history_id))
                ss.ans_history_id=[]
                st.write("Result recorded")

            
       
if __name__ == "__main__":
    pitch_main()
