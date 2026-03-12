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

# Glossary: Generative AI Applications with RAG and LangChain


---

| Term                                     | Definition                                                                                                                                                                                   |
| ---------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Chunk size**                           | Refers to the maximum number of characters each text chunk can contain after being split by a text splitter.                                                                                 |
| **Chroma DB**                            | An open-source vector store supported by LangChain, used for storing and retrieving vector embeddings, particularly useful in semantic search engines over text data.                        |
| **Cosine similarity**                    | A measure used to calculate the similarity between two non-zero vectors of an inner product space, which measures the cosine of the angle between them.                                      |
| **Document loader**                      | A component in LangChain that gathers information from various sources (like websites, files, and databases) and converts it into a format that can be processed by the LangChain framework. |
| **Embedding**                            | A numerical representation of data, typically in a high-dimensional space, that captures the semantic meaning of the data.                                                                   |
| **JQ schema**                            | A schema used by the JSONLoader in LangChain to parse JSON files according to specific needs, particularly to extract particular values from a JSON structure.                               |
| **LangChain**                            | A framework that simplifies the development of applications using large language models (LLMs) by providing tools for loading, processing, and querying data from various sources.           |
| **Large language model (LLM)**           | A type of artificial intelligence model designed to understand and generate human language, often used in NLP tasks such as text generation, translation, and summarization.                 |
| **Markdown header text splitter**        | A tool in LangChain that splits a markdown file by a specified set of headers, useful for maintaining document structure during text processing.                                             |
| **Maximum marginal relevance (MMR)**     | A retrieval technique used in vector stores to balance the relevance and diversity of the retrieved results, ensuring comprehensive coverage of different aspects of the query.              |
| **PyPDFLoader**                          | A class in LangChain used to load PDF files into an array of document objects, each representing a page along with its metadata.                                                             |
| **PyMuPDF loader**                       | A tool in LangChain, known for its speed, that loads PDF files into document objects with detailed metadata about the PDF and its pages, providing one document object per page.             |
| **RecursiveCharacterTextSplitter**       | A text splitter in LangChain that employs recursion to split large texts into smaller chunks using a set of characters, suitable for general text processing.                                |
| **Retrieval-augmented generation (RAG)** | A method that combines retrieval-based and generative-based approaches to improve the quality of the generated responses, often used in question-answering systems.                          |
| **Self-query retriever**                 | A type of LangChain retriever that converts a query into two components: a string to look up semantically and a metadata filter, used to retrieve documents based on both text and metadata. |
| **Separator**                            | The character or set of characters used by a text splitter to divide the text into manageable chunks, such as a line break or a paragraph change.                                            |
| **Similarity search**                    | A method used in vector databases to find and retrieve the most relevant content based on the similarity of vector embeddings to a given query vector.                                       |
| **Vector database**                      | A specialized type of database designed to store and retrieve vector embeddings, allowing for efficient and effective information retrieval based on similarity calculations.                |
| **Vector store-based retriever**         | A retriever in LangChain that queries a vector database to retrieve the most similar chunks of data to a given query, without requiring an LLM.                                              |
| **WebBaseLoader**                        | A component in LangChain that extracts all text from HTML webpages, converting it into a document format suitable for downstream processing, avoiding unnecessary HTML tags and links.       |




## 8. References

* LangChain Documentation: [https://python.langchain.com](https://python.langchain.com)
* IBM Watsonx AI: [https://www.ibm.com/products/watsonx-ai](https://www.ibm.com/products/watsonx-ai)
* Chroma DB: [https://docs.trychroma.com](https://docs.trychroma.com)
* FAISS: [https://github.com/facebookresearch/faiss](https://github.com/facebookresearch/faiss)

---



