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
