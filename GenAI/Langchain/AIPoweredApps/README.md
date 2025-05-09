# 📘 LangChain Core Concepts

LangChain is an open-source interface that simplifies application development using Large Language Models (LLMs). It provides a structured approach for integrating LLMs into various applications, such as Natural Language Processing (NLP) and data retrieval.

## 🚀 What is LangChain?

LangChain allows developers to easily incorporate language models from leading providers like IBM WatsonX.AI, OpenAI, Google, and Meta. It supports applications requiring text generation, summarization, conversational AI, and structured data outputs.

---

## 🔑 Core Components

LangChain consists of several primary components:

- **Documents**
- **Chains**
- **Agents**
- **Language Model**
- **Chat Model**
- **Chat Message**
- **Prompt Templates**
- **Output Parsers**

Below is a detailed explanation of key components discussed:

---

## 1️⃣ Language Model

The Language Model (LLM) in LangChain forms the core, generating text outputs from provided text inputs. It is used widely for document summarization, task completion, and Q&A applications.

**Example:**

To create a response for a new sales approach using IBM WatsonX.AI:

```python
from ibm_watson_machine_learning.foundation_models import ModelInference
from ibm_watson_machine_learning.foundation_models.utils.enums import GenParams

params = GenParams(max_new_tokens=100, temperature=0.7)
model = ModelInference(model="ibm/mixtral-8x7b-instruct-v01-q")

result = model.generate(prompt="Suggest a sales pitch", params=params)
print(result)
```

## 2. Chat Model
A Chat Model facilitates human-like conversational interactions. It understands context and manages dynamic dialogues.

Example:

Creating a conversational model using WatsonX.AI:

chat_model = model.chat()

response = chat_model.prompt("Who is man's best friend?")
print(response)


