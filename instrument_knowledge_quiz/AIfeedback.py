from openai import OpenAI
import os
import streamlit as st
api_key= st.secrets["OpenAI_key"]
client = OpenAI(api_key=api_key)


def provide_feedback(student_result,token=64):
    prompt = f"Please provide feedback on the following music theory result:\n\n{student_result}\n\nFeedback:"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a music theory teacher providing feedback to a student."},
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
