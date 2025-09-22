from openai import OpenAI
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
api_key= os.getenv("DeepseekAPI_key")
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")


def provide_feedback(student_result,token=64):
    prompt = f"Please provide feedback on the following music theory result:\n\n{student_result}\n\nFeedback:"

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a music theory teacher providing feedback to a student. Don't explain the answer since there is another modal doing such job."},
            {"role": "user", "content": prompt}
        ],
        temperature=1,
        max_tokens=token,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    feedback = response.choices[0].message.content+"..."
    return feedback
