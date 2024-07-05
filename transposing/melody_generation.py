import random
from transposing.notation import major_keys,minor_keys,keyscale,transposition,each_note_transposition,alphabat
option_problems = {
    "wrong_accidental": "Student does not carefully count semitones on the keyboard",
    "wrong_letter": "Student does not carefully count letters",
    "wrong_key_sign": "Student has some knowledge on transposing but forgot that transposing includes key signature",
    "wrong_key_sign_and_accidental": "Student has poor knowledge on transposing",
    "wrong_key_sign_and_letter": "Student has poor knowledge on transposing"
}
def add_accidental(melody=list)->list:
    picked=[]
    while True:
        idx = random.randint(0, len(melody)-1)
        if idx not in picked:
            if "f" in melody[idx] or "s" in melody[idx]:
                melody[idx]= melody[idx][0]
            else:
                melody[idx]=melody[idx]+random.choice(["s", 'f'])
            picked.append(idx)
        if len(picked)==3:
            break
    return melody

def melody_generation_n_tansposition():
    pick_a_key=random.choice(major_keys)
    scale=keyscale[pick_a_key]
    while True:
        melody=[]
        for _ in range(6):
            melody.append(random.choice(scale))
        if len(melody) - len(set(melody))>1:
            continue
        else:
            break
    melody=add_accidental(melody)
    transposing_by= random.choice(transposition)
    transposed_melody=[]
    note_split = pick_a_key.split()
    transposed_key = each_note_transposition(note_split[0],transposing_by)
    transposed_key = transposed_key.replace("'","")
    transposed_key = transposed_key.replace(",","")
    for note in melody:
        transposed_melody.append(each_note_transposition(note,transposing_by))
    if None in transposed_melody:
        print(melody, transposed_melody)
        raise Exception("None in transposed melody")
    question_data={"original_key":pick_a_key,
                   "original_melody":melody,
                   "transposed_key":transposed_key+" "+note_split[1],
                   "transposed_melody":transposed_melody,
                   "transposing_by":transposing_by}
    return question_data


def wrong_accdental(transposed_melody=list):
    idx=random.randint(0,len(transposed_melody)-1)
    if "'" in transposed_melody[idx] or "," in transposed_melody[idx]:
        octave = transposed_melody[idx][-1]
    else:
        octave = ""

    if "s" not in transposed_melody[idx] and "f" not in transposed_melody[idx]:
        transposed_melody[idx]=transposed_melody[idx][0]+random.choice(["s",'f'])
    else:
        transposed_melody[idx] = transposed_melody[idx][0]
    transposed_melody[idx] += octave
    return transposed_melody 
        
def wrong_letter(transposed_melody=["f"]):
    idx=random.randint(0,len(transposed_melody)-1)
    pick_note = transposed_melody[idx]
    alpha_idx= alphabat.index(pick_note[0])
    alpha_idx+= random.choice([-1,1])
    
    if len(transposed_melody[idx])>1:
        accidental = transposed_melody[idx][1] if "f" == transposed_melody[idx][1] or "s" ==  transposed_melody[idx][1] else ""
        octave = transposed_melody[idx][-1] if "'" == transposed_melody[idx][-1] or "," == transposed_melody[idx][-1] else ""
    else:
        accidental=''
        octave =''
    if alpha_idx > len(alphabat)-1 :
        alpha_idx=alpha_idx%(len(alphabat))
        if "," in pick_note:
            transposed_melody[idx]=alphabat[alpha_idx]+accidental
        else:
            transposed_melody[idx]=alphabat[alpha_idx]+accidental+"'"
    elif alpha_idx < 0:
        alpha_idx=alpha_idx%(len(alphabat))
        if "'" in pick_note:
            transposed_melody[idx]=alphabat[alpha_idx]+accidental
        else:
            transposed_melody[idx]=alphabat[alpha_idx]+accidental+","
    else:
        transposed_melody[idx]=alphabat[alpha_idx]+accidental+octave
    return transposed_melody

def wrong_key_sign(key="bf minor"):
    key_letter=key.split(" ")
    wrong_dir = random.choice(["up a perfect 5th","down a perfect 5th"])
    wrong_key_sign = each_note_transposition(key_letter[0],wrong_dir)
    wrong_key_sign = wrong_key_sign.replace("'", "").replace(",", "")  if "'" in wrong_key_sign or  "," in wrong_key_sign  else wrong_key_sign

    return wrong_key_sign+" "+key_letter[1]
import copy

def options_main(melody=list, key="d minor"):
    options = [
        [key, wrong_accdental(copy.deepcopy(melody)), "wrong_accidental"],
        [key, wrong_letter(copy.deepcopy(melody)), "wrong_letter"],
        [wrong_key_sign(copy.deepcopy(key)), copy.deepcopy(melody), "wrong_key_sign"],
        [wrong_key_sign(copy.deepcopy(key)), wrong_accdental(copy.deepcopy(melody)), "wrong_key_sign_and_accidental"],
        [wrong_key_sign(copy.deepcopy(key)), wrong_letter(copy.deepcopy(melody)), "wrong_key_sign_and_letter"]
    ]
    return options
