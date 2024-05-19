import random
import subprocess
from PIL import Image
from inversion.notation import easymode,tonal_triad,roman_numerial,inversion_type

def simple_triad():
    key = random.choice(easymode)
    triad_dict = tonal_triad(key)
    triad_list = []
    value_list = []
    for triad_key, value in triad_dict.items():
        triad_list.append(triad_key)
        value_list.append(value)

    picked_triad = random.choice(triad_list)
    triad_notes = ['a','c', 'e'] #triad_dict[picked_triad]

    inversion_keys = ["a", "b", "c"]
    inversion = "c"#random.choice(inversion_keys)
    if inversion == "b":
        triad_notes[1], triad_notes[2] = triad_notes[2], triad_notes[1]
    elif inversion == "c":
        triad_notes[0], triad_notes[1], triad_notes[2] = triad_notes[2], triad_notes[0], triad_notes[1]
    # first note is always the bass and below middle c, c'
    triad_notes[0]=triad_notes[0]+","
    question_data = {"key_sign": key, "triad": picked_triad,
                     "inversion_type": inversion, "notes": triad_notes}
    print(triad_notes)
    return question_data

def chord_four_voices(triad):
    if "'" in triad[0]:
        triad[0] = triad[0][:-1]  # Remove the last character using slicing
    triad[0] = triad[0] + ","

    du_note = random.choice(triad[1:])
    if "'" in du_note:
        du_note.replace(",","")  # Remove the last character using slicing
    triad.append(du_note + "'")
    #if triad[0][0] > triad[-1][0]:
        #triad[-1][0].replace(",","")
    #adjusted_triad = adjust_notes_for_grand_staff(triad)
    #lilypond_generation_grand_staff("grand_staff", triad)
    print(triad)

def adjust_notes_for_grand_staff(triad):
    adjusted_triad = triad.copy()
    
    # Ensure two notes are in the treble clef range
    while sum(note[0] >= 'c' for note in adjusted_triad[:2]) < 2:
        adjusted_triad[0] = adjusted_triad[0] + "'"
    
    # Ensure two notes are in the bass clef range
    while sum(note[0] <= 'b' for note in adjusted_triad[2:]) < 2:
        adjusted_triad[3] = adjusted_triad[3].replace("'", "")
    
    return adjusted_triad

def lilypond_generation_grand_staff(name, accompany):
    tre_accompany = ' '.join(accompany[2:])
    bass_accompany = ' '.join(accompany[:2])
    lilypond_score = f"""
\\version "2.22.0"  
\\header {{
  tagline = "" \\language "english"
}}

#(set-global-staff-size 26)
\\new PianoStaff <<
  \\new Staff {{
    \\clef treble
    \\omit Staff.TimeSignature
    <{tre_accompany}>1
  }}
  \\new Staff {{
    \\clef bass
    \\omit Staff.TimeSignature
    <{bass_accompany}>1
  }}
>>
"""

    with open('score.ly', 'w') as f:
        f.write(lilypond_score)

    # Generate PNG image and MIDI file
    subprocess.run(['lilypond', '-dpreview', '-dbackend=eps', '--png', '-dresolution=300', 
                    '--output=score', 'score.ly'],
                   check=True)
    with Image.open('score.png') as img:
        width, height = img.size
        crop_height = height
        crop_rectangle = (0, 75, width, height)
        cropped_img = img.crop(crop_rectangle)

        cropped_img.save(f'inversion/cropped_score_{name}.png')

    return f'inversion/cropped_score_{name}.png'

def options_generation(answer="VI b"):
    options_list=[answer]
    while len(options_list)<5:
        option= f"{random.choice(roman_numerial)} {random.choice(inversion_type)}"
        if option not in options_list:
            options_list.append(option)
    random.shuffle(options_list)
    return options_list
