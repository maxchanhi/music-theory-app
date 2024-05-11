import random
from cml.note_to_key import *


def calculate_interval(first_note_position,second_note_position):
    if second_note_position>first_note_position:
        return second_note_position-first_note_position+1
    elif second_note_position<first_note_position:
        return second_note_position+8-first_note_position
    
def calculate_semitone(first_note, second_note):
    if NOTE_TO_SEMITONES[second_note]>NOTE_TO_SEMITONES[first_note]:
        return NOTE_TO_SEMITONES[second_note]-NOTE_TO_SEMITONES[first_note]+1
    elif NOTE_TO_SEMITONES[second_note]<NOTE_TO_SEMITONES[first_note]:
        return NOTE_TO_SEMITONES[second_note]+13-NOTE_TO_SEMITONES[first_note]
    
def generate_correct_option():
    first_note_position = random.randint(0, 6)
    second_note_position = random.randint(0, 6)
    note1 = NOTENAME[first_note_position] + ACCIDENTAL[random.randint(0, 2)]
    note2 = NOTENAME[second_note_position] + ACCIDENTAL[random.randint(0, 2)]

    interval_number = calculate_interval(first_note_position, second_note_position)
    semitone_count = calculate_semitone(note1, note2)
    key = (str(interval_number), str(semitone_count))

    if key in JUMP_CHART:
        print("Whis is the interval of:",note1, note2,"?")
        e_ans = JUMP_CHART[key]
        no_ans = NUM_PLACEMENT[str(interval_number)]
        ans = f"{e_ans} {no_ans}"
        return ans
    else:
        return generate_correct_option()

#generate_correct_option()
#user_ans = input("What is the interval?")
#print ("Interval",calculate_interval(),";Semitone",calculate_semitone(note1, note2))
#print ("The interval is a ",ans)

         