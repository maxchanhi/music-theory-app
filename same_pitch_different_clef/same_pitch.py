import streamlit as st
from notation import main_generation
from urls import rain_emoji
ss=st.session_state

def press_callback_check_ans():
    ss.button_clicked_check_ans = False

def option_callback(p_idx):
    if p_idx not in ss.pick_ans:
        ss.pick_ans.append(p_idx)

if "button_clicked_check_ans" not in ss:
    ss.button_clicked_check_ans = False
    ss.pick_ans=[]
    ss.data_pc=[]
st.header("Clef and Pitch quiz")
col1, col2 = st.columns([4, 1])

with col1:
    st.subheader("Pick two melody that they are at the same pitch.")
if ss.data_pc:
    with col2:
        st.write("   ")
        if st.button("Reset",type="primary"):
            ss.pick_ans = []
            st.rerun()
    for idx, link in enumerate(ss.data_pc):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.image(link+".png")
        with col2:
            st.button(f"Option {idx+1}",key=idx,disabled=idx in ss.pick_ans, on_click=option_callback,args=(idx,))


col1, col2 = st.columns([4, 1])
with col1:
    new_ques = st.button("New Question", disabled=ss.button_clicked_check_ans)

with col2:
    check_ans= st.button("Check Answer", disabled=not ss.button_clicked_check_ans or len(ss.pick_ans)!=2, on_click=press_callback_check_ans)
        
if new_ques:
    ss.data_pc=main_generation()
    print("data:",ss.data_pc)
    ss.button_clicked_check_ans = True
    ss.pick_ans=[]
    st.rerun()

if check_ans:
    correct_idx=[]
    for idx_l,link in enumerate(ss.data_pc):
        if "same" in link:
            correct_idx.append(idx_l)
    if set(ss.pick_ans) == set(correct_idx):
        st.success("Correct!")
        rain_emoji()
    else:
        str_ans = ' and '.join(str(idx+1) for idx in correct_idx)
        st.error(f"Incorrect! The correct pair should be {str_ans}.")