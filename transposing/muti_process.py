from concurrent.futures import ThreadPoolExecutor
from subprocess import run
from PIL import Image
import os

# Existing function kept for compatibility (single-file generation)
def lilypond_generation(key_sign='fs minor', melody=['d', 'es', 'a'], name="testing"):
    melody = [f"{note}8 " for note in melody]
    lily_melody = ' '.join(melody)
    lilypond_content = f"""
        \\version "2.22.0"
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
    
    lilypond_file = f"transposing/static/{name}.ly"
    with open(lilypond_file, 'w') as file:
        file.write(lilypond_content)

    # Generate PNG from LilyPond file (single invocation)
    run(["lilypond", "-o", "transposing/static/", "--png", lilypond_file])
    png_file = f"transposing/static/{name}.png"
    
    return png_file

# New: write .ly only (to support batched rendering), return (ly_path, png_path)
def write_lilypond_file(key_sign='fs minor', melody=['d', 'es', 'a'], name="testing"):
    melody = [f"{note}8 " for note in melody]
    lily_melody = ' '.join(melody)
    lilypond_content = f"""
        \\version "2.22.0"
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

    ly_path = f"transposing/static/{name}.ly"
    with open(ly_path, 'w') as f:
        f.write(lilypond_content)
    png_path = f"transposing/static/{name}.png"
    return ly_path, png_path


def crop_image(image_path, output_path):
    with open(image_path, 'rb') as file:
        img = Image.open(file)
        img.load()  # Required for PIL to read the image data

    width, height = img.size
    crop_box = (80, 25, width//2, int(height/9.5))
    cropped_img = img.crop(crop_box)
    cropped_img.save(output_path)

# Kept for compatibility (no longer used in batched path)
def process_task(task):
    key_sign, melody, name = task
    png_file = lilypond_generation(key_sign, melody, name)
    crop_image(png_file, png_file)


def main_generation(tasks_list):
    # 1) Write all .ly files first
    ly_files = []
    png_files = []
    for key_sign, melody, name in tasks_list:
        ly_path, png_path = write_lilypond_file(key_sign, melody, name)
        ly_files.append(ly_path)
        png_files.append(png_path)

    if ly_files:
        # 2) Single batch lilypond invocation for all .ly files
        cmd = ["lilypond", "-o", "transposing/static/", "--png", *ly_files]
        run(cmd)

        # 3) Parallelize cropping (I/O-bound) using a small thread pool
        max_workers = min(8, len(png_files)) or 1
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for png in png_files:
                executor.submit(crop_image, png, png)

