#"Off-beat grouped rest in compound time","Incorrect rest duration",
import random

catagory = ["Correct notation", "Dotted rest in simple time",
            "Syncopated rest",
            "Breaking a rest",
            "Beaming issue","Unclear down beat","Hemiola grouping"]

urls = ["Correct_rest", "Dotted_rhythm",
        "Syncopated_rest",
        "Breaking_a_rest",
        "beaming","confused_syncopation","hemiola"]

options = list(zip(catagory, urls))
def get_catagory():
    chosen_option = random.choice(options)
    chosen_cat, chosen_url = chosen_option
    return chosen_cat, chosen_url

import os
import random

def get_picture(url=str):
    target_url = "grouping_quiz/static/" + url
    
    image_files = [f for f in os.listdir(target_url)]
    
    if not image_files:
        print(f"No image files found in {target_url}")
        return None

    random_image = random.choice(image_files)
    image_path = os.path.join(target_url, random_image)
    
    return image_path

def main_option()->dict:
    chosen_cat, chosen_url= get_catagory()
    image_path= get_picture(chosen_url)
    question_data={"Catagory": chosen_cat, "Picture": image_path}
    return question_data

fun_emoji_list = [
    "😂",  "🎉",   "🚀",  "🐱", 
    "🐶",  "🦄",  
    "🎶",  "😱","👼🏻","💃🏻","🐰","🐒","🐣","🦀","💥","✨","🥳",
    "🍦",  "🌟",  "👻",  
    "🎈",   "🎮",  "💩"
]
