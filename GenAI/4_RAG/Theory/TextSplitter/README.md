# 📄 LangChain Text Splitters Guide (Detailed Edition)

## 🚀 Overview

In LangChain, **text splitters** help prepare large documents for LLM (Large Language Model) processing by breaking them into smaller, manageable pieces (called chunks). This is important because LLMs like GPT have context limits—they can only read a certain amount of text at a time.

By using splitters, we ensure:

* Text fits inside the model’s limit.
* Related text stays together (preserving meaning).
* Better performance in retrieval and generation tasks.

---

## 📚 Workflow Summary

1. **Load** the documents using a document loader.
2. **Split/Transform** the documents using a splitter.
3. **Use** the chunks in downstream LLM tasks like RAG (Retrieval-Augmented Generation), summarization, or QA.

---

## ⚙️ How Splitters Work: Two Key Dimensions

### 1. **Splitting Method** – How the text is broken apart

* By **character** (e.g., spaces, newlines)
* By **words**
* By **sentences**
* By **paragraphs**
* Or using **custom separators**

### 2. **Chunk Measurement** – How the size of each chunk is calculated

* Number of **characters**
* Number of **words**
* Number of **tokens** (common with transformer models)

---

## 🔑 Core Parameters of a Text Splitter

| Parameter         | Description                                                                  |
| ----------------- | ---------------------------------------------------------------------------- |
| `separator`       | The character or string used to divide the text. Examples: `\n`, space, etc. |
| `chunk_size`      | Maximum size of a chunk (in characters by default).                          |
| `chunk_overlap`   | Number of characters that should overlap between adjacent chunks.            |
| `length_function` | Function used to measure the chunk's length (like `len()` or token count).   |

---

## 🔨 Types of Text Splitters (With Examples)

### 🧱 1. **Character Text Splitter**

* Simplest method: splits based on a fixed separator (like `\n`, space, or dot).
* Best for predictable structures (e.g., paragraphs).

```python
from langchain.text_splitter import CharacterTextSplitter

splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=200,
    chunk_overlap=20
)
chunks = splitter.split_text(my_text)
```

* This breaks `my_text` into pieces of 200 characters each.
* 20 characters from the end of one chunk appear at the start of the next one (to preserve context).

---

### 🔁 2. **Recursive Character Text Splitter** (Most Useful!)

* **Smart** splitter that tries to preserve semantic structure.
* First, it tries splitting by big units (like paragraphs).
* If chunks are still too big, it goes one level smaller (like sentences), and so on.

#### 🧠 How It Works:

1. Start with the full document.
2. Try to split by `\n\n` (paragraph breaks).
3. If any chunk > `chunk_size`, split that chunk by sentence (`. `).
4. Still too big? Try splitting by space or character.
5. Combine as many small pieces as possible while staying under the `chunk_size`.
6. Add overlap between chunks (if `chunk_overlap` is set).

#### Code Example:

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20
)
chunks = splitter.split_text(my_text)
```

* Good default choice for unstructured text like blogs, essays, and webpages.

---

### 💻 3. **Code Text Splitter** (For Programming Code)

* Based on recursive splitting, but understands code structure like functions, classes, etc.
* Avoids splitting in the middle of a function.

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter, Language

splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON,
    chunk_size=120,
    chunk_overlap=10
)
chunks = splitter.split_text(code_snippet)
```

* Supported languages: Python, JavaScript, Java, C++, and more.

---

### 📝 4. **Markdown Header Text Splitter** (For Markdown Files)

* Splits text based on header levels (`#`, `##`, `###`, etc.).
* Keeps all the content under a header grouped together.
* Useful for documentation, blog posts, etc.

```python
from langchain.text_splitter import MarkdownHeaderTextSplitter

splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=[("#", "H1"), ("##", "H2"), ("###", "H3")]
)
chunks = splitter.split_text(markdown_content)
```

---

## 📌 Summary Table

| Splitter Type                  | Best Use Case                        | Smart Splitting? | Respects Structure? |
| ------------------------------ | ------------------------------------ | ---------------- | ------------------- |
| CharacterTextSplitter          | Simple structured data (logs, lists) | ❌                | ❌                   |
| RecursiveCharacterTextSplitter | General text (articles, essays)      | ✅                | ✅                   |
| CodeTextSplitter               | Python, Java, etc.                   | ✅                | ✅                   |
| MarkdownHeaderTextSplitter     | Markdown docs, blogs                 | ✅                | ✅                   |

---

## 🔚 Final Thoughts

