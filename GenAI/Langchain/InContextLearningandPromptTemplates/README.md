# 🌐 LangChain Core Concepts Explained

LangChain is an **open-source framework** that simplifies building applications using large language models (LLMs). It provides modular components that make it easy to connect prompts, models, inputs, outputs, tools, and memory into structured workflows.

---

## 📦 1. What is LangChain?

LangChain is:
- A **framework** that connects LLMs with tools, documents, APIs, and user inputs.
- Used for building NLP applications, chatbots, RAG (retrieval-augmented generation), and automation.
- Designed to be **modular**, **composable**, and **extensible**.

---

## 🧠 2. LangChain Core Components

### 🔹 Language Model

The **language model** is the core LLM that processes text inputs and generates outputs. It can be from:
- **OpenAI** (e.g., GPT-3.5, GPT-4)
- **Google** (e.g., PaLM)
- **Meta** (e.g., LLaMA)
- **IBM WatsonX**
- **Hugging Face** (e.g., `flan-t5-base`)

#### Example:
```python
from transformers import pipeline
from langchain_community.llms import HuggingFacePipeline

pipe = pipeline("text2text-generation", model="google/flan-t5-base")
llm = HuggingFacePipeline(pipeline=pipe)
