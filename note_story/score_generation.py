clefs = {
    "treble":{
        "instaff": ['d', 'e', 'f', 'g', 'a', 'b', "c'", "d'", "e'", "f'", "g'"],
        "leger_lines": ["g,", "a,", "b,", "c", "a'", "b'", "c''", "d''","e''","f''"], "pitch_range":"c'"
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
import random
import subprocess
from PIL import Image
def map_note(chosen_clef="treble", chosen_word="CAFE", add_line=True):
    
    fix_pitch = clefs[chosen_clef]["pitch_range"]
    display_note = []
    available_note = []
    for note in chosen_word: #C
        if add_line is None:
            leger_line = random.choice([True, False])
        else:
            leger_line = add_line
        note_list = clefs[chosen_clef]["ledger_lines" if leger_line else "instaff"]

        for opt in note_list: 
            if note.lower() in opt:
                available_note.append(opt)
        pick_note=random.choice(available_note)
        display_note.append(pick_note)
        available_note=[]
    return fix_pitch," ".join(display_note)

import subprocess,os

def score_generation(chosen_clef="treble", word=("c'", "c a' f'' e''"), output_filename="score"):
    fixed_pitch, melody = word
    lilypond_score = f"""
\\version "2.24.3"
\\header {{
  tagline = ""
}}
#(set-global-staff-size 26)

\\score {{
  \\new Staff {{
    \\clef {chosen_clef}
    \\omit Staff.TimeSignature
    \\omit Staff.BarLine
    \\fixed {fixed_pitch} {{
    {melody}
    }}
  }}
  \\layout {{ }}
}}"""
    with open(f"note_story/static/{output_filename}.ly", "w") as ly_file:
        ly_file.write(lilypond_score)
    
    static_dir = "note_story/static"
    os.makedirs(static_dir, exist_ok=True)
    
    # Write the .ly file to the static directory
    ly_file_path = os.path.join(static_dir, f"{output_filename}.ly")
    with open(ly_file_path, "w") as ly_file:
        ly_file.write(lilypond_score)
    
    # Run LilyPond to generate the PNG in the static directory
    subprocess.run(["lilypond", "-fpng", "-o", static_dir, ly_file_path])
    png_path = os.path.join(static_dir, f"{output_filename}.png")
    length=len(word[1].split())
    if length>=5 and length<7:
        width_pt=2.5
    elif length==4:
        width_pt=3
    elif length>=7:
        width_pt=2
    else:
        width_pt=3.5
    with Image.open(png_path) as img:
        width, height = img.size
        crop_rectangle = (100, 20, width//width_pt, height // 9)
        cropped_img = img.crop(crop_rectangle)
        cropped_img.save(png_path)

def main_score_generation(chosen_clef,word,add_leger=bool,file_name=str):
    fix_pitch,notes=map_note(chosen_clef, word, add_leger)
    score_generation(chosen_clef, (fix_pitch,notes), file_name)

