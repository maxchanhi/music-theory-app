from transposing.melody_generation import melody_generation_n_tansposition, options_main, option_problems
from transposing.muti_process import main_generation

def picture_generation():
    data = melody_generation_n_tansposition()
    question_melody = [[data["original_key"], data["original_melody"], "question"],
                       [data["transposed_key"], data["transposed_melody"], "correct"]]
    options_list = options_main(melody=data["transposed_melody"], key=data["transposed_key"])
    idx = 1
    generated_option_problems = {}
    for task in options_list:
        task_name = f"wrong_{idx}"
        question_melody.extend([[task[0], task[1], task_name]])
        generated_option_problems[task_name] = option_problems[task[2]]
        idx += 1

    main_generation(question_melody)
    return data["transposing_by"], generated_option_problems

if __name__ == "__main__":
    picture_generation()