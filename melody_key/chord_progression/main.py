def chord_progression_main():
    import streamlit as st
    from melody_key.chord_progression.notation import fun_emoji_list
    import random
    from melody_key.chord_progression.question import lilypond_generation,question_generation,display_options,chord_accompany,audio_generation
    from melody_key.chord_progression.progression import main_generation,key_generation
    from streamlit_extras.let_it_rain import rain
    ss=st.session_state
    if "button_pressed_chord" not in ss:
        ss["button_pressed_chord"]=False
    def new_question(choosen_range="Major"):
        choosen_key=key_generation(choosen_range)
        ss["question_data"] = main_generation(choosen_key)
        score_melody = ss["question_data"]["melody"]
        correct_option = ss["question_data"]["chord"]
        key_signature = ss["question_data"]["key"]
        accom_part=chord_accompany(key_signature,correct_option)
        lilypond_generation(score_melody, "question",key_signature,accom_part)
        correct_index,options=question_generation(correct_option)
        options= display_options(options)
        
        return correct_index,options,key_signature
    def button_pressed():
        ss["button_pressed_chord"]=True

    #st.set_page_config(page_title="Harmonise melody")

    st.title("Identify the Correct Harmonic Pattern")
    choosen_range = st.multiselect("Select the keys:",["Major","minor"],default=["Major"])

    if len(choosen_range) ==0:
        st.warning("Please select a key.")
        st.stop()
    new_score = st.button("Generate Score")

    if new_score and ss["button_pressed_chord"]:
        ss["question_data"]=new_question(choosen_range)
        st.rerun()
    if "question_data" not in ss:
        ss["question_data"]=new_question(choosen_range)

    correct_index,options,key_signature=ss["question_data"]

    st.image("melody_key/chord_progression/static/cropped_score_question.png", use_column_width=True)
    user_ans = st.radio(f"Select the correct harmonic pattern in {key_signature}:",options)

    if st.button("Submit",on_click=button_pressed,disabled=ss["button_pressed_chord"]):
        if options.index(user_ans) == correct_index:
            emoji= random.choice(fun_emoji_list)
            st.success(f"Correct!{emoji}")
            rain(emoji=emoji,animation_length=1)
            st.balloons()
            audio_generation()
            st.audio("melody_key/chord_progression/static/question.mp3")
        else:
            st.warning(f"Incorrect! The answer is {options[correct_index]}")
if __name__ == "__main__":
    chord_progression_main()
