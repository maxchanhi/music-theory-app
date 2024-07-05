import streamlit as st
import random
import subprocess
from PIL import Image
import os
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
        "leger_lines": ["g,,", "a,,", "b,,", "g", "a", "b", "c''"], "pitch_range":"c'"
    },
    "alto": {
        "instaff": ['e,', 'f,', 'g,', 'a,', 'b,', "c", "d", "e", "f","g",'a'],
        "leger_lines": ["c,",'d,', "b", "c'","d'","e'"], "pitch_range":"c'"
    }
}


#print(get_note(leger_line=True))
def ranged_score_generation(chosen_clef,chosen_note,chosen_range):
    lilypond_score = f"""
  \\version "2.22.0"  % ensure this matches your LilyPond version
  \\header {{
    tagline = ""  % removes the default LilyPond tagline
  }}
  #(set-global-staff-size 26)  % Adjust staff size to affect resolution

  \\score {{
    {{
      \\clef {chosen_clef}
      \\fixed {chosen_range}
      {chosen_note}
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


    with open('score.ly', 'w') as f:
        f.write(lilypond_score)

    subprocess.run(['lilypond', '-dpreview', '-dbackend=eps', '--png', '-dresolution=300', '--output=score', 'score.ly'],
                   check=True)

  
def get_note(available_clef=["treble","bass","tenor","alto"],
             accidentals=accidentals,
             leger_line=bool):
    chosen_clef = random.choice(available_clef)
    clef_data=clefs[chosen_clef]
    chosen_accidental = random.choice(accidentals)
    tran_acc= accidentals_lilypond[chosen_accidental]
    if leger_line:
        note_list=clef_data["leger_lines"]
    else:
        note_list=clef_data["instaff"]
    chosen_note = random.choice(note_list)
    octave= chosen_note[1:] if len(chosen_note)>1 else ""
    picked_note=chosen_note[0]+tran_acc+octave
    ranged_score_generation(chosen_clef,picked_note,clef_data['pitch_range'])
    return chosen_clef,chosen_note[0].upper()+" "+chosen_accidental,clef_data['pitch_range']
