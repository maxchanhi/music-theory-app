import streamlit as st
from data_func import record_feedback
import random
from melody_key.chord_progression.question import lilypond_generation, question_generation, display_options, chord_accompany, audio_generation, chord_progression_checking
from melody_key.chord_progression.progression import main_generation, key_generation
from urls import disclaimer, rain_emoji
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
    ss["question_data"] = {
        "correct_index": correct_index,
        "options": options,
        "dis_options": dis_options,
        "key_signature": key_signature
    }

def button_pressed():
    ss["button_pressed_chord"] = True
def chord_progression_main():
    if "question_data" not in ss:
        ss["question_data"] = new_question(["Major"])  # Generate initial question
        ss["button_pressed_chord"] = True  # Allow checking answer for the first question
    if "ans_his_chord" not in ss:
        ss.ans_his_chord = []
    st.title("Identify the Correct Harmonic Progression")
    choosen_range = st.multiselect("Select the keys:", ["Major", "minor"], default=["Major"])

    if len(choosen_range) == 0:
        st.warning("Please select a key.")
        st.stop()
    
    if ss["question_data"]:
        st.image("melody_key/chord_progression/static/cropped_score_question.png", use_column_width=True)
        display_key = ss['question_data']['key_signature']
        display_opts = ss["question_data"]["dis_options"]
        user_ans = st.radio(f"Select the correct harmonic pattern in {display_key}:", display_opts, index=None)
    
    col1, col2 = st.columns([4, 1])
    with col1:
        if st.button("New Question", disabled=not ss["button_pressed_chord"]):
            new_question(choosen_range)  # Update question data
            ss["button_pressed_chord"] = False  # Allow checking answer for the new question
            st.rerun()
    with col2:
        check_ans = st.button("Check Answer", disabled= ss["button_pressed_chord"] or user_ans is None, on_click=button_pressed)
    
    if check_ans:
        options = ss["question_data"]["options"]
        correct_index = ss["question_data"]["correct_index"]
        if display_opts.index(user_ans) == correct_index:
            st.success(f"Correct!")
            rain_emoji()
            st.balloons()
            audio_generation()
            st.audio("melody_key/chord_progression/static/question.mp3")
            feedback = "correct"
        else:
            dis_idx = display_opts[ss["question_data"]["correct_index"]]
            st.warning(f"Incorrect! The answer is {dis_idx}")
            pick_idx = display_opts.index(user_ans)
            legal_progression = chord_progression_checking(options[pick_idx])
            feedback = "wrong"
            if legal_progression:
                feedback +=  ". But user can identify a legal progression."
            else:
                feedback += ". User with poor chord progression knowledge."
            st.write(f"Feedback: {feedback}")
        feedback += f" User picked range: {choosen_range}"
        ss.ans_his_chord.append(feedback)
        if ss.logged and len(ss.ans_his_chord) > 2:
            record_feedback(subject="chord progression", text =str(ss.ans_his_chord))
            ss.ans_his_chord = []
            st.write("Feedback recorded.")
    disclaimer()

if __name__ == "__main__":
    chord_progression_main()
