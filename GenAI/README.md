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

---

## Medium Articles

Published articles mapped to repository folders.

| # | Article | Folder | Description |
|---|---------|--------|-------------|
| 1 | [Understanding the Mechanics of Neural Machine Translation](https://saifalikheraj.medium.com/understanding-the-mechanics-of-neural-machine-translation-b07e3c758bed) | `1_Foundations/Transformers/` | Encoder-decoder models with pre-attention and attention mechanisms |
| 2 | [Similarity Measures — Scoring Textual Articles](https://medium.com/towards-data-science/similarity-measures-e3dbd4e58660) | `1_Foundations/NLP_Basics/` | Similarity measures for text comparison in NLP and computer vision |
| 3 | [Parameter-Efficient Finetuning (PEFT) and Adapter Modules in Transformers](https://pub.towardsai.net/parameter-efficient-finetuning-peft-and-adapter-modules-in-transformers-784230ef5a10) | `2_Training/Finetuning/PEFT/` | Efficient fine-tuning with adapter modules vs full fine-tuning |
| 4 | [Training Less, Achieving More: Unlocking Transformers with LoRA](https://pub.towardsai.net/training-less-achieving-more-unlocking-transformers-with-lora-5af5263ae22e) | `2_Training/Finetuning/PEFT/` | Low-Rank Adaptation for efficient transformer fine-tuning |
| 5 | [Why QLoRA Changes the Game: A Quick Dive into Efficient Fine-Tuning with BERT](https://pub.towardsai.net/why-qlora-changes-the-game-a-quick-dive-into-efficient-fine-tuning-with-bert-b75e71d1456d) | `2_Training/Finetuning/PEFT/` | Quantized Low-Rank Adaptation for fine-tuning on mid-range GPUs |
| 6 | [A Real World LangChain Guide and Playbook](https://saifalikheraj.medium.com/a-real-world-langchain-guide-and-playbook-6254830cdb4b) | `3_Prompting/` | Automating a hospital's workflow using 5 LangChain concepts |
| 7 | [Dense Passage Retrieval (2020) and Contriever (2021): The Models That Paved the Way](https://pub.towardsai.net/dense-passage-retrieval-2020-and-contriever-2021-the-models-that-paved-the-way-for-future-8ec140398ead) | `4_RAG/Theory/` | How DPR and Contriever shaped modern retrieval for LLMs |
| 8 | [A Deep Technical Exploration of RAG with Transformers, DPR, FAISS](https://pub.towardsai.net/a-deep-technical-exploration-of-retrieval-augmented-generation-rag-with-transformers-dpr-faiss-acdd00fe1ed0) | `4_RAG/Theory/` | End-to-end RAG pipeline with transformers, dense retrieval, and FAISS |
| 9 | [Beyond Basic RAG: A Practical Guide to Advanced Indexing Techniques](https://saifalikheraj.medium.com/beyond-basic-rag-a-practical-guide-to-advanced-indexing-techniques-a3efe7c6d78c) | `4_RAG/Advanced/` | Advanced indexing techniques for RAG systems over large document collections |
| 10 | [Cutting Batch Release from 14 Days to 3: A Case Study in Multi-Agent AI for Pharmaceutical](https://saifalikheraj.medium.com/cutting-batch-release-from-14-days-to-3-a-case-study-in-multi-agent-ai-for-pharmaceutical-859a81ea90a7) | `5_Agents/` | Agentic AI architectures compressing decision cycles in regulated manufacturing |
