import os
import subprocess
import uuid
from PIL import Image
def lilypond_score_uid(data, melody):
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
\\language "english"
\\paper {{
  #(set-global-staff-size 32)
}}
\\score {{
  \\new Staff {{
    \\omit Stem
    \\clef {clef}
    \\fixed {fix_pitch} {{
      \\omit TimeSignature
      \\omit Score.BarLine
      \\omit Score.TimeSignature
      \\override Staff.Clef.color = #white
      \\override Staff.Clef.layer = #-1
      {str_melody}
    }}
  }}
  \\layout {{}}
}}
"""

    with open(temp_ly_file, "w") as file:
        file.write(lilypond)

    output_png = None
    cropped_png = None

    try:
        subprocess.run(["lilypond", "--png", f"--output={temp_output_file}", temp_ly_file], check=True)
        output_png = f"{temp_output_file}.png"
        cropped_png = f"{file_name}.png"
        
        # Crop the image using Pillow
        image = Image.open(output_png)
        # Define the box to crop the image (left, upper, right, lower)
        box = (125, 20, image.width//2.5, image.height//12)  # Adjust these values as needed
        cropped_image = image.crop(box)
        cropped_image.save(cropped_png)

        print(f"Score image saved as '{cropped_png}'")
    except subprocess.CalledProcessError as e:
        print(f"Error running LilyPond: {e}")
    except FileNotFoundError:
        print("LilyPond is not installed or not found in the system PATH.")
    finally:
        # Clean up temporary files
        if os.path.exists(temp_ly_file):
            os.remove(temp_ly_file)
        if output_png and os.path.exists(output_png):
            os.remove(output_png)

def display_note(note="af"):
    if len(note)==2:
        match note[1]:
            case "f":
                return note[0].upper()+"-flat"
            case "s":
                return note[0].upper()+"-sharp"
            case _:
                return note
    else:
        return note.upper()
print(display_note("g"))
# Example usage
"""data = ["c'", "score_cm", "treble"]
melody = ['a', 'b', "c'", "d'", "e'", "f'", "gs'", "a'"]
lilypond_score_uid(data, melody)"""
