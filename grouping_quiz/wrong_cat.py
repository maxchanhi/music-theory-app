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
def get_picture(url):
    target_url = "grouping_quiz/static/" + url
    
    image_files = [f for f in os.listdir(target_url) if f.lower().endswith('.png')]
    
    if not image_files:
        print(f"No PNG image files found in {target_url}")
        return None, None

    random_image = random.choice(image_files)
    image_path = os.path.join(target_url, random_image)
    problem_idx = urls.index(url)
    problem_tag = catagory[problem_idx]
    return image_path, problem_tag


def needle_in_haystack():
    img_list_path = []
    
    # First, get the correct answer
    correct_url, correct_tag = get_picture(urls[0])
    while not correct_url or not correct_url.lower().endswith('.png'):
        correct_url, correct_tag = get_picture(urls[0])
    
    img_list_path.append((correct_url, correct_tag))
    
    # Then get the incorrect answers
    while len(img_list_path) < 5:
        url = random.choice(urls[1:])
        img_path, problem_tag = get_picture(url)
        if img_path and img_path.lower().endswith('.png') and img_path not in [img for img, _ in img_list_path]:
            img_list_path.append((img_path, problem_tag))
    
    random.shuffle(img_list_path)
    return img_list_path