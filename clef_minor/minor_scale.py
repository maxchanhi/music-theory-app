starting_pitch_easy=['a','e','b','d','g'] 
starting_pitch_intermediate=['fs','cs','c','f']
starting_pitch_hard=['gs','ds','bf','ef'] 

harmonic_ascending = {
    'a': ['a', 'b', 'c', 'd', 'e', 'f', 'gs'],
    'e': ['e', 'fs', 'g', 'a', 'b', 'c', 'ds'],
    'b': ['b', 'cs', 'd', 'e', 'fs', 'g', 'as'],
    'd': ['d', 'e', 'f', 'g', 'a', 'bf', 'cs'],
    'g': ['g', 'a', 'bf', 'c', 'd', 'ef', 'fs'],
    'fs': ['fs', 'gs', 'a', 'b', 'cs', 'd', 'e'],
    'cs': ['cs', 'ds', 'e', 'fs', 'gs', 'a', 'b'],
    'c': ['c', 'd', 'ef', 'f', 'g', 'af', 'b'],
    'f': ['f', 'g', 'af', 'bf', 'c', 'df', 'e'],
    'gs': ['gs', 'as', 'b', 'cs', 'ds', 'e', 'fss'],
    'ds': ['ds', 'es', 'fs', 'gs', 'as', 'b', 'css'], 
    'bf': ['bf', 'c', 'df', 'ef', 'f', 'gf', 'a'],
    'ef': ['ef', 'f', 'gf', 'af', 'bf', 'cf', 'd']
}
harmonic_descending = {
    key: [scale[0]] + scale[:0:-1] for key, scale in harmonic_ascending.items()
}

melodic_ascending = {
    key: scale[:5] + [
        scale[5][0] + 's' if scale[5][-1] != 's' and scale[5][-1] != 'f' else 
        scale[5][0] if scale[5][-1] == 'f' else 
        scale[5], 
        scale[6]
    ]
    for key, scale in harmonic_ascending.items()
}

melodic_descending = {
    key: [scale[0]] + scale[:0:-1] for key, scale in melodic_ascending.items()
}

import random
minor_types=[
        "harmonic ascending", "harmonic descending",
        "melodic ascending", "melodic descending"
    ]
def add_octave_indicators(tonic):
    minor_type = random.choice(minor_types)
    if minor_type == "harmonic ascending":
        minor_scale = harmonic_ascending[tonic].copy()
    elif minor_type == "harmonic descending":
        minor_scale = harmonic_descending[tonic].copy()
    elif minor_type == "melodic ascending":
        minor_scale = melodic_ascending[tonic].copy()
    elif minor_type == "melodic descending":
        minor_scale = melodic_descending[tonic].copy()

    ascending = "ascending" in minor_type
    descending = "descending" in minor_type

    c_index = next((i for i, note in enumerate(minor_scale) 
                    if note.startswith('c')), None)
    print(c_index,ascending,descending)
    if ascending:
        if c_index >= 2:
            for i in range(c_index,len(minor_scale)):
                minor_scale[i] += "'"
        elif c_index == 1:
            minor_scale[0] += ','
            
        last_note = minor_scale[0]
        if ',' in last_note:
            minor_scale.append(last_note.replace(',', ''))
        else:
            minor_scale.append(last_note + "'")
    if descending:
        if c_index >= 2:
            for i in range(c_index+1, len(minor_scale)):
                minor_scale[i] += ","
        else:
            for i in range(c_index + 1):
                minor_scale[i] += "'"  
        first_note = minor_scale[0]
        if "'" in first_note:
            minor_scale.append(first_note.replace("'", ""))
        else:                                                      
            minor_scale.append(first_note + ",")                    

    return minor_type, minor_scale

def pick_clef_range(clef_list=['treble','alto','tenor','bass']):
    clef = random.choice(clef_list)
    if clef == 'treble':
        fixed_pitch="c''"
    elif clef == 'alto':
        fixed_pitch="c'"
    elif clef == 'tenor':
        fixed_pitch="c"
    else:
        fixed_pitch="c,"
    return clef, fixed_pitch


