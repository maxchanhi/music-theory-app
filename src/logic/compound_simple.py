import random
PITCH_LIST = ["e", "f", "g", "a", "b"]

RHYTHM_SETTING = {
    "simple": ["4", "8 8", "\\tuplet 3/2 {8 8 8}",  # this list each item is one beat
            "\\tuplet 3/2 {4 8}", "\\tuplet 3/2 {8 4}", "8. 16"],
    "compound": ["4.", "\\tuplet 2/3 {8 8}", "8 8 8", # this list each item is 1.5 beat
            "4 8", "8 4", "\\tuplet 2/3 {8. 16}"]
}

TIME_SIGN_CAT = { #(time sign, total of beat value)
    "simple duple": [("2/2",4), ("2/4",2), ("2/8",1)],
    "simple triple": [("3/2",6), ("3/4",3), ("3/8",1.5)],
    "simple quadruple": [("4/4",4), ("4/2",8), ("4/8",2)],
    "compound duple": [("6/2",6), ("6/4",3), ("6/8",1.5), ("6/16",0.75)],
    "compound triple": [ ("9/4",4.5), ("9/8",2.25)],
    "compound quadruple": [("12/4",6), ("12/8",3)]
}
#1. Pick the time signature category
time_sign_cat, time_sign_list = random.choice(list(TIME_SIGN_CAT.items()))
time_sign = random.choice(time_sign_list)
print(time_sign_cat,time_sign[0])
total_beat = time_sign[1]
print("total_beat", total_beat)
#2. Pick the rhythm setting as the quesiton
melody = []
beat = 0
while beat < total_beat:
    if "simple" in time_sign_cat:
        rhythm = random.choice(RHYTHM_SETTING["simple"])
        melody.append(rhythm)
        beat += 1
    else:
        rhythm = random.choice(RHYTHM_SETTING["compound"])
        melody.append(rhythm)
        beat += 1.5
print(melody)
#3. Generate correct answer
simple_or_compound = "simple" if "simple" in time_sign_cat else "compound" 

# Define target category mapping
cat_type = time_sign_cat.split(" ")[1] # duple, triple, quadruple
target_cat_prefix = "compound" if simple_or_compound == "simple" else "simple"
target_cat = f"{target_cat_prefix} {cat_type}"

# Pick a target time signature
target_time_sign_list = TIME_SIGN_CAT[target_cat]
target_time_sign = random.choice(target_time_sign_list)

print(f"Target category: {target_cat}, Target time signature: {target_time_sign[0]}")

def translate_melody(melody, source_type):
    translated = []
    if source_type == "simple":
        # Simple to Compound
        for rhythm in melody:
            if "tuplet 3/2" in rhythm:
                # \tuplet 3/2 {8 8 8} -> 8 8 8
                content = rhythm.split("{")[1].split("}")[0].strip()
                translated.append(content)
            elif " " not in rhythm and "." not in rhythm:
                # Single note: 4 -> 4.
                translated.append(rhythm + ".")
            else:
                # Multi note: 8 8 -> \tuplet 2/3 {8 8}
                translated.append(f"\\tuplet 2/3 {{ {rhythm} }}")
    else:
        # Compound to Simple
        for rhythm in melody:
            if "tuplet 2/3" in rhythm:
                # \tuplet 2/3 {8 8} -> 8 8
                content = rhythm.split("{")[1].split("}")[0].strip()
                translated.append(content)
            elif " " not in rhythm and "." in rhythm:
                # Single dotted note: 4. -> 4
                translated.append(rhythm.replace(".", ""))
            else:
                # Multi note: 8 8 8 -> \tuplet 3/2 {8 8 8}
                translated.append(f"\\tuplet 3/2 {{ {rhythm} }}")
    return translated

correct_melody_rhythm = translate_melody(melody, simple_or_compound)

# 4. Add random pitches
def add_pitches(rhythm_list):
    pitched_melody = []
    all_assigned_pitches = []
    for segment in rhythm_list:
        if "tuplet" in segment:
            prefix = segment.split("{")[0]
            content = segment.split("{")[1].split("}")[0].strip()
            notes = content.split(" ")
            pitched_notes = []
            for n in notes:
                p = random.choice(PITCH_LIST)
                pitched_notes.append(p + n)
                all_assigned_pitches.append(p)
            pitched_melody.append(f"{prefix}{{ {' '.join(pitched_notes)} }}")
        else:
            notes = segment.split(" ")
            pitched_notes = []
            for n in notes:
                p = random.choice(PITCH_LIST)
                pitched_notes.append(p + n)
                all_assigned_pitches.append(p)
            pitched_melody.append(" ".join(pitched_notes))
    return pitched_melody, all_assigned_pitches

