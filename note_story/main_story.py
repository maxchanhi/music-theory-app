import streamlit as st
import asyncio, os, base64
from note_story.find_note import main_process_story, generate_html
from note_story.score_generation import main_score_generation
import streamlit.components.v1 as components

def get_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

async def async_main_score_generation(*args):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, main_score_generation, *args)

async def process_story(title, story, clef, leger_line):
    output_story, keywords = main_process_story(title, story, clef, leger_line)
    generate_html(output_story, title)
    
    tasks = [async_main_score_generation(*args) for args in keywords]
    await asyncio.gather(*tasks)

    return output_story

async def async_story_main():
    title = st.text_input("Enter the title of the story:", "My Music Story")
    story = st.text_area("Enter your story:", "Capitalise your words to generate the music notes: \nE.g. CAGE, ABCDEF, spEED. \nThe app only recognises 3 and more note letters in succession.\nOnce upon a time in a magical musical land...")
    col1, col2 = st.columns(2)
    with col1:
        clef = st.selectbox("Choose the clef:", ["treble", "bass", "alto", "tenor"])
    with col2:
        leger_line_option = st.selectbox("Ledger line option:", ["Random", "Use ledger lines", "Don't use ledger line"])
    
    leger_line = None if leger_line_option == "Random" else leger_line_option == "Use ledger lines"

    if st.button("Generate Exercise"):
        with st.spinner("Getting your musical story..."):
            output_story = await process_story(title, story, clef, leger_line)
            file_path = f"note_story/{title}.html"
            with open(file_path, "r", encoding="utf-8") as file:
                sample_html = file.read()

            # Handle image paths
            static_dir = "note_story/static"
            for img_file in os.listdir(static_dir):
                if img_file.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    img_path = os.path.join(static_dir, img_file)
                    img_base64 = get_image_base64(img_path)
                    sample_html = sample_html.replace(f'src="static/{img_file}"', f'src="data:image/png;base64,{img_base64}"')
            
            components.html(sample_html, height=600, scrolling=True)

def story_main():
    # Run the asynchronous part of the app
    asyncio.run(async_story_main())

if __name__ == "__main__":
    story_main()
