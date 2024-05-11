NOTENAME = ["C","D","E","F","G","A","B"]
ACCIDENTAL = ["#","","b"]
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
    
    ('7', '10'): "Diminished",('7', '11'): "Minor",
    ('7', '12'): "Major",('7', '13'): "Augmented",
    
    ('8', '12'): "Diminished",
    ('8', '13'): "Perfect",('8', '14'): "Augmented",
}
NOTE_TO_SEMITONES = {
    'C': 0, 'B#':0,
    'C#': 1, 'Db': 1,
    'D': 2,
    'D#': 3, 'Eb': 3,
    'E': 4, 'Fb': 4,
    'F': 5,'E#':5,
    'F#': 6, 'Gb': 6,
    'G': 7,
    'G#': 8, 'Ab': 8,
    'A': 9,
    'A#': 10, 'Bb': 10,
    'B': 11,'Cb':11
}
NUM_PLACEMENT = {'1':"Unison",'2':"Second",
                 '3':"Third", '4':"Fourth",
                 '5':"Fifth", '6':"Sixth",
                 '7':"Seventh",'8':"Octave"}