# DPR encoding logic
# encoder.py

from transformers import DPRContextEncoder, DPRContextEncoderTokenizer
from transformers import DPRQuestionEncoder, DPRQuestionEncoderTokenizer
import torch
from config import DPR_CTX_ENCODER, DPR_Q_ENCODER

# Load pretrained Dense Passage Retrieval (DPR) context encoder and tokenizer
ctx_tokenizer = DPRContextEncoderTokenizer.from_pretrained(DPR_CTX_ENCODER)
ctx_encoder = DPRContextEncoder.from_pretrained(DPR_CTX_ENCODER)

# Load pretrained DPR question encoder and tokenizer
q_tokenizer = DPRQuestionEncoderTokenizer.from_pretrained(DPR_Q_ENCODER)
q_encoder = DPRQuestionEncoder.from_pretrained(DPR_Q_ENCODER)

def encode_paragraphs(paragraphs):
    """
    Encode a list of paragraphs into dense vector embeddings using DPR context encoder.

    Args:
        paragraphs (list of str): The text chunks to be encoded.
    
    Returns:
        numpy.ndarray: Array of shape (num_paragraphs, 768) containing dense embeddings.
    """
    embeddings = []
    for text in paragraphs:
        # Tokenize each paragraph (with padding/truncation)
        inputs = ctx_tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=256)
        
        # Disable gradient tracking for inference
        with torch.no_grad():
            outputs = ctx_encoder(**inputs)
        
        # Get [CLS] token embedding and normalize it
        embedding = outputs.pooler_output  # shape: (1, 768)
        embedding = embedding / embedding.norm(dim=1, keepdim=True)
        
        # Append normalized embedding
        embeddings.append(embedding)

    # Concatenate all paragraph embeddings into a single numpy array
    return torch.cat(embeddings).cpu().numpy()

def encode_question(question):
    """
    Encode a single user question into a dense vector using DPR question encoder.

    Args:
        question (str): User's natural language query.
    
    Returns:
        numpy.ndarray: Array of shape (1, 768) representing the question embedding.
    """
    # Tokenize the question
    inputs = q_tokenizer(question, return_tensors='pt')
    with torch.no_grad():
        outputs = q_encoder(**inputs)
    embedding = outputs.pooler_output
    embedding = embedding / embedding.norm(dim=1, keepdim=True)
    return embedding.cpu().numpy()

