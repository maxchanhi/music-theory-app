import streamlit as st
ss = st.session_state
from PIL import Image
import io
from grouping_quiz.wrong_cat import needle_in_haystack
from urls import rain_emoji
from data_func import record_feedback
def button_pressed_gp(idx):
    ss["press_idx_gp"] = idx

def check_answer_gp():
    ss["check_ans"] = True
def grouping_quiz_main():
    if "grouping_link" not in ss:
        ss["grouping_link"] = []
        ss.ans_his_gp = []
    if "check_ans" not in ss:
        ss["check_ans"] = True
    
    if "press_idx_gp" not in ss:
        ss["press_idx_gp"] = None

    st.title("Grouping and beaming quiz")
    st.subheader("Which melody is correctly grouped and beaming without hemiola?")
    if len(ss["grouping_link"]) > 0:
        for idx, link in enumerate(ss["grouping_link"]):
            col_1, col_2 = st.columns([5, 1])
            with col_1:
                st.image(link[0])
            with col_2:
                st.write("    ")
                st.button(f"Option {idx+1}", key=idx, on_click=button_pressed_gp, args=(idx,), disabled=idx == ss["press_idx_gp"] or ss["check_ans"])
    col_1, col_2 = st.columns([4, 1])
    with col_1:
        if st.button("New Question",disabled= not ss["check_ans"]) and ss["check_ans"]:
            ss["grouping_link"] = needle_in_haystack()
            ss["check_ans"] = False
            ss["press_idx_gp"] = None
            st.rerun()
    with col_2:
        check_ans_gp = st.button("Check answer", on_click=check_answer_gp, disabled= ss["check_ans"])
    if check_ans_gp and ss["press_idx_gp"] is not None:
        selected_image, selected_tag = ss["grouping_link"][ss["press_idx_gp"]]
        correct_idx = next((i for i, (_, tag) in enumerate(ss["grouping_link"]) if "Correct notation" in tag), None)
        
        if correct_idx is None:
            st.error("Error: No correct answer found in the options. Please generate a new question.")
            feedback = None
        elif ss["press_idx_gp"] == correct_idx:
            st.success("Correct")
            feedback = "correct"
            rain_emoji()
        else:
            useridx=ss["press_idx_gp"]
            st.warning(f"Option {useridx+1} is wrong. The correct answer is option {correct_idx + 1}. The problem with your choice is: {selected_tag}.")
            feedback =f"Option {useridx+1} is wrong. The problem with your choice is: {selected_tag}."
        if ss.logged:
            ss.ans_his_gp.append(feedback)
            if len(ss.ans_his_gp) > 2:
                record_feedback(subject="grouping and beaming", text=str(ss.ans_his_gp))
                st.write("Feedback recorded")
                ss.ans_his_gp = []
        ss["press_idx_gp"] = None
        ss["check_ans"] = True
if __name__ == "__main__":
    grouping_quiz_main()
