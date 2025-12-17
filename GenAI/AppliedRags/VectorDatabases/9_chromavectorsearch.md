# ChromaDB Multimodal Embeddings – Basic Steps

This README explains the **basic concept and steps** to use **ChromaDB** for storing and querying **multimodal embeddings (text + images)**. The goal is understanding, not implementation details.

---

## 1. What We Are Doing (Big Picture)

* We have **images** and **text descriptions**
* We want both to live in the **same vector space**
* We use a **multimodal embedding model (CLIP)**
* ChromaDB stores the embeddings and lets us **search by similarity**

You can:

* Search images using text
* Search text using an image

---

## 2. Import Required Components

We need four things:

* **ChromaDB** → vector database
* **Embedding function** → converts text & images into vectors
* **Data loader** → loads image files when needed
* **Basic utilities** → file handling and CSV loading

Key idea:

> Chroma can generate embeddings for us using built-in models.

---

## 3. Configure the Embedding Model

* Use a **CLIP-based model** (`ViT-B-32`)
* This model understands **both images and text**
* Text and images become vectors of the **same dimension**

```python
from chromadb.utils import embedding_functions

embedding_function = embedding_functions.OpenCLIPEmbeddingFunction(
    model_name="ViT-B-32"
)
```

Why this matters:

> Similar text and images end up **close together** in vector space.

---

## 4. Configure the Data Loader

* Images are stored **outside ChromaDB**
* Chroma stores only the **URI (file path)**
* The loader fetches images when embedding or querying

```python
from chromadb.utils.data_loaders import ImageLoader

data_loader = ImageLoader()
```

This keeps the database lightweight.

---

## 5. Create a Chroma Client

* The client manages:

  * Collections
  * Embeddings
  * Queries

```python
import chromadb

client = chromadb.Client()
```

Think of it as the **database connection**.

---

## 6. Create a Collection

A collection is like a table in a database.

It includes:

* A **name**
* An **embedding function**
* A **similarity metric** (cosine is common)
* A **data loader** (for images)

```python
collection = client.create_collection(
    name="multimodal_embeddings_collection",
    embedding_function=embedding_function,
    data_loader=data_loader,
    metadata={"hnsw:space": "cosine"}
)
```

All items added here share the same embedding logic.

---

## 7. Prepare the Data

We prepare:

* Image IDs
* Image file paths
* Text descriptions
* Description IDs

```python
import pandas as pd
import os

df = pd.read_csv("descriptions.csv")
image_dir = "images/"

image_ids, image_paths = [], []
desc_ids, descriptions = [], []

for i, row in df.iterrows():
    img_path = os.path.join(image_dir, row["image_file"])
    image_ids.append(f"img_{i}")
    image_paths.append(img_path)
    desc_ids.append(f"desc_{i}")
    descriptions.append(row["description"])
```

Key idea:

> Images and text are treated as **separate entries**, but linked via metadata.

---

## 8. Add Data to the Collection

### Add Images

```python
for img_id, img_path, desc in zip(image_ids, image_paths, descriptions):
    collection.add(
        ids=[img_id],
        uris=[img_path],
        metadatas=[{"image_uri": img_path, "description": desc}]
    )
```

Chroma:

* Loads the image
* Generates an embedding
* Stores the vector

### Add Text Descriptions

```python
for desc_id, desc, img_path in zip(desc_ids, descriptions, image_paths):
    collection.add(
        ids=[desc_id],
        documents=[desc],
        metadatas=[{"image_uri": img_path, "description": desc}]
    )
```

Now both image and text live in the **same vector space**.

---

## 9. Query the Collection

### Text → Image Search

```python
results = collection.query(
    query_texts=["a dog playing on the beach"],
    n_results=3
)
```

### Image → Text / Image Search

```python
results = collection.query(
    query_uris=["images/sample.jpg"],
    n_results=3
)
```

What Chroma does:

1. Embed the query
2. Compare with stored vectors
3. Return closest matches

---

## 10. (Optional) Delete the Collection

```python
client.delete_collection("multimodal_embeddings_collection")
```

* Removes all vectors and metadata
* Useful for cleanup or experiments

---

## 11. Key Concepts to Remember

* **Embeddings = numbers representing meaning**
* **Multimodal models align text & images**
* **Chroma stores vectors, not raw files**
* **Similarity search = nearest vectors**

If you understand this flow, you understand how **most multimodal RAG systems work**.

---

✅ Simple, scalable, and open-source.
