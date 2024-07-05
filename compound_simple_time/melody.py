from compound_simple_time.notation import  setting_generation,correct_tran_time_sign,equal_list,key_list,value_list
from compound_simple_time.asynchronous import remove_duplication
import random

def rhythm_generation(all_rhythm_list,number_of_beat, 
                      lowertime):
  
    melody = []
    while len(melody) < number_of_beat:
        melody.append(random.choice(all_rhythm_list))
    tuplet_check = single_check = muti_check = False
    for note in melody:
        if "tuplet" in note: 
            tuplet_check = True
        elif len(note) <= 2:
            single_check = True
        elif len(note) > 2:
            muti_check = True
    if tuplet_check and single_check or muti_check:
        return melody
    else:
        return rhythm_generation(all_rhythm_list, number_of_beat, lowertime)

def random_insert_note(melody, pitch_list= ["e","f","g","a","b"]):
    updated_melody = []
    for note in melody:
        if "tuplet" in note:
            start_idx = note.find("{") + 1
            end_idx = note.find("}")
            tuplet_notes = note[start_idx:end_idx].split()
            updated_tuplet_notes = [random.choice(pitch_list) + n for n in tuplet_notes]
            updated_note = note[:start_idx] + ' '.join(updated_tuplet_notes) + note[end_idx:]
            updated_melody.append(updated_note)
        else:
            split_notes = note.split()
            updated_notes = [random.choice(pitch_list) + n  for n in split_notes]
            updated_melody.append(' '.join(updated_notes))
    return updated_melody

def tran_simple_compound(melody=[],setting="simple",pass_step = False,seed=random.randint(0, 2)):
    new_melody = []
    pass_1 = pass_2 = pass_3 = False
    if pass_step:
        seed = random.randint(0, 2)
        if seed == 0:
            pass_1 = True
        elif seed == 1:
            pass_2 = True
        elif seed == 2:
            pass_3 = True

    if  "simple" in setting:  # translate to compound
        for note in melody:
            if "tuplet" in note:
                if not pass_1:
                    start_idx = note.find("{") + 1
                    end_idx = note.find("}")
                    tuplet_notes = note[start_idx:end_idx].split("[]")
                    new_melody.extend(tuplet_notes)
                elif pass_1:
                    new_melody.append(note)
            elif len(note) == 2:  # single note, e.g., 'a4'
                if not pass_2:
                    new_melody.append(f'{note[0]}{int(note[1])}.')
                elif pass_2:
                    new_melody.append(note)
            else:
                if not pass_3:
                    new_melody.append("\\tuplet 2/3 "+"{ "+note+" }")
                elif pass_3:
                    new_melody.append(note)
    elif "compound" in setting:  # translate to simple
        for note in melody:
            if "tuplet" in note:
                if not pass_1:
                    start_idx = note.find("{") + 1
                    end_idx = note.find("}")
                    tuplet_notes = note[start_idx:end_idx].split()
                    new_melody.extend(tuplet_notes)
                elif pass_1:
                    new_melody.append(note)
            elif len(note) == 3:  # single note, e.g., 'a4.'
                if not pass_2:
                    new_melody.append(f'{note[0]}{int(note[1])}')
                elif pass_2:
                    new_melody.append(note)
            else: #to triplet 'g4 e8', 'b8 g8 e8'
                if not pass_3:
                    new_melody.append("\\tuplet 3/2 "+"{ "+note+" }")
                elif pass_3:
                    new_melody.append(note)           
    return  new_melody

def main_generate():
    while True:
        # Generate initial melody and time signature
        time_cat, numerator, denominator, rhythm_list = setting_generation()
        rhythm_melody = rhythm_generation(rhythm_list, numerator, denominator)
        melody = random_insert_note(rhythm_melody)
        time_sign = correct_tran_time_sign(numerator, denominator, False)
        
        # Create original and translated melodies
        original_melody = [time_sign, melody]
        translated_melody = [correct_tran_time_sign(numerator, denominator), 
                             tran_simple_compound(melody, setting=time_cat)]
        
        # Generate wrong melodies with reasons
        wrong_melodies = [
            ([correct_tran_time_sign(numerator, denominator), 
              tran_simple_compound(melody, setting=time_cat, pass_step=True, seed=1)],
             "Failed to remove duplet when compound time modulates to simple time, or vice versa"),
            ([correct_tran_time_sign(numerator, denominator), 
              tran_simple_compound(melody, setting=time_cat, pass_step=True, seed=2)],
             "Failed to identify the value of each beat"),
            ([correct_tran_time_sign(numerator, denominator),
              tran_simple_compound(melody, setting=time_cat, pass_step=True, seed=3)],
             "Triplet or duplet did not apply during modulation")
        ]
        
        # Filter and create all_options
        all_options = [(option, reason) for option, reason in wrong_melodies 
                       if option != translated_melody and option != original_melody]
        
        # Handle equal time signatures
        if time_sign in equal_list:
            equal_time = value_list[key_list.index(time_sign)] if time_sign in key_list else key_list[value_list.index(time_sign)]
            equal_time_melody = [equal_time, translated_melody[1]]
            wrong_equal_time_melody = [equal_time, tran_simple_compound(melody, setting=time_cat, pass_step=True)]
            
            if len(all_options) >= 3:
                all_options = all_options[:2]
            all_options.append((equal_time_melody, "Time signature with different value of beat"))
            all_options.append((wrong_equal_time_melody, "Time signature and metric modulation incorrect"))
        
        # Add translated melody (correct answer) to options
        all_options.append((translated_melody, "Correct translation"))
        
        # Remove duplicates and shuffle
        #all_options = remove_duplication(all_options)
        random.shuffle(all_options)
        
        # Check if we have enough options and the correct answer is included
        if len(all_options) >= 3 and any(option == translated_melody for option, _ in all_options):
            break
        
        print("Regenerating options...")

    # Create and return question data
    question_data = {
        "question": "Which one is the correct metric modulation between simple time and compound time?",
        "melody": original_melody,
        "options": [(option, reason) for option, reason in all_options],
        "answer": translated_melody
}
    return question_data


def wrong_halfen_double_time_sign(melody=list,time_cat=str,switch="halfen"): #4/4 2/2, 12/8 6/4
    if switch == "same":
        equal_dic={(2,2): (4, 4),(3,2):(6,4),
                   (6,8):(3,4),(12,8):(6,4),(2,4):(4, 8)}
        key_list =[]
        value_list = []
        equal_list = []
        for key, value in equal_dic.items():
            key_list.append(key)
            value_list.append(value)
        equal_list.extend(key_list)
        equal_list.extend(value_list)
        return equal_list,
        #code to reverse the key and value in the dictionary
    elif switch == "halfen": #4/4 to 2/4, should be 4/8
        halfen_dic={(4,4): [(2, 4),(4,8)],(12,8):[(6,8),(12)]}
    elif switch == "double":
        double_dic={(4, 4): (2, 2),}
        pass
    return melody
