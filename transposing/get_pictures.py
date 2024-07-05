import random
import os

def get_pic_link():
    link_list = []
    base_path = "transposing/static"
    for idx in range(1, 6):
        file_name = f"wrong_{idx}.png"
        if os.path.exists(os.path.join(base_path, file_name)):
            link_list.append(f"static/{file_name}")
    if os.path.exists(os.path.join(base_path, "correct.png")):
        link_list.append("static/correct.png")
    random.shuffle(link_list)
    return link_list