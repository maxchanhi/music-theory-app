

def knowledgemain():
    import streamlit as st
    from instrument_knowledge_quiz.topics import pick_topic
    from instrument_knowledge_quiz.data import fun_emoji_list
    from streamlit_extras.let_it_rain import rain
    from instrument_knowledge_quiz.AIfeedback import provide_feedback
    from instrument_knowledge_quiz.preembed import login_for_feedback,rag_feedback
    import random

    ss = st.session_state
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

    def password_entered():
        if ss['userpd'] in st.secrets['Password'] :
            ss["pw_visible"] = False
            st.rerun()
        else:
            st.write("You can only preview!")
    if ss["pw_visible"]:
        ss['userpd'] = st.text_input('Enter your password for full access or find Max for password:',type= "password")
        if st.button('Submit Password'):
            password_entered()
    if not ss["pw_visible"]:
        st.success("You now have full access to the feedback!")
    if len(ss["student_ans"])==0:
        st.warning("Tip: You need to answer at least 5 questions to get the AI feedback.")
    topics = ['Reed', 'Transposing', "Clef", "Voice types", "Piano", "Ornaments", "Inst. technique"]
    topics_selected = st.multiselect('Select topics to be quizzed on:', topics, default=topics)
    new_question = st.button('New question')
    if not topics_selected:
        st.warning('Please select at least one topic.')
    if new_question and topics_selected and ss["pressed_kn"]:
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
        reed_options = st.radio("Options:", choosen_topic['options'])
        if st.button('Check Answer', disabled=ss["pressed_kn"]):
            ss["pressed_kn"] = True
            if reed_options == choosen_topic['answer']:
                fun_emoji = random.choice(fun_emoji_list)
                st.success(f"Correct!{fun_emoji}")
                rain(emoji=fun_emoji, animation_length="1")
                st.balloons()
                ss["student_ans"].append([choosen_topic['question'], "student answer: " + reed_options, "correct"])
            else:
                st.error(f"Wrong! The correct answer is {choosen_topic['answer']}.")
                ss["student_ans"].append([choosen_topic['question'], "student answer: " + reed_options, "incorrect"])
            print(ss["student_ans"])

    if len(ss["student_ans"]) > 5:
        if st.button('You can get an AI feedback'):
            with st.spinner("Generating feedback..."):
                if not ss["pw_visible"]:
                    st.write("Full feedback: ")
                    feedback = provide_feedback(ss["student_ans"], 512)
                else:
                    st.write("Limited feedback: ")
                    feedback = provide_feedback(ss["student_ans"], 64)
            st.success(feedback)
            ss["student_ans"] = []

if __name__ == '__main__':
    knowledgemain()
