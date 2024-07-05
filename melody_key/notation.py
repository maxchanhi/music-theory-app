from fractions import Fraction
easymode= ["C major","A minor" ,"D major","B minor", "F major","D minor", "G major","E minor",
                   "B-flat major","G minor"]
intermediate = ["A major", "F-sharp minor",
                   "E major","C-sharp minor","B major","G-sharp minor",
                   "B-flat major","G minor", "E-flat major", "C minor",
                   "A-flat major","F minor", "D-flat major","B-flat minor"]
hard = ['E major', 'C-sharp minor', 'B major', 'G-sharp minor', 'F-sharp major',
        'D-sharp minor', 'G-flat major', 'E-flat minor', 'D-flat major', 
        'B-flat minor', 'A-flat major', 'F minor']

sharp_keys = {
    "sharp_major": ["G major", "D major", "A major", "E major", "B major", "F-sharp major"],
    "sharp_minor": ["E minor", "B minor", "F-sharp minor", "C-sharp minor", "G-sharp minor", "D-sharp minor"]
}

flat_keys = {
    "flat_major": ["F major", "B-flat major", "E-flat major", "A-flat major", "D-flat major", "G-flat major"],
    "flat_minor": ["D minor", "G minor", "C minor", "F minor", "B-flat minor", "E-flat minor"]
}
all_sharpkeys= sharp_keys['sharp_major']+sharp_keys['sharp_minor']
all_flatkeys= flat_keys['flat_major']+flat_keys['flat_minor']
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
key_list=[]
for key,value in keyscale.items():
    key_list.append(key)
def tonal_triad(key):
    scale = keyscale[key]
    triad_dic = {
        "tonic": [scale[0], scale[2], scale[4]],
        "supertonic": [scale[1], scale[3], scale[5]],
        "mediant": [scale[2], scale[4], scale[6]],
        "subdominant": [scale[3], scale[5], scale[0]],
        "dominant": [scale[4], scale[6], scale[1]],
        "submediant": [scale[5], scale[0], scale[2]],
        "leadingtone": [scale[6], scale[1], scale[3]]
    }
    return triad_dic


def chord_finder(key,melody,activaion):
    triad_list=["tonic","supertonic","mediant","subdominant",
                "dominant","submediant","leadingtone"]
    triad_dic = tonal_triad(key)
    count_list=[]
    for triad in triad_list:
        j= 0
        for note in melody:
            if note[0] in triad_dic[triad]:
                j += 1*durations_fraction[note[1]]
        count_list.append(j)
    print(count_list,max(count_list),
          triad_list[count_list.index(max(count_list))])
    if max(count_list) < activaion or count_list.count(max(triad_list)) > 1:
        return False
    else:
        return triad_list[count_list.index(max(count_list))]
    
