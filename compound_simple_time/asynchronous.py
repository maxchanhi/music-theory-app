import asyncio
from PIL import Image
import os
from compound_simple_time.score_gen import format_melody
async def lilypond_generation(melody, name, uppertime, lowertime):
    lilypond_score = f"""
\\version "2.24.1"  
\\header {{
  tagline = "" \\language "english"
}}

#(set-global-staff-size 26)

\\score {{
    \\fixed c' {{
      \\time {uppertime}/{lowertime}
      \\omit Score.BarLine
      {format_melody(melody)}
    }}
    \\layout {{
      indent = 0\\mm
      ragged-right = ##f
      \\context {{
        \\Score
        \\remove "Bar_number_engraver"
      }}
    }}
}}


"""

    with open(f'compound_simple_time/temp/score_{name}.ly', 'w') as f:
        f.write(lilypond_score)

    # Generate PNG image and MIDI file
    proc = await asyncio.create_subprocess_exec(
        'lilypond', '-dpreview', '-dbackend=eps', '--png', '-dresolution=300',
       f'--output=compound_simple_time/static/score_{name}', f'compound_simple_time/temp/score_{name}.ly'
    )
    await proc.wait()
    with Image.open(f'compound_simple_time/static/score_{name}.png') as img:
        width, height = img.size
        crop_height = height
        crop_rectangle = (0, 75, width, crop_height / 10)
        cropped_img = img.crop(crop_rectangle)

        cropped_img.save(f'compound_simple_time/static/cropped_score_{name}.png')
    return f'compound_simple_time/static/cropped_score_{name}.png'

async def score_generation(question_data):
    tasks = []
    tasks.append(asyncio.create_task(lilypond_generation(question_data['melody'][1], 'question_melody', question_data['melody'][0][0], question_data['melody'][0][1])))
    for idx, option in enumerate(question_data['options']):
        tasks.append(asyncio.create_task(lilypond_generation(option[1], f'wr_option_{idx}', option[0][0], option[0][1])))

    await asyncio.gather(*tasks)
