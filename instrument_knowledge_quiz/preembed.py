import time

import streamlit as st
from langchain_community.embeddings import OpenAIEmbeddings

def rag_feedback(student_result):
    from langchain_community.vectorstores import FAISS
    from langchain.prompts import ChatPromptTemplate
    from langchain_openai import ChatOpenAI

    INDEX_PATH = "instrument_knowledge_quiz/faiss_index"
    OPENAI_API_KEY = st.secrets["OpenAI_key"]

    # Create an Embeddings object
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    
    # Load the precomputed FAISS index from disk with the embeddings object
    db_faiss = FAISS.load_local(INDEX_PATH, embeddings=embeddings, allow_dangerous_deserialization=True)
    print("Getting knowledge at database.")
    docs_faiss = db_faiss.similarity_search(student_result, k=1)

    # Generate an answer based on given user query and retrieved context information
    context_text = "\n\n".join([doc.page_content for doc in docs_faiss])

    # Load retrieved context and user query in the prompt template
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

    # Call LLM model to generate the feedback based on the given context and student result
    model = ChatOpenAI(openai_api_key=OPENAI_API_KEY)
    feedback = model.predict(prompt)
    return feedback

def rag_chat(student_result):
    from langchain_community.vectorstores import FAISS
    from langchain.prompts import ChatPromptTemplate
    from langchain_openai import ChatOpenAI

    INDEX_PATH = "instrument_knowledge_quiz/faiss_index"
    OPENAI_API_KEY = st.secrets["OpenAI_key"]

    # Create an Embeddings object
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    
    # Load the precomputed FAISS index from disk with the embeddings object
    db_faiss = FAISS.load_local(INDEX_PATH, embeddings=embeddings, allow_dangerous_deserialization=True)
    context_text = db_faiss.similarity_search(student_result, k=1)

    # Generate an answer based on given user query and retrieved context information
    #context_text = "\n\n".join([doc.page_content for doc in docs_faiss])
    print("context_text:",context_text)
    # Load retrieved context and user query in the prompt template
    PROMPT_TEMPLATE = """
    Answer questions about music theory based on the given context to the student:
    {context}
    Student's question: {student_result}
    Do not say "according to the context" or "mentioned in the context" or similar.
    Feedback:
    """
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, student_result=student_result)

    # Call LLM model to generate the feedback based on the given context and student result
    model = ChatOpenAI(openai_api_key=OPENAI_API_KEY)
    feedback = model.predict(prompt)
    return feedback

def login_for_feedback():
    pw = st.secrets["Password"]

    if "login" not in st.session_state:
        st.session_state["login"] = False
        st.session_state["pw"] = ""

    def login_button_clicked():
        if st.session_state["pw"] in pw:
            st.session_state["login"] = True
        elif st.session_state["pw"] not in pw and st.session_state["pw"] is not None:
            st.error("Wrong password")
        else:
            st.warning("Please enter your password")

    if st.session_state["login"] == False:
        with st.expander(label="Login"):
            st.session_state["pw"] = st.text_area("Password")
            st.button("OK", on_click=login_button_clicked)
    elif st.session_state["login"]:
        st.write("You are logged in!")

    if st.session_state["login"]:
        with st.expander("Chat with AI"):
            prompt = st.text_input("Ask me anything you want to know about music theory:")
            if prompt:
                with st.spinner("Generating..."):
                    feedback = rag_chat(prompt)
                st.write(f"User: {prompt}")
                st.write(f"AI: {feedback}")
                time.sleep(5)
