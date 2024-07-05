import streamlit as st
from instrument_knowledge_quiz.topics import pick_topic
from urls import rain_emoji
import random
from data_func import record_feedback,get_feedback
import json

ss = st.session_state

def callback():
    ss["pressed_kn"] = True

def new_question_call(topics_selected):
    ss["pressed_kn"] = False
    test_topic = random.choice(topics_selected)
    ss["choosen_topic"] = pick_topic(test_topic)
    choosen_topic = ss["choosen_topic"]
    if test_topic == "Ornaments":
        ss["get_url"] = "instrument_knowledge_quiz/" + ss["choosen_topic"]["pic_url"]
    else:
        ss["get_url"] = None

def initialize_session_state():
    if "choosen_topic" not in ss:
        ss["choosen_topic"] = None
        ss["userpd"] = None
        ss["get_url"] = None
    if "student_ans" not in ss:
        ss["student_ans"] = []
    if "pressed_kn" not in ss:
        ss["pressed_kn"] = True
        ss["pw_visible"] = True

def display_quiz_interface(topics_selected):
    if ss["choosen_topic"]:
        choosen_topic = ss["choosen_topic"]
        st.subheader(choosen_topic['question'])
        if ss["get_url"]:
            st.image(ss["get_url"])
        reed_options = st.radio("Options:", choosen_topic['options'], index=None)
    else:
        reed_options = None

    col_1, col_2 = st.columns([4,1])
    with col_1:
        st.button('New question', disabled=not ss["pressed_kn"], on_click=lambda: new_question_call(topics_selected))
    with col_2:
        check_bn = st.button('Check Answer', disabled=ss["pressed_kn"] or reed_options is None, on_click=callback)

    return reed_options, check_bn

def process_answer(reed_options, choosen_topic):
    if reed_options == choosen_topic['answer']:
        rain_emoji()
        st.success(f"Correct!")
        st.balloons()
        ss["student_ans"].append([choosen_topic['question'], "student answer: " + reed_options, "correct"])
    else:
        st.error(f"Wrong! The correct answer is {choosen_topic['answer']}.")
        ss["student_ans"].append([choosen_topic['question'], "student answer: " + reed_options, "incorrect"])
    print(ss["student_ans"])

def record_answers():
    if len(ss["student_ans"]) > 2:
        if ss.logged:
            record_feedback("instrumental knowledge", str(ss["student_ans"]))
            st.write("Feedback recorded.")
        ss["student_ans"] = []

def knowledgemain():
    initialize_session_state()
    st.title('Instrumental Knowledge Quiz')

    if len(ss["student_ans"]) == 0:
        st.warning("Tip: You need to answer at least 5 questions to get the AI feedback.")

    topics = ['Reed', 'Transposing', "Clef", "Voice types", "Piano", "Ornaments", "Inst. technique"]
    topics_selected = st.multiselect('Select topics to be quizzed on:', topics, default=topics)
    
    if not topics_selected:
        st.warning('Please select at least one topic.')
    else:
        reed_options, check_bn = display_quiz_interface(topics_selected)
        
        if check_bn:
            process_answer(reed_options, ss["choosen_topic"])
        
        record_answers()

if __name__ == '__main__':
    knowledgemain()