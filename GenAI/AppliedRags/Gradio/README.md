# Getting Started with Gradio

Gradio is an **open-source Python library** for creating customizable **web-based user interfaces**. It is particularly useful for deploying machine learning models and computational tools in a simple and interactive way.

---

## Key Concepts

### What is Gradio?

Gradio allows you to easily create a web interface around your Python functions. This makes it simple to share your models and tools with others via a web link.

---

## How to Set Up a Gradio Interface

### 1. Install Gradio

```bash
pip install gradio
```

### 2. Import Gradio

```python
import gradio as gr
```

### 3. Define Your Function

This is the logic or functionality you want to expose via a web interface.

```python
def my_function(input_text):
    return input_text
```

### 4. Create an Interface

Use `gr.Interface()` to specify:

* the function to execute
* the types of inputs
* the types of outputs

```python
iface = gr.Interface(fn=my_function,
                     inputs=gr.Textbox(label="Enter Text"),
                     outputs=gr.Textbox(label="Output Text"))
```

### 5. Launch the Interface

```python
iface.launch()
```

This starts a local server and provides a **local or public URL** where the web interface can be accessed.

---

## Examples

### Simple Text Input & Output

```python
def echo_text(text):
    return text

iface = gr.Interface(fn=echo_text,
                     inputs=gr.Textbox(label="Enter your message"),
                     outputs=gr.Textbox(label="Echoed message"))
iface.launch()
```

### Multiple Inputs

```python
def combine_text_and_number(text, number):
    return f"Text: {text}, Number: {number}"

iface = gr.Interface(fn=combine_text_and_number,
                     inputs=[gr.Textbox(label="Enter Text"), gr.Number(label="Enter Number")],
                     outputs=gr.Textbox(label="Output"))
iface.launch()
```

### File Upload Example

```python
def count_files(files):
    return f"Number of files uploaded: {len(files)}"

iface = gr.Interface(fn=count_files,
                     inputs=gr.File(file_types=None, label="Upload Files", file_count="multiple"),
                     outputs=gr.Textbox(label="File Count"))
iface.launch()
```

---

## Summary

* Gradio makes it easy to turn Python functions into web apps.
* Setup steps:

  1. Write Python function
  2. Create Gradio interface using `gr.Interface`
  3. Launch the interface
  4. Access via local/public URL
* You can create interfaces with text inputs, numbers, and file uploads.

For more details, visit the [Gradio documentation](https://gradio.app/docs/).

Steps
- pip install gradio

![alt text](image.png)


# README.md

# Generative AI Applications with RAG and LangChain

This project demonstrates how to build Generative AI applications using Retrieval-Augmented Generation (RAG) and LangChain, leveraging document loaders, text splitters, embeddings, vector databases, and a chatbot interface via Gradio.

---

## 1. Project Overview

* **Framework**: LangChain
* **Embeddings**: WatsonxEmbeddings (IBM)
* **LLM**: Mixtral-8x7B (Mistral AI) via WatsonxLLM
* **Vector Databases**: Chroma / FAISS
* **Interface**: Gradio Web UI
* **Supported Documents**: PDF, TXT, Markdown, DOCX, HTML, CSV, JSON

---

## 2. Application Structure

### Main Functional Blocks

1. **Document Loaders**

   * PyPDFLoader, UnstructuredFileLoader, PyMuPDFLoader, CSVLoader, etc.

2. **Text Splitters**

   * RecursiveCharacterTextSplitter
   * MarkdownHeaderTextSplitter
   * HTMLHeaderTextSplitter
   * Code Splitter

3. **Embedding Model**

   * IBM Slate-125M-English retriever

4. **Vector Stores**

   * Chroma DB
   * FAISS DB

5. **Retriever Techniques**

   * Similarity Search
   * MMR Retrieval
   * Similarity Score Threshold
   * Self-Querying Retriever
   * Parent Document Retriever
   * Multi-Query Retriever

6. **Question-Answering Chain**

   * RetrievalQA Chain

7. **Interface**

   * Gradio Web Interface
   * Upload PDF -> Ask Question -> Get Answer

---

## 3. Setup Instructions

### Prerequisites

* Python 3.11
* Install packages:

```bash
pip install langchain langchain_community ibm_watsonx_ai gradio faiss-cpu chromadb bs4 requests
```

---

### Running the Application

```bash
python3.11 qabot.py
```

---

## 4. File: `qabot.py`

### Key Components

1. **Initialize LLM**

   * Mixtral-8x7b-instruct-v01

2. **Load PDF Document**

   * PyPDFLoader

3. **Text Splitter**

   * RecursiveCharacterTextSplitter (chunk\_size=1000, overlap=50)

4. **Embed Documents**

   * WatsonxEmbeddings

5. **Store Embeddings**

   * Chroma Vector Store

6. **Retriever**

   * Chroma.as\_retriever()

7. **RetrievalQA Chain**

   * RetrievalQA.from\_chain\_type(llm, retriever)

8. **Gradio Interface**

   * File Upload (.pdf)
   * Input Query
   * Output Answer

9. **Launch**

   * `rag_application.launch(server_name="0.0.0.0", server_port=7860)`

---

## 5. Usage

1. Open the web interface: [http://localhost:7860](http://localhost:7860)
2. Upload a PDF file.
3. Enter your query.
4. Receive an answer based on the document.

---

## 6. Example Queries

```text
- "What is the email policy in this document?"
- "When was the company founded?"
- "Explain section 3 of the document."
```

---

## 7. Advanced Features (Optional)

* MMR Retrieval
* Similarity Score Threshold Retrieval
* Self-Querying Retriever
* Parent Document Retriever
* Multi-Query Retriever

---

## 8. References

* LangChain Documentation: [https://python.langchain.com](https://python.langchain.com)
* IBM Watsonx AI: [https://www.ibm.com/products/watsonx-ai](https://www.ibm.com/products/watsonx-ai)
* Chroma DB: [https://docs.trychroma.com](https://docs.trychroma.com)
* FAISS: [https://github.com/facebookresearch/faiss](https://github.com/facebookresearch/faiss)

---


