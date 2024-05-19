import streamlit as st
def main_inversion():
    from inversion.inversion_gen import main_generation
    from inversion.notation import roman_numerial, inversion_type,fun_emoji_list
    import random
    from streamlit_extras.let_it_rain import rain
    st.title("Inversion quiz")
    select_clef = st.selectbox("Select the clef that you want to test on:",options=["treble","bass","grand staff"],index=0)
    # Initialize session state variables
    if "question_data_iv" not in st.session_state:
        st.session_state["question_data_iv"] = None
    if "pressed_iv" not in st.session_state:
        st.session_state["pressed_iv"] = True

    try:
        key_signature = st.session_state["question_data_iv"]["key_sign"]
        st.subheader(f"What is this chord in {key_signature}?")
        st.image("inversion/cropped_score.png", use_column_width="auto")
    except:
        st.warning("Please generate a New Question")

    col1, col2 = st.columns(2)
    with col1:
        user_nu = st.selectbox("Choose the Roman numeral:", options=roman_numerial)
        if st.button("New Question") and st.session_state["pressed_iv"]:
            st.session_state["pressed_iv"] = False
            print(select_clef)
            st.session_state["question_data_iv"] = main_generation()
            st.rerun()
    with col2:
        user_iv = st.selectbox("Choose the inversion type:", options=inversion_type)
        check_ans= st.button("Check Answer", disabled=st.session_state["pressed_iv"])
    if check_ans and st.session_state["question_data_iv"]:
        st.session_state["pressed_iv"] = True
        user_ans = f'{user_nu} {user_iv}'
        correct_ans = st.session_state["question_data_iv"]["triad"] + " " + st.session_state["question_data_iv"]["inversion_type"]
        print("User answer:", user_ans,"Correct answer:", correct_ans)
        if user_ans == correct_ans:
            emo = random.choice(fun_emoji_list)
            st.success(f"Correct!{emo}")
            st.balloons()
            rain(emo,animation_length=1)
        elif user_ans != correct_ans:
            st.warning(f"The correct answer is {correct_ans}")
        else:
            st.error("Please try again.")
