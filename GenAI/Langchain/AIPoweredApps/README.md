# LangChain Core Concepts

LangChain is an open-source framework designed to streamline the integration of large language models (LLMs) into various applications, particularly focusing on Natural Language Processing (NLP), data retrieval tasks, and retrieval augmented generation (RAG) applications. It provides structured tools and components for efficient application development.

## Core Components

LangChain includes several primary components:

* **Documents**
* **Chains**
* **Agents**
* **Language Models**
* **Chat Models**
* **Chat Messages**
* **Prompt Templates**
* **Output Parsers**

---

## 1. Documents

Documents in LangChain represent structured information sources, such as text files, web pages, PDFs, or other textual data used as inputs for language models.

### Document Object

Document objects contain key attributes:

* `page_content`: Document content in string format.
* `metadata`: Arbitrary data such as document\_id, filename, etc.

```python
from langchain.docstore.document import Document

doc = Document(page_content="Sample content", metadata={"document_id": 1, "filename": "sample.txt"})
print(doc)
```

### Document Loader

LangChain loads documents from various sources such as HTML, PDF, and more.

```python
from langchain.document_loaders import WebBaseLoader

loader = WebBaseLoader("https://example.com")
documents = loader.load()
print(documents)
```

### Text Splitter

Manages large documents by splitting them into chunks.

```python
from langchain.text_splitter import CharacterTextSplitter

text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_text("Long document text here...")
print(len(chunks))
```

### Vector Database

Stores document embeddings for similarity search.

```python
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(api_key="your-api-key")
vector_db = Chroma.from_texts(["Sample text"], embeddings)
query_result = vector_db.similarity_search("query text")
print(query_result)
```

### Retriever

Retrieves relevant documents from vector databases.

```python
retriever = vector_db.as_retriever()
retrieved_docs = retriever.get_relevant_documents("query text")
print(retrieved_docs)
```

---

## 2. Chains

Chains link multiple LangChain components, enabling sequential or parallel execution.

### Sequential Chains

Sequential chains use the output from one step as the input for the next.

```python
from langchain.chains import LLMChain, SequentialChain
from langchain.prompts import PromptTemplate

# Chain 1: Famous dish from location
prompt_location = PromptTemplate(input_variables=["location"], template="Famous dish from {location}?")
location_chain = LLMChain(llm=chat_model, prompt=prompt_location, output_key="meal")

# Chain 2: Recipe
prompt_recipe = PromptTemplate(input_variables=["meal"], template="Recipe for {meal}?")
dish_chain = LLMChain(llm=chat_model, prompt=prompt_recipe, output_key="recipe")

# Chain 3: Cooking time
prompt_time = PromptTemplate(input_variables=["recipe"], template="Estimated cooking time for {recipe}?")
recipe_chain = LLMChain(llm=chat_model, prompt=prompt_time, output_key="time")

# Combine into sequential chain
sequential_chain = SequentialChain(chains=[location_chain, dish_chain, recipe_chain], verbose=True)
output = sequential_chain.run("China")
print(output)
```

### Memory Storage

Stores historical data for context preservation.

```python
from langchain.memory import ChatMessageHistory

memory = ChatMessageHistory()
memory.add_ai_message("Hi")
memory.add_user_message("What is the capital of France?")
print(memory.messages)
```

---

## 3. Agents

Agents autonomously determine actions based on context, integrating with external tools.

### Example: Pandas DataFrame Agent

```python
from langchain.agents import create_pandas_dataframe_agent
import pandas as pd

# Sample DataFrame
df = pd.DataFrame({"Country": ["Italy", "France"], "Population": [60, 67]})

# Initialize agent
agent = create_pandas_dataframe_agent(llm=chat_model, df=df, verbose=True)

# Query
result = agent.invoke("How many rows in the DataFrame?")
print(result)
```

---

## 4. Language Models

Process textual inputs into meaningful textual outputs.

```python
from ibm_watson_machine_learning import GenParams, ModelInference

gen_params = GenParams(tokens=250, temperature=0.7)
model = ModelInference(model_name="mixtral_8x7b_instruct", params=gen_params)
response = model.generate("Describe a new sales approach.")
print(response)
```

---

## 5. Chat Models

Conversational interactions using specialized language models.

```python
chat_model = model.to_chat_model()
chat_response = chat_model.chat("Who is man's best friend?")
print(chat_response)
```

