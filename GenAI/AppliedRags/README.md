# Introduction to Vector Databases for Storing Embeddings

This guide provides a comprehensive overview of how to store embeddings using a vector database, specifically focusing on **Chroma DB**, an open-source vector store supported by **LangChain**. It covers the process of storing, retrieving, and performing similarity search operations on vector embeddings to enable efficient and relevant information retrieval.

---

## Why Use a Vector Database?

When working with unstructured data like text, images, or audio, embeddings are used to represent this data as numerical vectors in a high-dimensional space. These vectors capture semantic relationships, making it easier to search and retrieve related content. However, traditional databases (e.g., SQL) are not optimized for handling such data. Vector databases solve this problem by:

* Storing high-dimensional vectors efficiently
* Indexing embeddings for fast retrieval
* Enabling similarity-based search

This makes them ideal for applications like semantic search, recommendation engines, question answering, and more.

---

## What is Chroma DB?

**Chroma DB** is an open-source vector store built to work seamlessly with LangChain. Its key features include:

* Efficient storage and retrieval of vector embeddings
* Support for metadata attached to each vector
* Seamless integration with LangChain's language model ecosystem
* Ideal for building semantic search engines and memory components for LLMs

---

## Setting Up Chroma DB with LangChain

To store embeddings in Chroma DB, you must first:

1. **Load and split** your target data into smaller chunks
2. **Generate embeddings** for each chunk using an embedding model (e.g., OpenAI, Hugging Face, IBM WatsonX)

Then, you can construct the Chroma DB store:

```python
from langchain.vectorstores import Chroma

# Assume `documents` is a list of text chunks
# Assume `embedding_model` is an instance of a model with an embed_documents method

vectorstore = Chroma.from_documents(documents=documents, embedding=embedding_model)
```

Chroma DB will automatically:

* Embed each document
* Store both the embeddings and associated metadata
* Prepare for similarity search

---

## Performing a Similarity Search

Once the embeddings are stored, you can perform a similarity search on the vector database. Here’s how the process works:

1. **Input Query**: User provides a natural language query
2. **Query Embedding**: The embedding model converts the query to a high-dimensional vector
3. **Similarity Matching**: Chroma DB compares the query vector with stored vectors using distance metrics (e.g., cosine similarity, Euclidean distance)
4. **Return Results**: Top-N most similar documents are returned

### Sample Code

```python
query = "What is the company’s email policy?"
results = vectorstore.similarity_search(query, k=4)

for result in results:
    print(result.page_content)  # Or result.metadata if needed
```

By default, Chroma returns the top 4 most relevant results (`k=4`), but you can modify this as needed.

---

## Key Benefits

* **Accuracy**: Semantic similarity captures meaning better than keyword search
* **Speed**: Fast retrieval using vector indices
* **Scalability**: Efficient for large-scale unstructured datasets

---

## Summary

* Vector embeddings convert unstructured data into numerical vectors for downstream tasks
* A vector database like Chroma DB stores these embeddings and enables similarity-based search
* Chroma DB integrates smoothly with LangChain, making embedding storage and retrieval seamless
* The similarity search process involves embedding the query and finding nearest neighbors in vector space

Using Chroma DB, developers can build powerful, intelligent applications that retrieve relevant information efficiently and accurately.

---
# 📘 LangChain Advanced Retrievers - Part 1: Vector Store-Based Retriever

## 🔍 What is a LangChain Retriever?

A **LangChain Retriever** is a core interface used to fetch relevant documents (or their chunks) based on a **free-form, unstructured query**.

Unlike a vector store, a retriever does **not necessarily store** the documents — it simply focuses on **returning relevant content**. You give it a query string, and it returns a list of documents or chunks related to that query.

This abstraction allows LangChain to support **multiple types of retrievers**, including those based on vector similarity, keyword search, hybrid retrieval, and more.

---

## 🧠 Vector Store-Based Retriever: Simplest Type

### 🔗 How It Works

The **Vector Store-Based Retriever** relies on a **vector database** that stores documents in **embedded form**. Here's a step-by-step breakdown:

1. **Load documents** into LangChain.
2. **Split** documents into chunks (e.g., 500-word segments).
3. **Embed** each chunk using a text embedding model (like OpenAI, Hugging Face, etc.).
4. Store the embedded chunks in a **vector database** (e.g., FAISS, Chroma, Pinecone).

Now, when a user provides a query:

* The query is **embedded** using the same embedding model.
* LangChain searches the vector store for **similar embeddings**.
* The top `k` most similar chunks are returned as results.

### 📌 Example:

```python
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import TextLoader

# Step 1: Load documents
loader = TextLoader("docs/email_policy.txt")
documents = loader.load()

# Step 2-3: Embed and store into FAISS
embedding = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(documents, embedding)

# Step 4: Create retriever
retriever = vectorstore.as_retriever()

# Step 5: Query the retriever
query = "What is the company's email policy?"
results = retriever.get_relevant_documents(query)
for doc in results:
    print(doc.page_content)
```

---

## 🔁 Maximum Marginal Relevance (MMR)

MMR enhances retrieval by **balancing relevance and diversity**:

* Traditional similarity search returns the top `k` results based solely on cosine similarity.
* MMR ensures that the returned documents are not only **relevant** but also **not too similar to each other**.

This prevents **redundancy** and allows **coverage of multiple aspects** of the query.

### 🔍 MMR in Action

Imagine you're querying: `"company email policy"`

Using regular similarity:

* Result 1: "Email policy outlines appropriate use"
* Result 2: "Email policy defines what emails can be sent"
* Result 3: "Email policy is for internal communication only"

Using MMR:

