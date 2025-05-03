# FAISS retrieval logic

# retriever.py

import faiss
import numpy as np
import os
from config import FAISS_INDEX_PATH

def build_faiss_index(embeddings):
    """Create and return FAISS index from embeddings."""
    dim = embeddings.shape[1]
    # Normalize embeddings before adding to index
    embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)

    index = faiss.IndexFlatIP(dim)  # IP = Inner Product (acts as cosine sim if vectors are normalized)
    index.add(embeddings.astype('float32'))

    return index

def save_faiss_index(index, path=FAISS_INDEX_PATH):
    faiss.write_index(index, path)

def load_faiss_index(path=FAISS_INDEX_PATH):
    if os.path.exists(path):
        return faiss.read_index(path)
    else:
        return None

def search(index, query_embedding, top_k=3):
    # Normalize query embedding before cosine similarity search
    query_embedding = query_embedding / np.linalg.norm(query_embedding, axis=1, keepdims=True)
    distances, indices = index.search(query_embedding.astype('float32'), top_k)
    return distances[0], indices[0]
