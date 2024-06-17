import streamlit as st
from melody_key.chord_progression.notation import fun_emoji_list
import random
from melody_key.chord_progression.question import lilypond_generation, question_generation, display_options, chord_accompany, audio_generation
from melody_key.chord_progression.progression import main_generation, key_generation
from streamlit_extras.let_it_rain import rain
from urls import disclaimer
ss = st.session_state
def new_question(choosen_range="Major"):
    choosen_key = key_generation(choosen_range)
    question_data = main_generation(choosen_key)
    score_melody = question_data["melody"]
    correct_option = question_data["chord"]
    key_signature = question_data["key"]
    accom_part = chord_accompany(key_signature, correct_option)
    lilypond_generation(score_melody, "question", key_signature, accom_part)
    correct_index, options = question_generation(correct_option)
    dis_options = display_options(options)
    ss["button_pressed_chord"] = False
    return {
        "correct_index": correct_index,
        "options": options,
        "dis_options": dis_options,
        "key_signature": key_signature
    }

def button_pressed():
    ss["button_pressed_chord"] = True
def chord_progression_main():
    
    if "button_pressed_chord" not in ss:
        ss["button_pressed_chord"] = False
    # st.set_page_config(page_title="Harmonise melody")
    
    st.title("Identify the Correct Harmonic Pattern")
    choosen_range = st.multiselect("Select the keys:", ["Major", "minor"], default=["Major"])

    if len(choosen_range) == 0:
        st.warning("Please select a key.")
        st.stop()

    if "question_data" not in ss:
        ss["question_data"] = new_question(choosen_range)
        
    st.image("melody_key/chord_progression/static/cropped_score_question.png", use_column_width=True)
    display_key = ss['question_data']['key_signature']
    display_opts = ss["question_data"]["dis_options"]
    user_ans = st.radio(f"Select the correct harmonic pattern in {display_key}:", display_opts)

    col1, col2 = st.columns([4, 1])
    with col1:
        new_score = st.button("New Question", disabled=not ss["button_pressed_chord"], on_click=new_question, args=(choosen_range,))
    with col2:
        check_ans = st.button("Check Answer", disabled=ss["button_pressed_chord"], on_click=button_pressed)

    if check_ans:
        options = ss["question_data"]["options"]
        correct_index = ss["question_data"]["correct_index"]
        if display_opts.index(user_ans) == correct_index:
            emoji = random.choice(fun_emoji_list)
            st.success(f"Correct!{emoji}")
            rain(emoji=emoji, animation_length=1)
            st.balloons()
            audio_generation()
            st.audio("melody_key/chord_progression/static/question.mp3")
        else:
            dis_idx = display_opts[ss["question_data"]["correct_index"]]
            st.warning(f"Incorrect! The answer is {dis_idx}")
    disclaimer()

if __name__ == "__main__":
    chord_progression_main()
