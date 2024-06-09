import random
from notation import major_keys,minor_keys,keyscale,transposition,each_note_transposition,alphabat
def melody_generation():
    pick_a_key=random.choice(major_keys+minor_keys)
    scale=keyscale[pick_a_key]
    while True:
        melody=[]
        for _ in range(6):
            melody.append(random.choice(scale))
        if len(melody) - len(set(melody))>1:
            continue
        else:
            break 
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
    question_data={"original key":pick_a_key,
                   "original melody":melody,
                   "transposed key":transposed_key+" "+note_split[1],
                   "transposed melody":transposed_melody,
                   "transposing by":transposing_by}
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
    if alpha_idx >= len(alphabat)-1 :
        alpha_idx=alpha_idx%(len(alphabat))
        if "," in pick_note:
            transposed_melody[idx]=alphabat[alpha_idx]+accidental
        else:
            transposed_melody[idx]=alphabat[alpha_idx]+"'"+accidental
    elif alpha_idx < 0:
        alpha_idx=alpha_idx%(len(alphabat))
        if "'" in pick_note:
            transposed_melody[idx]=alphabat[alpha_idx]+accidental
        else:
            transposed_melody[idx]=alphabat[alpha_idx]+","+accidental
    else:
        transposed_melody[idx]=alphabat[alpha_idx]+accidental+octave
    return transposed_melody

def wrong_key_sign(key="bf minor", dir = "up a major 2nd"):
    key_letter=key.split(" ")
    tran_letter = each_note_transposition(key_letter[0], dir)
    tran_letter = tran_letter.replace("'", "").replace(",", "")  if "'" in tran_letter or  "," in tran_letter  else tran_letter
    wrong_dir = random.choice(["up a perfect 5th","down a perfect 5th"])
    wrong_key_sign = each_note_transposition(tran_letter,wrong_dir)
    wrong_key_sign = wrong_key_sign.replace("'", "").replace(",", "")  if "'" in wrong_key_sign or  "," in wrong_key_sign  else wrong_key_sign

    return wrong_key_sign+" "+key_letter[1]

def options_main(melody=list,key="bf minor",dir="up a major 2nd"):
    options = [(key,melody), (key,wrong_accdental(melody)),
            (key,wrong_letter(melody)), (wrong_key_sign(key, dir),melody),
            (wrong_key_sign(key, dir),random.choice([wrong_accdental(melody),
            wrong_letter(melody)]))]
    return options

def main_question():
    data = melody_generation()
    return data["original key"],data["original melody"],data["transposing by"],options_main(data["transposed melody"],data["transposed key"],data["transposing by"])