* Always use `RecursiveCharacterTextSplitter` as a **default** for general use.
* Use overlapping chunks when your task requires **context continuity**.
* Markdown and Code splitters are powerful when working with structured data.
* Adjust `chunk_size` and `chunk_overlap` based on your **LLM’s context window** and your **task needs**.

---

## 🧪 Try This

Create your own splitter in LangChain:

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

text = """
# Introduction
LangChain is a framework for building LLM applications.

## Components
- Loaders
- Splitters
- Chains

### Loaders
Load documents into LangChain.

### Splitters
Break documents into chunks.
"""

splitter = RecursiveCharacterTextSplitter(chunk_size=80, chunk_overlap=10)
chunks = splitter.split_text(text)
for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1}:\n{chunk}\n")
```

---

If you still have doubts or want a visual example of how the splitting works, I can generate a diagram or simulation next.


# README.md - Comprehensive Explanation for `text_splitter.ipynb`

## Overview

This notebook provides a hands-on demonstration of multiple text splitting techniques available in LangChain. It showcases how to process a variety of document types and segment large texts into manageable chunks for downstream applications like search, RAG (Retrieval-Augmented Generation), summarization, or Q\&A systems.

---

## 🔧 Dependencies

* `langchain`
* `nltk`
* `spacy`
* `PyMuPDF` or `pdfminer.six`
* `tiktoken` or `transformers`
* `beautifulsoup4` (for HTML parsing)
* `markdown`

---

## 📂 Document Loaders Covered

These are used to ingest different file formats:

### 1. **TextLoader**

* Loads `.txt` files.

### 2. **PyPDFLoader / PDFMinerLoader**

* Used for `.pdf` files.
* Extracts raw text while preserving paragraph breaks.

### 3. **UnstructuredHTMLLoader / BSHTMLLoader**

* Loads `.html` or `.htm` files.
* Strips HTML tags while preserving logical content structure.

### 4. **CSVLoader**

* Loads `.csv` files as structured tables.
* Optionally extracts row-wise or column-wise text.

### 5. **UnstructuredMarkdownLoader / MarkdownLoader**

* Parses `.md` files.
* Maintains headers, lists, and markdown structure.

### 6. **DocxLoader**

* Loads `.docx` files using `python-docx`.
* Extracts paragraph-based text.

### 7. **EPubLoader** *(Optional)*

* For `.epub` ebooks. Extracts full text.

---

## ✂️ Text Splitters Explained

These tools divide large documents into smaller, manageable chunks:

### 1. **CharacterTextSplitter**

* Naïvely splits text by character count.
* Parameters: `chunk_size`, `chunk_overlap`.

### 2. **RecursiveCharacterTextSplitter**

* Tries splitting using newlines, sentences, then words.
* Preserves semantic boundaries better than naive splitters.

### 3. **NLTKTextSplitter**

* Uses NLTK sentence tokenizer.
* Good for grammar-sensitive content.

### 4. **SpacyTextSplitter**

* Uses SpaCy's NLP pipeline to split based on sentences and token limits.

### 5. **MarkdownHeaderTextSplitter**

* Splits markdown files by headers (e.g., `#`, `##`, etc.).
* Great for tech docs, README files, structured notes.

### 6. **TokenTextSplitter**

* Uses tokenizers (like GPT's) to split text according to token count.
* Ensures chunks align with LLM input limits.

### 7. **LanguageAwareSplitter (Experimental)**

* Chooses splitting rules based on language model estimates (e.g., BERT).

---

## 📊 Sample Flow

1. Load document using appropriate loader.
2. Choose and configure a text splitter.
3. Apply the splitter to the loaded document.
4. View the number of resulting chunks.
5. Optionally visualize or inspect a few chunks.

---

## 🎯 Use Cases

* RAG (Retrieval-Augmented Generation)
* Document summarization
* Fine-tuning models on chunked data
* Searchable knowledge bases
* Legal and medical document parsing

---

## 🧠 Tips

* For structured files (e.g., Markdown or HTML), prefer semantic-aware splitters.
* Use `chunk_overlap` > 0 when you need context carry-over between chunks.
* For LLMs, ensure `chunk_size` < model token limit (e.g., 2048 for GPT-2, \~8000 for GPT-4).

---

## ✅ Conclusion

This notebook is a flexible playground for exploring LangChain’s document preprocessing capabilities across multiple file formats. It enables better preparation of input data for modern LLMs by breaking content into meaningful and manageable chunks.

If you want an automated pipeline, you can combine:

* `Loader` → `Splitter` → `Embedder` → `Vector Store` → `LLM/RAG`

Each component in this notebook is modular and can be adapted for different use cases or pipelines.



