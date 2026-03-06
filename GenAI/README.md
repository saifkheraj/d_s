# GenAI Learning Repository

Structured around the **LLM lifecycle** — from foundations to production.

---

## Structure

### 1_Foundations/
Core building blocks before touching LLMs.

| Folder | Contents |
|--------|----------|
| **NLP_Basics/** | Tokenizers, dataloaders, document classification, NLP fundamentals |
| **Transformers/** | Encoder (self-attention, BERT), Decoder architectures |

### 2_Training/
How to adapt and align LLMs.

| Folder | Contents |
|--------|----------|
| **Finetuning/** | Transfer learning, PEFT (LoRA, QLoRA, adapters) |
| **RLHF/** | Instruction tuning, reward modeling, PPO |

### 3_RAG/
Everything retrieval-augmented generation — unified from multiple sources.

| Folder | Contents |
|--------|----------|
| **Core/** | RAG from scratch (PyTorch, HuggingFace implementations) |
| **Pipeline/** | Document loaders, text splitters, vector databases, embeddings, retrievers |
| **Advanced/** | Pre-retrieval query optimization, indexing optimization, post-retrieval techniques |
| **Prompting/** | In-context learning, prompt templates, document summarization |
| **Apps/** | Gradio apps, Streamlit project, AI-powered apps |

### 4_Agents/
Autonomous LLM systems.

| Folder | Contents |
|--------|----------|
| **CrewAgent/** | Multi-agent orchestration, hierarchical agents, specialized agents |
| **LangchainAgent/** | Langchain-based agent patterns |
| **MCP/** | Model Context Protocol |

### 5_Production/
Deploying and scaling LLM systems.

| Folder | Contents |
|--------|----------|
| **SystemDesign/** | Inference optimization, distributed systems, deployment calculations |
| **MLOps/** | Web endpoints, serverless functions, containers, Docker, Kubernetes, Kubeflow |
