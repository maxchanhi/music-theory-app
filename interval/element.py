note_letters = ['C', 'D', 'E', 'F', 'G','A','B']

basic_accidentals = ['Flat (♭)', 'Natural (♮)', 'Sharp (♯)']
advance_accidentals = ['Flat (♭)', 'Natural (♮)', 'Sharp (♯)','Double-sharp(x)','Double-flat(♭♭)']

accidentals_lilypond = {'Sharp (♯)':"is",'Natural (♮)':"",'Flat (♭)':"es",'Double-sharp(x)':"isis",'Double-flat(♭♭)':"eses"}
NOTE_TO_SEMITONES_LILYPOND = {
    'c': 0, 'bis':0,  # C, B#
    'cis': 1, 'des': 1,  # C#, Db
    'd': 2,  # D
    'dis': 3, 'ees': 3,  # D#, Eb
    'e': 4, 'fes': 4,  # E, Fb
    'f': 5, 'eis': 5,  # F, E#
    'fis': 6, 'ges': 6,  # F#, Gb
    'g': 7,  # G
    'gis': 8, 'aes': 8,  # G#, Ab
    'a': 9,  # A
    'ais': 10, 'bes': 10,  # A#, Bb
    'b': 11, 'ces': 11,  # B, Cb
    'cisis': 2, 'deses': 0,  # C## (equivalent to D), Dbb (enharmonic equivalent to C)
    'disis': 4, 'eeses': 2,  # D## (equivalent to E), Ebb (enharmonic equivalent to D)
    'eisis': 6, 'feses': 3,  # E## (equivalent to F#), Fbb (enharmonic equivalent to Eb)
    'fisis': 7, 'geses': 5,  # F## (equivalent to G), Gbb (enharmonic equivalent to F)
    'gisis': 9, 'aeses': 7,  # G## (equivalent to A), Abb (enharmonic equivalent to G)
    'aisis': 11, 'beses': 9,  # A## (equivalent to B), Bbb (enharmonic equivalent to A)
    'bisis': 1, 'ceses': 10  # B## (equivalent to C#), 
}
from collections import defaultdict
RE_NOTE_TO_SEMITONES = defaultdict(list)

# Populate the reversed dictionary
for key, value in NOTE_TO_SEMITONES_LILYPOND.items():
    RE_NOTE_TO_SEMITONES[value].append(key)

# Convert defaultdict back to a regular dictionary if needed
RE_NOTE_TO_SEMITONES = dict(RE_NOTE_TO_SEMITONES)

print(RE_NOTE_TO_SEMITONES)
JUMP_CHART = {

    ('2', '1'): "Diminished", ('2', '2'): "Minor",
    ('2', '3'): "Major", ('2', '4'): "Augmented",
    
    ('3', '3'): "Diminished",('3', '4'): "Minor",
    ('3', '5'): "Major", ('3', '6'): "Augmented",
    
    ('4', '5'): "Diminished",
    ('4', '6'): "Perfect",('4', '7'): "Augmented",
    
    ('5', '7'): "Diminished",
    ('5', '8'): "Perfect",('5', '9'): "Augmented",
    
    ('6', '8'): "Diminished",('6', '9'): "Minor",
    ('6', '10'): "Major",('6', '11'): "Augmented",
    
    ('0', '10'): "Diminished",('0', '11'): "Minor",
    ('0', '12'): "Major",('0', '13'): "Augmented",
    
    ('1', '2'): "Diminished",
    ('1', '13'): "Perfect",('1', '14'): "Augmented",
    ('1', '1'): "Perfect",('1', '12'): "Augmented"
}
def reverse_jump_chart(chart):
    reversed_chart = defaultdict(dict)
    for (interval_num, semitones), quality in chart.items():
        reversed_chart[quality][interval_num] = semitones
    return dict(reversed_chart)

