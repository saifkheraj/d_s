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
