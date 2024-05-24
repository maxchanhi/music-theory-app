import os
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import streamlit as st
DOC_PATH = "knowledge.txt"
INDEX_PATH = "faiss_index"

# Set up OpenAI API key
OPENAI_API_KEY =  st.secrets["OpenAI_key"]

loader = TextLoader(DOC_PATH)
pages = loader.load()

# Split the doc into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = text_splitter.split_documents(pages)

# Get OpenAI Embedding model
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

# Embed the chunks as vectors and load them into the database
db_faiss = FAISS.from_documents(chunks, embeddings)

# Save the FAISS index to disk
db_faiss.save_local(INDEX_PATH)

print("Index created successfull