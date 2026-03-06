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


# Load existing FAISS index if available; otherwise encode paragraphs using DPR,
# build a new FAISS index from their embeddings, and save it for future use.
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
st.title("RAG: Manufacturing Assistant")
st.markdown("Ask a question and get answers from your company policies knowledge base.")

question = st.text_input("❓ Your Question")

model_choice = st.selectbox("Select Answering Model", ["gpt2", "bart"])

if question:
    # Encode the user’s question using DPR question encoder
    q_embedding = encode_question(question)

    # Perform similarity search in FAISS index to get top matching paragraph(s)
    _, top_indices = search(index, q_embedding)

    # Retrieve the top matching paragraph (context) based on similarity
    top_contexts = [paragraphs[i] for i in top_indices]  # Extract all top-k contexts
    top_context = " ".join(top_contexts)  # Combine them into a single string for generation
    st.subheader("Retrieved Context")
    st.write(top_context)

    # Generate a natural-language answer using the selected model (GPT-2 or BART)
    st.subheader("Answer")
    answer = generate_answer(question, top_context, model_type=model_choice)
    st.write(answer)
