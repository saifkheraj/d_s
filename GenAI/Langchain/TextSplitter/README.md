# 📄 LangChain Text Splitters Guide

## 🚀 Overview

This guide explains how LangChain uses **text splitters** to transform and prepare documents for Large Language Model (LLM) processing. The goal is to split documents into **semantically meaningful, size-constrained chunks** that preserve context and fit into the LLM's context window.

By the end of this guide, you'll understand:

* The purpose and mechanics of text splitting in LangChain
* Common splitter types and how to use them
* Parameters that control splitter behavior

---

## 🔧 Document Processing Flow

1. **Load Documents**: Use a `DocumentLoader` to load your documents.
2. **Transform Documents**: Apply a text splitter to break large documents into smaller, manageable parts.
3. **Use with LLM**: Feed the chunks into the LLM for downstream tasks like QA, summarization, or RAG.

---

## 🧠 Why Split Text?

Most LLMs have a limited context window. If documents exceed this limit, they must be split intelligently to:

* Avoid truncation
* Preserve semantic coherence
* Ensure optimal performance during retrieval or inference

---

## 🔍 How Text Splitters Work

Text splitters operate along **two key axes**:

### 1. **Split Strategy (How text is split)**

* Characters
* Words
* Sentences
* Paragraphs
* Custom-defined tokens

### 2. **Chunk Measurement (How chunk size is determined)**

* Number of characters
* Number of words
* Token count
* Custom logic

### 📐 Key Parameters

| Parameter            | Description                                                             |
| -------------------- | ----------------------------------------------------------------------- |
| **separator**        | The delimiter used to split the text. Examples: `\n`, space, paragraph. |
| **chunk\_size**      | The max number of characters per chunk. Default: `1000`.                |
| **chunk\_overlap**   | Number of characters that overlap between chunks. Default: `200`.       |
| **length\_function** | Method to calculate chunk length (e.g., `len()`, token count).          |

---

## 🔨 Commonly Used Splitters

### 1. **Character Text Splitter**

* Splits text by a defined character separator.
* Simple and fast, suitable for structured/uniform data.

**Code Example:**

```python
from langchain.text_splitter import CharacterTextSplitter

splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=200,
    chunk_overlap=20
)
chunks = splitter.split_text(my_text)
```

---

### 2. **Recursive Character Text Splitter**

* Best for generic, unstructured text.
* Recursively splits large text by trying different separators in order (e.g., paragraph → sentence → word → character).

**Code Example:**

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20
)
chunks = splitter.split_text(my_text)
```

**Behavior:**

* Tries to split by `\n` (paragraph), then `. ` (sentence), then space, etc.
* Automatically merges smaller pieces under limit.

---

### 3. **Code Text Splitter**

* Specialized for programming code.
* Based on recursive splitting, but understands language-specific syntax.

**Supported Languages:** Python, JavaScript, Java, C++, etc.

**Code Example:**

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import Language

splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON,
    chunk_size=100,
    chunk_overlap=10
)
chunks = splitter.split_text(code_text)
```

---

### 4. **Markdown Header Text Splitter**

* Splits markdown documents based on header hierarchy.
* Useful for keeping structured sections together.

**Code Example:**

```python
from langchain.text_splitter import MarkdownHeaderTextSplitter

splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=[("#", "Header1"), ("##", "Header2"), ("###", "Header3")]
)
chunks = splitter.split_text(markdown_text)
```

---

## ✅ Summary

| Feature                   | Description                                     |
| ------------------------- | ----------------------------------------------- |
| **Goal**                  | Break large docs into LLM-sized chunks          |
| **Main Axes**             | Split method + Chunk size metric                |
| **Parameters**            | Separator, Chunk Size, Overlap, Length Function |
| **Recommended Splitters** | Character, Recursive, Code, Markdown Header     |

LangChain’s text splitting tools allow you to prepare data **intelligently** for LLM pipelines, ensuring context is preserved and memory limits are respected.

---

## 📚 Next Steps

* Try different splitters for different data types
* Use `RecursiveCharacterTextSplitter` as the default for general-purpose tasks
* Explore token-aware splitters if you're using LLMs with strict token constraints

---

Happy Splitting! 🧩
