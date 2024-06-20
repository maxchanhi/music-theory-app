import random
from multiprocessing import Process

fixed_pitch=["c","c'","c''"]
clefs=['bass','alto','tenor','treble']
notes=['c','d','e','f','g']
link_list=['diff','same_1','same_2']

def melody_generation():
    picked_clefs = random.choice([clefs[1:], clefs[:3]])
    if "bass" in picked_clefs:
        picked_ref = ["c", "c'"]
    else:
        picked_ref = ["c'", "c''"]
    add_idx = random.randint(0, 1)
    add_ref = [[picked_ref[add_idx], 'same_1'],
               [picked_ref[add_idx], 'same_2'],
               [picked_ref[1 - add_idx], 'diff']]
    random.shuffle(picked_clefs)
    for idx, clef in enumerate(picked_clefs):
        add_ref[idx].append(clef)
    melody = []
    while len(melody) < 4:
        note = random.choice(notes)
        if note not in melody:
            melody.append(note)
    
    return add_ref,melody
import os
import subprocess
import uuid

from PIL import Image

def lilypond_generation(data, melody):
    str_melody = " ".join(melody)
    clef = data[2]
    fix_pitch = data[0]
    file_name = data[1]
    
    # Generate a unique identifier for each job
    job_id = str(uuid.uuid4())
    
    # Incorporate the job_id into the temporary file names
    temp_ly_file = f"temp_{job_id}.ly"
    temp_output_file = f"temp_{job_id}_out"
    
    lilypond = f"""\\version "2.22.0"
#(set-global-staff-size 40)
\\score {{
  \\new Staff \\with {{
    \\remove "Time_signature_engraver"
  }}
  {{
    \\clef {clef}
    \\fixed {fix_pitch}{{
      {str_melody}
    }}
  }}
}}
"""

    with open(temp_ly_file, "w") as file:
        file.write(lilypond)

    try:
        subprocess.run(["lilypond", "-dpreview", "-dbackend=eps", "-dno-gs-load-fonts", "-dinclude-eps-fonts", "--png", f"--output={temp_output_file}", temp_ly_file], check=True)
        image = Image.open(f"{temp_output_file}.png")

        width, height = image.size
        left = 0
        top = 0
        right = width // 2
        bottom = height // 5
        cropped_image = image.crop((left, top, right, bottom))
        cropped_image.save(f"{file_name}.png")
        
    except subprocess.CalledProcessError as e:
        print(f"Error running LilyPond: {e}")
    except FileNotFoundError:
        print("LilyPond is not installed or not found in the system PATH.")
    finally:
        # Clean up temporary files
        if os.path.exists(temp_ly_file):
            os.remove(temp_ly_file)
        if os.path.exists(f"{temp_output_file}.eps"):
            os.remove(f"{temp_output_file}.eps")
        if os.path.exists(f"{temp_output_file}.png"):
            os.remove(f"{temp_output_file}.png")
def main_generation():
    link_list=['diff','same_1','same_2']
    random.shuffle(link_list)
    data, melody = melody_generation()
    job_list = []
    for el in data:
        job_list.append([el,melody])
    processes = []
    for job in job_list:
        p = Process(target=lilypond_generation, args=(job[0], job[1]))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    return link_list

if __name__ == '__main__':
    main_generation()
    
