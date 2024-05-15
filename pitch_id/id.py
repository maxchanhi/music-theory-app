import streamlit as st

def pitch_main():
    import random
    from pitch_id.main_generation import score_generation, accidentals, note_letters,levels,fun_emoji_list
    from streamlit_extras.let_it_rain import rain
    st.title('Music Note Identification')
    chosen_level = st.select_slider('Select the difficulty level:',options=["basic","intermediate","c clefs","all clefs"])
    chosen_clefs= st.multiselect('Select the clef:', default=levels[chosen_level][0],options=levels[chosen_level][0])
    chosen_accidental = st.multiselect('Select the accidental:', default=levels[chosen_level][1],options=levels[chosen_level][1])
    if len(chosen_clefs) ==0:
        st.warning("Please select at least one clef")
        st.stop()

    if 'current_answer' not in st.session_state:
        st.session_state.current_answer = None
    if 'pressed_id' not in st.session_state:
        st.session_state.pressed_id = True
    try:
        st.image("pitch_id/cropped_score.png", caption='Identify the note in the image') 
    except:
        st.warning("Get a new question")
    col1, col2 = st.columns(2)
    with col1:
        # The select box for the note letters
        selected_note = st.selectbox('Select the note letter:', note_letters)
        new_quest = st.button("New Question")
        if new_quest and st.session_state.pressed_id:
            st.session_state.pressed_id = False
            clef, note,acc = score_generation(chosen_clefs,chosen_accidental)
            st.session_state.current_answer = f"{note} {acc}"
            st.rerun()
        
    with col2:
        # The select box for the accidentals
        selected_accidental = st.selectbox('Select the accidental:', accidentals)
        check_ans = st.button("Check Answer", disabled=st.session_state.pressed_id)
    

    if check_ans and user_ans:
        user_ans = f"{selected_note} {selected_accidental}"
        print(st.session_state.current_answer,user_ans)
        st.session_state.pressed_id = True
        if user_ans.lower() == st.session_state.current_answer.lower():
            st.success("Correct")
            fun_emoji = random.choice(fun_emoji_list)
            rain(emoji = fun_emoji,animation_length="1")
        else:
            st.error(f"The answer should be {st.session_state.current_answer}")
       
if __name__ == "__main__":
    pitch_main()
