from fractions import Fraction
import random
pitch_list= ["e","f","g","a","b"]
easymode= ["C major","A minor" ,"D major","B minor", "F major","D minor", "G major","E minor",
                   "B-flat major","G minor"]
intermediate = ["C major","A minor" , "G major","E minor", "D major","B minor", "A major", "F-sharp minor",
                   "E major","C-sharp minor","B major","G-sharp minor",
                   "F major","D minor","B-flat major","G minor", "E-flat major", "C minor",
                   "A-flat major","F minor", "D-flat major","B-flat minor"]
rhythm_setting={"simple": ["4","8 8","\\tuplet 3/2 {8 8 8}","\\tuplet 3/2 {4 8}","\\tuplet 3/2 {8 4}","8. 16"],
                "compound":["4.","\\tuplet 2/3 {8 8}","8 8 8","4 8","8 4","\\tuplet 2/3 {8. 16}"]}
#setting {"compound quadruple":[4,Fraction(8,3),["4.","\\tuplet 2/3 {8 8}","8 8 8","4 8","8 4","\\tuplet 2/3 {8. 16}"]}
time_sign_cat={"simple duple":["2/2","2/4","2/8","2/16"],
               "simple triple":["3/2","3/4","3/8","3/16"],
               "simple quadruple":["4/2","4/4","4/8","4/16"],
               "compound duple":["6/2","6/4","6/8","6/16"],
               "compound triple":["9/2","9/4","9/8","9/16"],
               "compound quadruple":["12/2","12/4","12/8","12/16"]}

def adjust_rhythms(rhythms,rate=2):
    adjusted_rhythms = []
    for rhythm in rhythms:
        if "tuplet" in rhythm:
            # Handle tuplet cases
            start_idx = rhythm.find("{") + 1
            end_idx = rhythm.find("}")
            tuplet_notes = rhythm[start_idx:end_idx].split()
            adjusted_notes = []
            for note in tuplet_notes:
                # Adjust each note's duration within the tuplet
                if '.' in note:
                    base_duration = int(note.split('.')[0]) * rate
                    adjusted_notes.append(f'{base_duration}.')
                else:
                    # Regular notes
                    duration = int(note) * rate
                    adjusted_notes.append(str(duration))
            # Reconstruct the tuplet string
            adjusted_rhythms.append(f"{rhythm[:start_idx]}{' '.join(adjusted_notes)}{rhythm[end_idx:]}")
        else:
            # Handle regular and dotted notes
            parts = rhythm.split()
            adjusted_parts = []
            for part in parts:
                if '.' in part:
                    # Dotted notes
                    base_duration = int(part.split('.')[0]) * rate
                    adjusted_parts.append(f'{base_duration}.')
                else:
                    duration = int(part) * rate
                    adjusted_parts.append(str(duration))
            adjusted_rhythms.append(' '.join(adjusted_parts))
    return adjusted_rhythms
def adjust_rhythms_pitch(rhythms, rate=2):
    adjusted_rhythms = []
    for rhythm in rhythms:
        if "tuplet" in rhythm:
            # Find the tuplet contents within braces
            start_idx = rhythm.find("{") + 1
            end_idx = rhythm.find("}")
            tuplet_notes = rhythm[start_idx:end_idx].split()
            adjusted_notes = []
            for note in tuplet_notes:
                pitch = ''.join([char for char in note if not char.isdigit() and char != '.' and char !=""])
                duration = ''.join([char for char in note if char.isdigit()])
                if '.' in note:
                    # Handle dotted notes
                    base_duration = int(duration) * rate
                    adjusted_notes.append(f'{pitch}{base_duration}.')
                else:
                    duration = int(duration) * rate
                    adjusted_notes.append(f'{pitch}{duration}')
            # Reconstruct the tuplet string
            adjusted_rhythms.append(f"{rhythm[:start_idx]}{' '.join(adjusted_notes)}{rhythm[end_idx:]}")
        else:
            # Handle regular and dotted notes
            parts = rhythm.split()
            adjusted_parts = []
            for part in parts:
                pitch = ''.join([char for char in part if not char.isdigit() and char != '.'])
                duration = ''.join([char for char in part if char.isdigit()])
                if '.' in part:
                    # Handle dotted notes
                    base_duration = int(duration) * rate
                    adjusted_parts.append(f'{pitch}{base_duration}.')
                else:
                    duration = int(duration) * rate
                    adjusted_parts.append(f'{pitch}{duration}')
            adjusted_rhythms.append(' '.join(adjusted_parts))
    return adjusted_rhythms


