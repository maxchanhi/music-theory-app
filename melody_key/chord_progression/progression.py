
from fractions import Fraction
import sys
import os
from melody_key.chord_progression.notation import major_keys,minor_keys,durations_fraction

from melody_key.chord_progression.motif import rhythm_generation,get_rhythm_motif,melody_rhythm_gen

major_roman = ["I","ii","IV","V"]
chord_prograssion = {"I":["ii","IV","V"],
                    "ii":["IV","V"],
                    "IV":["I","ii","V"],
                    "V":["I"]}

from melody_key.chord_progression.notation import keyscale
import random
def major_tonal_triad(key):
    scale = keyscale[key]
    triad_dic ={
            "I": [scale[0], scale[2], scale[4]],
            "ii": [scale[1], scale[3], scale[5]],
            "iii": [scale[2], scale[4], scale[6]],
            "IV": [scale[3], scale[5], scale[0]],
            "V": [scale[4], scale[6], scale[1]],
            "vi": [scale[5], scale[0], scale[2]],
            "viio": [scale[6], scale[1], scale[3]]
        }
    return scale, triad_dic
def progression_generation():
    while True:
        melody_chord = []
        choosen_chord = random.choice(major_roman)
        melody_chord.append(choosen_chord)
        while len(melody_chord)<4:
            next_chord = random.choice(chord_prograssion[choosen_chord])
            melody_chord.append(next_chord)
            choosen_chord = next_chord
        if "V" not in melody_chord and "I" not in melody_chord:
            continue
        else:
            break
    return melody_chord

def weight_formula(rhythm,lowertime=4,strong_beat=True):
    if rhythm >= Fraction(1,lowertime) * 2:
        return Fraction(1,3)
    elif strong_beat:
        #weight=Fraction(11,30)*rhythm+0.15
        return Fraction(1,3)#weight
    else:
        weight=(Fraction(11,30)*(rhythm))+0.15
        return weight


def weight_scale(scale,traids,chord,
                 weight=Fraction(1,3),numberofchord=3): #triad
    chord_note=traids[chord] # ['c','e','g']
    w_scale=[]
    w = (1-(weight*numberofchord))/4
    for note in scale:
        if note in chord_note:
            w_scale.append(weight)
        else:
            w_scale.append(w)
    return w_scale
# add note
def add_note(melody, chord_acc,scale, traids,lowertime=4):
    lowertime = Fraction(1,lowertime)
    try:
        melody_acc=zip(melody,chord_acc)
        full_melody=[]
        last_note=None
        for bar,chord in melody_acc:
            beat=0
            measure=[]
            beat=[]
            for rhythm in bar:
                duration= durations_fraction[rhythm]
                beat.append(duration)
                if len(measure) ==0 or (sum(beat)-duration)%lowertime == 0:
                    on_beat = True 
                else:
                    on_beat =False
                if on_beat: #strong beat
                    #weight=weight_formula(rhythm=duration, lowertime=lowertime)
                    weight=Fraction(1, 3) 
                    weight_note = random.choices(scale, weights=weight_scale(scale, traids, chord,weight=weight))
                    measure.append(str(weight_note[0])+str(rhythm))
                else: #weak beat
                    if last_note[0] not in traids[chord]: #eg ['b', 'd', 'fs']
                        weight=Fraction(1, 3) 
                    else:
                        weight=weight_formula(rhythm=duration, lowertime=lowertime, strong_beat=False)
                    weight_note = random.choices(scale, weights=weight_scale(scale, traids, chord, weight=weight))
                    measure.append(str(weight_note[0])+str(rhythm))
                last_note=weight_note
            full_melody.append(measure)
        return full_melody
    except:
        raise ValueError("melody and chord prograssion must have the same length")
    
def key_generation(keys=["Major", "minor"]):
    if not keys:
        raise ValueError("No keys selected")
    
    all_keys = []
    if "Major" in keys:
        all_keys.extend(major_keys)
    if "minor" in keys:
        all_keys.extend(minor_keys)
    
    if not all_keys:
        raise ValueError("Invalid key selection")
    
    picked_key = random.choice(all_keys)
    return picked_key 

def main_generation(picked_key="C Major"):
    rhythm_list=["4","8","16","8."]
    time_signature = (4,4)
    melody_chord=progression_generation()
    scale, traids= major_tonal_triad(picked_key)
    first_bar_rhythm=rhythm_generation(rhythm_list,time_signature[0],time_signature[1])
    rhythm_motif=get_rhythm_motif(first_bar_rhythm,time_signature[1])
    melody=melody_rhythm_gen(first_bar_rhythm,time_signature[0],time_signature[1],rhythm_list=rhythm_motif)
    added_melody= add_note(melody, melody_chord, scale, traids)
    question_data= {"key":picked_key,"chord":melody_chord,"melody":added_melody}
    return question_data
