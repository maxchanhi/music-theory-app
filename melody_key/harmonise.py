from score_generation import lilypond_homophonic,format_chord, plain_melody,format_h_melody
from notation import *


def harmoniser(melody=[],key="D major"):
    uppertime = 4
    lowertime = Fraction(1,4)
    value=i = 0
    chord_rhy=beat_p=[0]
    accompany = []
    for i in range(len(melody)):
        value += durations_fraction[melody[i][1]]
        if value >=  uppertime*lowertime :
            chord = chord_finder(melody[beat_p[-1]:i+1],uppertime*lowertime)
            if not chord:
                mid = (i + 1+ beat_p[-1]) // 2
                chord1 = chord_finder(melody[beat_p[-1]:mid], uppertime*lowertime//2)
                chord2 = chord_finder(melody[mid:i+1], uppertime*lowertime//2)
                chord_rhy.append(mid)
                accompany.append(chord1)
                accompany.append(chord2)
            elif chord:
                chord_rhy.append(i+1)
                accompany.append(chord)
            beat_p.append(i+1)
            value =0
        i += 1
    print("chord_rhy", chord_rhy,"accompany",accompany)
    k = 0
    triad_dic = tonal_triad(key)
    chord_melody= []
    for k in range(len(chord_rhy)-1):
        duration = 0
        for note in melody[chord_rhy[k]:chord_rhy[k+1]]:
            duration += durations_fraction[note[1]]
        duration = durations_notation[duration]
        acc_chord = triad_dic[accompany[k]]
        chord_melody.append(["<",acc_chord,">",duration])
        k += 1
    return chord_melody

def homophonic_score_generation(melody=[], chord_melody=[]):
    melody = format_h_melody(melody)
    chord_melody = format_chord(chord_melody)
    print("melody",melody,"harmony",chord_melody)
    lilypond_homophonic(melody,chord_melody,"chord_melody",4,4)