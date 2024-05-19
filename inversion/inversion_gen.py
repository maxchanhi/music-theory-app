from inversion.notation import easymode,tonal_triad,roman_numerial,inversion_type
from inversion.grand_staff_gen import lilypond_generation_grand_staff
import random, subprocess 
from PIL import Image
def simple_triad(clef="grand"):
    if clef == "grand staff":
        clef = "grand"
    
    key = random.choice(easymode)
    triad_dict = tonal_triad(key)
    triad_list = []
    value_list = []
    for triad_key, value in triad_dict.items():
        triad_list.append(triad_key)
        value_list.append(value)

    picked_triad = random.choice(triad_list)
    triad_notes = triad_dict[picked_triad]
    exception_pitch=["a","b"]
    inversion_keys = ["a", "b","c"]
    inversion = random.choice(inversion_keys)
    if inversion == "a": #['fs', 'a', 'c']
        if triad_notes[0][0] in exception_pitch:
            triad_notes[1]=triad_notes[1]+"'"
            triad_notes[2]=triad_notes[2]+"'"
        elif triad_notes[1][0] in exception_pitch: #c e g
            triad_notes[2]=triad_notes[2]+"'"
    elif inversion == "b": 
        triad_notes[0], triad_notes[1],triad_notes[2] = triad_notes[1], triad_notes[2], triad_notes[0]
        if triad_notes[0][0] not in exception_pitch:
            if triad_notes[2][0] not in exception_pitch:
                triad_notes[2]=triad_notes[2]+"'"
            elif triad_notes[2][0] in exception_pitch:
                pass
        elif triad_notes[0][0] in exception_pitch:
            triad_notes[1]=triad_notes[1]+"'"
            triad_notes[2]=triad_notes[2]+"'"
    elif inversion == "c":
        triad_notes[0], triad_notes[1], triad_notes[2] = triad_notes[2], triad_notes[0],triad_notes[1]
        if triad_notes[0][0] not in exception_pitch:
            if triad_notes[2][0] in exception_pitch:
                pass
            elif triad_notes[2][0] not in exception_pitch:# e a c
                triad_notes[2]=triad_notes[2]+"'"
                if triad_notes[1][0] not in exception_pitch:
                    triad_notes[1]=triad_notes[1]+"'"
        elif triad_notes[0][0] in exception_pitch: #b e g
            if triad_notes[2][0] not in exception_pitch:
                triad_notes[2]=triad_notes[2]+"'"
            if triad_notes[1][0] not in exception_pitch:
                triad_notes[1]=triad_notes[1]+"'"
    print(triad_notes)
    # first note is always the bass and below middle c, c'
    adjust_notes=[]
    if clef =="treble":
        for note in triad_notes:
            adjust_notes.append(note+"'")
    elif clef == "bass":
        if triad_notes[0][0] in exception_pitch:
            triad_notes[0]=triad_notes[0]+","
            triad_notes[1]=triad_notes[1][:-1]
            triad_notes[2]=triad_notes[2][:-1]
            print("bass",triad_notes)
        adjust_notes=triad_notes
    elif clef == "grand":
        high_note = random.choice(triad_notes)
        triad_notes.append(high_note+"'")
        adjust_notes=adjust_notes+triad_notes
        if adjust_notes[2] not in exception_pitch and "'" not in adjust_notes[2]:
            adjust_notes[2]=adjust_notes[2]+"'"
    print(adjust_notes)
    
    question_data = {"clef":clef,"key_sign": key, "triad": picked_triad,
                     "inversion_type": inversion, "notes": adjust_notes}
    return question_data

def chord(chord_notes=["b'", "ds'", 'fs']):
    chord_str = "<" +" ".join(chord_notes) + ">1"
    return chord_str

def lilypond_generation(name,accompany,clef):
    str_accompany = chord(accompany)
    lilypond_score = f"""
\\version "2.22.0"  
\\header {{
  tagline = "" \\language "english"
}}

#(set-global-staff-size 26)
\\score {{  
 {{\\clef {clef} \\omit Staff.TimeSignature
      {str_accompany}
      \\bar "|"
    }}
}}
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
        crop_rectangle = (0, 75, width, crop_height / 5.5)
        cropped_img = img.crop(crop_rectangle)

        cropped_img.save(f'cropped_score_{name}.png')

    return f'cropped_score_{name}.png'
#question_data = {"clef":clef,"key_sign": key, "triad": picked_triad,
 #                    "inversion_type": inversion, "notes": adjust_notes}
def main_generation(clef="grand"):
    data = simple_triad(clef)
    triad_notes = data["notes"]
    clef= data["clef"]
    if clef == "bass"  or clef =="treble":
        lilypond_generation("main_tre",triad_notes,clef= data["clef"])
    else:
        lilypond_generation_grand_staff("main_grand", triad_notes)
    print(data["inversion_type"], triad_notes)
    return data


