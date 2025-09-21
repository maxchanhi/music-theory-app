import multiprocessing
import subprocess
from PIL import Image
import os
import glob

# Get the absolute path to the directory containing this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(BASE_DIR, 'temp')

def cleanup_temp_files():
    """Clean up all temporary files in the temp directory and ensure directory exists"""
    
    # Create temp directory if it doesn't exist
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
    else:
        # Clean up existing files in the temp directory
        files = glob.glob(os.path.join(TEMP_DIR, '*'))
        for file in files:
            try:
                if os.path.isfile(file):
                    os.remove(file)
            except Exception as e:
                print(f"Error removing file {file}: {e}")

def format_melody(melody):
    formatted = []
    for note in melody:
        # Remove unwanted characters
        note = note.replace("'", "").replace(',', '').strip()
        formatted.append(note)
    # Join the list into a string and return
    return ' '.join(formatted)

def remove_duplication(data=list()):
    unique_data = {}

    for time_sig, melodies in data:
        # Convert the list of melodies to a tuple to make it hashable
        melodies_tuple = tuple(melodies)
        # Use the time signature and melodies tuple as the key to ensure uniqueness
        unique_data[(time_sig, melodies_tuple)] = (time_sig, melodies)

    # Extract unique values from the dictionary
    unique_list = list(unique_data.values())
    return unique_list

def lilypond_generation(melody, name, uppertime, lowertime):
    # Use absolute paths for .ly file
    ly_file_path = os.path.join(TEMP_DIR, f'score_{name}.ly')
    
    lilypond_score = f"""
\\version "2.22.0"  
\\header {{
  tagline = "" \\language "english"
}}

#(set-global-staff-size 26)

\\score {{
    \\fixed c' {{
      \\time {uppertime}/{lowertime}
      \\omit Score.BarLine
      {format_melody(melody)}
    }}
    \\layout {{
      indent = 0\\mm
      ragged-right = ##f
      \\context {{
        \\Score
        \\remove "Bar_number_engraver"
      }}
    }}
}}
"""

    with open(ly_file_path, 'w') as f:
        f.write(lilypond_score)

    # Generate PNG image and MIDI file
    # Use absolute paths for output
    output_base_path = os.path.join(TEMP_DIR, f'score_{name}')
    subprocess.run([
        'lilypond', '-dpreview', '-dbackend=eps', '--png', '-dresolution=300',
       f'--output={output_base_path}', ly_file_path
    ])

    # Use absolute paths for image operations
    png_file_path = f'{output_base_path}.png'
    cropped_png_file_path = os.path.join(TEMP_DIR, f'cropped_score_{name}.png')

    with Image.open(png_file_path) as img:
        width, height = img.size
        crop_rectangle = (0, 0, width, height)
        cropped_img = img.crop(crop_rectangle)

        cropped_img.save(cropped_png_file_path)
    return cropped_png_file_path

def score_generation(question_data):
    cleanup_temp_files()

    # Generate question melody image
    melody = question_data['melody'][1]
    uppertime, lowertime = question_data['melody'][0]
    lilypond_generation(
        melody,
        "question_melody",
        uppertime,
        lowertime
    )

    # Generate images for each option and update the options list
    updated_options = []
    for i, (option, reason) in enumerate(question_data['options']):
        time_sign = option[0]
        melody = option[1]
        
        # Unpack the time signature
        uppertime, lowertime = time_sign
        
        # Generate the image for the option
        output_filename = f"option_{i}"
        lilypond_generation(
            melody, 
            output_filename,
            uppertime,
            lowertime
        )
        
        # The image path is now relative to the temp directory
        image_path = os.path.join(TEMP_DIR, f"cropped_score_{output_filename}.png")
        
        # Prepend the image path to the option tuple
        updated_options.append((image_path, option, reason))

    # Replace the old options with the updated ones
    question_data['options'] = updated_options

    # Add image paths to question_data
    question_data['question_image'] = os.path.join(TEMP_DIR, 'cropped_score_question_melody.png')

    return question_data