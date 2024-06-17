import streamlit as st
from transposing.main_generation import picture_generation
from transposing.get_pictures import get_pic_link
from urls import disclaimer, rain_emoji
def disable_option_tr(idx):
    st.session_state.dis_option_tr=idx
def transposing_main():
    st.header("Transposition Quiz")
    
    if "transposed_by" not in st.session_state:
        st.session_state['transposed_by'] = ""
        st.session_state['presses_tran'] = True
        st.session_state['img_link'] = []
        st.session_state['selected_answer_tr'] = None
        st.session_state['answer_checked_tr'] = False
        st.session_state.dis_option_tr=None
    
    if st.session_state.transposed_by:
        st.write("This is the original melody:")
        st.image("transposing/static/question.png", use_column_width=True)
        st.write(f"Which one is correctly transposed {st.session_state.transposed_by}?")
        st.write("Pick the correct answer:")
        
    for idx, link in enumerate(st.session_state.img_link):
        col1, col2 = st.columns([5, 1])
        with col1:
            st.image(f'transposing/{link}', use_column_width=True)
        with col2:
            if st.button(f"Option {idx + 1}", key=f"btn_{idx}", on_click=disable_option_tr, args=(idx,),
                         disabled=idx==st.session_state.dis_option_tr):
                st.session_state.selected_answer_tr = idx
                st.session_state.answer_checked_tr = False  # Reset check on new selection
    
    col1, col2 = st.columns([5, 1])
    with col2:
        if st.session_state.selected_answer_tr is not None and not st.session_state.answer_checked_tr:
            check_ans = st.button("Check answer",disabled=st.session_state.answer_checked_tr)
                
    
    with col1:
        if st.session_state.answer_checked_tr or not st.session_state.transposed_by:
            if st.button("Generate question"):
                st.session_state.transposed_by = picture_generation()
                st.session_state.presses_tran = False
                st.session_state.img_link = get_pic_link()
                st.session_state.selected_answer_tr = None
                st.session_state.answer_checked_tr = False
                st.session_state.dis_option_tr=None
                st.rerun()
    if check_ans:
        st.session_state.answer_checked_tr = True
        if "correct" in st.session_state['img_link'][st.session_state.selected_answer_tr]:
            st.success("Correct!")
            rain_emoji()
        else:
            correct_idx = [i for i, link in enumerate(st.session_state.img_link) if "correct" in link][0] + 1
            st.error(f"Incorrect. Image {correct_idx} is the correct answer.")
    disclaimer()