# Create the reversed JUMP_CHART
RE_JUMP_CHART = reverse_jump_chart(JUMP_CHART)
print(RE_JUMP_CHART)
OCTAVE={"c,":2,"c":3,"c'":4,"c''":5}
NUM_PLACEMENT = {
    '1':"Unison", '2': "Second",
    '3': "Third", '4': "Fourth",
    '5': "Fifth", '6': "Sixth",
    '7': "Seventh", '8': "Octave", '9': "Ninth",
    '10': "Tenth", '11': "Eleventh", '12': "Twelfth",
    '13': "Thirteenth", '14': "Fourteenth", '15': "Compound Octave",
    '16': "Sixteenth", '17': "Seventeenth", '18': "Eighteenth",
    '19': "Nineteenth", '20': "Twentieth", '21': "Twenty-first",
    '22': "2 Compound Octaves", '23': "Twenty-third", '24': "Twenty-fourth",
    '25': "Twenty-fifth", '26': "Twenty-sixth", '27': "Twenty-seventh",
    '28': "Twenty-eighth", '29': "3 Compound Octaves"
}
RE_NUM_PLACEMENT = {v: k for k, v in NUM_PLACEMENT.items()}
user_interval=["--","Unison","Second",
     "Third",  "Fourth", "Fifth", "Sixth", "Seventh", "Octave",  "Ninth",
    "Tenth", "Eleventh", "Twelfth", "Thirteenth",  "Fourteenth", "Compound Octave",
    "Sixteenth",  "Seventeenth", "Eighteenth", "Nineteenth",  "Twentieth", "Twenty-first",
     "2 Compound Octaves", "Twenty-third",  "Twenty-fourth", "Twenty-fifth",  "Twenty-sixth", "Twenty-seventh",
     "Twenty-eighth","3 Compound Octaves"]
user_quality=["--","Diminished","Minor", "Perfect","Major","Augmented"]
import random
#from generation import score_generation
def calculate_interval(octave1, octave2,first_note_position,second_note_position):
    if OCTAVE[octave1] == OCTAVE[octave2]:
        if first_note_position>second_note_position:
            return first_note_position-second_note_position+1
        elif first_note_position<second_note_position:
            return second_note_position-first_note_position+1
        else:
            return 1
    elif OCTAVE[octave1] > OCTAVE[octave2]:
        if first_note_position!=second_note_position:
            return (first_note_position-second_note_position)+((OCTAVE[octave1]-OCTAVE[octave2])*8)
        else:
            return (OCTAVE[octave1]-OCTAVE[octave2])*8
    elif OCTAVE[octave1] < OCTAVE[octave2]:
        if first_note_position!=second_note_position:
            return second_note_position-first_note_position+((OCTAVE[octave2]-OCTAVE[octave1])*8)-1
        else:
            return (OCTAVE[octave2]-OCTAVE[octave1])*8
def calculate_semitone(first_note, second_note,note_letter1,note_letter2,octave1, octave2):
    if note_letter1 == note_letter2 and OCTAVE[octave1] < OCTAVE[octave2]:
            return abs(NOTE_TO_SEMITONES_LILYPOND[second_note]-NOTE_TO_SEMITONES_LILYPOND[first_note]-1)
    elif note_letter1 == note_letter2 and OCTAVE[octave1] > OCTAVE[octave2]:
            return abs(NOTE_TO_SEMITONES_LILYPOND[first_note]-NOTE_TO_SEMITONES_LILYPOND[second_note]-1)
    elif note_letter1 == note_letter2 and OCTAVE[octave1] == OCTAVE[octave2] and NOTE_TO_SEMITONES_LILYPOND[first_note]!=NOTE_TO_SEMITONES_LILYPOND[second_note]:
        return 14
    if NOTE_TO_SEMITONES_LILYPOND[second_note]>NOTE_TO_SEMITONES_LILYPOND[first_note]:
        return NOTE_TO_SEMITONES_LILYPOND[second_note]-NOTE_TO_SEMITONES_LILYPOND[first_note]+1
    elif NOTE_TO_SEMITONES_LILYPOND[second_note]<NOTE_TO_SEMITONES_LILYPOND[first_note]:
        return NOTE_TO_SEMITONES_LILYPOND[second_note]+13-NOTE_TO_SEMITONES_LILYPOND[first_note]

difficulty_list= ["Beginner", "Intermediate", "Advanced", "C clef Fanfare", "Accidental Fanfare", "Expert"]

wrong_octave= {"Second":"Seventh", "Third": "Sixth", 
                "Fourth":"Fifth", "Fifth":"Fourth",
                "Sixth":"Third", "Seventh":"Second"}

wrong_compound = {
    "Second":"Ninth","Third":"Tenth","Fourth":"Eleventh","Fifth":"Twelfth",
    "Sixth":"Thirteenth","Seventh":"Fourteenth"
}