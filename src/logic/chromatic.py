alphabet = ["c", "d", "e", "f", "g", "a", "b"]
black_white_key = {
    0: ['c'], 1: ['cs', 'df'], 2: ['d'], 3: ['ds', 'ef'],
    4: ['e'], 5: ['f', 'es'], 6: ['fs', 'gf'], 7: ['g'],
    8: ['gs', 'af'], 9: ['a'], 10: ['as', 'bf'], 11: ['b']
}
accidentals = ["", "s","f"]
import random
starting_num = random.randint(0, 11)
starting_pitch = random.choice(black_white_key[starting_num])
scale = [starting_pitch]
next_num = starting_num
while len(scale) < 12:
    next_num  = (next_num + 1) % 12
    next_pitch = random.choice(black_white_key[next_num])
    if len(scale) > 2:
        if next_pitch[0] == scale[-1][0] and next_pitch[0] == scale[-2][0]:
            next_num  = (next_num - 1) % 12
        else:
            scale.append(next_pitch)
    else:
        scale.append(next_pitch)
if "'" in scale[0] or "," not in scale[0]:
    scale.append(scale[0]+"'")
elif "," in scale[0]:
    scale.append(scale[0].replace(",",""))
