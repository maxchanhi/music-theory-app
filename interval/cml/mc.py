from cml.note_to_key import *
from cml.interval import *
import random

def get_multiple_choice_options(correct_answer):
    e_question = list(JUMP_CHART.values())
    n_question =list(NUM_PLACEMENT.values())

    options = [correct_answer]

    while len(options) < 5:
        choice = random.choice(e_question)+" "+ random.choice(n_question)
        if choice not in options:
            options.append(choice)

    random.shuffle(options)

    for i in range(len(options)):
        if options[i] == correct_answer:
            return i, options
        else:
            pass


correct_answer = generate_correct_option()

ans_key, options = get_multiple_choice_options(correct_answer)

#print("What is the interval?")
for j, option in enumerate(options, 1):
    print(f"{j}. {option}")

user_ans = input("Your answer is:")

if user_ans.lower() == str(ans_key):
    print("Correct")
else:
    print("The answer was",ans_key+1,".",options[ans_key])
