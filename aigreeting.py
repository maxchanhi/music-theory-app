from data_func import get_feedback
from datetime import datetime
import json
import streamlit as st

from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

# Get the API key from environment variables
MISTRAL_API_KEY = st.secrets["MISTRAL_API_KEY"]

def get_mistral_analysis(results):
    client = MistralClient(api_key=MISTRAL_API_KEY)
    model = "mistral-large-latest"

    # Prepare the message for Mistral AI
    message_content = f"""You are a music teacher that review student's results:\n\n{json.dumps(results, indent=2)}. 
    If it is empty, just encourage him to start. If the student is struggling with certain subject, encourage him to practice the related test.
    If he has good result, enencourage him to practice other subjects.\n
    Here is a list of subjects:\n 
    Grouping and beaming, Duration calculation, Simple-compound Modulation, Calculation for time signature\n
    Pitch Identification, Chromatic scale, Same pitches with different clefs, Interval, Transposing\n
    Identifying Key in a Melody, Chord Inversion, Chord Progression, Identify clef from minor scale\n
    Instrumental Knowledge\n
    Give him a short feedback around 100 words
    """
    messages = [ChatMessage(role="user", content=message_content)]

    try:
        chat_response = client.chat(model=model, messages=messages)
        return chat_response.choices[0].message.content
    except Exception as e:
        print(f"An error occurred while contacting Mistral AI: {e}")
        return None