def setting_generation():
    time_cat=[]
    time_frac = []
    for key, list_t in time_sign_cat.items():
        time_cat.append(key)
        time_frac.append(list_t)
    pick_time_cat = random.choice(time_cat)
    pick_time_sign = random.choice(time_sign_cat[pick_time_cat][1:-1])
    numerator, denominator = pick_time_sign.split("/")
    pick_rhy_setting=[]
    if "compound" in pick_time_cat:
        numerator = int(numerator) * Fraction(1, 3)
        denominator = Fraction(int(denominator), 3)
    if int(denominator)==4:
        pick_rhy_setting = rhythm_setting['simple']
        denominator = int(denominator)
    elif int(denominator) == 8:
        pick_rhy_setting=adjust_rhythms(rhythm_setting['simple'],2)
        denominator = int(denominator)
    elif denominator == Fraction(8, 3):
        pick_rhy_setting = rhythm_setting['compound']
    elif denominator == Fraction(4, 3): 
        pick_rhy_setting = adjust_rhythms(rhythm_setting['compound'],Fraction(1,2))
    return [pick_time_cat,int(numerator),denominator,pick_rhy_setting]
def same_value_time_sign(time_cat=str,nu=int,de=int): # for wrong option
    same_value= {"compound quadruple":"compound duple", #12/8 6/4
                 "simple triple":"compound duple", #3/4 6/8
                 "simple quardruple":"simple duple", #4/4 2/2
                 "compound triple":"compound triple" #9/8 9/8
                 }
    key_list=[]
    value_list= []
    for key,value in same_value.items():
        key_list.append(key)
        value_list.append(value)
    if time_cat in key_list:
        return same_value[time_cat]
    elif time_cat in value_list:
        idx = value_list.index(time_cat)
        key = key_list[idx]
        return key
def correct_tran_time_sign(nu=2,de=4,switch=True): #12/8 4/4 6/8 2/4 9/8 3/4
    if de not in [2,4,8,16]:
        if switch:
            de=de*Fraction(3,2) #12/8
        elif not switch: #12/8  8/3
            nu*=3
            de*=3          
    elif de in [2,4,8,16]:
        if switch:
            nu*=3
            de*=2 #4/4 12/8
        elif not switch:
            pass
    
    return int(nu),int(de) #12/8
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

durations_fraction = {
    "2": Fraction(1, 2),
    "4": Fraction(1, 4),
    "8": Fraction(1, 8),
    "16": Fraction(1, 16),
    '4.': Fraction(3, 8),
    '8.': Fraction(3, 16),
}

durations_notation = {v: k for k, v in durations_fraction.items()}
keyscale = {
    "C major": ['c', 'd', 'e', 'f', 'g', 'a', 'b'],
    "A minor": ['a', 'b', 'c', 'd', 'e', 'f', 'gs'],
    "G major": ['g', 'a', 'b', 'c', 'd', 'e', 'fs'],
    "E minor": ['e', 'fs', 'g', 'a', 'b', 'c', 'ds'],
    "D major": ['d', 'e', 'fs', 'g', 'a', 'b', 'cs'],
    "B minor": ['b', 'cs', 'd', 'e', 'fs', 'g', 'as'],
    "A major": ['a', 'b', 'cs', 'd', 'e', 'fs', 'gs'],
    "F-sharp minor": ['fs', 'gs', 'a', 'b', 'cs', 'd', 'es'],
    "E major": ['e', 'fs', 'gs', 'a', 'b', 'cs', 'ds'],
    "C-sharp minor": ['cs', 'ds', 'e', 'fs', 'gs', 'a', 'bs'],
    "B major": ['b', 'cs', 'ds', 'e', 'fs', 'gs', 'as'],
    "G-sharp minor": ['gs', 'as', 'b', 'cs', 'ds', 'e', 'fss'],
    "F-sharp major": ['fs', 'gs', 'as', 'b', 'cs', 'ds', 'es'],
    "D-sharp minor": ['ds', 'es', 'fs', 'gs', 'as', 'b', 'css'],
    "G-flat major": ['gf', 'af', 'bf', 'cf', 'df', 'ef', 'f'],
    "E-flat minor": ['ef', 'f', 'gf', 'af', 'bf', 'cf', 'd'],
    "D-flat major": ['df', 'ef', 'f', 'gf', 'af', 'bf', 'c'],
    "B-flat minor": ['bf', 'c', 'df', 'ef', 'f', 'gf', 'a'],
    "A-flat major": ['af', 'bf', 'c', 'df', 'ef', 'f', 'g'],
    "F minor": ['f', 'g', 'af', 'bf', 'c', 'df', 'e'],
    "E-flat major": ['ef', 'f', 'g', 'af', 'bf', 'c', 'd'],
    "C minor": ['c', 'd', 'ef', 'f', 'g', 'af', 'b'],
    "B-flat major": ['bf', 'c', 'd', 'ef', 'f', 'g', 'a'],
    "G minor": ['g', 'a', 'bf', 'c', 'd', 'ef', 'fs'],
    "F major": ['f', 'g', 'a', 'bf', 'c', 'd', 'e'],
    "D minor": ['d', 'e', 'f', 'g', 'a', 'bf', 'cs']
}
major_keys=['C major', 'G major', 'D major', 'A major', 'E-flat major', 'B-flat major', 'F major']
minor_keys=['A minor', 'E minor', 'B minor', 'F-sharp minor', 'C minor', 'G minor', 'D minor']

    
