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

LangChain’s **Chat Models** wrap LLM APIs (like OpenAI’s GPT) into Python classes that mimic a chat interface. They handle message formatting, streaming, retry logic, and more.

```python
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)
import os

# Set your OpenAI key in the environment
os.environ['OPENAI_API_KEY'] = '<your-key>'

# Initialize the chat model
chat = ChatOpenAI(
    model_name='gpt-3.5-turbo',  # Choose which GPT engine to use
    temperature=0.7             # Controls randomness: 0.0 = deterministic, 1.0 = very creative
)
```

#### Message Types

* **SystemMessage**: Instructions for the assistant’s overall behavior (e.g., tone, role).
* **HumanMessage**: User input or question you want the model to answer.
* **AIMessage**: (Optional) Holds the assistant’s previous responses if you need to include them in context.

#### Why Use Multiple Messages?

LLMs like GPT expect a sequence of messages with roles (`system`, `user`, `assistant`). This structure helps maintain context, separate instructions from user queries, and improves response quality.

#### Example Usage

Send a sequence of messages just like a conversation:

```python
resp = chat([
    SystemMessage(content='You are a helpful assistant.'),
    HumanMessage(content='Hello!'),
    HumanMessage(content='Explain IoT simply.')
])

# The response is an AIMessage:
print(resp.content)
```

---

### 2. Prompt Templates

Prompt Templates in LangChain allow you to define reusable, parameterized prompts that can be filled in at runtime. Instead of building strings manually, templates ensure consistency, readability, and ease of maintenance.

#### Core Components

* **PromptTemplate**: For single-turn text-based prompts.
* **ChatPromptTemplate**: For multi-role chat-style prompts (system, user, assistant).
* **MessagesPlaceholder**: A placeholder slot within a `ChatPromptTemplate` where you can inject past conversation history or other message lists.

---

#### 2.1. Building a Basic PromptTemplate

```python
from langchain_core.prompts import PromptTemplate

# Define a template with a single variable {topic}
template = PromptTemplate(
    input_variables=["topic"],
    template="Explain the concept of {topic} in simple terms."
)

# Format it at runtime:
prompt_text = template.format(topic="convolutional neural networks")
print(prompt_text)
# -> "Explain the concept of convolutional neural networks in simple terms."
```

**Explanation:**

* `input_variables`: A list of placeholder names your template uses.
* `template`: The string with `{}` placeholders matching `input_variables`.
* `format(...)`: Fills in placeholders with actual values.

---

#### 2.2. ChatPromptTemplate for Conversation

For chat-based interactions, use `ChatPromptTemplate` to structure messages by role:

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

chat_prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="You are Dr. Care, a knowledgeable and compassionate health assistant."),
    MessagesPlaceholder(variable_name="history"),
    HumanMessage(content="{user_question}")
])
```

* **SystemMessage**: Sets the assistant’s overall behavior, tone, and role. Think of it as instructions to the model.
* **MessagesPlaceholder**: Marks where to insert a list of previous messages stored under the key `history`.
* **HumanMessage**: Represents the current user’s question at runtime, with a `{user_question}` placeholder.
* **AIMessage**: (Optional) You can include earlier assistant responses in a similar fashion.

##### Using ChatPromptTemplate

```python
# Imagine we have some past conversation stored:
past_conversation = [
    HumanMessage(content="Hello, who are you?"),
    AIMessage(content="I am Dr. Care, your AI health assistant."),
]

# Render messages before calling the LLM:
messages = chat_prompt.format_messages(
    history=past_conversation,
    user_question="What are the symptoms of diabetes?"
)

# `messages` is a list of SystemMessage, HumanMessage, and AIMessage in correct order
# Pass directly to a chat model:
response = chat(messages)
print(response.content)
```

**Why This Matters:**

* Maintains clear separation between instructions (system), past dialogue (history), and new queries (user).
* Ensures the model has all necessary context in the correct order.

---

#### 2.3. Integrating with LLMChain for Reuse

To avoid rewriting the same prompt logic, embed your `ChatPromptTemplate` in an `LLMChain`:

```python
from langchain import LLMChain

health_chain = LLMChain(
    llm=chat,
    prompt=chat_prompt,
    output_key="diagnosis"
)

# Invoke with a dict mapping your template variables:
result = health_chain.invoke({
    "history": past_conversation,
    "user_question": "How can I lower my blood pressure?"
})

print(result["diagnosis"])
```

* **LLMChain**: Couples an LLM with a prompt template, handling formatting and calling the model.
* **output\_key**: Specifies the key name under which the LLM’s response will appear in the result.

**Benefits:**

* Prompts and model calls become modular functions you can import and reuse across notebooks or scripts.
* Encapsulates prompt logic, reducing errors and duplication.

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

LangChain provides two high-level orchestration abstractions:

* **Chains**: Linear or branched pipelines with predetermined steps.
* **Agents**: Flexible, LLM-driven controllers that choose tools and actions dynamically.

---

#### 6.1. Chains (Fixed Workflows)

A **Chain** is a sequence of components (LLMs, prompt templates, retrievers, parsers) wired together for a specific task. Chains handle:

1. **Formatting** the inputs (merging templates with your variables).
2. **Calling** the underlying LLM or tool.
3. **Post-processing** outputs (e.g., parsing, combining results).

```python
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

# 1. Initialize model and retriever
chat = ChatOpenAI(model_name='gpt-3.5-turbo')
retriever = vectordb.as_retriever(search_kwargs={'k': 3})

