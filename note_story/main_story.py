import streamlit as st
import asyncio,os,base64
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

def story_main():
    st.title("Note Reading Exercise Generator")
    st.info("For further customization of your story or to support this project, please contact chakhangc@yahoo.com.hk. Your feedback and donations are appreciated.")
  
    if st.button("View a demo"):
        sample_html_path = "note_story/Muti_Day_Out.html"
        static_dir = "note_story/static"

        with open(sample_html_path, "r", encoding="utf-8") as file:
            sample_html = file.read()

        # Replace relative image paths with base64 encoded images
        for img_file in os.listdir(static_dir):
            if img_file.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                img_path = os.path.join(static_dir, img_file)
                img_base64 = get_image_base64(img_path)
                sample_html = sample_html.replace(
                    f'src="static/{img_file}"',
                    f'src="data:image/png;base64,{img_base64}"'
                )
        # Display the HTML with embedded images
        components.html(sample_html, height=600, scrolling=True)
    title = st.text_input("Enter the title of the story:", "My Music Story")
    
    story = st.text_area("Enter your story:", "Captitalise your words to generate the music notes: \nE.g. CAGE, ABCDEF, spEED. \nThe app only recongise 3 and more note letters in succession.\nOnce upon a time in a magical musical land...")
    col1,col2 = st.columns(2)
    with col1:  
        clef = st.selectbox("Choose the clef:", ["treble", "bass", "alto", "tenor"])
    
    with col2:
        leger_line_option = st.selectbox("Ledger line option:", ["Random", "Use ledger lines", "Don't use ledger line"])
    
    if leger_line_option == "Random":
        leger_line = None
    elif leger_line_option == "Use leger lines":
        leger_line = True
    else:
        leger_line = False

    if st.button("Generate Exercise"):

        static_dir = "note_story/static"
        with st.spinner("Getting your musical story..."):
            output_story = asyncio.run(process_story(title, story, clef, leger_line))
        with open(f"note_story/{title}.html", "r", encoding="utf-8") as file:
            sample_html = file.read()

        # Replace relative image paths with base64 encoded images
        for img_file in os.listdir(static_dir):
            if img_file.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                img_path = os.path.join(static_dir, img_file)
                img_base64 = get_image_base64(img_path)
                sample_html = sample_html.replace(
                    f'src="static/{img_file}"',
                    f'src="data:image/png;base64,{img_base64}"'
                )
        # Display the HTML with embedded images
        components.html(sample_html, height=600, scrolling=True)
        if not img_file:
            st.warning("Please contact support!")

if __name__ == "__main__":
    story_main()
