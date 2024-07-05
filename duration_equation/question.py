import time
from random import randint
from fractions import Fraction
hard_duration = ["hemidemisemiquaver","demisemiquaver", "semiquaver","quaver","crotchet","minim","semibreve","breve"]
easy_duration=["semiquaver","quaver","crotchet","minim","semibreve"]

duration_fration={"hemidemisemiquaver":Fraction(1,64),"demisemiquaver":Fraction(1,32), "semiquaver":Fraction(1,16), "quaver":Fraction(1,8), "crotchet":Fraction(1,4), "minim":Fraction(1,2), "semibreve":1, "breve":2}

dotted_duration=[1,Fraction(3,2),Fraction(7,4)]

def question_elements(hard=bool,simple=bool,double_dotted=bool):
    if hard:
        duration = hard_duration
    else:
        duration = easy_duration
    dotted_vartion=[" "]
    if simple:
        dotted_vartion.append("dotted ")
    if double_dotted:
        dotted_vartion.append('double-dotted ')
    
    return duration, dotted_vartion

def generate_question(duration,dotted_vartion):
    question_idx = randint(3, len(duration) - 1)  # Corrected the range to avoid IndexError
    question_dur = duration[question_idx]
    dotted_idx = randint(0,len(dotted_vartion)-1)
    question_dotted = dotted_vartion[dotted_idx]
    dotted_time = dotted_duration[dotted_idx]
    small_idx = question_idx // randint(2, 4)
    small_dur = duration[small_idx]
    return small_dur, question_dur,question_dotted,dotted_time

def user_input():
    user_ans = input('Enter your answer: ')
    return user_ans

def correct_ans(small,big,dotted_time):
    correct=(duration_fration[big]*dotted_time)//duration_fration[small]
    return correct

def check_ans(ans, correct):
    if str(ans) == str(correct):
        print("Correct answer")
    else:
        print("Wrong answer")

def main():
    small_dur, question_dur,dotted_time = generate_question()
    correct = correct_ans(small_dur, question_dur,dotted_time)
    result = user_input()
    check_ans(result, correct)

if __name__ == "__main__":
    main()
