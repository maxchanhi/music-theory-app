from rhythm_generation.grouping_quiz.main import grouping_quiz_main
from instrument_knowledge_quiz import knowledgemain
from compound_simple_time.main import compound_simple_main
from interval.interval_quiz import interval_main
from melody_key.find_key_main import melody_key_main
from pitch_id.id import pitch_main
from melody_key.chord_progression.main import chord_progression_main
from main_app import intro,main
import streamlit as st

    
page_names_to_funcs = {
    "—": intro,
    "Grouping and beaming": grouping_quiz_main,"Simple-compound Modulation": compound_simple_main,
    "Pitch Identification": pitch_main,"Interval": interval_main,
    "Identifying Key in a Melody": melody_key_main,"Chord Progression": chord_progression_main,
    "Instrumental Knowledge": knowledge_main,
}