---

## 6. Chat Messages

Manages conversational flows with different message types.

```python
messages = [
    {"role": "system", "content": "Fitness advisor."},
    {"role": "human", "content": "Healthy breakfast?"},
    {"role": "ai", "content": "Oatmeal and fruits."}
]
response = chat_model.chat(messages, input_message="Post-workout meal?")
print(response)
```

---

## 7. Prompt Templates

Structures inputs for language models.

```python
from langchain import ChatPromptTemplate

chat_prompt = ChatPromptTemplate(messages=[
    {"role": "system", "content": "AI assistant."},
    {"role": "human", "content": "Explain {topic}."}
])
formatted_prompt = chat_prompt.format(topic="quantum computing")
print(formatted_prompt)
```

---

## 8. Output Parsers

Formats outputs from language models.

```python
from langchain.output_parsers import CommaSeparatedListOutputParser

output_parser = CommaSeparatedListOutputParser()
response = model.generate("Top 5 programming languages.")
parsed_response = output_parser.parse(response)
print(parsed_response)
```


---

## Recap

LangChain provides comprehensive tools and structured methods to efficiently integrate language models into NLP and RAG applications, employing sequential chains, memory storage, dynamic agents, and extensive document management capabilities.



# Deep Explanation of notebook code

# Smarter AI App

Welcome to the **Smarter AI App** — a comprehensive LangChain‑powered notebook designed to illustrate, step by step, how to build robust AI applications with large language models (LLMs). This README provides deep explanations, context, and code snippets to guide you through every component of the `smarter_ai_app.ipynb` notebook.

---

