import random
from data import instrument_clef,instrument_reeds,piano,orniment_url,playing_technique, impossiable_technique,instrumental_families
def generate_options(correct,ava_options=list):
    options = [correct]
    while len(options) < 4:
        # Randomly select a reed type to add as an option
        option = random.choice(ava_options)
        # Ensure no duplicates in the options
        if option not in options:
            options.append(option)
    random.shuffle(options)
    return options
def reed():
    all_reed_types = ["headjoint (non-reed)", "single reed", "double reed", "mouthpiece"]
    instrument, correct_reed_type = random.choice(list(instrument_reeds.items()))
    options = [correct_reed_type]
    while len(options) < 4:
        # Randomly select a reed type to add as an option
        option = random.choice(all_reed_types)
        # Ensure no duplicates in the options
        if option not in options:
            options.append(option)
    random.shuffle(options)
    
    # Create the question
    question = f"How does a {instrument} produce sound?"
    question_data = {
        "question": question,
        "options": options,
        "answer": correct_reed_type
    }
    
    return question_data

def transposing():
    transposing_instruments = ["piccolo","clarinet","B-flat trumpet","horn","double bass","cor anglais"]
    concert_pitch_instruments = ["flute","oboe","bassoon","trombone","tuba","violin","viola","cello"]
    # Randomly select 4 instruments, 1 from 1 list, 3 from another list
    both_list =[transposing_instruments,concert_pitch_instruments]
    correct_list = random.choice(both_list)
    correct_ans = random.choice(correct_list)
    options = [correct_ans]
    false_list = [el for el in both_list if el != correct_list]
    while len(options) < 4:
        option = random.choice(false_list[0])
        if option not in options:
            options.append(option)
    random.shuffle(options)
    if correct_list == transposing_instruments:
        transposing_ins = "transposing instrument"
    elif correct_list == concert_pitch_instruments:
        transposing_ins = "in concert pitch"
    question = f"Which one is {transposing_ins} ?"
    question_data = {
        "question": question,
        "options": options,
        "answer": correct_ans
    }
    
    return question_data

def clef():
    
    all_clef = set(instrument_clef.values())
    all_clef = list(all_clef)
    # Randomly select one instrument
    instrument, use_clef = random.choice(list(instrument_clef.items()))
    options= generate_options(use_clef,all_clef)
    question = f"What clef(s) does a {instrument} use?"
    question_data = {
        "question": question,
        "options": options,
        "answer": use_clef
    }
    return question_data
male_voices = ["Bass","Baritone","Tenor"]
female_voices = ["Alto","Mezzo-soprano","Soprano"]
gender_lists = [male_voices, female_voices]
def random_pick(lists=[]):
    lists = random.choice(lists) 
    voice = random.choice(lists)
    return voice

def voice_high_low_options():
    wrong_list = []
    correct_answer = None

    while len(wrong_list) < 3 or not correct_answer:
        voice_1 = random_pick(gender_lists)
        voice_2 = random_pick(gender_lists)

        if voice_1 == voice_2:
            continue  # Skip if both picks are the same

        statement = f"{voice_1} is higher than {voice_2}."

        # Determine if the statement is correct or wrong
        if voice_1 in female_voices and voice_2 in male_voices:
            if not correct_answer:
                correct_answer = statement
            continue

        elif voice_1 in male_voices and voice_2 in female_voices:
            if statement not in wrong_list and len(wrong_list) < 3:
                wrong_list.append(statement)
            continue

        index_1 = male_voices.index(voice_1) if voice_1 in male_voices else female_voices.index(voice_1)
        index_2 = male_voices.index(voice_2) if voice_2 in male_voices else female_voices.index(voice_2)

        if index_1 > index_2:
            if not correct_answer:
                correct_answer = statement
        else:
            if statement not in wrong_list and len(wrong_list) < 3:
                wrong_list.append(statement)

    # Ensure unique options and a correct answer
    if correct_answer in wrong_list or len(set(wrong_list)) < 3:
        print("Regenerating options...")
        return voice_high_low_options()  # Recursively call function to regenerate

    return wrong_list, correct_answer

def voice_types():
    choosen_topic_list = random.choices(["gender_voice", "voice_range"], weights=[3, 7], k=1)
    choosen_topic = choosen_topic_list[0]    #choosen_topic = random.choice(["gender_voice" ,"voice_range"])
    options = []
    if choosen_topic == "gender_voice":
        correct_list = random.choice(gender_lists)  # Randomly select which list to pick the correct answer from
        correct_answer = random.choice(correct_list)  # Select the correct answer from the chosen list
        false_list = [lst for lst in gender_lists if lst != correct_list] 
        options = [correct_answer]
        while len(options) < 4:
            option = random.choice(false_list[0])  # Pick voice types from the other list
            if option not in options:
                options.append(option)
        if correct_list == male_voices:
            voice_type = "a male voice type"
        elif correct_list == female_voices:
            voice_type = "a female voice type"
        question = f"Which one is {voice_type}?"
    elif choosen_topic == "voice_range":
        options,correct_answer = voice_high_low_options()
        options.append(correct_answer)
        print(options,correct_answer)
        question = "Which statement is correct?"
    
    random.shuffle(options)  # Shuffle the options to randomize their order in the quiz
    
    question_data = {
        "question": question,
        "options": options,
        "answer": correct_answer
    }
    return question_data

def piano_knowledge():
    all_key = []
    all_options = []
    for key, value in piano.items():
        all_options.append(value)
        all_key.append(key)
    # randomly pick an item in piano
    correct_question = random.choice(all_key)
    correct_answer = piano[correct_question]
    options=[correct_answer]
    while len(options) < 4:
        option = random.choice(all_options)
        if option not in options:
            options.append(option)
    random.shuffle(options)
    question = f"What does {correct_question} mean?"
    question_data = {
        "question": question,
        "options": options,
        "answer": correct_answer
    }
    return question_data

def orniments():
    all_url = []
    all_options = []
    for key, value in orniment_url.items():
        all_url.append(key)
        all_options.append(value)
        
    all_options= list(set(all_options))
    # randomly pick an item in piano
    correct_question_url = random.choice(all_url)
    correct_answer = orniment_url[correct_question_url]
    options=[correct_answer]
    while len(options) < 4:
        option = random.choice(all_options)
        if option not in options:
            options.append(option)
    random.shuffle(options)
    question = f"What is this ornament?"

    question_data = {
        "question": question,
        "pic_url": "static/"+correct_question_url,
        "options": options,
        "answer": correct_answer
    }
    return question_data

def instrumental_technique():
    all_families = []
    all_options = []
    for key, value in playing_technique.items():
        all_families.append(key)
        all_options.append(value)
    correct_family = random.choice(all_families)
    instrument = random.choice(instrumental_families[correct_family])
    this_technique = random.choice(playing_technique[correct_family])
    correct_option = f"A {instrument} can perform {this_technique}."
    options = [] 
    while len(options) < 4:
        wrong_family = random.choice(all_families)
        wrong_instrument = random.choice(instrumental_families[wrong_family])
        wrong_technique = random.choice(impossiable_technique[wrong_family])
        wrong_option = f"A {wrong_instrument} can perform {wrong_technique}."
        if wrong_option not in options:
            options.append(wrong_option)
    options.append(correct_option)
    random.shuffle(options)
    question = "Which statement is correct?"
    question_data = {
        "question": question,
        "options": options,
        "answer": correct_option
    }
    return question_data