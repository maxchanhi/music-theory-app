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
pc_to_keyboard = {
    0: "C",
    1: "C#\nDb",
    2: "D",
    3: "D#\nEb",
    4: "E",
    5: "F",
    6: "F#\nGb",
    7: "G",
    8: "G#\nAb",
    9: "A",
    10: "A#\nBb",
    11: "B"
}

note_letter="c d e f g a b"
letter_list= note_letter.split()

def show_letter_count(lower_pitch="b", higher_pitch="a"):
    lower_index = letter_list.index(lower_pitch[0])
    higher_index = letter_list.index(higher_pitch[0])
    if lower_index>higher_index:
        higher_index+=8
        two_oct_list = letter_list+letter_list.copy()
        return " ".join(two_oct_list[lower_index:higher_index]).upper()
    else:
        return " ".join(letter_list[lower_index:higher_index+1]).upper()


from interval.piano_keyboard.piano import piano_generation
def create_note_list(lower_pitch="b", higher_pitch="a"):
    letter_show=show_letter_count(lower_pitch,higher_pitch)
    keyboard_list = ['C', 'C#\nDb', 'D', 'D#\nEb', 'E', 'F', 'F#\nGb', 'G', 
                     'G#\nAb', 'A', 'A#\nBb', 'B',"C'", "C#\nDb'", "D'", "D#\nEb'",
                     "E'", "F'", "F#\nGb'", "G'", "G#\nAb'", "A'", "A#\nBb'", "B'"]
    lower_note = pc_to_keyboard[NOTE_TO_SEMITONES_LILYPOND[lower_pitch]]
    higher_note = pc_to_keyboard[NOTE_TO_SEMITONES_LILYPOND[higher_pitch]]
    if letter_list.index(lower_pitch[0])>letter_list.index(higher_pitch[0]):
        lower_index = keyboard_list.index(lower_note)
        if higher_note=="B" or lower_note=="C":
            higher_index = keyboard_list.index(higher_note)
            keyboard_list= keyboard_list[:12]
        else:    
            higher_index = keyboard_list.index(higher_note+"'")
    elif lower_pitch==higher_pitch:
        lower_index = keyboard_list.index(lower_note)
        higher_index = keyboard_list.index(higher_note+"'")
    else:
        lower_index = keyboard_list.index(lower_note)
        if lower_pitch=="ces" or lower_pitch=="ceses":
            higher_index = keyboard_list.index(higher_note+"'")
        else:    
            higher_index = keyboard_list.index(higher_note)
            keyboard_list= keyboard_list[:12]
    keyboard_list[lower_index]=keyboard_list[lower_index]+"p"
    keyboard_list[higher_index]=keyboard_list[higher_index]+"p"
    html = piano_generation(keyboard_list)
    return html,letter_show,higher_index+1-lower_index


#def note_cal_from_note_steps(note="cis",quality="Perfect",interval = 'Third')