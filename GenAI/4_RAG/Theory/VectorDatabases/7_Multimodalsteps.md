# CLIP Image–Text Embedding Pipeline (Step‑by‑Step)

This document explains **exactly what happens in CLIP** when an image or text is converted into an embedding and how similarity is computed.

---

## Big Picture

> **CLIP converts images and text into the same 512‑dimensional vector space and compares them using cosine similarity.**

---

## Image → 512‑D Embedding

### Step 1: Input Image

* RGB image
* Resized to **224 × 224** pixels

---

### Step 2: Patch Extraction (ViT‑B/32)

* Patch size: **32 × 32**
* Image size: **224 × 224**

```
224 / 32 = 7 patches per side
Total patches = 7 × 7 = 49
```

Each patch is a small image region containing local visual information.

---

### Step 3: Patch Embedding

* Each patch has shape `32 × 32 × 3 = 3,072` pixel values
* Patch is:

  1. Flattened
  2. Passed through a linear layer

Result:

* Each patch → **embedding vector** (e.g. 768‑D)

---

### Step 4: Position Embeddings

* A learnable **position embedding** is added to each patch embedding
* This tells the model *where* each patch is located in the image

Without this, the model would not know spatial relationships.

---

### Step 5: Transformer Encoder

* **12 self‑attention layers**
* All patches attend to each other
* Enables global understanding (objects, scenes, relationships)

---

### Step 6: Global Aggregation

* Patch information is pooled
* A global image representation is formed

This vector represents the **entire image**.

---

### Step 7: Projection + Normalization

* Linear projection → **512‑D vector**
* L2 normalization:

```python
image_embedding = image_embedding / ||image_embedding||
```

✅ **Final result:** 512‑D normalized image embedding

---

## Text → 512‑D Embedding

### Step 1: Input Text

Example:

```
"a cat sitting on grass"
```

---

### Step 2: Tokenization

* Text → tokens
* Special tokens added
* Max length: **77 tokens**
* Longer text is truncated

---

### Step 3: Token + Position Embeddings

* Each token → embedding vector
* Position embeddings encode word order

---

### Step 4: Transformer Encoder

* **12 transformer layers**
* Bidirectional self‑attention
* Contextual meaning is learned

---

### Step 5: Text Pooling

* Special end‑of‑text token is used
* Represents the full sentence meaning

---

### Step 6: Projection + Normalization

* Linear projection → **512‑D vector**
* L2 normalization

```python
text_embedding = text_embedding / ||text_embedding||
```

✅ **Final result:** 512‑D normalized text embedding

---

## Image–Text Similarity

After encoding:

```
Image embedding: [512 numbers]
Text embedding:  [512 numbers]
```

### Similarity Calculation

```python
similarity = image_embedding · text_embedding
```

Because both vectors are normalized:

```
Dot product = cosine similarity
```

* High similarity → semantically related
* Low similarity → unrelated

---

## Important Training Insight

❗ **Image and text encoders are NOT trained separately.**

* Both encoders are trained **together**
* One shared **contrastive loss** aligns them
* Gradients update both encoders simultaneously

This is why image and text embeddings live in the same semantic space.

---

## Mental Model

```
Image Encoder:  "What does this look like?"
Text Encoder:   "What does this mean?"
Projection:     "Map both into the same concept space"
Similarity:     "Are they talking about the same thing?"
```

---

## Final Summary

* Image → patches → transformer → **512‑D embedding**
* Text → tokens → transformer → **512‑D embedding**
* Both are normalized
* Similarity = cosine similarity (dot product)

✔️ This is the complete CLIP embedding pipeline.