* Result 1: "Email policy outlines appropriate use"
* Result 2: "Penalties for email misuse"
* Result 3: "Internal email archiving rules"

➡️ **MMR brings broader coverage** of the topic instead of repeating similar content.

### 📌 Enabling MMR in LangChain

```python
retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 3})
```

---

## ✅ Summary

* A **LangChain retriever** is an interface for returning relevant documents given a free-text query.
* The **vector store-based retriever** works by comparing the embedding of the query with embedded chunks in a vector database.
* Two retrieval methods:

  * **Similarity search** – retrieves most similar chunks.
  * **MMR (Maximum Marginal Relevance)** – retrieves a diverse and relevant set of chunks.
* LangChain provides a convenient `.as_retriever()` method to convert a vector store into a retriever.

---

## 🧪 Try It Yourself

1. Load a text document.
2. Embed it and store in FAISS.
3. Convert to retriever.
4. Query with and without MMR.
5. Compare the output.

🔗  we'll now cover **hybrid and self-query retrievers** for smarter retrieval!

# 📘 LangChain Advanced Retrievers - Part 2: Multi-Query, Self-Query, and Parent Document Retrievers

LangChain retrievers go beyond simple similarity search. In this guide, we’ll explore **three advanced retrievers** that solve specific challenges in retrieval:

* Multi-Query Retriever
* Self-Query Retriever
* Parent Document Retriever

---

## 🔄 1. Multi-Query Retriever

### 💡 What It Does

The **Multi-Query Retriever** uses an **LLM to generate multiple variations of a user query**. This is useful when embeddings don't capture all the semantic richness or when the wording of the query might miss relevant documents.

### 🧠 Why It’s Useful

* Retrieves a **broader and more diverse** set of relevant documents.
* Helps mitigate query sensitivity and embedding limitations.

### 🧱 How It Works

1. Accepts a base retriever (e.g., vector store or MMR).
2. Uses an LLM to generate alternative phrasings of the input query.
3. Retrieves results for each variation.
4. Takes the **union** of all results, removing duplicates.

### 📌 Code Example

```python
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI()
retriever = vectorstore.as_retriever()

multi_query_retriever = MultiQueryRetriever.from_llm(
    retriever=retriever,
    llm=llm
)

results = multi_query_retriever.get_relevant_documents("email policy")
```

---

## 🧠 2. Self-Query Retriever

### 💡 What It Does

The **Self-Query Retriever** uses an LLM to convert a query into:

* A semantic search query
* A **metadata filter**

This allows **filtering documents** not just by content, but also by their **metadata**, such as date, author, tags, etc.

### 📦 Use Case

Retrieving documents like:

> “Find movies directed by Nolan after 2015 with a rating above 8.5.”

### 🧱 How It Works

1. Documents are stored in a vector store with metadata.
2. Metadata fields are defined and described.
3. The LLM understands these descriptions.
4. The retriever uses both semantic lookup and metadata filtering.

### 📌 Code Example

```python
from langchain.retrievers import SelfQueryRetriever
from langchain.chains.query_constructor.base import AttributeInfo

metadata_field_info = [
    AttributeInfo(name="year", description="Year released", type="integer"),
    AttributeInfo(name="rating", description="IMDB rating", type="float")
]

retriever = SelfQueryRetriever.from_llm(
    llm=llm,
    vectorstore=vectorstore,
    document_contents="Brief description of the movie",
    metadata_field_info=metadata_field_info
)

results = retriever.get_relevant_documents("I want to watch a movie rated higher than 8.5")
```

---

## 🧱 3. Parent Document Retriever

### 💡 What It Does

Balances between **chunking for embedding** and **retrieving long documents**. It:

* Chunks text into **small segments** for embedding (child splitter)
* Maintains **large parent documents** for context (parent splitter)

### ⚖️ Why It’s Useful

* Embedding requires small, focused text chunks.
* But retrieval often needs **full context** (i.e., a whole section or page).

### 🧱 How It Works

1. Split documents into small chunks (child splitter).
2. Also split into larger chunks (parent splitter).
3. Store child chunks in vector DB.
4. When a match is found, **retrieve the parent document** it came from.

### 📌 Code Example

```python
from langchain.retrievers import ParentDocumentRetriever

parent_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
child_splitter = RecursiveCharacterTextSplitter(chunk_size=200)

retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=parent_docstore,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter
)

retriever.add_documents(docs)
results = retriever.get_relevant_documents("smoking policy")
```

📝 In this case, the retrieved content will be from the **parent chunk**, offering better context.

---

## ✅ Recap

| Retriever Type            | Purpose                     | Requires LLM | Key Feature                         |
| ------------------------- | --------------------------- | ------------ | ----------------------------------- |
| Multi-Query Retriever     | Improve recall              | ✅            | Generates alternate phrasings       |
| Self-Query Retriever      | Use metadata filters        | ✅            | Parses query into semantic + filter |
| Parent Document Retriever | Balance chunking vs context | ❌            | Retrieves full parent docs          |

Each retriever solves a different retrieval challenge:

* **Multi-query** helps when your query may miss relevant phrases.
* **Self-query** enables advanced filtering by metadata.
* **Parent-doc** ensures context-rich responses.

---

we’ll explore **contextual compression** and **ensemble retrievers** for even more powerful hybrid approaches!





## Further Reading

* [Chroma DB GitHub](https://github.com/chroma-core/chroma) *(if public)*
* [LangChain Documentation](https://docs.langchain.com)
* [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)
* [Vector Search Concepts](https://www.pinecone.io/learn/vector-search/)

---

> Ready to build your first semantic search engine? Start by chunking your data, embedding it, and storing it with Chroma DB!
