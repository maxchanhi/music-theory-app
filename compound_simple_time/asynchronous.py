import subprocess
from PIL import Image
import os

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
    processed_score = f"""\
\\version "2.24.3"  
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

    temp_dir = 'compound_simple_time/temp'
    os.makedirs(temp_dir, exist_ok=True)

    ly_path = os.path.join(temp_dir, f'score_{name}.ly')
    output_base = os.path.join(temp_dir, f'score_{name}')
    png_path = os.path.join(temp_dir, f'score_{name}.png')
    cropped_png_path = os.path.join(temp_dir, f'cropped_score_{name}.png')


    with open(ly_path, 'w') as f:
        f.write(processed_score)

    # Generate PNG image and MIDI file
    subprocess.run([
        'lilypond', '-dpreview', '-dbackend=eps', '--png', '-dresolution=300',
       f'--output={output_base}', ly_path
    ])

    with Image.open(png_path) as img:
        width, height = img.size
        crop_rectangle = (0, 0, width, height//10)
        cropped_img = img.crop(crop_rectangle)

        cropped_img.save(cropped_png_path)
    return cropped_png_path

def score_generation(question_data):
    tasks_args = []
    tasks_args.append((question_data['melody'][1], 'question_melody', question_data['melody'][0][0], question_data['melody'][0][1]))
    for idx, option in enumerate(question_data['options']):
        tasks_args.append((option[0][1], f'wr_option_{idx}', option[0][0][0], option[0][0][1]))

    for args in tasks_args:
        lilypond_generation(*args)

    # Add image paths to question_data
    question_data['question_image'] = f'compound_simple_time/temp/cropped_score_question_melody.png'
    for idx, option in enumerate(question_data['options']):
        question_data['options'][idx] = (*option, f'compound_simple_time/temp/cropped_score_wr_option_{idx}.png')

    return question_data

async def process_melody(melody_data, base_path, i=None):
    """Processes a single melody to generate and crop its score image."""
    if isinstance(melody_data, tuple) and len(melody_data) == 2:
        melody, reason = melody_data
        time_signature, notes = melody
        filename = f"option_{i}" if i is not None else "question_melody"
    else:
        melody = melody_data
        time_signature, notes = melody_data
        reason = ""
        filename = "question_melody"

    uppertime, lowertime = time_signature

    processed_score = f"""\
    \\version "2.24.3"
    \\header {{
      tagline = "" \\language "english"
    }}

    #(set-global-staff-size 26)

    \\score {{
        \\fixed c' {{
          \\time {uppertime}/{lowertime}
          \\omit Score.BarLine
          {format_melody(notes)}
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

    os.makedirs(base_path, exist_ok=True)
    ly_path = os.path.join(base_path, f"score_{filename}.ly")
    output_base = os.path.join(base_path, f"score_{filename}")
    png_path = os.path.join(base_path, f"score_{filename}.png")
    cropped_png_path = os.path.join(base_path, f"cropped_score_{filename}.png")

    with open(ly_path, 'w') as f:
        f.write(processed_score)

    # Generate PNG image and MIDI file
    subprocess.run([
        'lilypond', '-dpreview', '-dbackend=eps', '--png', '-dresolution=300',
       f'--output={output_base}', ly_path
    ])

    with Image.open(png_path) as img:
        width, height = img.size
        crop_rectangle = (0, 0, width, height//10)
        cropped_img = img.crop(crop_rectangle)

        cropped_img.save(cropped_png_path)
    return cropped_png_path
