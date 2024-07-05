
import streamlit as st
from instrument_knowledge_quiz.topics import pick_topic
from urls import rain_emoji
import random
from data_func import record_feedback_list
import json
ss = st.session_state
def callback():
    ss["pressed_kn"] = True
def knowledgemain():
    if "choosen_topic" not in ss:
        ss["choosen_topic"] = None
        ss["userpd"] = None
        ss["get_url"] = None

    if "student_ans" not in ss:
        ss["student_ans"] = []
    if "pressed_kn" not in ss:
        ss["pressed_kn"] = True
        ss["pw_visible"] = True   
    st.title('Instrumental Knowledge Quiz')

    if len(ss["student_ans"])==0:
        st.warning("Tip: You need to answer at least 5 questions to get the AI feedback.")
    topics = ['Reed', 'Transposing', "Clef", "Voice types", "Piano", "Ornaments", "Inst. technique"]
    topics_selected = st.multiselect('Select topics to be quizzed on:', topics, default=topics)
    if not topics_selected:
        st.warning('Please select at least one topic.')
    def new_question_call():
        ss["pressed_kn"] = False
        test_topic = random.choice(topics_selected)
        ss["choosen_topic"] = pick_topic(test_topic)
        choosen_topic = ss["choosen_topic"]
        if test_topic == "Ornaments":
            ss["get_url"] = "instrument_knowledge_quiz/"+ss["choosen_topic"]["pic_url"]
        else:
            ss["get_url"] = None
    
    if ss["choosen_topic"]:
        choosen_topic = ss["choosen_topic"]
        st.subheader(choosen_topic['question'])
        if ss["get_url"]:
            st.image(ss["get_url"])
        reed_options = st.radio("Options:", choosen_topic['options'],index=None)
    col_1,col_2=st.columns([4,1])
    with col_1:
        st.button('New question',disabled= not ss["pressed_kn"],on_click=new_question_call)
    with col_2:
        check_bn = st.button('Check Answer', disabled=ss["pressed_kn"] or 
                             reed_options is None, on_click=callback)
            
    if check_bn:
        if reed_options == choosen_topic['answer']:
            rain_emoji()
            st.success(f"Correct!")
            st.balloons()
            ss["student_ans"].append([choosen_topic['question'], "student answer: " + reed_options, "correct"])
        else:
            st.error(f"Wrong! The correct answer is {choosen_topic['answer']}.")
            ss["student_ans"].append([choosen_topic['question'], "student answer: " + reed_options, "incorrect"])
        print(ss["student_ans"])
    
    
    if len(ss["student_ans"]) > 5 and ss.logged:
        ans = json.dumps(ss["student_ans"])  # Convert to JSON string
        user = ss.user_info["user_id"]
        record_feedback_list(user, "instrumental knowledge", ans)
        st.success("Your answers have been recorded.")
        ss["student_ans"] = []

if __name__ == '__main__':
    knowledgemain()
