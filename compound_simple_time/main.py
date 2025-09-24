from compound_simple_time.melody import main_generate
from urls import disclaimer,rain_emoji
import random
import time
import os
import asyncio
from compound_simple_time.asynchronous import score_generation
from data_func import record_feedback
import streamlit as st

ss=st.session_state
if 'submit_pressed_com' not in st.session_state:
    st.session_state.submit_pressed_com = False

if 'new_question_pressed_com' not in st.session_state:
    st.session_state.new_question_pressed_com = False
    
def new_question_pressed():
    st.session_state.new_question_pressed_com = True

def submit_pressed():
    st.session_state.submit_pressed_com = True

def select_option(idx):
    if st.session_state.option_selected is not None:
        st.session_state[f"disabled_{st.session_state.option_selected}"] = False
    st.session_state.option_selected = idx
    st.session_state[f"disabled_{idx}"] = True
    

def compound_simple_main():
    # Initialize session state variables
    if 'option_selected' not in st.session_state:
        st.session_state.option_selected = []
        ss["feedback_mm"]=[]
        st.session_state.new_question_pressed_com = False

    # Generate the first question if not exists
    if 'question_data_com' not in st.session_state:
        # Ensure proper randomization for the first question
        random.seed(int(time.time() * 1000))
        
        st.session_state.question_data_com = main_generate()
        st.session_state.question_data_com = asyncio.run(score_generation(st.session_state.question_data_com))
        st.session_state.submit_pressed_com = False

    question_data = st.session_state.question_data_com
    st.title("Compound-simple-time Modulation Quiz")
    st.subheader(question_data['question'])
    
    st.image("compound_simple_time/temp/cropped_score_question_melody.png", caption='Question')

    for idx, option_data in enumerate(question_data['options']):
        # Defensive unpack: support (option, reason) and (option, reason, image_path)
        if len(option_data) == 3:
            option, reason, image_path = option_data
        else:
            option, reason = option_data
            image_path = None
        container = st.container()
        col1, col2 = container.columns([6, 1])
        if image_path:
            col1.image(image_path)  # Use the image path from the option data if available
        
        if f"disabled_{idx}" not in st.session_state:
            st.session_state[f"disabled_{idx}"] = False

        col2.button(
            f'Option {idx + 1}',
            key=f"option_{idx}",
            on_click=select_option,
            args=(idx,),
            disabled=st.session_state[f"disabled_{idx}"]
        )

        # Store the reason in session state
        st.session_state[f"reason_{idx}"] = reason
    if st.session_state.new_question_pressed_com:
        # Generate new question synchronously
        st.session_state.new_question_pressed_com = False
        random.seed(int(time.time() * 1000))
        st.session_state.question_data_com = main_generate()
        st.session_state.question_data_com = asyncio.run(score_generation(st.session_state.question_data_com))

        # Reset all states for the new question
        st.session_state.submit_pressed_com = False
        
        st.session_state.option_selected = []
        # Reset disabled state for options
        for i in range(len(st.session_state.question_data_com['options'])):
            if f"disabled_{i}" in st.session_state:
                del st.session_state[f"disabled_{i}"]
        st.rerun()
    pressed= st.session_state.submit_pressed_com


    col_1,col_2=st.columns([4,1])
    with col_1:
        new_question_btn = st.button("New Question", on_click=new_question_pressed, disabled=not pressed)
    with col_2:
        check_ans_mm=st.button("Check Answer",on_click=submit_pressed,disabled=pressed)

    # Handle new question logic ONLY when the button is actually clicked
    

    if check_ans_mm and st.session_state.option_selected is not None:
        correct_idx = None
        for idx, option_data in enumerate(question_data["options"]):
            # Defensive unpack again for answer-checking
            if len(option_data) == 3:
                option, reason, image_path = option_data
            else:
                option, reason = option_data
                image_path = None

            if isinstance(option, (tuple, list)) and len(option) >= 2:
                time_signature, melody = option[0], option[1]
            else:
                st.warning(f"Unexpected option format at index {idx}: {option}")
                continue

            if time_signature == question_data["answer"][0] and melody == question_data["answer"][1]:
                correct_idx = idx
                break

        if correct_idx is not None:
            if st.session_state.option_selected == correct_idx:
                rain_emoji()
                st.success("Correct answer!")
                ss["feedback_mm"].append(("Correct", ""))
            else:
                st.error(f"Wrong answer! The correct answer is Option {correct_idx + 1}")
                if f"reason_{st.session_state.option_selected}" in st.session_state:
                    feedback = f"Reason for the wrong choice: {st.session_state[f'reason_{st.session_state.option_selected}']}"
                    st.info(feedback)
                    ss["feedback_mm"].append(("Wrong", feedback))
                else:
                    ss["feedback_mm"].append(("Wrong", "No reason found for the selected option"))
        else:
            st.error("An error occurred: Could not find the correct answer in the options.")
            
    if len(ss["feedback_mm"])>2 and ss.logged:
        record_feedback("metric modulation",ss.feedback_mm)
        st.write("Feedback recorded")
        ss["feedback_mm"]=[]

    disclaimer()

if __name__ == "__main__":
    compound_simple_main()
