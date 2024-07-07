note_name = 'abcdefg'

def three_notename(word=str):
    note_count = 0
    start_idx = -1
    for i, letter in enumerate(word):
        if letter in note_name:
            if start_idx == -1:
                start_idx = i
            note_count += 1
            if note_count >= 3:
                return True, start_idx
        else:
            if note_count >= 3:
                return True, start_idx
            note_count = 0
            start_idx = -1
    return False, None

def to_notename(word=str):
    start_idx = -1
    end_idx = -1
    in_note_sequence = False
    
    for i, letter in enumerate(word):
        if letter.lower() in note_name:  # Convert to lowercase for checking
            if not in_note_sequence:
                start_idx = i
                in_note_sequence = True
        else:
            if in_note_sequence:
                end_idx = i
                break
    
    if in_note_sequence and end_idx == -1:
        end_idx = len(word)
    
    if start_idx == -1 or end_idx == -1:
        return word, '', ''
    
    non_notename = word[:start_idx]
    notepart = word[start_idx:end_idx]
    fin_nonnote = word[end_idx:]
    
    return non_notename, notepart, fin_nonnote
def upper_3(word=str):
    count = 0
    for i in word:
        if i.isupper():
            count = count + 1
        else:
            count = 0
        if count >2:
            return True
    return False
