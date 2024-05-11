import subprocess
from PIL import Image
import random
from interval.element import basic_accidentals, accidentals_lilypond, note_letters,calculate_interval,JUMP_CHART,NUM_PLACEMENT,calculate_semitone,advance_accidentals
def clef_range(clef):
    if clef=="treble":
        fix_octave = str(random.choice(["c'","c''"]))
    elif clef == "alto" or clef== "tenor":
        fix_octave = str(random.choice(["c","c'"]))
    elif clef=="bass":
        fix_octave = str(random.choice(["c,","c"]))
    return fix_octave
    
def score_generation(selected_clef=["treble"],accidental=basic_accidentals,
                     same_clef=True,compund_octave=False):
    while True: 
        clef1 = random.choice(selected_clef)
        if same_clef:
            clef2 = clef1 
        else:
            clef2  = random.choice(selected_clef)    
        fix_octave1 = clef_range(clef1)
        if compund_octave:
            fix_octave2 = clef_range(clef2)
        else:
            fix_octave2 = fix_octave1
        output_note = [random.choice(note_letters), random.choice(accidental), fix_octave1]
        output_note2 = [random.choice(note_letters), random.choice(accidental), fix_octave2]

        if output_note==output_note2 and random.randint(0, 3) != 0:
            continue

        note = f"{output_note[0]}{accidentals_lilypond[output_note[1]]}".lower()
        note2 = f"{output_note2[0]}{accidentals_lilypond[output_note2[1]]}".lower()

        interval_number = calculate_interval(fix_octave1, fix_octave2, note_letters.index(output_note[0]), note_letters.index(output_note2[0]))
        semitone_count = calculate_semitone(note, note2, note_letters.index(output_note[0]), note_letters.index(output_note2[0]),fix_octave1, fix_octave2)
        print(interval_number,semitone_count)
        if interval_number >= 24:
            interval_number -= 2
        elif interval_number > 15 and interval_number <=23:
            interval_number -= 1 
        key = (str(interval_number%7), str(semitone_count))
        # Check if the key exists in JUMP_CHART
        if key in JUMP_CHART:
            e_ans = JUMP_CHART[key]
            no_ans = NUM_PLACEMENT[str(interval_number)]
            ans = f"{e_ans} {no_ans}"
            print(note, note2, ans)
            return ans,clef1,clef2,fix_octave1, fix_octave2, note, note2

def lilypond_generation(clef, clef2,fix_octave1,fix_octave2,note,note2):
    lilypond_score = f"""
  \\version "2.24.3"  
  \\header {{}}
    tagline = "" 
  
  #(set-global-staff-size 26) 

  \\score {{
    {{
      \\clef "{clef}" 
      \\fixed {fix_octave1} {note}
      \\clef "{clef2}"
      \\fixed {fix_octave2} {note2}
    }}
    \\layout {{
      indent = 0\\mm  % Remove indentation to avoid unnecessary space
      line-width = #50  % Adjust line width to fit your content
      ragged-right = ##f  % To avoid ragged right lines
      \\context {{
        \\Score
        \\omit TimeSignature
        \\remove "Bar_number_engraver"  % Remove bar numbers
      }}
    }}
  }}
  """

  # Write the string to a LilyPond (.ly) file
    with open('interval/static/score.ly', 'w') as f:
      f.write(lilypond_score)

  # Run LilyPond on the file to generate the score
  # Ensure that LilyPond is in your system's PATH or provide the full path to the LilyPond executable
    subprocess.run(['lilypond', '--png', '-dresolution=300', f'--output=interval/static/score', f'interval/static/score.ly'], check=False)
 
  # Open the generated PNG file
    with Image.open('interval/static/score.png') as img:
      # Calculate the crop rectangle
      width, height = img.size
      crop_height = height
      crop_rectangle = (120, 0, width/4, crop_height/10)
      
      # add code to crop 1/10 from the top
      cropped_img = img.crop(crop_rectangle)
      cropped_img.save("interval/static/images/cropped_score_ans.png")

def level_difficulty(level="Expert"):
    level_dic = {"Beginner":[["treble","bass"],True,['Natural (♮)'],False],
                 "Intermediate":[["treble","bass"],True,basic_accidentals,False],
                 "Advanced":[["treble","bass"],False,basic_accidentals,True],
                 "C clef Fanfare":[["tenor","alto"],True,basic_accidentals,False],
                 "Accidental Fanfare":[["treble","bass"],True,advance_accidentals,True],
                 "Expert":[["treble","alto","tenor","bass"],False,advance_accidentals,True]}
    selected_level = {"clef" :level_dic[level][0],
                      "same_clef":level_dic[level][1],
                      "accidentals":level_dic[level][2],
                      "compound_octave":level_dic[level][3]}
    return selected_level

   