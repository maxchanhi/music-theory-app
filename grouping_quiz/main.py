import streamlit as st
#st.set_page_config(page_title="Grouping and beaming quiz")
def grouping_quiz_main():
    
    import random
    from grouping_quiz.wrong_cat import main_option,catagory,fun_emoji_list
    from streamlit_extras.let_it_rain import rain
    
    ss=st.session_state
    if "question_data_g" not in ss:
        ss.question_data_g=main_option()
        ss["check_ans"]=False

    question_data=ss.question_data_g
    st.title("Grouping and beaming quiz")
    new_question = st.button("New Question")
    st.image(question_data["Picture"])
    user_ans=st.radio("Choose the correct answer",catagory)
    correct_ans=question_data["Catagory"]


    if st.button("Check answer",disabled=ss["check_ans"]):
        ss["check_ans"]=True
        print(user_ans,question_data["Picture"])
        if user_ans==correct_ans:
            st.success("Correct")
            fun_emoji = random.choice(fun_emoji_list)
            rain(emoji = fun_emoji,animation_length="1")
        else:
            st.warning(f"Wrong. The answer is {correct_ans}")

    if new_question and ss["check_ans"]:
        ss.question_data_g=main_option()
        ss["check_ans"]=False
        st.rerun()
if __name__=="__main__":
    grouping_quiz_main()
