def interval_main():
    import streamlit as st
    import random
    from interval.generation import score_generation,lilypond_generation,level_difficulty
    from interval.element import user_quality, user_interval, fun_emoji_list
    from interval.element import advance_accidentals, difficulty_list
    from streamlit_extras.let_it_rain import rain
    #st.set_page_config(page_title="Interval Quiz")

    def new_question(selected_clef,selected_acci,same_clef,compound_o):
        ans, clef, clef2, fix_octave1, fix_octave2, note, note2 = score_generation(selected_clef,selected_acci,same_clef,compound_o)
        lilypond_generation(clef, clef2, fix_octave1, fix_octave2, note, note2)
        st.session_state['current_answer'] = ans
        st.session_state['feedback'] = ""

    def check_answer():
        user_ans = f"{st.session_state['user_quality']} {st.session_state['user_interval']}"
        current_answer = st.session_state.get('current_answer')

        if current_answer is None:
            feedback = 'Error: No current answer available. Please try a new question.'
        elif user_ans.lower() == current_answer.lower():
            feedback = 'Correct!'
            fun_emoji = random.choice(fun_emoji_list)
            rain(emoji = fun_emoji,animation_length="1")
            st.session_state['new_quest'] = True
        else:
            feedback = f'Incorrect. The answer should be {current_answer}'

        st.session_state['feedback'] = feedback
    if 'new_quest' not in st.session_state:
        st.session_state['new_quest'] = True
    if 'selected_clef' not in st.session_state:
        st.session_state['selected_clef'] = ["treble"]
    if 'selected_acci' not in st.session_state:
        st.session_state['selected_clef'] = ["Natural (♮)"]
    if 'difficulty' not in st.session_state:
        st.session_state['difficulty'] = "Beginner"
    if "picture" not in st.session_state:
        st.session_state['picture'] = None

    st.title("Music Note App")
    col1, col2 = st.columns(2)
    auto_level = st.session_state.get('auto_mode', True)
    if auto_level:
        show_selectbox = True
        st.session_state['difficulty'] = st.select_slider("Pick your poison💀:",options=difficulty_list)
        st.session_state['selected_clef'] = level_difficulty(st.session_state['difficulty'])['clef']
        st.session_state['selected_acci'] = level_difficulty(st.session_state['difficulty'])['accidentals']
        same_clef = level_difficulty(st.session_state['difficulty'])['same_clef']
        compound_octave = level_difficulty(st.session_state['difficulty'])["compound_octave"] 
    else:
        show_selectbox = False
        compound_octave = False
    with col1:
        st.checkbox("Auto mode", key='auto_mode',value=True)
        st.session_state['selected_clef']=st.multiselect("Select clef:", ["treble", "bass", "alto", "tenor"],
                                                        default=st.session_state['selected_clef'],disabled=show_selectbox)
    with col2:
        st.checkbox("Compound Interval", key='compound_octave',value=compound_octave,disabled=show_selectbox)
        st.session_state['selected_acci']=st.multiselect("Select accidental:", advance_accidentals,
                                                        default=st.session_state['selected_acci'],disabled=show_selectbox)
    if not st.session_state['selected_clef'] or not st.session_state['selected_acci']:
        st.warning("Please select a clef and a accidental.")
    
    if st.button("New Question") and st.session_state['selected_clef'] and st.session_state['selected_acci']:
        new_question(st.session_state['selected_clef'],st.session_state['selected_acci'],same_clef,compound_octave)
        st.session_state['picture'] = True
        st.rerun()
    
    if st.session_state['picture'] :
        image_path = "interval/static/images/cropped_score_ans.png"
        st.image(image_path, use_column_width=False)
    else:
        st.warning("⬆️Press for a New Question")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        Qualityans=st.selectbox("Quality", user_quality, key='user_quality')

    with col2:
        Intervalans=st.selectbox("Interval", user_interval, key='user_interval')

    with col3:
        if st.button("Check Answer") and Qualityans != "--"and Intervalans!= "--":
            check_answer()
            if st.session_state.get('feedback',None):
                st.write(st.session_state['feedback'])
    

if __name__ == '__main__':
    interval_main()