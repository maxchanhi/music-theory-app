import subprocess
from PIL import Image
import random
from pitch_id.element import *
levels={"basic":[["treble","bass"],['Natural (♮)']],
        "intermediate":[["treble","bass"],['Flat (♭)', 'Natural (♮)', 'Sharp (♯)']],
        "advanced":[["treble","bass"],accidentals],
        "c clefs":[["alto","tenor"],['Natural (♮)']],"all clefs":[["treble","alto","tenor","bass"],accidentals]}
fun_emoji_list = [
    "😂",  "🎉",   "🚀",  "🐱", 
    "🐶",  "🦄",  
    "🎶",  "😱","👼🏻","💃🏻","🐰","🐒","🐣","🦀","💥","✨","🥳",
    "🍦",  "🌟",  "👻",  
    "🎈",   "🎮",  "💩"
] 
def score_generation(chosen_clef,chosen_accidental):
  clef = random.choice(chosen_clef)
  output_note = random.choice(note_letters)
  output_accidental = random.choice(chosen_accidental)
  if clef=="treble":
    note = f"{output_note+accidentals_lilypond[output_accidental]}'".lower()
  elif clef == "alto" or clef == "tenor":
    note = f"{output_note+accidentals_lilypond[output_accidental]}".lower()
  elif clef=="bass":
    note = f"{output_note+accidentals_lilypond[output_accidental]},".lower()

  lilypond_score = f"""
  \\version "2.24.3"  % ensure this matches your LilyPond version
  \\header {{
    tagline = ""  % removes the default LilyPond tagline
  }}
  #(set-global-staff-size 26)  % Adjust staff size to affect resolution

  \\score {{
    {{
      \\clef "{clef}" 
      {note}
    }}
    \\layout {{
      indent = 0\\mm  % Remove indentation to avoid unnecessary space
      line-width = #150  % Adjust line width to fit your content
      ragged-right = ##f  % To avoid ragged right lines
      \\context {{
        \\Score
        \\omit TimeSignature
        \\remove "Bar_number_engraver"  % Remove bar numbers
      }}
    }}
  }}
  """

  # Write the string to a LilyPond (.ly) file
  with open('pitch_id/score.ly', 'w') as f:
      f.write(lilypond_score)

  subprocess.run(['lilypond', '-dpreview', '-dbackend=eps', '--png', '-dresolution=300', '--output=pitch_id/score', 'pitch_id/score.ly'],
                   check=True)
  # Open the generated PNG file
  with Image.open('pitch_id/score.png') as img:
      # Calculate the crop rectangle
      width, height = img.size
      crop_height = height // 10 
      crop_rectangle = (120, 0, 350, crop_height)
      
      # add code to crop 1/10 from the top
      cropped_img = img.crop(crop_rectangle)
      cropped_img.save(f'pitch_id/cropped_score.png')
  return clef, output_note, output_accidental
