from transposing.melody_generation import melody_generation_n_tansposition,options_main
from transposing.muti_process import main_generation
import asyncio
def picture_generation():

    data= melody_generation_n_tansposition()
    question_melody = [[data["original_key"], data["original_melody"],"question"],
                    [data["transposed_key"],data["transposed_melody"],"correct"]]
    options_list = options_main(melody=data["transposed_melody"],key=data["transposed_key"])
    idx = 1
    for task in options_list:
        task.append(f"wrong_{idx}")
        question_melody.extend([task])
        idx += 1

    main_generation(question_melody)
    return data["transposing_by"]
if __name__ == "__main__":
    picture_generation()
