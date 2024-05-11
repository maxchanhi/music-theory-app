import subprocess
from PIL import Image
import random
from element import *
import os
def score_generation():
  clef = random.choice(["treble","bass"])
  if clef=="treble":
    output_note = random.choice(note_letters)
    note = f"{output_note}'".lower()
  elif clef=="bass":
    output_note = random.choice(note_letters)
    note = f"{output_note},".lower()

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
  with open('score.ly', 'w') as f:
      f.write(lilypond_score)

  # Run LilyPond on the file to generate the score
  # Ensure that LilyPond is in your system's PATH or provide the full path to the LilyPond executable
  subprocess.run(['lilypond', '--png', '-dresolution=300', 'score.ly'], check=True)

  # Open the generated PNG file
  with Image.open('score.png') as img:
      # Calculate the crop rectangle
      width, height = img.size
      crop_height = height // 10 
      crop_rectangle = (120, 0, 350, crop_height)
      
      # add code to crop 1/10 from the top
      cropped_img = img.crop(crop_rectangle)
      cropped_img.save('/Users/chakhangchan/Documents/VS_code/Music_theory_app/lilypond_generation/Flask_project2/static/images/cropped_score_f.png')
  return clef, output_note

def idx_score_generation(idx_l,treble_e,bass_e,correct_c):
  clef = random.choice(["treble","bass"])
  print("local idx:",idx_l)
  if idx_l > 4:
    if treble_e and bass_e > 2:
        print("normal mode")
        pass
    else:
      if treble_e > 2:
        print("treble mode")
        clef = random.choice(["treble"])
      elif bass_e > 2:
        print("bass mode")
        clef = random.choice(["bass"])
      elif treble_e < 5 and bass_e < 5 and correct_c >=8:
        print("super hard mode")
        clef = random.choice(["tenor","alto"])
      elif correct_c >=4:
        print("hard mode")
        clef = random.choice(["treble","bass","tenor","alto"])
      else:
         print("normal mode")
         pass
  else:
      print("normal mode")
      pass

  if clef=="treble":
    fix_octave = str(random.choice(["c'","c''"]))
  elif clef == "alto" or clef== "tenor":
    fix_octave = str(random.choice(["c","c'"]))
  elif clef=="bass" :
    fix_octave = str(random.choice(["c,","c"]))
  
  output_note = random.choice(note_letters)  
  note = f"{output_note}".lower()

  lilypond_score = f"""
  \\version "2.24.3"  % ensure this matches your LilyPond version
  \\header {{
    tagline = ""  % removes the default LilyPond tagline
  }}
  #(set-global-staff-size 26)  % Adjust staff size to affect resolution

  \\score {{
    {{
      \\clef "{clef}" 
      \\fixed {fix_octave} {{{note}}}
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
  with open('score.ly', 'w') as f:
      f.write(lilypond_score)

  # Run LilyPond on the file to generate the score
  # Ensure that LilyPond is in your system's PATH or provide the full path to the LilyPond executable
  subprocess.run(['lilypond', '--png', '-dresolution=300', 'score.ly'], check=True)

  # Open the generated PNG file
  with Image.open('score.png') as img:
      # Calculate the crop rectangle
      width, height = img.size
      crop_height = height // 10 
      crop_rectangle = (120, 0, 350, crop_height)
      
      # add code to crop 1/10 from the top
      cropped_img = img.crop(crop_rectangle)
      cropped_img.save('/Users/chakhangchan/Documents/VS_code/Music_theory_app/lilypond_generation/Flask_project2/static/images/cropped_score_f.png')
  return clef, output_note, idx_l
