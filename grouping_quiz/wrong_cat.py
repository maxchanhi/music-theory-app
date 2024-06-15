#"Off-beat grouped rest in compound time","Incorrect rest duration",
import random

catagory = ["Correct notation", "Dotted rest in simple time",
            "Syncopated rest",
            "Breaking a rest",
            "Beaming issue","Unclear down beat","Hemiola"]

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
    target_url = "grouping_quiz/static/" + url #tag
    
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

def needle_in_haystack():
    img_list_path = []
    while len(img_list_path) < 4:
        url = str(random.choice(urls[1:]))
        img_path = get_picture(url)
        _, file_extension = os.path.splitext(img_path)
        if file_extension.lower() == ".png" and img_path not in img_list_path:
            img_list_path.append(img_path)
    
    correct_url = get_picture(urls[0])
    _, file_extension = os.path.splitext(correct_url)
    while file_extension.lower() != ".png":
        correct_url = get_picture(urls[0])
        _, file_extension = os.path.splitext(correct_url)
    
    img_list_path.append(correct_url)
    random.shuffle(img_list_path)
    print(img_list_path)
    return img_list_path
