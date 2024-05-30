import fractions
import random

digit_to_rhythm_british = {
    1: "semibreve",
    2: "minim",
    4: "crotchet",
    8: "quaver",
    16: "semiquaver",
    32: "demisemiquaver",
    64: "hemidemisemiquaver"
}
simple_time_numerator = [2, 3, 4]
compound_time_numerator = [6, 9, 12]
time_denominator = [16, 8, 4, 2]

denominator = [64, 32, 16, 8, 4, 2,1]
DOTTED = fractions.Fraction(3, 2)
def generate_question():
    get_time_signature = (random.choice(compound_time_numerator), random.choice(time_denominator))
    denominator_idx = denominator.index(get_time_signature[1])
    idx_offset =1# random.randint(0, 1)
    small_dur = denominator[denominator_idx + idx_offset]
    question_title= f"How many dotted {digit_to_rhythm_british[small_dur]}s in {get_time_signature[0]}/{get_time_signature[1]}?"

    measured_small_dur = DOTTED * fractions.Fraction(1,small_dur)
    full_bar_value=fractions.Fraction(1, get_time_signature[1]) * get_time_signature[0]
    answer= full_bar_value/measured_small_dur

    return question_title, answer


