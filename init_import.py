from instrument_knowledge_quiz.music_quiz import knowledgemain
from compound_simple_time.main import compound_simple_main
from interval.interval_quiz import interval_main
from melody_key.find_key_main import melody_key_main
from pitch_id.ranged_id import pitch_main
from melody_key.chord_progression.main import chord_progression_main
from inversion.main_iv import main_inversion
from duration_equation.cal_main import duration_cal_main
from duration_equation.time_main import main_ts
from chromatic_scale.chromatic_main import chr_main
from urls import fun_emoji_list,button_style
from transposing.app import transposing_main
from clef_minor.clef_minor_main import clef_main
from same_pitch_different_clef.same_pitch import main_sp
from create_ac import sign_up
from data_func import login_form
from grouping_quiz.needle_main import grouping_quiz_main
import os
from pymongo import MongoClient
from data_func import login_form
#from main_app import intro
import time
import random
from aigreeting import get_mistral_analysis, get_feedback
from datetime import datetime, timedelta
import streamlit as st
import json
from note_story.main_story import story_main
from interval.main_calculator import in_calculator_main
from clef_minor.main_findkey import find_key_main

# Add this line near the other session state initialization
ss = st.session_state
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017')
DB_NAME = 'users'

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
users_collection = db['login']

def test_db_connection():
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        users_collection = db['login']
        # Try to insert a test document
        test_doc = {"test": "connection"}
        result = users_collection.insert_one(test_doc)
        # If successful, delete the test document
        users_collection.delete_one({"_id": result.inserted_id})
        print("Database connection and insertion test successful!")
    except Exception as e:
        print(f"Database connection or insertion failed: {e}")

@st.cache_resource
def init_connection():
    return MongoClient(MONGO_URI)

def get_database():
    client = init_connection()
    return client[DB_NAME]
test_db_connection()

def login_greeting():
    db = get_database()
    users_collection = db['login']

    if "logged" not in ss:
        ss.logged = False
    if "last_ai_greeting" not in ss:
        ss.last_ai_greeting = None
    if "ai_feedback" not in ss:
        ss.ai_feedback = None

    if not ss.logged:
        st.warning("You are not logged in")
    elif ss.logged:
        user = ss.user_info['user_name']
        st.success(f"Hi, {user}")
        current_time = datetime.now()
        if ss.last_ai_greeting is None or (current_time - ss.last_ai_greeting) > timedelta(minutes=1):
            show_aifeedback = st.button("Get your AI feedback:")
            if show_aifeedback:
                with st.spinner("Loading..."):
                    feedback_record = get_feedback(userid=ss.user_info['user_id'])
                    print(feedback_record)
                    results = []
                    for record in feedback_record:
                        date = record['date'].strftime('%m-%d')
                        subject = record['subject']
                        details = record['details']
                        results.append({
                            'date': date,
                            'subject': subject,
                            'result': details
                        })
                    
                    ai_analysis = get_mistral_analysis(results)
                    try:
                        ss.ai_feedback = ai_analysis
                        ss.last_ai_greeting = current_time
                    except Exception as e:
                        print(f"Error: {e}")
                        st.warning("AI review is not available.")
                        
        if ss.ai_feedback:
            with st.expander("AI Feedback", expanded=True):
                st.info(ss.ai_feedback)
        

def back_home():
    if st.button("Home"):
        st.session_state.demo_name = "—"
        st.rerun()