## 🚀 Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Project Structure](#project-structure)
5. [Key Concepts](#key-concepts)

   * [Chat Models](#chat-models)
   * [Prompt Templates](#prompt-templates)
   * [Document Loading & Splitting](#document-loading--splitting)
   * [Embeddings & Vector Stores](#embeddings--vector-stores)
   * [Retrievers & RetrievalQA](#retrievers--retrievalqa)
   * [Chains vs Agents](#chains-vs-agents)
   * [Memory & State](#memory--state)
6. [Detailed Code Examples](#detailed-code-examples)
7. [Extending the Notebook](#extending-the-notebook)
8. [Troubleshooting & Tips](#troubleshooting--tips)
9. [License](#license)

---

## 📄 Overview

LangChain is a framework that standardizes the process of building applications driven by LLMs. It abstracts away boilerplate around:

* **Models** (e.g., OpenAI GPT)
* **Prompts** and **Templates**
* **Document loaders** for PDFs, URLs, etc.
* **Text splitting** for large inputs
* **Embeddings** and **Vector Stores** for similarity search
* **Retrievers** to fetch relevant context
* **Chains** to compose workflows
* **Agents** to orchestrate tools and actions
* **Memory** to maintain conversational state

This notebook walks through each of these components with runnable code and explanations, culminating in a simple but powerful Retrieval‑Augmented Generation (RAG) QA system.

---

## 🔑 Prerequisites

1. **Python 3.8+**
2. **OpenAI API Key** (set as `OPENAI_API_KEY` in your environment)
3. **Jupyter Notebook** or **JupyterLab**

---

## 💾 Installation

Install dependencies with:

```bash
pip install --user \
  tenacity \
  ibm-watsonx-ai==1.0.4 \
  ibm-watson-machine-learning==1.0.357 \
  langchain-ibm==0.1.7 \
  langchain-community==0.2.1 \
  langchain-experimental==0.0.59 \
  langchainhub==0.1.17 \
  langchain==0.2.1 \
  pypdf==4.2.0 \
  chromadb==0.4.24
```

> **Tip:** Use a virtual environment to avoid conflicts.

---

## 📂 Project Structure

```
smarter_ai_app.ipynb      # Main walkthrough notebook
README.md                # This documentation
requirements.txt         # Pinning versions for reproducibility
```

In the notebook, you'll find sections corresponding to each key concept below.

---

## 🔍 Key Concepts

### 1. Chat Models

LangChain provides wrappers around various LLM providers. The simplest is `ChatOpenAI`:

```python
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
import os

os.environ['OPENAI_API_KEY'] = '<your-key>'
chat = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.7)
```

**Explanation:**

* `model_name`: Selects the underlying GPT model.
* `temperature`: Controls randomness (0.0 = deterministic, 1.0 = very random).

Use this object like a function to send a list of messages:

```python
resp = chat([
    HumanMessage(content='Hello!'),
    HumanMessage(content='Explain IoT simply.')
])
print(resp.content)
```

---

### 2. Prompt Templates

Rather than hard‑coding prompts, LangChain’s `PromptTemplate` and `ChatPromptTemplate` let you insert variables:

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage

prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content='You are Dr. Care, a health assistant.'),
    MessagesPlaceholder(variable_name='history'),
    HumanMessage(content='{question}')
])
```

**Explanation:**

* `SystemMessage`: Sets the assistant’s identity and style.
* `MessagesPlaceholder`: Allows conversational memory.
* `{question}`: A placeholder for runtime input.

Combine with an `LLMChain` for reuse:

```python
from langchain import LLMChain
chain = LLMChain(llm=chat, prompt=prompt, output_key='answer')
result = chain.invoke({'question': 'What is blood pressure?'})
print(result['answer'])
```

---

### 3. Document Loading & Splitting

To ingest large texts (e.g., PDF or web articles), use **Loaders** and **Splitters**:

```python
from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

loader = UnstructuredURLLoader(urls=['https://example.com/article'])
docs = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = splitter.split_documents(docs)
```

**Deep Dive:**

* **Loaders** standardize reading from diverse sources.
* **TextSplitter** ensures chunks are within model input limits while preserving context overlap.

---

### 4. Embeddings & Vector Stores

Convert text to numeric vectors for similarity search:

```python
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

emb = OpenAIEmbeddings()
vectordb = Chroma.from_documents(chunks, emb)
```

**Why It Matters:**
Near‑duplicate detection, semantic search, and RAG workflows all rely on embedding quality.

---

### 5. Retrievers & RetrievalQA

A **Retriever** fetches top‑k relevant chunks for a query:

```python
retriever = vectordb.as_retriever(search_kwargs={'k': 3})
relevant = retriever.get_relevant_documents('How to measure blood sugar?')
```

Wrap into a **RetrievalQA** chain:

```python
from langchain.chains import RetrievalQA
qa_chain = RetrievalQA.from_chain_type(
    llm=chat,
    chain_type='map_reduce',
    retriever=retriever
)
answer = qa_chain.run('Explain RAG simply.')
print(answer)
```

**Insight:**

* **`map_reduce`** splits the query across chunks, summarizes each (“map”), then combines summaries (“reduce”).

---

### 6. Chains vs Agents

* **Chains**: Fixed pipelines (e.g., `RetrievalQA`).
* **Agents**: Dynamic decision‑makers that call tools (search, calculator, etc.) based on LLM reasoning.

```python
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType

def search_fn(query): ...
search_tool = Tool(name='WebSearch', func=search_fn, description='Search web')
agent = initialize_agent([search_tool], chat, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION)
agent.run('What’s the latest on LangChain?')
```

**When to Use:**

* Use **Chains** for predictable flows.
* Use **Agents** when uncertain about which tool or action is needed at runtime.

---

### 7. Memory & State

Persist conversational history or custom variables:

```python
from langchain.memory import ConversationBufferMemory
memory = ConversationBufferMemory(memory_key='history')
# Attach `memory` to chains/agents to keep track of past messages.
```

**Benefits:**

* Contextual replies in multi‑turn dialogs.
* Tracking user preferences across interactions.

---

## 🛠️ Detailed Code Examples

Explore the notebook to see each component in action. Cells include:

* Error handling with **Tenacity** retries
* Parsing LLM output into structured JSON
* Evaluating QA performance on sample questions

Refer to corresponding headings in `smarter_ai_app.ipynb` for live demos.

---

## ✨ Extending the Notebook

* **Custom Loaders:** Integrate with proprietary data sources (databases, APIs).
* **New Tools:** Build agents for enterprise APIs or internal microservices.
* **Advanced Chains:** Combine summarization, translation, and QA in a composite pipeline.

Feel free to fork and adapt!

---

## 🐞 Troubleshooting & Tips

* **API Quotas:** Monitor your usage to avoid rate limits.
* **Chunk Sizes:** Tune `chunk_size` and `chunk_overlap` for optimal context and cost.
* **Temperature vs. Consistency:** Lower temperature yields more deterministic answers.

---


---

*Happy LangChaining!*

