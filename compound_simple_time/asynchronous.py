import asyncio
from PIL import Image
import os


def format_melody(melody):
  formatted = []
  for note in melody:
      # Remove unwanted characters
      note = note.replace("'", "").replace(',', '').strip()#.replace('"', '')
      formatted.append(note)
  # Join the list into a string and return
  return ' '.join(formatted)

def remove_duplication(data=list()):
    unique_data = {}

    for option, reason in data:
        time_sig, melodies = option
        # Ensure melodies is iterable (list or tuple)
        if not isinstance(melodies, (list, tuple)):
            # If melodies is not iterable, convert it to a list
            melodies = [melodies] if melodies is not None else []
        # Convert the list of melodies to a tuple to make it hashable
        melodies_tuple = tuple(melodies)
        # Use the time signature and melodies tuple as the key to ensure uniqueness
        unique_data[(time_sig, melodies_tuple)] = (option, reason)

    # Extract unique values from the dictionary
    unique_list = list(unique_data.values())
    return unique_list
  
async def lilypond_generation(melody, name, uppertime, lowertime):
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
    proc = await asyncio.create_subprocess_exec(
        'lilypond', '-dpreview', '-dbackend=eps', '--png', '-dresolution=300',
       f'--output=compound_simple_time/temp/score_{name}', f'compound_simple_time/temp/score_{name}.ly'
    )
    await proc.wait()
    with Image.open(f'compound_simple_time/temp/score_{name}.png') as img:
        width, height = img.size
        crop_rectangle = (0, 0, width, height)#crop_height / 10
        cropped_img = img.crop(crop_rectangle)

        cropped_img.save(f'compound_simple_time/temp/cropped_score_{name}.png')
    return f'compound_simple_time/temp/cropped_score_{name}.png'

async def score_generation(question_data):
    tasks = []
    # Task for the main question melody
    tasks.append(lilypond_generation(question_data['melody'][1], 'question_melody', question_data['melody'][0][0], question_data['melody'][0][1]))
    
    # Tasks for the options
    for idx, option in enumerate(question_data['options']):
        # option is a tuple like ( ( (uppertime, lowertime), melody), 'correct' or 'incorrect')
        melody_part = option[0] # melody_part is ( (uppertime, lowertime), melody )
        time_sig = melody_part[0] # time_sig is (uppertime, lowertime)
        melody = melody_part[1]
        uppertime = time_sig[0]
        lowertime = time_sig[1]
        tasks.append(lilypond_generation(melody, f'wr_option_{idx}', uppertime, lowertime))

    # Run all generation tasks concurrently
    results = await asyncio.gather(*tasks)
    
    # First result is for the question
    question_data['question_image'] = results[0]
    
    # Subsequent results are for the options
    for idx, option in enumerate(question_data['options']):
        image_path = results[idx + 1]
        question_data['options'][idx] = (*option, image_path)

    return question_data