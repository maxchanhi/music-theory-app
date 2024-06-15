import streamlit as st
ss = st.session_state
from PIL import Image
import io
from grouping_quiz.wrong_cat import needle_in_haystack
from urls import rain_emoji

def button_pressed_gp(idx):
    ss["press_idx_gp"] = idx
    print("Pressed", idx)

def grouping_quiz_main():
    if "grouping_link" not in ss:
        ss["grouping_link"] = []
    
    if "check_ans" not in ss:
        ss["check_ans"] = True
    
    if "press_idx_gp" not in ss:
        ss["press_idx_gp"] = None

    st.title("Grouping and beaming quiz")

    if st.button("New Question") and ss["check_ans"]:
        ss["grouping_link"] = needle_in_haystack()
        ss["check_ans"] = False
        ss["press_idx_gp"] = None

    if len(ss["grouping_link"]) > 0:
        for idx, link in enumerate(ss["grouping_link"]):
            col_1, col_2 = st.columns([5, 1])
            with col_1:
                st.image(link)

            with col_2:
                st.write("    ")
                st.button(f"Option {idx+1}", key=idx, on_click=button_pressed_gp, args=(idx,), disabled=idx == ss["press_idx_gp"])

    if st.button("Check answer", disabled=ss["check_ans"]) and ss["press_idx_gp"] is not None:
        ss["check_ans"] = True
        if "Correct_rest" in ss["grouping_link"][ss["press_idx_gp"]]:
            st.success("Correct")
            rain_emoji()
        else:
            correct_idx = ss["press_idx_gp"]
            st.warning(f"Wrong. The answer is option {correct_idx}")
        ss["press_idx_gp"] = None

if __name__ == "__main__":
    grouping_quiz_main()
