note_letters = ['C', 'D', 'E', 'F', 'G','A','B']
accidentals_lilypond = {'Sharp (♯)': "is", 'Natural (♮)': "", 'Flat (♭)': "es", 'Double-sharp(x)': "isis", 'Double-flat(♭♭)': "eses"}

NOTE_TO_SEMITONES = {
    'c': 0, 'cis': 1, 'd': 2, 'dis': 3, 'e': 4, 'f': 5, 'fis': 6, 'g': 7, 'gis': 8, 'a': 9, 'ais': 10, 'b': 11, 'cisis': 2,
    'deses': 11, 'disis': 4, 'eeses': 2, 'eisis': 6, 'feses': 4, 'fisis': 8, 'geses': 6, 'gisis': 10, 'aeses': 8, 'aisis': 12,
    'beses': 10, 'bisis': 13, 'ceses': 11
}

OCTAVE = {"c,": 2, "c": 3, "c'": 4, "c''": 5}
NUM_PLACEMENT = {
    '1': "Unison", '2': "Second", '3': "Third", '4': "Fourth", '5': "Fifth", '6': "Sixth",
    '7': "Seventh", '8': "Octave", '9': "Ninth", '10': "Tenth", '11': "Eleventh", '12': "Twelfth",
    '13': "Thirteenth", '14': "Fourteenth", '15': "Octave", '16': "Sixteenth"
}

JUMP_CHART = {
    ('2', '1'): "Diminished", ('2', '2'): "Minor", ('2', '3'): "Major", ('2', '4'): "Augmented",
    ('3', '3'): "Diminished", ('3', '4'): "Minor", ('3', '5'): "Major", ('3', '6'): "Augmented",
    ('4', '5'): "Diminished", ('4', '6'): "Perfect", ('4', '7'): "Augmented",
    ('5', '7'): "Diminished", ('5', '8'): "Perfect", ('5', '9'): "Augmented",
    ('6', '8'): "Diminished", ('6', '9'): "Minor", ('6', '10'): "Major", ('6', '11'): "Augmented",
    ('7', '10'): "Diminished", ('7', '11'): "Minor", ('7', '12'): "Major", ('7', '13'): "Augmented",
    ('1', '0'): "Diminished", ('1', '1'): "Perfect", ('1', '2'): "Augmented"
}

def calculate_interval(note1, octave1, note2, octave2):
    semitones = NOTE_TO_SEMITONES[note2] - NOTE_TO_SEMITONES[note1]
    if semitones < 0:
        semitones += 12
    octaves = OCTAVE[octave2] - OCTAVE[octave1]
    interval_number = octaves * 7 + note_letters.index(note2[0]) - note_letters.index(note1[0]) + 1
    semitone_count = semitones + octaves * 12

    return interval_number, semitone_count

def get_interval_name(interval_number, semitone_count):
    key = (str(interval_number % 7 or 7), str(semitone_count))
    quality = JUMP_CHART[key]
    interval_name = NUM_PLACEMENT[str(interval_number)]
    return f"{quality} {interval_name}"

# Inputs
output_note1 = ["C", "Sharp (♯)"]
output_note2 = ["C", "Natural (♮)"]
octave1 = "c'"
octave2 = "c"

# Convert notes to Lilypond format
note1 = f"{output_note1[0]}{accidentals_lilypond[output_note1[1]]}".lower()
note2 = f"{output_note2[0]}{accidentals_lilypond[output_note2[1]]}".lower()

note_letters = ['C', 'D', 'E', 'F', 'G', 'A', 'B']

# Maps notes to semitone values, considering accidentals
note_to_semitones = {
    'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11,
    'C##': 2, 'D##': 4, 'E#': 5, 'F##': 7, 'G##': 10, 'A##': 12, 'B#': 0,
    'Cb': 11, 'Db': 1, 'Eb': 3, 'Fb': 4, 'Gb': 6, 'Ab': 8, 'Bb': 10,
    'Cbb': 10, 'Dbb': 0, 'Ebb': 2, 'Fbb': 3, 'Gbb': 5, 'Abb': 7, 'Bbb': 9
}

# Maps intervals to their names
interval_names = {
    0: 'Unison', 1: 'Second', 2: 'Third', 3: 'Fourth', 4: 'Fifth', 5: 'Sixth', 6: 'Seventh', 7: 'Octave',
    8: 'Ninth', 9: 'Tenth', 10: 'Eleventh', 11: 'Twelfth', 12: 'Thirteenth', 13: 'Fourteenth', 14: 'Fifteenth'
}

# Maps semitone differences to interval qualities
interval_qualities = {
    -1: 'Diminished', 0: 'Perfect', 1: 'Augmented', 2: 'Double Augmented',
    3: 'Minor', 4: 'Major', 5: 'Diminished', 6: 'Minor', 7: 'Major', 8: 'Diminished', 9: 'Perfect', 10: 'Augmented'
}

def calculate_interval(note1, note2):
    semitones1 = note_to_semitones[note1]
    semitones2 = note_to_semitones[note2]
    semitone_difference = (semitones2 - semitones1) % 12

    letter1 = note_letters.index(note1[0])
    letter2 = note_letters.index(note2[0])
    letter_difference = (letter2 - letter1) % 7

    interval_number = letter_difference
    interval = interval_names[interval_number]
    quality = interval_qualities[semitone_difference - (interval_number * 2)]
    
    return f"{quality} {interval}"

# Inputs
note1 = "C#"
note2 = "C"

# Calculate and print the interval
print(calculate_interval(note1, note2))