# 2. Create a QA chain that will format prompts, call the model, and collect sources
qa_chain = RetrievalQA.from_chain_type(
    llm=chat,
    chain_type='map_reduce',    # map: answer per chunk, reduce: combine answers
    retriever=retriever,
    return_source_documents=True  # also return docs used
)
```

##### 6.1.1. How Formatting Works in a Chain

Under the hood, a chain uses a **PromptTemplate** or **ChatPromptTemplate**. When you call the chain, you provide a dict of inputs:

```python
# Direct invocation by input key names
result = qa_chain({'query': 'Explain RAG simply.'})
```

* The chain looks up the template expecting a variable named `query`.
* It calls `template.format(query='Explain RAG simply.')` to produce the final prompt.
* It passes that prompt (or list of messages) to the LLM.
* Finally, it collects and returns the model’s answer (and any extra outputs like source docs).

##### 6.1.2. Chain.run vs Chain.invoke vs Chain.**call**

* **`chain.run(input_str)`**: When your chain has a single input variable (commonly named `query`), you can shortcut with `.run()`:

  ```python
  answer = qa_chain.run('What is RAG?')
  ```

  This is equivalent to `qa_chain({'query': 'What is RAG?'})['result']`.

* **`chain.invoke(inputs_dict)`**: Use `.invoke()` when you need access to all outputs, especially if the chain returns multiple keys:

  ```python
  full_output = qa_chain.invoke({'query': 'What is RAG?'})
  print(full_output['result'], full_output['source_documents'])
  ```

* **`chain(inputs_dict)`**: Direct call (syntactic sugar) that returns the primary output.

**When to Use Which:**

* Use `.run()` for quick single-answer queries.
* Use `.invoke()` or direct call when you need detailed outputs or have multiple input variables.

````python
# Examples:
short_answer = qa_chain.run('Define vector embeddings')
detailed = qa_chain.invoke({'query': 'Define vector embeddings'})
```python
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

# Initialize model and retriever (from previous sections)
chat = ChatOpenAI(model_name='gpt-3.5-turbo')
retriever = vectordb.as_retriever(search_kwargs={'k': 3})

# Create a QA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=chat,
    chain_type='map_reduce',    # map: answer per chunk, reduce: combine answers
    retriever=retriever,
    return_source_documents=True  # returns docs used for the answer
)

# Run the chain
result = qa_chain({'query': 'Explain RAG simply.'})
print('Answer:', result['result'])
print('Sources:', [doc.metadata['source'] for doc in result['source_documents']])
````

**Key Points:**

* **Predictable**: Always follows the same steps.
* **Easy to debug**: You know exactly which component did what.
* **Best for**: Standardized pipelines like summarization, translation, QA.

---

#### 6.2. Agents (Adaptive Tool Use)

An **Agent** wraps an LLM in a reasoning loop (often ReAct: Reason + Act) that:

1. **Thinks** (generates a reasoning trace)
2. **Acts** (selects a tool, invokes it)
3. **Observes** (captures tool output)
4. **Repeats** until a final answer is returned.

```python
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType

# Define a simple search function
def search_fn(query: str) -> str:
    # Imagine hooking into a real search API
    return "Top result summary for: " + query

# Wrap it as a Tool
search_tool = Tool(
    name='WebSearch',
    func=search_fn,
    description='Useful for searching the web to answer questions.'
)

# Initialize the agent with the tool and chat model
agent = initialize_agent(
    tools=[search_tool],
    llm=chat,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True  # prints each reasoning and action step
)

# Run the agent
response = agent.run('What is the latest development in LangChain?')
print(response)
```

**Key Points:**

* **Dynamic**: Chooses which tool(s) to use at runtime based on the query.
* **Interpretable**: With `verbose=True`, you see the reasoning trace and tool calls.
* **Best for**: Multi-step tasks where the next action depends on intermediate results (e.g., calculations, database lookups, API calls).

---

### 7. Memory & State

Memory components help chains and agents maintain context across invocations.

#### 7.1. ConversationBufferMemory

A rolling window of past messages stored as a list of `HumanMessage` and `AIMessage`.

```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(
    memory_key='history',  # corresponds to MessagesPlaceholder 'history'
    return_messages=True   # returns full message objects when accessed
)

# Attach memory to a chain
chain_with_memory = LLMChain(
    llm=chat,
    prompt=chat_prompt,
    memory=memory
)

# Invoke twice
chain_with_memory.invoke({'user_question': 'Hello, who are you?'})
chain_with_memory.invoke({'user_question': 'What can you do?'
})
# Memory now holds both turns, enabling contextual replies
```

#### 7.2. SummaryMemory

Stores a rolling summary instead of full messages, reducing token usage.

```python
from langchain.memory import ConversationSummaryMemory

summary_memory = ConversationSummaryMemory(
    llm=chat,
    memory_key='summary',
    max_token_limit=500
)
```

#### 7.3. Custom Variables

You can store arbitrary key/value data:

```python
from langchain.memory import CombinedMemory
from langchain.memory import SimpleMemory

# SimpleMemory stores a dict of variables
prefs = SimpleMemory(memories={"username": "Alice"})
combined = CombinedMemory(memories=[memory, prefs])
```

**Benefits of Memory:**

* **Contextual Understanding:** Chains and agents reply with awareness of prior exchanges.
* **Personalization:** Remember user preferences, settings, or profiles.
* **Cost Efficiency:** SummaryMemory conserves tokens over long dialogs.

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

## 📝 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

*Happy LangChaining!*
