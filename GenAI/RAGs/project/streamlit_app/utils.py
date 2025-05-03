# Helper functions (e.g., load text, chunking)

# utils.py

def load_paragraphs(filepath):
    """Load and clean text file into list of paragraphs."""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
    return paragraphs
