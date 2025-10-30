# ANN Indexes for LLM Context Retrieval: Practical Guide

## What Problem Do We Solve?

When an LLM answers a question, it needs relevant context from stored documents. Comparing the question to 10 million documents would be too slow. **ANN indexes find the right chunks in milliseconds**.

```
User Question → [ANN Index finds relevant chunks in 5-50ms] → LLM generates answer
```

---

## Quick Comparison: When to Use What

| Method | Speed | Memory | Best For | Deployment |
|--------|-------|--------|----------|-----------|
| **IVF** | Fast | Low | Millions of docs, budget-friendly | CPU/GPU |
| **HNSW** | Fastest | Medium | Real-time chat, <100M docs | CPU/small GPU |
| **Tree** | Medium | Low | Small datasets (<1M) | CPU only |
| **LSH** | Very Fast | Low | Streaming/real-time | CPU, scales horizontally |
| **DiskANN** | Fast | Minimal | Billions of docs, cost-efficient | SSD storage |

---

## 1. IVF (Inverted File Index)

**Concept**: Split documents into topic buckets. Search only in the relevant bucket.

**When to use**: Large document sets, you care about cost/memory.

### Code Example
```python
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

# Step 1: Create IVF index (offline)
embeddings = OpenAIEmbeddings()
documents = ["Transformers use attention...", "Neural networks learn..."]
vector_store = FAISS.from_texts(documents, embeddings)

# Step 2: Query (real-time)
query = "How do transformers work?"
results = vector_store.similarity_search(query, k=3)
# Returns: top 3 chunks from relevant bucket
```

### Deployment Considerations
- **Setup time**: ~2-5 seconds for 1M documents
- **Query latency**: 10-50ms per query
- **Memory needed**: ~4GB for 1M documents
- **Best for**: Content platforms, FAQ systems, documentation search

---

## 2. HNSW (Hierarchical Navigable Small World)

**Concept**: Navigate through related documents like following friend suggestions until you find the answer.

**When to use**: Real-time Q&A, chatbots, <100M documents.

### Code Example
```python
from langchain.vectorstores import Milvus
from langchain.embeddings import OpenAIEmbeddings

# Step 1: Create HNSW index
vector_store = Milvus.from_texts(
    texts=documents,
    embedding_function=OpenAIEmbeddings(),
    index_name="hnsw_index"
)

# Step 2: Real-time query
results = vector_store.similarity_search(query, k=5)
# Returns: top 5 most relevant chunks in ~5-10ms
```

### Deployment Considerations
- **Query latency**: 5-15ms (fastest for CPU)
- **Memory**: ~8GB per 1M documents
- **Best for**: Chatbots, live search, interactive applications
- **Scaling**: Add more servers for more queries/second

---

## 3. Tree-Based (Ball Tree / KD-Tree)

**Concept**: Navigate like folders: AI → Machine Learning → Transformers.

**When to use**: Small datasets (<1M), structured hierarchies.

### Code Example
```python
from sklearn.neighbors import BallTree
import numpy as np
from sentence_transformers import SentenceTransformer

# Step 1: Embed documents
model = SentenceTransformer('all-MiniLM-L6-v2')
doc_embeddings = model.encode(documents)

# Step 2: Build tree
tree = BallTree(doc_embeddings, leaf_size=30, metric='euclidean')

# Step 3: Query
query_embedding = model.encode([query])[0]
distances, indices = tree.query([query_embedding], k=5)
# Returns: indices of top 5 closest documents
```

### Deployment Considerations
- **Query latency**: 10-30ms
- **Memory**: Low (good for edge devices)
- **Best for**: Mobile apps, small enterprise search, APIs with <1M docs
- **Limitation**: Doesn't scale beyond 10M docs efficiently

---

## 4. LSH (Locality Sensitive Hashing)

