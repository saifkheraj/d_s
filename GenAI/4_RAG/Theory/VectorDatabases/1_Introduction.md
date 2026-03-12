# Vector Database Architecture

This architecture shows how applications interact with a **Vector Database** to store, manage, and search vector data.

---

## 📌 Components

### 1. Applications
- Entry point for sending and receiving requests.
- Can **store, retrieve, update, delete, and query vectors**.

### 2. API (Vector DB)
- Interface between applications and the database.
- Exposes core functions:
  - `store vector()`
  - `retrieve vector()`
  - `update vector()`
  - `delete vector()`
  - `search similar vectors()`

### 3. Indexing Layer
- Builds and maintains efficient vector indexes.
- Organizes stored vectors for **fast similarity search**.
- Works with both the **query processing layer** and the **storage layer**.

### 4. Query Processing Layer
- Takes query vectors from applications.
- Performs similarity checks (e.g., cosine similarity, Euclidean distance).
- Returns the most relevant vectors.

### 5. Storage Layer
- Persists vector data and metadata.
- Ensures durability and reliability.
- Supplies raw data to the indexing layer when needed.

---

## 🔄 Data Flow

1. **Applications** send vectors or queries to the **API**.  
2. **API** forwards requests to the **Indexing Layer**:
   - Store/update/delete → sent to **Storage Layer**.  
   - Query → processed by the **Query Processing Layer**.  
3. **Indexing Layer** ensures efficient search and retrieval.  
4. Results are sent back to the **Applications**.

---

## 🚀 Key Operations

- **Store Vector** → Save embeddings in storage and index them.  
- **Retrieve Vector** → Fetch vectors using ID or metadata.  
- **Update Vector** → Modify an existing stored vector.  
- **Delete Vector** → Remove a vector from both index and storage.  
- **Search Similar Vectors** → Return top-k closest vectors to a query vector.  
