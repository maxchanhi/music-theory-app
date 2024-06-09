from fractions import Fraction

durations_fraction = {
    "2": Fraction(1, 2),
    "4": Fraction(1, 4),
    "8": Fraction(1, 8),
    "16": Fraction(1, 16),
    '4.': Fraction(3, 8),
    '8.': Fraction(3, 16),
    "1":1
}

durations_notation = {v: k for k, v in durations_fraction.items()}
keyscale = {
    "c major": ['c', 'd', 'e', 'f', 'g', 'a', 'b'],
    "a minor": ['a', 'b', 'c', 'd', 'e', 'f', 'gs'],
    "g major": ['g', 'a', 'b', 'c', 'd', 'e', 'fs'],
    "e minor": ['e', 'fs', 'g', 'a', 'b', 'c', 'ds'],
    "d major": ['d', 'e', 'fs', 'g', 'a', 'b', 'cs'],
    "b minor": ['b', 'cs', 'd', 'e', 'fs', 'g', 'as'],
    "a major": ['a', 'b', 'cs', 'd', 'e', 'fs', 'gs'],
    "fs minor": ['fs', 'gs', 'a', 'b', 'cs', 'd', 'es'],
    "e major": ['e', 'fs', 'gs', 'a', 'b', 'cs', 'ds'],
    "cs minor": ['cs', 'ds', 'e', 'fs', 'gs', 'a', 'bs'],
    "b major": ['b', 'cs', 'ds', 'e', 'fs', 'gs', 'as'],
    "gs minor": ['gs', 'as', 'b', 'cs', 'ds', 'e', 'fss'],
    "fs major": ['fs', 'gs', 'as', 'b', 'cs', 'ds', 'es'],
    "ds minor": ['ds', 'es', 'fs', 'gs', 'as', 'b', 'css'],
    "gf major": ['gf', 'af', 'bf', 'cf', 'df', 'ef', 'f'],
    "ef minor": ['ef', 'f', 'gf', 'af', 'bf', 'cf', 'd'],
    "df major": ['df', 'ef', 'f', 'gf', 'af', 'bf', 'c'],
    "bf minor": ['bf', 'c', 'df', 'ef', 'f', 'gf', 'a'],
    "af major": ['af', 'bf', 'c', 'df', 'ef', 'f', 'g'],
    "f minor": ['f', 'g', 'af', 'bf', 'c', 'df', 'e'],
    "ef major": ['ef', 'f', 'g', 'af', 'bf', 'c', 'd'],
    "c minor": ['c', 'd', 'ef', 'f', 'g', 'af', 'b'],
    "bf major": ['bf', 'c', 'd', 'ef', 'f', 'g', 'a'],
    "g minor": ['g', 'a', 'bf', 'c', 'd', 'ef', 'fs'],
    "f major": ['f', 'g', 'a', 'bf', 'c', 'd', 'e'],
    "d minor": ['d', 'e', 'f', 'g', 'a', 'bf', 'cs']
}

major_keys = ['g major', 'd major', 'a major', 'ef major', 'bf major',"ef major"]
minor_keys = ['e minor', 'b minor', 'fs minor', 'c minor', 'g minor', 'd minor',"fs minor"]
transposition = ["up a major 2nd","down a minor 3rd","up a perfect 5th"]
alphabat= ["c","d","e","f","g","a","b"]
JUMP_CHART = {
    ('2', "major"): 3, 
    ('3', 'minor'): 4,
    ('5', 'perfect'): 8
}
SEMITONES = {
    0: ['c', 'bs'],1: ['cs', 'df'],
    2: ['d','css'],3: ['ds', 'ef'],
    4: ['e', 'ff'],5: ['f', 'es'],
    6: ['fs', 'gf'],7: ['g',"fss"],
    8: ['gs', 'af'],9: ['a'],
    10: ['as', 'bf'],11: ['b', 'cf']
}
NOTE_TO_SEMITONES_LILYPOND = {
    'c': 0, 'bs': 0,  # C, B#
    'cs': 1, 'df': 1,  # C#, Db
    'd': 2,'css':2,  # D
    'ds': 3, 'ef': 3,  # D#, Eb
    'e': 4, 'ff': 4,  # E, Fb
    'f': 5, 'es': 5,  # F, E#
    'fs': 6, 'gf': 6,  # F#, Gb
    'g': 7, "fss":7, # G
    'gs': 8, 'af': 8,  # G#, Ab
    'a': 9,  # A
    'as': 10, 'bf': 10,  # A#, Bb
    'b': 11, 'cf': 11
}
def count_alphabat(ori_note="bf",transpose_by="up a major 2nd"):
    note=ori_note[0]
    if transpose_by=="up a major 2nd":
        pos = alphabat.index(note)+1
    elif transpose_by=="down a minor 3rd":
        pos=alphabat.index(note)-2
    elif transpose_by=="up a perfect 5th":
        pos=alphabat.index(note)+4
    elif transpose_by == "down a perfect 5th":
        pos = alphabat.index(note) - 4
    tran_idx=pos%len(alphabat)
    if pos > len(alphabat)-1:
        octave="'"
    elif pos < 0:
        octave = ","
    else:
        octave = ""
    return alphabat[tran_idx],octave

def count_piano(original_note="as,",new_letter="e",octave='',transpose_by="up a perfect 5th"):
    original_note = original_note.replace("'", "").replace(",", "")  if "'" in original_note or  "," in original_note  else original_note
    if transpose_by=="up a major 2nd":
        tran_idx=(NOTE_TO_SEMITONES_LILYPOND[original_note.lower()]+2)%12
    elif transpose_by=="down a minor 3rd":
        tran_idx=(NOTE_TO_SEMITONES_LILYPOND[original_note.lower()]-3)%12
    elif transpose_by=="up a perfect 5th":
        tran_idx=(NOTE_TO_SEMITONES_LILYPOND[original_note.lower()]+7)%12
    elif transpose_by == "down a perfect 5th":
        tran_idx = (NOTE_TO_SEMITONES_LILYPOND[original_note.lower()] - 7) % 12
    new_enhar=SEMITONES[tran_idx]
    for note in new_enhar:
        if note[0]==new_letter.lower():
            return note+octave

def each_note_transposition(note="es",transpose_by="up a major 2nd"):
    trans_letter,octave = count_alphabat(note,transpose_by)
    return count_piano(note,trans_letter,octave,transpose_by)


