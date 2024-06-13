import random
def get_pic_link():
    link_list=[]
    for idx in range(1,6):
        link_list.append(f"static/wrong_{idx}.png")
    link_list.append("static/correct.png")
    random.shuffle(link_list)   
    return link_list