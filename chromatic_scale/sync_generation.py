import abjad
from abjad import persist
from PIL import Image
import asyncio
import subprocess
import multiprocessing
def generate_lilypond_score(args):
    scale, name, clef, octave, acc_dir = args
    tran = 0 if acc_dir else 1
    octave_list =  ["c,","c","c'","c''"]
    # Create a new LilyPond file content
    lilypond_content = '''
\\version "2.24.3" % specify the LilyPond version
\\paper {
    #(set-paper-size "a4landscape")
    left-margin = 10
    right-margin = 10
    top-margin = 10
    bottom-margin = 10
    indent = 0
}

\\layout {
    \\context {
        \\Score
        \\omit BarLine
        \\omit TimeSignature
    }
    \\context {
        \\Staff
        \\remove "Time_signature_engraver"
    }
    ragged-right = ##t
}

#(set-global-staff-size 30)

\\new Staff {
    \\accidentalStyle modern-voice
    \\clef ''' + clef + '''
    \\language "english"
    \\fixed
    ''' +octave_list[octave+tran] + '''{
'''

    # Add notes to the content
    for pitch in scale:
        lilypond_content += f" {pitch}"

    lilypond_content += '''
    }
}
'''

    # Write the content to a .ly file
    ly_file_path = f"{name}.ly"
    with open(ly_file_path, "w") as ly_file:
        ly_file.write(lilypond_content)

    # Run LilyPond to generate the PNG file
    subprocess.run(["lilypond", "-o", "static/", "--png", ly_file_path])

async def crop_image(image_path, output_path):
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, sync_crop_image, image_path, output_path)

def sync_crop_image(image_path, output_path):
    # Open an image file
    with open(image_path, 'rb') as file:
        img = Image.open(file)
        img.load()  # Required for PIL to read the image data

    # Get image dimensions
    width, height = img.size
    crop_box = (0, 25, width//2, height / 5.5)
    cropped_img = img.crop(crop_box)
    cropped_img.save(output_path)
import random

async def main(scale_list=dict,dir=bool, clef_list=list, octave=int):
    chromatic_scale, wrong_options,dir = scale_list
    clef=random.choice(clef_list)
    if clef == "treble":
        octave = 2
    elif clef == "alto":
        octave = 1
    elif clef == "tenor":
        octave = 1
    elif clef == "bass":
        octave = 0
    tasks = [(chromatic_scale, "Correct", clef, octave, dir)]
    for idx in range(len(wrong_options) - 1):
        tasks.append((wrong_options[idx], f"wrong_{idx}", clef, octave,dir))
    with multiprocessing.Pool() as pool:
        pool.map(generate_lilypond_score, tasks)

    # Create a list of crop tasks
    crop_list = [crop_image(f"static/{name}.png", f"static/{name}.png") for name in ["Correct"] + [f"wrong_{idx}" for idx in range(len(wrong_options) - 1)]]

    # Crop the generated images
    await asyncio.gather(*crop_list)
