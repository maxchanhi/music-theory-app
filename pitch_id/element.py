import streamlit as st
import random
import subprocess
from PIL import Image
note_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
accidentals = ['Flat (♭)', 'Natural (♮)', 'Sharp (♯)','Double-sharp (x)','Double-flat (𝄫)']

accidentals_lilypond = {'Sharp (♯)':"is",'Natural (♮)':"",'Flat (♭)':"es",'Double-sharp (x)':"isis",'Double-flat (𝄫)':"isis"}
levels={"basic":[["treble","bass"],['Natural (♮)']],
        "intermediate":[["treble","bass"],['Flat (♭)', 'Natural (♮)', 'Sharp (♯)']],
        "advanced":[["treble","bass"],accidentals],
        "c clefs":[["alto","tenor"],['Natural (♮)']],"all clefs":[["treble","alto","tenor","bass"],accidentals]}
clefs = {
    "treble":{
        "instaff": ['d', 'e', 'f', 'g', 'a', 'b', "c'", "d'", "e'", "f'", "g'"],
        "leger_lines": ["g,", "a,", "b,", "c", "a'", "b'", "c''", "d''"], "pitch_range":"c'"
    },
    "bass": {
        "instaff": ['f,', 'g,', 'a,', 'b,', "c", "d", "e", "f", "g","a","b"],
        "leger_lines": ["c,", "d,", "e,", "c'", "d'","e'","f'"], "pitch_range":"c"
    },
    "tenor":{
        "instaff": ["c,",'d,', 'e,', 'f,', 'g,', 'a,', 'b,', "c", "d", "e", "f"],
        "leger_lines": ["g,,", "a,,", "b,,", "g", "a", "b", "c'","d'"], "pitch_range":"c'"
    },
    "alto": {
        "instaff": ['e,', 'f,', 'g,', 'a,', 'b,', "c", "d", "e", "f","g",'a'],
        "leger_lines": ["c,",'d,', "b", "c'","d'","e'"], "pitch_range":"c'"
    }
}

def ranged_score_generation(chosen_clef, chosen_note, acc, chosen_range):
    lilypond_score = f"""
  \\version "2.22.0"
  \\header {{
    tagline = ""
  }}
  #(set-global-staff-size 26)

  \\score {{
    {{
      \\clef {chosen_clef}
      \\fixed {chosen_range}
      {chosen_note}{acc}
    }}
    \\layout {{
      indent = 0\\mm
      line-width = #150
      ragged-right = ##f
      \\context {{
        \\Score
        \\omit TimeSignature
        \\remove "Bar_number_engraver"
      }}
    }}
  }}
  """

    with open('score.ly', 'w') as f:
        f.write(lilypond_score)

    try:
        subprocess.run(['lilypond', '-dpreview', '-dbackend=eps', '--png', '-dresolution=300', '--output=score', 'score.ly'],
                       check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"LilyPond error: {e.stderr}")
        raise
    try:
      with Image.open('score.png') as img:
          width, height = img.size
          crop_height = height
          crop_rectangle = (0, 0, width//5, crop_height)
          cropped_img = img.crop(crop_rectangle)
          cropped_img.save('score.png')
    except Exception as e:
        print(f"Image processing error: {str(e)}")
        raise


def get_note(available_clef=["treble","bass","tenor","alto"],
             accidentals=accidentals,
             leger_line=bool):
    chosen_clef = random.choice(available_clef)
    clef_data = clefs[chosen_clef]
    chosen_accidental = random.choice(accidentals)
    tran_acc = accidentals_lilypond[chosen_accidental]
    if leger_line:
        note_list = clef_data["leger_lines"]
    else:
        note_list = clef_data["instaff"]
    chosen_note = random.choice(note_list)
    octave = chosen_note[1:] if len(chosen_note) > 1 else ""
    picked_note = chosen_note[0] + tran_acc + octave
    ranged_score_generation(chosen_clef, picked_note, tran_acc, clef_data['pitch_range'])
    return chosen_clef, chosen_note[0].upper() + " " + chosen_accidental, clef_data['pitch_range']
