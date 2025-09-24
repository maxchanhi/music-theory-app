import asyncio
from PIL import Image
import os
import logging

# Configure logging to display informative messages
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def format_melody(melody):
  """
  Formats a list of notes into a single string for LilyPond.
  It filters out any non-note-like strings to prevent errors.
  """
  if not isinstance(melody, list):
    logging.error(f"Invalid melody format: expected a list, but got {type(melody)}")
    return ""

  formatted = []
  for note in melody:
      # Basic validation to ensure the item is a musical note and not descriptive text.
      # This check can be made more robust depending on the expected note format.
      if isinstance(note, str) and not ' ' in note and any(c.isalpha() for c in note):
          # Remove unwanted characters
          cleaned_note = note.replace("'", "").replace(',', '').strip()
          formatted.append(cleaned_note)
      else:
          logging.warning(f"Skipping invalid item in melody list: {note}")
          
  # Join the list into a string and return
  return ' '.join(formatted)

def remove_duplication(data=list()):
    """
    Removes duplicate entries from a list of tuples, where each tuple
    contains a time signature and a list of melodies.
    """
    unique_data = {}
    for time_sig, melodies in data:
        # Convert the list of melodies to a tuple to make it hashable
        melodies_tuple = tuple(melodies)
        # Use the time signature and melodies tuple as the key to ensure uniqueness
        unique_data[(time_sig, melodies_tuple)] = (time_sig, melodies)

    # Extract unique values from the dictionary
    unique_list = list(unique_data.values())
    return unique_list
  
async def lilypond_generation(melody, name, uppertime, lowertime):
    """
    Generates a musical score image from a melody using LilyPond.
    """
    # Ensure the output directory exists
    output_dir = 'compound_simple_time/temp'
    os.makedirs(output_dir, exist_ok=True)
    
    formatted_melody = format_melody(melody)
    if not formatted_melody:
        logging.error(f"Skipping score generation for '{name}' due to empty or invalid melody.")
        return None

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
      {formatted_melody}
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
    
    file_path = os.path.join(output_dir, f'score_{name}')
    ly_file = f'{file_path}.ly'

    with open(ly_file, 'w') as f:
        f.write(lilypond_score)

    # Generate PNG image from the LilyPond file
    proc = await asyncio.create_subprocess_exec(
        'lilypond', '-dpreview', '-dbackend=eps', '--png', '-dresolution=300',
       f'--output={file_path}', ly_file
    )
    
    stdout, stderr = await proc.communicate()

    if proc.returncode != 0:
        logging.error(f"LilyPond failed to process {ly_file}.")
        if stderr:
            logging.error(f"LilyPond Errors:\n{stderr.decode()}")
        return None

    png_path = f'{file_path}.png'
    cropped_png_path = os.path.join(output_dir, f'cropped_score_{name}.png')

    try:
        with Image.open(png_path) as img:
            width, height = img.size
            # Example crop, adjust as needed
            crop_rectangle = (0, 0, width, height) 
            cropped_img = img.crop(crop_rectangle)
            cropped_img.save(cropped_png_path)
        logging.info(f"Successfully generated cropped score: {cropped_png_path}")
        return cropped_png_path
    except FileNotFoundError:
        logging.error(f"Could not find generated PNG file at {png_path}")
        return None

async def score_generation(question_data):
    """
    Orchestrates the generation of a question melody and multiple-choice
    option scores asynchronously.
    """
    tasks = []
    
    # Task for the main question melody
    if 'melody' in question_data and len(question_data['melody']) == 2:
        melody_info = question_data['melody']
        time_sig = melody_info[0]
        melody = melody_info[1]
        tasks.append(
            asyncio.create_task(
                lilypond_generation(melody, 'question_melody', time_sig[0], time_sig[1])
            )
        )
    else:
        logging.error("Invalid format for 'question_data['melody']'.")

    # Tasks for the multiple-choice options
    if 'options' in question_data:
        for idx, option in enumerate(question_data['options']):
            if len(option) == 2:
                time_sig = option[0]
                melody = option[1]
                tasks.append(
                    asyncio.create_task(
                        lilypond_generation(melody, f'wr_option_{idx}', time_sig[0], time_sig[1])
                    )
                )
            else:
                 logging.warning(f"Skipping invalid option at index {idx}.")

    await asyncio.gather(*tasks)

