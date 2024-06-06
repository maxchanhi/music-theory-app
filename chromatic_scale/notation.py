alphabat= ["c","d","e","f","g","a","b"]
import random

black_white_key = {
    0: ['c', 'bs'], 2: ['d'], 4: ['e'],
    5: ['f', 'es'], 7: ['g'], 9: ['a'],
    11: ['b', 'cf'], 1: ['cs', 'df'], 3: ['ds', 'ef'],
    6: ['fs', 'gf'], 8: ['gs', 'af'], 10: ['as', 'bf']
}
alphabet = ["c", "d", "e", "f", "g", "a", "b"]

def generate_chromatic_scale(accending_dir):
    starting_pc = random.randint(0, 11)
    starting_note = random.choice(black_white_key[starting_pc])

    chromatic_list = [[starting_note]]
    
    if accending_dir:
        chromatic_scale =accending(starting_pc,chromatic_list)
    elif not accending_dir:
        chromatic_scale = descending(starting_pc, chromatic_list)

    return chromatic_scale


def descending(starting_pc,chromatic_list=list):
    for i in range(11):
        octave = starting_pc - i -1
        note_idx = octave % 12
        note_list = black_white_key[note_idx]
        if octave < 0:
            note_list = [el + "," for el in note_list]
        chromatic_list.append(note_list)

    chromatic_scale = []
    for note in chromatic_list:
        chromatic_scale.append(note[0])
    missing_letter=None
    chromatic_scale.append(chromatic_scale[0]+",")  # Append the first note to the end
    for i in range(2, len(chromatic_scale)):
        if chromatic_scale[i-2][0] == chromatic_scale[i-1][0] == chromatic_scale[i][0]:
            three_same = chromatic_list[i-2:i+1]
            for idx in range(len(three_same)):
                if len(three_same[idx]) > 1:
                    chromatic_scale[i+idx-2] = three_same[idx][1]
    
    for letter in alphabet:
        if letter not in ''.join(chromatic_scale):
            missing_letter = letter
            break
    if missing_letter:
        next_note = alphabet[(alphabet.index(missing_letter) + 1) % len(alphabet)]
        for i in range(len(chromatic_list)):
            for el in chromatic_list[i]:
                if missing_letter in el and next_note in chromatic_scale[i+1]:
                    chromatic_scale[i] = chromatic_list[i][1]
                    break
    if "bs" in chromatic_scale[0]:
        for i in range(len(chromatic_scale)-1):
            if i>0:
                chromatic_scale[i] = chromatic_scale[i].replace(",", "")
        chromatic_scale[-1] = "bs,"
    return chromatic_scale

def accending(starting_pc,chromatic_list=list):
    for i in range(11):
        octave = starting_pc + i + 1
        note_idx = octave % 12
        note_list = black_white_key[note_idx]
        if octave > 11:
            note_list = [el + "'" for el in note_list]
        chromatic_list.append(note_list)

    chromatic_scale = []
    for note in chromatic_list:
        chromatic_scale.append(note[0])
    missing_letter=None
    chromatic_scale.append(chromatic_scale[0]+"'")  # Append the first note to the end
    for i in range(2, len(chromatic_scale)):
        if chromatic_scale[i-2][0] == chromatic_scale[i-1][0] == chromatic_scale[i][0]:
            three_same = chromatic_list[i-2:i+1]
            for idx in range(len(three_same)):
                if len(three_same[idx]) > 1:
                    chromatic_scale[i] = three_same[idx][1]
    for letter in alphabet:
        if letter not in ''.join(chromatic_scale):
            missing_letter = letter
            break
    
    if missing_letter:
        next_note = alphabet[(alphabet.index(missing_letter) + 1) % len(alphabet)]
        for i in range(len(chromatic_list)):
            for el in chromatic_list[i]:
                if missing_letter in el and next_note in chromatic_scale[i+1]:
                    chromatic_scale[i] = chromatic_list[i][1]
                    break
    if "bs" in chromatic_scale[0]:
        chromatic_scale[0] = "bs,"
        chromatic_scale[-1] = "bs"

    return chromatic_scale

from copy import copy
def generate_wrong_options(original_scale=list,accending_dir=bool): 
    wrong_options=[]
    used_idx=[]
    while len(wrong_options) < 4:
        idx=random.randint(0,len(original_scale)-1)
        if idx in used_idx:
            continue
        chromatic_scale=original_scale.copy()
        used_idx.append(idx)

        if accending_dir:
            chromatic_scale = wrong_accending(idx, chromatic_scale)
        elif not accending_dir:
            chromatic_scale = wrong_descending(idx, chromatic_scale)
        wrong_options.append(chromatic_scale)

    return wrong_options

def wrong_accending(idx,chromatic_scale):
    wrong_idx = alphabat.index(chromatic_scale[idx][0])+1
    wrong_letter= alphabat[wrong_idx%len(alphabat)]
    octave = "'" if "'" in chromatic_scale[idx] else ""
    add_acc=random.choice(["s","f"])
    if len(chromatic_scale[idx]) ==1 or( "s" != chromatic_scale[idx][1] and "f" != chromatic_scale[idx][1]):
        chromatic_scale[idx]= chromatic_scale[idx][0]+add_acc
        if chromatic_scale[idx][0] == "c":
            chromatic_scale[idx]=chromatic_scale[idx]
    elif idx%2==0:
        chromatic_scale[idx]=chromatic_scale[idx][0]
        if chromatic_scale[idx][0] == "c":
            chromatic_scale[idx]=chromatic_scale[idx]
    else:
        chromatic_scale[idx]=wrong_letter+"f"
        if wrong_letter=="c":
            chromatic_scale[idx]=chromatic_scale[idx]+"'"
    if octave:
        chromatic_scale[idx]=chromatic_scale[idx]+octave
    return chromatic_scale
def wrong_descending(idx, chromatic_scale):
    wrong_idx = alphabat.index(chromatic_scale[idx][0])+1
    wrong_letter= alphabat[wrong_idx%len(alphabat)]
    octave = "," if "," in chromatic_scale[idx] else ""
    add_acc=random.choice(["s","f"])
    if len(chromatic_scale[idx]) ==1 or( "s" != chromatic_scale[idx][1] and "f" != chromatic_scale[idx][1]):
        chromatic_scale[idx]= chromatic_scale[idx][0]+add_acc
        if chromatic_scale[idx][0] == "b":
            chromatic_scale[idx]=chromatic_scale[idx]
    elif idx%2==0:
        chromatic_scale[idx]=chromatic_scale[idx][0]
        if chromatic_scale[idx][0] == "b":
            chromatic_scale[idx]=chromatic_scale[idx]+","
    else:
        chromatic_scale[idx]=wrong_letter+"f"
        if wrong_letter=="c":
            chromatic_scale[idx]=chromatic_scale[idx]+","
    if octave:
        chromatic_scale[idx]=chromatic_scale[idx]+octave
    return chromatic_scale 

def main_chromatic_generator():
    accending_dir=random.choice([True,False])
    
    chromatic_scale=generate_chromatic_scale(accending_dir)
    wrong_options=generate_wrong_options(chromatic_scale,accending_dir)
    return chromatic_scale,wrong_options,accending_dir

import os
def get_png_files(directory="chromatic_scale/static"):
    return [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.png')]
