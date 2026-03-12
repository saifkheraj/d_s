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

### 3_Prompting/
How to communicate effectively with LLMs — applies to everything.

| Folder | Contents |
|--------|----------|
| **PromptEngineering.md** | Techniques: zero-shot, few-shot, chain-of-thought, self-consistency, role-based |
| **InContextLearningandPromptTemplates/** | LangChain prompt templates, in-context learning |
| **DocumentSummarization/** | Summarization techniques and notebooks |

### 4_RAG/
Retrieval-augmented generation — theory, optimization, and working apps.

| Folder | Contents |
|--------|----------|
| **Theory/** | RAG from scratch (PyTorch, HuggingFace), document loaders, text splitters, vector databases, embeddings, retrievers |
| **Advanced/** | Pre-retrieval query/indexing optimization, post-retrieval techniques |
| **Apps/** | Gradio apps, Streamlit project, AI-powered apps |

### 5_Agents/
Autonomous LLM systems.

| Folder | Contents |
|--------|----------|
| **CrewAgent/** | Multi-agent orchestration, hierarchical agents, specialized agents |
| **LangchainAgent/** | Langchain-based agent patterns |
| **MCP/** | Model Context Protocol |

### 6_Production/
Deploying and scaling LLM systems.

| Folder | Contents |
|--------|----------|
| **SystemDesign/** | Inference optimization, distributed systems, deployment calculations |
| **MLOps/** | Web endpoints, serverless functions, containers, Docker, Kubernetes, Kubeflow |
