from collections import Counter
from clef_minor.all_keys1 import melodic_minor_scales, harmonic_ascending, major_scale

accidental_tran = {"bb": "ff", "b": "f", "#": "s", "x": "ss"}
note_letter= "a b c d e f g"

def smart_input(notes="bb")->str:
    note_letter_list = note_letter.split()
    note_list = set(notes.lower().split())
    if len(note_list)==0:
        return note_letter
    else:
        acc_lst= []
        for note in note_list:
            if len(note)>1:
                acc_lst.append(note)
        for acc in acc_lst:
            note_letter_list[note_letter_list.index(acc[0])]=acc
        for note in note_letter_list:
            if note[1:] in accidental_tran.keys():
                note_letter_list[note_letter_list.index(note)]=note[0]+accidental_tran[note[1:]]
        return ' '.join(note_letter_list)

def get_max_freq(counter):
    if not counter:
        return []
    max_freq = max(counter.values())
    return [(key, freq) for key, freq in counter.items() if freq == max_freq]

def finding_key(notes=""):
    notes =smart_input(notes)
    note_list = set(notes.lower().split())
    mm_minor, hm_minor, c_major = [], [], []
    
    for note in note_list:
        
        for k, v in melodic_minor_scales.items():
            if note in v:
                mm_minor.append(k)
        for k, v in harmonic_ascending.items():
            if note in v:
                hm_minor.append(k)
        for k, v in major_scale.items():
            if note in set(v):
                c_major.append(k)

    mm_count = Counter(mm_minor)
    hm_count = Counter(hm_minor)
    ma_count = Counter(c_major)

    max_major = get_max_freq(ma_count)
    max_harmonic_minor = get_max_freq(hm_count)
    max_melodic_minor = get_max_freq(mm_count)

    results = []
    results.extend([(key, freq, "Major") for key, freq in max_major])
    results.extend([(key, freq, "Harmonic Minor") for key, freq in max_harmonic_minor])
    results.extend([(key, freq, "Melodic Minor") for key, freq in max_melodic_minor])

    # Filter to keep only the highest frequency results
    max_freq = max(result[1] for result in results) if results else 0
    results = [result for result in results if result[1] == max_freq]
    return results
