from compound_simple_time.melody import main_generate
from urls import disclaimer,rain_emoji
import asyncio,random
from compound_simple_time.asynchronous import score_generation
def submit_pressed():
    st.session_state.submit_pressed_com = True
def select_option(idx):
    if st.session_state.option_selected is not None:
        st.session_state[f"disabled_{st.session_state.option_selected}"] = False
    st.session_state.option_selected = idx
    st.session_state[f"disabled_{idx}"] = True
def compound_simple_main():
    if 'option_selected' not in st.session_state:
        st.session_state.option_selected = []
    
    if 'question_data_com' not in st.session_state:
        st.session_state.question_data_com = main_generate()
        st.session_state.submit_pressed_com = False
        asyncio.run(score_generation(st.session_state.question_data_com))
    
    question_data = st.session_state.question_data_com
    st.title("Compound-simple-time Modulation Quiz")
    st.subheader(question_data['question'])
    
    st.image("compound_simple_time/temp/cropped_score_question_melody.png", caption='Question')

    for idx, option in enumerate(question_data['options']):
        container = st.container()
        col1, col2 = container.columns([6, 1])
        col1.image(f"compound_simple_time/temp/cropped_score_wr_option_{idx}.png")
            
        if f"disabled_{idx}" not in st.session_state:
            st.session_state[f"disabled_{idx}"] = False

        col2.button(
            f'Option {idx + 1}',
            key=f"option_{idx}",
            on_click=select_option,
            args=(idx,),
            disabled=st.session_state[f"disabled_{idx}"]
        )

    pressed= st.session_state.submit_pressed_com
    col_1,col_2=st.columns([5,1])
    with col_1:
        if st.button("New Question",on_click=submit_pressed,disabled= not pressed ) and st.session_state.submit_pressed_com:
            st.session_state.question_data_com = main_generate()
            asyncio.run(score_generation(st.session_state.question_data_com))
            st.session_state.submit_pressed_com = False
            st.rerun()
    with col_2:
        check_ans_mm=st.button("Check Answer",on_click=submit_pressed,disabled=pressed)
    if check_ans_mm and st.session_state.option_selected is not None:
        correct_idx = None
        for idx, (time, melody) in enumerate(question_data["options"]):
            if time == question_data["answer"][0] and melody == question_data["answer"][1]:
                correct_idx = idx
                break

        if st.session_state.option_selected == correct_idx:
            rain_emoji()
        else:
            st.error(f"Wrong answer! The correct answer is Option {correct_idx + 1}")

    disclaimer()
if __name__ == "__main__":
    compound_simple_main()
