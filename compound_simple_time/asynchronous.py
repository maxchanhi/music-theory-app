import multiprocessing
import subprocess
from PIL import Image
import os
import glob

def cleanup_temp_files():
    """Clean up all temporary files in the temp directory and ensure directory exists"""
    temp_dir = 'compound_simple_time/temp'
    
    # Create temp directory if it doesn't exist
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    else:
        # Clean up existing files in the temp directory
        files = glob.glob(os.path.join(temp_dir, '*'))
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

    with open(f'compound_simple_time/temp/score_{name}.ly', 'w') as f:
        f.write(lilypond_score)

    # Generate PNG image and MIDI file
    subprocess.run([
        'lilypond', '-dpreview', '-dbackend=eps', '--png', '-dresolution=300',
       f'--output=compound_simple_time/temp/score_{name}', f'compound_simple_time/temp/score_{name}.ly'
    ])

    with Image.open(f'compound_simple_time/temp/score_{name}.png') as img:
        width, height = img.size
        crop_rectangle = (0, 0, width, height)
        cropped_img = img.crop(crop_rectangle)

        cropped_img.save(f'compound_simple_time/temp/cropped_score_{name}.png')
    return f'compound_simple_time/temp/cropped_score_{name}.png'

def score_generation(question_data):
    # Clean up old files before generating new ones
    cleanup_temp_files()
    
    tasks_args = []
    tasks_args.append((question_data['melody'][1], 'question_melody', question_data['melody'][0][0], question_data['melody'][0][1]))
    for idx, option in enumerate(question_data['options']):
        tasks_args.append((option[0][1], f'wr_option_{idx}', option[0][0][0], option[0][0][1]))

    with multiprocessing.Pool() as pool:
        pool.starmap(lilypond_generation, tasks_args)

    # Add image paths to question_data
    question_data['question_image'] = f'compound_simple_time/temp/cropped_score_question_melody.png'
    for idx, option in enumerate(question_data['options']):
        question_data['options'][idx] = (*option, f'compound_simple_time/temp/cropped_score_wr_option_{idx}.png')

    return question_data