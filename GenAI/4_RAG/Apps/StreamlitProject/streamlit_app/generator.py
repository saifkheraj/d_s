# GPT-2 / BART generation

# generator.py

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BartTokenizer,
    BartForConditionalGeneration
)
from config import GPT2, BART
import torch

def generate_answer(question, context, model_type="gpt2"):
    """Generate answer from context and question using the specified model."""
    
    if model_type == "gpt2":
        prompt = f"Context: {context}\n\nQuestion: {question}\nAnswer:"
        tokenizer = AutoTokenizer.from_pretrained(GPT2)
        model = AutoModelForCausalLM.from_pretrained(GPT2)
    elif model_type == "bart":
        prompt = f"question: {question} context: {context}"
        tokenizer = BartTokenizer.from_pretrained(BART)
        model = BartForConditionalGeneration.from_pretrained(BART)
    else:
        raise ValueError("Model must be 'gpt2' or 'bart'.")

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)

    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=50)

    return tokenizer.decode(outputs[0], skip_special_tokens=True)
