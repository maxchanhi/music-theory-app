from melody_generation import main_question
from subprocess import run
from PIL import Image
import asyncio
import multiprocessing
original_key,original_melody,transposing_by,option_list=main_question()

def lilypond_generation(key_sign='fs minor', melody=['d', 'gs', 'a', 'a', 'es', 'a'], name="testing"):
    # Convert melody notes to LilyPond format
    melody = [f"{note}8 " for note in melody]

    lily_melody = ' '.join(melody)
    
    # Define the LilyPond content
    lilypond_content = f"""
    \\version "2.24.3"
    \\language "english"
    \\fixed c' {{
      \\clef treble
      \\key {key_sign.split()[0]} \\{key_sign.split()[1]}
      \\time 3/4
      {lily_melody}
    }}
    #(set-global-staff-size 30)
    """
    
    lilypond_file = f"static/{name}.ly"
    with open(lilypond_file, 'w') as file:
        file.write(lilypond_content)

    # Generate PNG from LilyPond file
    run(["lilypond", "-o", "static/", "--png", lilypond_file])    
    # Define the generated PNG file path
    png_file = f"static/{name}.png"
    
    return png_file
def sync_crop_image(image_path, output_path):
    # Open an image file
    with open(image_path, 'rb') as file:
        img = Image.open(file)
        img.load()  # Required for PIL to read the image data

    width, height = img.size
    crop_box = (80, 25, width//1.8, height/10)
    cropped_img = img.crop(crop_box)
    cropped_img.save(output_path)
sync_crop_image("static/testing.png","static/croptesting.png")