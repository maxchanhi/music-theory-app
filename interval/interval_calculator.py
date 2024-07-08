from interval.element import NOTE_TO_SEMITONES_LILYPOND,JUMP_CHART,NUM_PLACEMENT,RE_NUM_PLACEMENT,RE_NOTE_TO_SEMITONES,RE_JUMP_CHART
note_letter = "abcdefg"
accidental_translation = {"Double-flat":"eses","Flat":"es","Sharp":"is","Double-sharp":"isis"}
def interval_calculation(lower_pitch="g",higher_pitch="c"):
    lower_idx =note_letter.index(lower_pitch[0])
    higher_idx = note_letter.index(higher_pitch[0])
    if lower_idx<higher_idx:
        letter_interval = higher_idx-lower_idx+1
    elif lower_idx>higher_idx:
        letter_interval = higher_idx+len(note_letter)-lower_idx+1
    elif lower_idx==higher_idx:
        letter_interval = 1

    lower_pc = NOTE_TO_SEMITONES_LILYPOND[lower_pitch]
    higher_pc = NOTE_TO_SEMITONES_LILYPOND[higher_pitch]
    pitch_interval = abs(higher_pc-lower_pc+1)
    cal_quality,cal_interval = None, None
    cal_quality,cal_interval = JUMP_CHART[str(letter_interval),str(pitch_interval)],NUM_PLACEMENT[str(letter_interval)]
    if cal_quality and cal_interval:
        return cal_quality,cal_interval
    else:
        return False,False

def note_calculation(note="bis",quality="Perfect", interval="Ninth"):
    letter_idx = note_letter.index(note[0])
    interval_idx = int(RE_NUM_PLACEMENT[interval])%len(note_letter)
    higher_letter = note_letter[(letter_idx+interval_idx)%len(note_letter)]
    cal_semitone=None
    for key,value in JUMP_CHART.items():
        if key[0]==str(interval_idx) and value==quality:
            cal_semitone = int(key[1])
    if cal_semitone:
        enharmonic_eq_list = RE_NOTE_TO_SEMITONES[NOTE_TO_SEMITONES_LILYPOND[note]+cal_semitone+1]
        for el in enharmonic_eq_list:
            if el[0]==higher_letter:
                return el
    else:
        return False
    