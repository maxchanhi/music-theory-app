import time
import streamlit as st
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("DeepseekAPI_key")

def rag_feedback(student_result):
    from langchain_community.vectorstores import FAISS
    from langchain.prompts import ChatPromptTemplate
    from langchain_openai import ChatOpenAI

    INDEX_PATH = "instrument_knowledge_quiz/faiss_index"
    
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    
    db_faiss = FAISS.load_local(INDEX_PATH, embeddings=embeddings, allow_dangerous_deserialization=True)
    
    context_text = db_faiss.similarity_search(student_result, k=1)
    print("Getting knowledge at database.",context_text)

    PROMPT_TEMPLATE = """
    You are a music theory teacher. Please provide feedback according to studnet's music theory result based on the given context:
    {context}
    Music theory result: {student_result}
    Provide short feedback.
    Do not say "according to the context" or "mentioned in the context" or similar.
    Feedback:
    """
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, student_result=student_result)

    model = ChatOpenAI(openai_api_key=OPENAI_API_KEY)
    feedback = model.predict(prompt)
    return feedback

def rag_chat(student_result):
    from langchain_community.vectorstores import FAISS
    from langchain.prompts import ChatPromptTemplate
    from langchain_openai import ChatOpenAI

    INDEX_PATH = "instrument_knowledge_quiz/faiss_index"

    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    
    db_faiss = FAISS.load_local(INDEX_PATH, embeddings=embeddings, allow_dangerous_deserialization=True)
    context_text = db_faiss.similarity_search(student_result, k=1)

    print("context_text:",context_text)
    PROMPT_TEMPLATE = """
    Answer questions about music theory based on the given context to the student:
    {context}
    Student's question: {student_result}
    Do not say "according to the context" or "mentioned in the context" or similar.
    Feedback:
    """
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, student_result=student_result)

    model = ChatOpenAI(openai_api_key=OPENAI_API_KEY)
    feedback = model.predict(prompt)
    return feedback

def login_for_feedback():
    if "login" not in st.session_state:
        st.session_state["login"] = False

    password = os.getenv("Password")
    if not password:
        st.error("Password not configured in .env file.")
        return

    def login_button_clicked():
        if st.session_state["pw"] == password:
            st.session_state["login"] = True
        else:
            st.error("Wrong password")

    if not st.session_state["login"]:
        with st.popover(label="Login to chat with AI"):
            st.session_state["pw"] = st.text_input("Password", type="password")
            st.button("OK", on_click=login_button_clicked)
    
    if st.session_state["login"]:
        st.write("You are logged in!")
        with st.popover("Chat with AI", use_container_width=True):
            prompt = st.chat_input("Ask me anything you want to know about music theory:")
            if prompt:
                with st.spinner("Generating..."):
                    feedback = rag_chat(prompt)
                st.write(f"User: {prompt}")
                st.write(f"AI: {feedback}")
                time.sleep(5)

st.title("Music Knowledge QA System")
login_for_feedback()
st.image(image_path, width='stretch')
