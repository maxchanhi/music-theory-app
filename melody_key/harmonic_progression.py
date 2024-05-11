from notation import *
import random

#I V|I V |I ii V|I
scale = keyscale["C major"] #['c', 'd', 'e', 'f', 'g', 'a', 'b']
triad_chord = tonal_triad("C major") #{'tonic': ['c', 'e', 'g'], 'supertonic': ['d', 'f', 'a'], 'mediant': ['e', 'g', 'b'], 'subdominant': ['f', 'a', 'c'], 'dominant': ['g', 'b', 'd'], 'submediant': ['a', 'c', 'e'], 'leadingtone': ['b', 'd', 'f']}
print(scale,triad_chord)
melody = []
rhythm_list = ["4","8","8.","16"]
harmonic_rhythm = [Fraction(1,2),Fraction(1,2),
                   Fraction(1,2),Fraction(1,2),
                   Fraction(1,2),Fraction(1,4),Fraction(1,4),
                   Fraction(1,1)]

for rhythm in harmonic_rhythm:
    duration = 0
    while duration < rhythm:
        available_list = [rhy for rhy in rhythm_list if duration + durations_fraction[rhy] <= rhythm]
        if not available_list:
            print("No available durations fit the remaining rhythm.")
            break
        note_rhy = random.choice(available_list)
        pitch = random.choice(scale)
        melody.append([pitch, note_rhy])
        duration += durations_fraction[note_rhy]
    melody.append("|")
print(melody)
def chord_checker(key="C major",melody=[['b', '8'], ['d', '8'], ['f', '8']],chord="tonic",activaion=Fraction(1,4)):
    triad_dic = tonal_triad(key)
    j= 0
    for note in melody:
        if note =="|":
            pass
        elif note[0] in triad_dic[chord]:
            j += 1*durations_fraction[note[1]]

    if j < activaion:
        return False
    else:
        return True 