**Concept**: Hash query into buckets (#NLP, #Transformers). Find matching bucket.

**When to use**: Streaming data, very fast initial filtering, distributed systems.

### Code Example
```python
from datasketch import MinHashLSH, MinHash
from sentence_transformers import SentenceTransformer

# Step 1: Create LSH index
lsh = MinHashLSH(num_perm=128)

# Step 2: Add documents
for i, doc in enumerate(documents):
    mh = MinHash(num_perm=128)
    for token in doc.split():
        mh.update(token.encode('utf8'))
    lsh.insert(f"doc_{i}", mh)

# Step 3: Query (fast initial filter)
query_mh = MinHash(num_perm=128)
for token in query.split():
    query_mh.update(token.encode('utf8'))
candidates = lsh.query(query_mh)
# Returns: ~100 candidate docs in <1ms
# Then use another index to rank these candidates
```

### Deployment Considerations
- **Query latency**: <1ms (filtering), needs re-ranking
- **Memory**: Minimal
- **Best for**: Pre-filtering before precise ranking, distributed search
- **Tip**: Often combined with HNSW for two-stage retrieval

---

## 5. DiskANN (Microsoft)

**Concept**: Keep massive index on SSD, not RAM. Useful for 1B+ documents.

**When to use**: Billions of documents, cost-constrained infrastructure.

### Code Example
```python
from pyannoy import AnnoyIndex  # Similar concept to DiskANN
import numpy as np

# Step 1: Build index (stores on disk)
index = AnnoyIndex(384, metric='angular')  # 384-dim embeddings

for i, embedding in enumerate(doc_embeddings):
    index.add_item(i, embedding)

index.build(n_trees=10)
index.save('disk_index.ann')  # Stored on SSD

# Step 2: Query (loads from disk on demand)
query_embedding = model.encode([query])[0]
results = index.get_nns_by_vector(query_embedding, 5)
# Returns: top 5 docs, loaded from SSD
```

### Deployment Considerations
- **Query latency**: 20-100ms (depends on SSD speed)
- **Memory required**: ~100MB (vs 100GB for in-memory)
- **Storage**: Must have fast SSD (NVMe recommended)
- **Best for**: Enterprise search, web-scale systems, cost optimization
- **Example use**: Google Search, Bing, enterprise knowledge bases

---

## How to Choose: Decision Tree

```
START
  ├─ Documents < 1M?
  │   └─ YES → Use HNSW (best speed) or Tree (if structured)
  │   └─ NO → Next question
  │
  ├─ Documents 1M - 100M?
  │   └─ YES → Use IVF (good balance) or HNSW (if real-time critical)
  │   └─ NO → Next question
  │
  ├─ Documents > 100M?
  │   ├─ Real-time chat? → Use LSH (filter) + HNSW (rank)
  │   ├─ Budget limited? → Use DiskANN
  │   └─ Standard search? → Use IVF
  │
  └─ Need streaming updates?
      └─ YES → Use LSH or append-friendly index
```

---

## Real-World Example: RAG Pipeline Selection

### Scenario 1: ChatGPT-like Chatbot
```
Query comes in → LSH filters 1M→100k docs (1ms) 
              → HNSW ranks top 10 (5ms) 
              → LLM gets 10 chunks → answers
Total latency: ~50ms ✓ Good for chat
```

### Scenario 2: Enterprise Documentation Search
```
Query → IVF finds topic bucket (20ms) 
     → Return top 20 → LLM generates answer
Total latency: ~100ms ✓ Fine for search
```

### Scenario 3: Billion-Doc Web Search
```
Query → LSH pre-filters (1ms) 
     → DiskANN ranks from disk (50ms) 
     → Return top 5 → Display
Total latency: ~100ms ✓ Acceptable for web search
```

---

## Quick Start: Python

```python
# Install
pip install langchain faiss-cpu sentence-transformers

# Minimal code
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

docs = ["doc1", "doc2", "doc3"]
embeddings = HuggingFaceEmbeddings()

# Create index
vector_store = FAISS.from_texts(docs, embeddings)

# Query
results = vector_store.similarity_search("your question", k=3)
print([doc.page_content for doc in results])
```

---

## Key Takeaway

| You Need | Choose |
|----------|--------|
| Fastest response (chat) | HNSW |
| Biggest documents | DiskANN |
| Cheapest setup | IVF or Tree |
| Streaming/real-time | LSH |
| Small, simple data | Tree |

**Most common in production**: IVF (simplicity) + HNSW (real-time systems)