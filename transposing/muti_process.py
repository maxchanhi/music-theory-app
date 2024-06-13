import multiprocessing
from subprocess import run
from PIL import Image
import os

def lilypond_generation(key_sign='fs minor', melody=['d', 'es', 'a'], name="testing"):
    melody = [f"{note}8 " for note in melody]
    lily_melody = ' '.join(melody)
    lilypond_content = f"""
        \\version "2.24.3"
        \\language "english"
        {{
        \\omit Staff.TimeSignature
        \\fixed c' {{
            \\clef treble
            \\key {key_sign.split()[0]} \\{key_sign.split()[1]}
            \\time 3/4
            {lily_melody}
        }}
        }}
        #(set-global-staff-size 30)
        """
    
    lilypond_file = f"static/{name}.ly"
    with open(lilypond_file, 'w') as file:
        file.write(lilypond_content)

    # Generate PNG from LilyPond file
    run(["lilypond", "-o", "static/", "--png", lilypond_file])
    png_file = f"static/{name}.png"
    
    return png_file

def crop_image(image_path, output_path):
    with open(image_path, 'rb') as file:
        img = Image.open(file)
        img.load()  # Required for PIL to read the image data

    width, height = img.size
    crop_box = (80, 25, width//2, height//9.5)
    cropped_img = img.crop(crop_box)
    cropped_img.save(output_path)

def process_task(task):
    key_sign, melody, name = task
    png_file = lilypond_generation(key_sign, melody, name)
    crop_image(png_file, png_file)

def main_generation(tasks_list):
    # Create a multiprocessing pool
    pool = multiprocessing.Pool()

    # Map the tasks to the pool
    pool.map(process_task, tasks_list)

    # Close the pool and wait for all processes to finish
    pool.close()
    pool.join()

# Example usage
tasks_list = [
    ['fs minor', ['d', 'es', 'a'], 'test1'],
    ['g major', ['g', 'a', 'b'], 'test2'],
    # Add more tasks as needed
]

if __name__ == "__main__":
    main_generation(tasks_list)