# FAISS retrieval logic

# retriever.py

import faiss
import numpy as np
import os
from config import FAISS_INDEX_PATH

def build_faiss_index(embeddings):
    """Create and return FAISS index from embeddings."""
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
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
    """Return distances and indices of top_k similar embeddings."""
    distances, indices = index.search(query_embedding, top_k)
    return distances[0], indices[0]