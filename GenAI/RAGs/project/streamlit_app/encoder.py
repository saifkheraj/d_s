# DPR encoding logic
# encoder.py

from transformers import DPRContextEncoder, DPRContextEncoderTokenizer
from transformers import DPRQuestionEncoder, DPRQuestionEncoderTokenizer
import torch
from config import DPR_CTX_ENCODER, DPR_Q_ENCODER

# Load DPR encoders and tokenizers
ctx_tokenizer = DPRContextEncoderTokenizer.from_pretrained(DPR_CTX_ENCODER)
ctx_encoder = DPRContextEncoder.from_pretrained(DPR_CTX_ENCODER)

q_tokenizer = DPRQuestionEncoderTokenizer.from_pretrained(DPR_Q_ENCODER)
q_encoder = DPRQuestionEncoder.from_pretrained(DPR_Q_ENCODER)

def encode_paragraphs(paragraphs):
    """Encode a list of paragraphs using DPR context encoder."""
    embeddings = []
    for text in paragraphs:
        inputs = ctx_tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=256)
        with torch.no_grad():
            outputs = ctx_encoder(**inputs)
        embeddings.append(outputs.pooler_output)
    return torch.cat(embeddings).cpu().numpy()

def encode_question(question):
    """Encode the user's question using DPR question encoder."""
    inputs = q_tokenizer(question, return_tensors='pt')
    with torch.no_grad():
        outputs = q_encoder(**inputs)
    return outputs.pooler_output.cpu().numpy()