# Add pitches to original melody
final_question_melody, question_pitches = add_pitches(melody)

# The pitches in the answer and options must match the question's pitches
def apply_pitches_to_rhythm(rhythm_list, pitches):
    pitched_result = []
    pitch_idx = 0
    for segment in rhythm_list:
        if "tuplet" in segment:
            prefix = segment.split("{")[0]
            content = segment.split("{")[1].split("}")[0].strip()
            notes = content.split(" ")
            pitched_notes = []
            for n in notes:
                p = pitches[pitch_idx % len(pitches)]
                pitched_notes.append(p + n)
                pitch_idx += 1
            pitched_result.append(f"{prefix}{{ {' '.join(pitched_notes)} }}")
        else:
            notes = segment.split(" ")
            pitched_notes = []
            for n in notes:
                p = pitches[pitch_idx % len(pitches)]
                pitched_notes.append(p + n)
                pitch_idx += 1
            pitched_result.append(" ".join(pitched_notes))
    return pitched_result

final_correct_melody = apply_pitches_to_rhythm(correct_melody_rhythm, question_pitches)

print("Question Melody:", final_question_melody)
print("Correct Answer Melody:", final_correct_melody)

# 5. Generate wrong options
def generate_wrong_options(original_rhythms, source_type, correct_rhythm_list, pitches, time_sign_cat, total_beat):
    wrongs = []
    
    # New Strategy: If triple time, add an option in duple/quadruple with same total beats
    if "triple" in time_sign_cat:
        # Find a time signature in duple or quadruple with the same total_beat
        candidate_signs = []
        for cat, signs in TIME_SIGN_CAT.items():
            if "duple" in cat or "quadruple" in cat:
                for sign, beat in signs:
                    if beat == total_beat:
                        candidate_signs.append(sign)
        
        if candidate_signs:
            wrong_time = random.choice(candidate_signs)
            # Use original rhythm but with the wrong time signature
            wrongs.append({"time": wrong_time, "melody": apply_pitches_to_rhythm(original_rhythms, pitches), "correct": False})

    # Strategy 1: The original rhythm (no transformation)
    # Using target_time_sign[0] as default for existing strategy logic
    wrongs.append({"time": target_time_sign[0], "melody": apply_pitches_to_rhythm(original_rhythms, pitches), "correct": False})
    
    # Strategy 2: Partially transformed
    if len(original_rhythms) > 1:
        partial = list(original_rhythms)
        partial[0] = correct_rhythm_list[0]
        wrongs.append({"time": target_time_sign[0], "melody": apply_pitches_to_rhythm(partial, pitches), "correct": False})
    else:
        fallback = list(correct_rhythm_list)
        if "4." in fallback[0]: fallback[0] = fallback[0].replace("4.", "2")
        elif "4" in fallback[0]: fallback[0] = fallback[0].replace("4", "2")
        wrongs.append({"time": target_time_sign[0], "melody": apply_pitches_to_rhythm(fallback, pitches), "correct": False})

    # Strategy 3: Incorrect transformation
    incorrect = []
    for r in original_rhythms:
        if " " not in r and "." not in r:
            incorrect.append(r.replace("4", "2"))
        else:
            incorrect.append(r)
    wrongs.append({"time": target_time_sign[0], "melody": apply_pitches_to_rhythm(incorrect, pitches), "correct": False})
    
    return wrongs

# Update the call
wrong_options_data = generate_wrong_options(melody, simple_or_compound, correct_melody_rhythm, question_pitches, time_sign_cat, total_beat)

# Final Output Structure
question_data = {
    "question_time": time_sign[0],
    "question_melody": final_question_melody,
    "options": [
        {"time": target_time_sign[0], "melody": final_correct_melody, "correct": True}
    ]
}

# Add wrong options, ensuring we don't exceed 4 total options and they are unique
for opt in wrong_options_data:
    if len(question_data["options"]) < 4:
        # Check if this exact melody/time combo is already in options
        exists = False
        for existing in question_data["options"]:
            if existing["time"] == opt["time"] and existing["melody"] == opt["melody"]:
                exists = True
                break
        if not exists:
            question_data["options"].append(opt)

# Ensure we have 4 options
while len(question_data["options"]) < 4:
    question_data["options"].append({"time": target_time_sign[0], "melody": apply_pitches_to_rhythm(melody, question_pitches), "correct": False})

# Shuffle options
random.shuffle(question_data["options"])
print("\nFinal Question Data:")
import json
print(json.dumps(question_data, indent=2))