def option_generation(starting_pitch='a',ans_dir="harmonic descending",
                      option_list=['a','e','b','d','g']):
    key_list=['c','g','d','a','e','b','fs','gf','cs','df','gs','af','ef','ds','bf','f']
    user_options=[starting_pitch+" "+ans_dir.split()[0]+" minor"]
    while len(user_options)<4:
        new_option=random.choice(option_list)
        new_dir= random.choice(minor_types)
        minor_type = new_dir.split()[0]
        if len(option_list)>8:
            distance=abs(key_list.index(starting_pitch)
                       -key_list.index(new_option))
            if distance<=1 or distance>= len(key_list)-1: 
                continue
        option = new_option+" "+minor_type+" minor"
        #breakpoint()
        if option not in user_options:
            user_options.append(option)
        
    random.shuffle(user_options)
    return user_options

from clef_minor.score_gen import lilypond_score_uid
def main_generation(level="easy"):
    if level == "easy":
        option_list=starting_pitch_easy
    elif level == "intermediate":
        option_list=starting_pitch_intermediate+starting_pitch_easy
    elif level == "hard":
        option_list=starting_pitch_hard+starting_pitch_intermediate

    starting_pitch = random.choice(option_list)
    clef, fixed_pitch = pick_clef_range()
    minor_type, minor_scale = add_octave_indicators(tonic=starting_pitch)
    print(clef,fixed_pitch,minor_type,minor_scale)
    data = [fixed_pitch, "score_cm", clef]
    lilypond_score_uid(data=data, melody=minor_scale)
    user_options=option_generation(starting_pitch=starting_pitch,ans_dir=minor_type
                                   ,option_list=option_list)
    return clef, starting_pitch, minor_type, user_options

"""
import subprocess
import os
import tempfile

def lilypond_score(clef='treble', fix_pitch="c'", melody=['a', 'b', "c'", "d'", "e'", "f'", "gs'", "a'"]):
    # Generate the LilyPond string
    lily_string = "\\version \"2.24.1\"\n"
    lily_string += "\\language \"english\"\n"  # Set language to English
    lily_string += "\\score {\n"
    lily_string += "  \\new Staff {\n"
    lily_string += "    \\omit Stem\n"
    lily_string += f"    \\clef {clef}\n"
    lily_string += f"   \\fixed {fix_pitch} {{\n"
    lily_string += "    \\omit TimeSignature\n"
    lily_string += "    \\omit Score.BarLine\n"
    lily_string += "    \\omit Score.TimeSignature\n"
    lily_string +="     \\override Staff.Clef.color = #white"
    lily_string +="     \\override Staff.Clef.layer = #-1"
    # Add the melody notes
    lily_string += "      "
    for note in melody:
        lily_string += f"{note}4 "
    lily_string += "\n    }\n"  # Close the music expression
    lily_string += "  }\n"  # Close the Staff block
    lily_string += "}\n"  # Close the score block

    # Create a temporary directory
    with tempfile.TemporaryDirectory() as tmpdir:
        # Write the LilyPond string to a temporary file
        ly_file = os.path.join(tmpdir, "score.ly")
        with open(ly_file, 'w') as f:
            f.write(lily_string)
        try:
            subprocess.run(["lilypond", "--png", "-o", tmpdir, ly_file], check=True)
            png_file = os.path.join(tmpdir, "score_cm.png")
            with open(png_file, 'rb') as f:
                png_data = f.read()
            with open("score_cm.png", "wb") as f:
                f.write(png_data)
            print("Score image saved as 'score.png'")

        except subprocess.CalledProcessError as e:
            print(f"Error running LilyPond: {e}")
            return None
        except FileNotFoundError:
            print("LilyPond is not installed or not in the system PATH")
            return None
"""     