# Main app

# app.py

import streamlit as st
from utils import load_paragraphs
from encoder import encode_paragraphs, encode_question
from retriever import build_faiss_index, search, load_faiss_index, save_faiss_index
from generator import generate_answer
from config import KB_PATH, FAISS_INDEX_PATH

import os
import numpy as np

# Load knowledge base
paragraphs = load_paragraphs(KB_PATH)
if not paragraphs:
    st.error("❗ knowledge_base.txt is empty or missing. Please add content and restart.")
    st.stop()


# Load or build FAISS index
if os.path.exists(FAISS_INDEX_PATH):
    index = load_faiss_index()
    st.sidebar.success("FAISS index loaded from file.")
else:
    st.sidebar.info("Encoding paragraphs and building FAISS index...")
    ctx_embeddings = encode_paragraphs(paragraphs)
    index = build_faiss_index(ctx_embeddings)
    save_faiss_index(index)
    st.sidebar.success("FAISS index built and saved.")

# Streamlit UI
st.title("🧠 Streamlit RAG: Company Policy Assistant")
st.markdown("Ask a question and get answers from your company policies knowledge base.")

question = st.text_input("❓ Your Question")

model_choice = st.selectbox("Select Answering Model", ["gpt2", "bart"])

if question:
    q_embedding = encode_question(question)
    _, top_indices = search(index, q_embedding)

    top_context = paragraphs[top_indices[0]]
    st.subheader("🔎 Retrieved Context")
    st.write(top_context)

    st.subheader("💬 Answer")
    answer = generate_answer(question, top_context, model_type=model_choice)
    st.write(answer)
