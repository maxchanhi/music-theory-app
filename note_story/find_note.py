from story import story_line,html_upper_pt,html_lower_pt
from score_generation import main_score_generation
from test_3 import three_notename, to_notename,upper_3
import random
import multiprocessing

def main_process_story(title = "Grand_Day_Out",story=str,clef=str,leger_line=None):
    text_list = story.split()
    output_story = []
    keywords = []
    i=1
    for word in text_list:
        if word.isupper():
            cleaned_word = word.replace(",", "").replace(".", "")
            output_story.append([f"!{title}_pic_{i}",cleaned_word])
            keywords.append((clef, cleaned_word,leger_line,f"!{title}_pic_{i}"))
        else:
            pick = random.choices([True,False],[4,1])[0] 
            check_3, _ = three_notename(word)
            if upper_3(word) or (pick and check_3):
                result = to_notename(word)
                if len(result[1])<3:
                    output_story.append(word)
                    continue
                output_story.append(result[0])
                cleaned_word = result[1].replace(",", "").replace(".", "")
                output_story.append([f"!{title}_pic_{i}",cleaned_word])
                keywords.append((clef, cleaned_word,leger_line,f"!{title}_pic_{i}"))
                output_story.append(result[2])
            else:
                output_story.append(word)
        i+=1
    return output_story, keywords
def generate_html(output_story,title):
    story_content = ""
    for item in output_story:
        if isinstance(item, list):
            image_name, answer = item
            story_content += f'<img src="static/{image_name}.png" class="note-image"><span class="blank"><input type="text" data-answer="{answer}"></span>'
        else:
            story_content += item + " "
            
    html_content = html_upper_pt+story_content+html_lower_pt

    # Generate the HTML file
    with open(f"note_story/{title}.html", "w") as f:
        f.write(html_content)


if __name__ == '__main__':
    cpus = multiprocessing.cpu_count()
    title = "Muti_Day_Out"
    story=story_line,clef="treble"
    leger=None
    output_story, keywords = main_process_story(title,leger)
    generate_html(output_story, title)
    pool = multiprocessing.Pool(processes=cpus)
    pool.starmap(main_score_generation, keywords)