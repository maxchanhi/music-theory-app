import subprocess
from PIL import Image
import os
import re
def format_melody(melody):
  formatted = []
  for note in melody:
      # Remove unwanted characters
      note = note.replace("'", "").replace(',', '').strip()#.replace('"', '')
      formatted.append(note)
  # Join the list into a string and return
  return ' '.join(formatted)

def plain_melody(melody):
  plain_melody =[]
  for note in melody:
    plain_melody.append(note[0]+note[1])
  return plain_melody

def lilypond_generation(melody, name, 
                        uppertime, lowertime):
    lilypond_score = f"""
\\version "2.24.1"  
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

    with open('score.ly', 'w') as f:
        f.write(lilypond_score)

    # Generate PNG image and MIDI file
    subprocess.run(['lilypond', '-dpreview', '-dbackend=eps', '--png', '-dresolution=300', '--output=compound_simple_time/score', 'compound_simple_time/score.ly'],
                   check=True)

    with Image.open('compound_simple_time/score.png') as img:
        width, height = img.size
        crop_height = height
        crop_rectangle = (0, 75, width, crop_height / 10)
        cropped_img = img.crop(crop_rectangle)

        os.makedirs('static', exist_ok=True)
        cropped_img.save(f'compound_simple_time/static/cropped_score_{name}.png')
    return f'compound_simple_time/static/cropped_score_{name}.png'

def split_contect(data=[(6, 8), ['\\tuplet 2/3 {a8 g8}', 'b4.', 'e8 b8 g8', 'a8 e4']]):
    uppertime = data[0][0]
    lowertime = data[0][1]
    melody = data[1]
    return uppertime,lowertime,melody

def score_generation(data):
    question_melody = data['melody']
    uppertime,lowertime,melody = split_contect(question_melody)
    lilypond_generation(melody,name="question_melody",uppertime=uppertime,lowertime=lowertime)

    ans_melody = data['answer']
    uppertime,lowertime,melody = split_contect(ans_melody)
    lilypond_generation(melody, name="answer_melody", uppertime=uppertime, lowertime=lowertime)
    idx=0
    for option in data["options"]:
        uppertime,lowertime,melody = split_contect(option)
        lilypond_generation(melody, name=f"wr_option_{idx}", uppertime=uppertime, lowertime=lowertime)
        idx+=1
   
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
