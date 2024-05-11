
def compound_simple_main():

    def select_option(idx):
        if st.session_state.option_selected is not None:
            st.session_state[f"disabled_{st.session_state.option_selected}"] = False
        st.session_state.option_selected = idx
        st.session_state[f"disabled_{idx}"] = True
    from compound_simple_time.melody import main_generate
    from compound_simple_time.notation import fun_emoji_list
    import asyncio,random
    from compound_simple_time.asynchronous import score_generation
    import streamlit as st
    from streamlit_extras.let_it_rain import rain

    if 'option_selected' not in st.session_state:
        st.session_state.option_selected = []
    
    if 'question_data_com' not in st.session_state:
        st.session_state.question_data_com = main_generate()
        st.session_state.submit_pressed_com = False
        asyncio.run(score_generation(st.session_state.question_data_com))
    

    question_data = st.session_state.question_data_com
    st.title("Compound-simple-time Modulation Quiz")
    st.subheader(question_data['question'])
    if st.button("Generate New Question") and st.session_state.submit_pressed_com:
        st.session_state.question_data_com = main_generate()
        asyncio.run(score_generation(st.session_state.question_data_com))
        st.session_state.submit_pressed_com = False
    st.image("compound_simple_time/static/cropped_score_question_melody.png", caption='Question')

    for idx, option in enumerate(question_data['options']):
        container = st.container()
        col1, col2 = container.columns([6, 1])
        col1.image(f"compound_simple_time/static/cropped_score_wr_option_{idx}.png")
            
        if f"disabled_{idx}" not in st.session_state:
            st.session_state[f"disabled_{idx}"] = False

        col2.button(
            f'Option {idx + 1}',
            key=f"option_{idx}",
            on_click=select_option,
            args=(idx,),
            disabled=st.session_state[f"disabled_{idx}"]
        )
    def submit_pressed():
        st.session_state.submit_pressed_com = True
    pressed= st.session_state.submit_pressed_com
    if st.button("Submit Answer",on_click=submit_pressed,disabled=pressed):
        correct_idx = None
        for idx, (time, melody) in enumerate(question_data["options"]):
            if time == question_data["answer"][0] and melody == question_data["answer"][1]:
                correct_idx = idx
                break

        if st.session_state.option_selected == correct_idx:
            fun_emoji = random.choice(fun_emoji_list)
            st.success(f"Correct! {fun_emoji}")
            rain(emoji=fun_emoji, animation_length="1")
        else:
            st.error(f"Wrong answer! The correct answer is Option {correct_idx + 1}")


if __name__ == "__main__":
    compound_simple_main()