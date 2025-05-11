# LangChain Core Concepts

LangChain is an open-source framework designed to streamline the integration of large language models (LLMs) into various applications, particularly focusing on Natural Language Processing (NLP) and data retrieval tasks. It provides structured tools and components for efficient application development.

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

### Example: Loading Text Document

```python
from langchain.document_loaders import TextLoader

loader = TextLoader("example.txt")
document = loader.load()
print(document)
```

---

## 2. Chains

Chains link multiple LangChain components, enabling sequential or parallel execution to complete complex tasks.

### Example: Simple Sequential Chain

```python
from langchain.chains import SequentialChain

chain_1 = lambda x: f"Hello {x}"
chain_2 = lambda x: f"{x}, Welcome to LangChain!"

seq_chain = SequentialChain(chains=[chain_1, chain_2])
output = seq_chain.run("Developer")

print(output)
```

---

## 3. Agents

Agents in LangChain autonomously decide on the next action based on the current context and available tools, such as APIs, databases, or other LLMs.

### Example: Basic Agent with Tools

```python
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI

# Define available tools
tools = [
    Tool(name="search", func=lambda x: f"Searching for {x}", description="Searches for information")
]

# Initialize Agent
agent = initialize_agent(tools, OpenAI(api_key="your-api-key"), agent_type="zero-shot-react-description")

# Agent action
response = agent.run("Find the latest LangChain updates")
print(response)
```

---

## 4. Language Models

Language models in LangChain process textual inputs to produce meaningful textual outputs. They are pivotal for tasks like text generation, summarization, and question-answering.

### Example: IBM WatsonX.AI (Mixtral 8x7 Billion Instruct Model)

```python
from ibm_watson_machine_learning import GenParams, ModelInference

# Initialize model with parameters
gen_params = GenParams(tokens=250, temperature=0.7)
model = ModelInference(model_name="mixtral_8x7b_instruct", params=gen_params)

# Generate response
prompt = "Describe a new sales approach for a tech product."
response = model.generate(prompt)
print(response)
```

---

## 5. Chat Models

Chat models are specialized versions of language models designed for conversational interactions, generating contextually relevant, human-like responses.

### Example: Creating Chat Model from IBM WatsonX.AI

```python
chat_model = model.to_chat_model()

# Generate a conversational response
chat_response = chat_model.chat("Who is man's best friend?")
print(chat_response)
```

---

## 6. Chat Messages

Chat models utilize various message types to handle dynamic conversational flows effectively:

* **Human Message**: User inputs.
* **AI Message**: Model-generated responses.
* **System Message**: Instructions for the model.
* **Function Message**: Function call outcomes.
* **Tool Message**: Results from interactions with external tools.

Each chat message includes:

* **Role**: The entity speaking (e.g., human, AI, system).
* **Content**: The message itself.

### Example: Configuring a Fitness Bot

```python
messages = [
    {"role": "system", "content": "You are a fitness activity advisor."},
    {"role": "human", "content": "Suggest a healthy breakfast."},
    {"role": "ai", "content": "Oatmeal with fresh fruits."}
]

new_response = chat_model.chat(messages, input_message="What should I eat after a workout?")
print(new_response)
```

---

## 7. Prompt Templates

Prompt Templates convert user inputs into structured instructions for the language model, enhancing response coherence and flexibility.

### Example: Chat Prompt Template

```python
from langchain import ChatPromptTemplate

chat_prompt = ChatPromptTemplate(
    messages=[
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "human", "content": "Explain {topic} in simple terms."}
    ]
)

formatted_prompt = chat_prompt.format(topic="quantum computing")
print(formatted_prompt)
```

---

## 8. Example Selectors

Example Selectors optimize View Shot Prompt Templates by selecting relevant examples to include based on semantic similarity, diversity, and textual overlap.

### Example: N-Gram Overlap Selector

```python
from langchain.example_selector import NGramOverlapExampleSelector

examples = [
    {"input": "What is AI?", "output": "AI means artificial intelligence."},
    {"input": "Explain ML.", "output": "ML stands for machine learning."}
]

selector = NGramOverlapExampleSelector(examples=examples, threshold=0.7)
selected_examples = selector.select_examples("What does AI stand for?")

print(selected_examples)
```

---

## 9. Output Parsers

Output Parsers format LLM responses into structured data, supporting various formats like JSON, XML, CSV, and Pandas DataFrames.

### Example: Comma-Separated List Output Parser

```python
from langchain.output_parsers import CommaSeparatedListOutputParser

output_parser = CommaSeparatedListOutputParser()
response = model.generate("List top 5 programming languages.")
parsed_response = output_parser.parse(response)

print(parsed_response)
```

---

## Recap

LangChain offers comprehensive tools to integrate language models efficiently, enhancing NLP application development.
