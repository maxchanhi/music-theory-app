import streamlit as st
from melody_key.notation import keyscale,easymode,intermediate,fun_emoji_list,hard
import random
from melody_key.score_generation import lilypond_generation
from melody_key.motif import generate_options,main_generation
from streamlit_extras.let_it_rain import rain
from urls import disclaimer,rain_emoji
#st.set_page_config(page_title="Identify Key in Melody")
def melody_key_main():
    
    st.title("Identify the Key in Melody")

    difficulty = st.selectbox("Select Difficulty", ["Easy Mode (2 sharps to 2 flats)", 
                                                    "Intermediate Mode (5 sharps to 5 flats)",
                                                    "Advanced Mode (All sharps and flats)",
                                                    "Custom Mode"])

    # Filter the keyscale dictionary based on the selected difficulty
    filtered_keyscale = {}

    if difficulty == "Easy Mode (2 sharps to 2 flats)":
        disable_select = True
        for key, scale in keyscale.items():
            if key in easymode:
                filtered_keyscale[key] = scale
    elif difficulty == "Intermediate Mode (5 sharps to 5 flats)":
        disable_select = True  
        for key, scale in keyscale.items():
            if key in intermediate:
                filtered_keyscale[key] = scale
    elif difficulty == "Advanced Mode (All sharps and flats)":
        disable_select = True 
        for key, scale in keyscale.items():
            if key in hard:
                filtered_keyscale[key] = scale
    else:
        filtered_keyscale = keyscale
        disable_select = False

    selected_keys = st.multiselect("Selected Keys", list(filtered_keyscale.keys()),filtered_keyscale,disabled=disable_select)
    if len(selected_keys) <5:
        st.warning("Please select at least five keys to generate a question.")
        st.stop()
    if 'user_answer_mk' not in st.session_state:
        st.session_state['user_answer_mk'] = ''
    if 'ans_key_mk' not in st.session_state:
        st.session_state['ans_key_mk'] = ''
    if 'options_mk' not in st.session_state:
        st.session_state['options_mk'] = ''
    if "pressed_mk" not in st.session_state:
        st.session_state["pressed_mk"] = True
    
    col1, col2 = st.columns([4, 1])

    with col1:
        new_score = st.button("Generate Score")
    with col2:
        check = st.button("Check Answer", disabled=st.session_state["pressed_mk"])
    if new_score and selected_keys and st.session_state["pressed_mk"]:
        st.session_state["pressed_mk"] = False
        st.session_state['ans_key_mk'] = random.choice(selected_keys)
        st.session_state['options_mk'] = generate_options(st.session_state['ans_key_mk'], selected_keys)
        melody = main_generation(st.session_state['ans_key_mk'])
        lilypond_generation(melody, "testing", 4, 4)
        print("options", st.session_state['options_mk'])
        st.rerun()
    
        if st.session_state['options_mk']:
            st.write("What key is the score in?")
            try:
                st.image("melody_key/score.png", use_column_width=True)
                st.audio("melody_key/testing.mp3", format="audio/mpeg")
                user_answer = st.radio("Select the key:", st.session_state['options_mk'], index=None)
                st.session_state['user_answer_mk'] = user_answer
    
                ans_key = st.session_state['ans_key_mk']
                print("user_answer", st.session_state['user_answer_mk'], "ans_key", ans_key)
            except:
                st.warning("Press Generate Score")
    if check and st.session_state['user_answer_mk'] is not None:
        st.session_state["pressed_mk"] = True
        if st.session_state['user_answer_mk'] == ans_key and st.session_state['user_answer_mk'] is not None:
            st.success("Correct!")
            rain_emoji()
        elif user_answer != ans_key:
            st.warning(f"Incorrect. The correct answer is {st.session_state['ans_key_mk']}.")

    disclaimer()
if __name__ == "__main__":
    melody_key_main()
