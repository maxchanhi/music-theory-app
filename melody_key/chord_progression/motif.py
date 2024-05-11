#44 for two bars
import random
from fractions import Fraction
from melody_key.chord_progression.notation import * 


def rhythm_generation(all_rhythm_list, number_of_beat, lowertime):
  available_list = all_rhythm_list[:]
  beat_amount = Fraction(1, lowertime)
  melody = []
  melody_duration_sum = 0

  while melody_duration_sum < number_of_beat * beat_amount:
    rhythm_choice = random.choice(available_list)
    melody.append(rhythm_choice)
    melody_duration_sum += durations_fraction[rhythm_choice]

    if melody_duration_sum % beat_amount == 0:
      available_list = all_rhythm_list[:]
    else:
      # Update available_list based on remaining beat amount
      remaining_beat = beat_amount - (melody_duration_sum % beat_amount)
      available_list = [
          rhythm for rhythm in all_rhythm_list
          if durations_fraction[rhythm] <= remaining_beat
      ]

  return melody

def get_motif(melody,scale,lowertime):
    interval_list = []
    i = 0
    while i < len(melody)-1:
        interval_list.append(abs(scale.index(melody[i][0])-scale.index(melody[i+1][0])))
        i+= 1
    value=k = 0
    rhythm_list=[]
    p_list = [0]

    for note in melody:
        value+=durations_fraction[note[1]]
        if value % Fraction(1,lowertime) ==0:
           p_list.append(k+1)
           value = 0         
        k+= 1
    j=0
    while j < len(p_list)-1:
        rhythm = []
        for el in melody[p_list[j]:p_list[j+1]]:
           rhythm.append(el[1])
        rhythm_list.append(rhythm)
        j +=1
    return interval_list,rhythm_list

def get_rhythm_motif(melody, lowertime):
    value = k = 0
    rhythm_list = []
    p_list = [0]

    for note in melody:
        value += durations_fraction[note]
        if value % Fraction(1, lowertime) == 0:
            p_list.append(k + 1)
            value = 0
        k += 1

    j = 0
    while j < len(p_list) - 1:
        rhythm = []
        for el in melody[p_list[j]:p_list[j+1]]:
            rhythm.append(el)
        rhythm_list.append(rhythm)
        j += 1

    return rhythm_list
def melody_rhythm_gen(motif=[], uppertime=4,lowertime=4,bar=3,
                   rhythm_list=[]):
    beat_sum = uppertime*Fraction(1,lowertime)*bar
    motif_sum=0
    for note in rhythm_list[0]:#each rhythm duration
        motif_sum+=durations_fraction[note]
    duration_sum=0
    while duration_sum<beat_sum:
        choice = random.choice(rhythm_list)
        duration_sum+=motif_sum
        motif.extend(choice)
    melody = []
    bar = []
    duration_sum = 0

    for note in motif:
        duration_sum += durations_fraction[note]
        bar.append(note)
        if duration_sum == (Fraction(1, lowertime)*uppertime):
            melody.append(bar)
            bar = []
            duration_sum = 0

    if bar:
        melody.append(bar)
    return melody

def melody_rhy_gen(motif, uppertime=4,lowertime=4,bar=2,
                   rhythm_list=[]):
    beat_sum = uppertime*Fraction(1,lowertime)*bar
    motif_sum=0
    melody=[]
    for note in motif:
        motif_sum+=durations_fraction[note[1]]
        melody.append(note)
    print("motif_sum",motif_sum)
    while motif_sum<beat_sum:
       choice = random.choice(rhythm_list)
       for note in choice:
        motif_sum+=durations_fraction[note]
        melody.append(note)
    return melody

def insert_note(melody, interval_list, scale):
    i = 0
    while i < len(melody):
        if isinstance(melody[i], list):
            pitch = melody[i][0]
        else:
            j = i - 1
            while j >= 0:
                if isinstance(melody[j], list):
                    pitch = melody[j][0]
                    break
                j -= 1
            if j < 0:
                raise ValueError("No previous pitch found.")

        pitch_pos = scale.index(pitch)
        n_pitch = (pitch_pos + random.choice(interval_list)) % len(scale)
        #print([scale[n_pitch], melody[i] if isinstance(melody[i], str) else melody[i][1]])

        if isinstance(melody[i], list):
            melody[i][0] = scale[n_pitch]
        else:
            melody[i] = [scale[n_pitch], melody[i]]
        i += 1
    return melody

def check_contour(melody,scale):
    tonic=donminant=mediant=leading=False
    for note in melody:
        if scale[0] in note:
            tonic = True
        elif scale[2] in note:
            mediant = True
        elif scale[4] in note:
            donminant = True
        elif scale[6] in note:
            leading = True
    check_list=[tonic,mediant,donminant,leading]
    if False not in check_list:
       return True
    else:
       return False

def main_generation(key):
    rhythm_list=["4","8","8.","16"]
    scale=keyscale[key]
    rhy_motif=rhythm_generation(rhythm_list,2,4)
    melody = []
    for note in rhy_motif:
        melody.append([random.choice(scale),note])
    motifinterval_list,motifrhythm_list = get_motif(melody,scale,4)
    melody = melody_rhy_gen(melody, uppertime=4,lowertime=4,bar=2,
                    rhythm_list=motifrhythm_list)
    melody = insert_note(melody, motifinterval_list, scale)
    while check_contour(melody,scale) == False:
       return main_generation(key)
    return melody

def generate_options(ans_key,filtered_keyscale):
    options = []
    ans_key_index = list(keyscale.keys()).index(ans_key)
    for key in filtered_keyscale:
        if key != ans_key:
            key_index = list(keyscale.keys()).index(key)
            if abs(key_index - ans_key_index) > 1:
                options.append(key)
        if len(options) == 4:
            break
    options.append(ans_key)
    random.shuffle(options)
    return options


   
