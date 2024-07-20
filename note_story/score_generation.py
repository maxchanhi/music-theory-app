clefs = {
    "treble":{
        "instaff": ['d', 'e', 'f', 'g', 'a', 'b', "c'", "d'", "e'", "f'", "g'"],
        "ledger_lines": ["g,", "a,", "b,", "c", "a'", "b'", "c''", "d''","e''","f''"], "pitch_range":"c'"
    },
    "bass": {
        "instaff": ['f,', 'g,', 'a,', 'b,', "c", "d", "e", "f", "g","a","b"],
        "ledger_lines": ["c,", "d,", "e,", "c'", "d'","e'","f'"], "pitch_range":"c"
    },
    "tenor":{
        "instaff": ["c,",'d,', 'e,', 'f,', 'g,', 'a,', 'b,', "c", "d", "e", "f"],
        "ledger_lines": ["g,,", "a,,", "b,,", "g", "a", "b", "c'","d'"], "pitch_range":"c'"
    },
    "alto": {
        "instaff": ['e,', 'f,', 'g,', 'a,', 'b,', "c", "d", "e", "f","g",'a'],
        "ledger_lines": ["c,",'d,', "b", "c'","d'","e'"], "pitch_range":"c'"
    }
}
import random,time
import subprocess
from PIL import Image
def map_note(chosen_clef="treble", chosen_word="CAFE", add_line=True):
    fix_pitch = clefs[chosen_clef]["pitch_range"]
    display_note = []

    for note in chosen_word:
        leger_line = random.choice([True, False]) if add_line is None else add_line
        note_list = clefs[chosen_clef]["ledger_lines" if leger_line else "instaff"]
        available_note = [opt for opt in note_list if note.lower() in opt]

        # Ensure there's always a note to choose
        pick_note = random.choice(available_note) if available_note else random.choice(note_list)
        display_note.append(pick_note)

    return fix_pitch, " ".join(display_note)

import os
import subprocess
from PIL import Image

def score_generation(chosen_clef="treble", word=("c'", "c a' f'' e''"), output_filename="score"):
    fixed_pitch, melody = word
    output_filename = output_filename.replace(" ", "_")
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
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    static_dir = os.path.join(current_dir, "static")
    os.makedirs(static_dir, exist_ok=True)
    
    # Write the .ly file to the static directory
    ly_file_path = os.path.join(static_dir, f"{output_filename}.ly")
    with open(ly_file_path, "w") as ly_file:
        ly_file.write(lilypond_score)

    try:
        command = "lilypond -fpng -o "+static_dir+" "+ly_file_path
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"LilyPond output:\n{result.stdout}")
        print(f"LilyPond errors:\n{result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"Error running LilyPond: {e}")
        print(f"LilyPond output:\n{e.output}")
        print(f"LilyPond errors:\n{e.stderr}")
        return
    
    png_path = os.path.join(static_dir, f"{output_filename}.png")
    print(f"PNG path: {png_path}")
    
    length = len(word[1].split())
    if 5 <= length < 7:
        width_pt = 2.5
    elif length == 4:
        width_pt = 3
    elif length >= 7:
        width_pt = 2
    else:
        width_pt = 3.5
    
    if os.path.exists(png_path):
        with Image.open(png_path) as img:
            width, height = img.size
            crop_rectangle = (100, 20, width // width_pt, height // 9)
            cropped_img = img.crop(crop_rectangle)
            cropped_img.save(png_path)
        print(f"Image processed and saved: {png_path}")
    else:
        print(f"Error: PNG file not found at {png_path}")
def main_score_generation(chosen_clef,word,add_leger=bool,file_name=str):
    fix_pitch,notes=map_note(chosen_clef, word, add_leger)
    file_name = file_name.replace(" ", "_")
    score_generation(chosen_clef, (fix_pitch,notes), file_name)

