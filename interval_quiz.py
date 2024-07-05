import streamlit as st
from interval.generation import score_generation,lilypond_generation,level_difficulty
from interval.element import user_quality, user_interval, wrong_octave,wrong_compound
from interval.element import advance_accidentals, difficulty_list
from data_func import record_feedback
from urls import rain_emoji
ss= st.session_state
#st.set_page_config(page_title="Interval Quiz")
def click_in():
    st.session_state['new_quest'] = True
def new_question(selected_clef,selected_acci,same_clef,compound_o):
    #breakpoint()
    ans, clef, clef2, fix_octave1, fix_octave2, note, note2 = score_generation(selected_clef,selected_acci,same_clef,compound_o)
    lilypond_generation(clef, clef2, fix_octave1, fix_octave2, note, note2)
    st.session_state['current_answer'] = ans
    st.session_state['feedback'] = ""

def check_answer():
    user_quality = st.session_state['user_quality']
    user_interval = st.session_state['user_interval']
    user_ans = f"{user_quality} {user_interval}"
    current_answer = st.session_state.get('current_answer')

    correct_quality, correct_interval = current_answer.rsplit(' ', 1)
    quality_correct = user_quality.lower() == correct_quality.lower()
    interval_correct = user_interval.lower() == correct_interval.lower()
    wrong_hi_lo = wrong_octave[user_interval] == correct_interval
    wrong_compound_oct = wrong_compound[user_interval] == correct_interval
    feedback_parts = []
    if quality_correct and interval_correct:
        feedback = st.success('Correct!')
        rain_emoji()
        result = "Correct"
        feedback_parts.append("Both correct!")
    else:
        if quality_correct:
            feedback_parts.append("Interval wrong, careful of counting letter")
        elif interval_correct:
            feedback_parts.append("Quality wrong, careful of counting semitone on keyboard.") 
        else:
            feedback_parts.append("Poor knowledge on interval.")

        if wrong_hi_lo:
            feedback_parts.append("Fail to identify which note is higher/lower.")
        if wrong_compound_oct:
            feedback_parts.append("Fail to identify compound octave.")

        feedback_text = f"The full correct answer is {current_answer}."
        feedback = st.warning(feedback_text)
        result = "Incorrect"

    # Store the answer in history
    st.session_state['answer_history_in'].append({
        'result': result,
        'feedback': feedback_parts
    })

    
    
def interval_main():
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
    if 'answer_history_in' not in st.session_state:
        st.session_state['answer_history_in'] = []

    st.title("Interval")
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
        same_clef= not compound_octave
    with col1:
        st.checkbox("Auto mode", key='auto_mode', value=True)
        st.write("    ")

    with col2:
        compound_octave = st.checkbox("Compound Interval", key='compound_octave', value=compound_octave, disabled=show_selectbox)
        same_clef = st.checkbox("Same Clef", key='same_clef', value=same_clef, disabled=show_selectbox)
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state['selected_clef'] = st.multiselect("Select clef:", ["treble", "bass", "alto", "tenor"],
                                                     default=st.session_state['selected_clef'], disabled=show_selectbox)
    with col2:
        st.session_state['selected_acci'] = st.multiselect("Select accidental:", advance_accidentals,
                                                           default=st.session_state['selected_acci'], disabled=show_selectbox)

    if not st.session_state['selected_clef'] or not st.session_state['selected_acci']:
        st.warning("Please select a clef and a accidental.")
    
    if st.session_state['picture'] :
        image_path = "interval/static/images/cropped_score_ans.png"
        st.image(image_path, use_column_width=True)
    else:
        st.warning("Press for a New Question")
    
    col1, col2 = st.columns(2)
    with col1:
        Qualityans=st.selectbox("Quality", user_quality, key='user_quality')

    with col2:
        Intervalans=st.selectbox("Interval", user_interval, key='user_interval')
        
    col1, col2 = st.columns(2)
    with col2:
        check_ans_bn = st.button("Check Answer",disabled=st.session_state['new_quest'],on_click=click_in)
    if check_ans_bn and Qualityans != "--" and Intervalans != "--":
        check_answer()
        if 'feedback' in st.session_state:
            st.write(st.session_state['feedback'])
    with col1:
        if st.button("New Question", disabled= not st.session_state['new_quest']) and st.session_state['selected_clef'] and st.session_state['selected_acci']:
            new_question(st.session_state['selected_clef'], st.session_state['selected_acci'], same_clef, compound_octave)
            st.session_state['picture'] = True
            st.session_state['new_quest'] = False
            st.rerun()

    if len(st.session_state['answer_history_in'])>2:
        if ss.logged:
            record_feedback(subject="Interval",text=str(ss['answer_history_in']))
            st.write("Feedback recorded!")
        st.session_state['answer_history_in']=[]

if __name__ == '__main__':
    interval_main()
