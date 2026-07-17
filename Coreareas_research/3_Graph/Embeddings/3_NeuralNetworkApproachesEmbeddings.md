# Deep Autoencoders, SDNE, and LINE: Simple Explanation

## 1. Deep Autoencoders

### What is it?

A neural network that **compresses data and then reconstructs it**.

```
Input (complex)  →  COMPRESS  →  Small summary  →  DECOMPRESS  →  Output (reconstructed)
                    (Encoder)      (Embedding)        (Decoder)
```

### For Graphs:

```
Adjacency Matrix [who connects to whom]
        ↓
    ENCODER (neural net)
        ↓
    Embedding [64 numbers per node] ← This is our representation
        ↓
    DECODER (neural net)
        ↓
    Reconstructed Adjacency Matrix
```

### Why useful?

The embedding (64 numbers) becomes a compact summary of each node's connections.

---

## 2. SDNE (Structural Deep Network Embedding)

### What is it?

**Autoencoder + 2 extra rules**

```
SDNE Loss = Autoencoder Loss + Rule 1 + Rule 2
```

### Rule 1: First-Order Proximity

**"If two nodes are directly connected, their embeddings should be close"**

```
Graph:  Alice -------- Bob
        
Embedding: Alice [0.1, 0.2, ...] should be close to Bob [0.12, 0.19, ...]
           Distance = 0.015 (small) ✓

If far: Distance = 0.8 (large) ✗ → Add penalty to loss
```

### Rule 2: Second-Order Proximity

**"If two nodes have similar neighborhoods, their embeddings should be close"**

```
Graph:
    A connects to: {B, C}
    D connects to: {B, C}
    
→ A and D have SAME neighbors (100% overlap)
→ Their embeddings should be close, even if no direct edge

Embedding: A [0.1, 0.2] should be close to D [0.11, 0.21]
           Distance = 0.015 ✓
           
If far: Add penalty to loss
```

### Why "Semi-Supervised"?

```
Autoencoder part = Unsupervised (no labels needed, just reconstruct)
Rule 1 + Rule 2 = Supervised (we tell it what to do)
```

### How it works:

```
Iteration 1:
    Total Loss = 2.50
    Update weights
    
Iteration 2:
    Total Loss = 2.45 (better!)
    Update weights
    
... repeat until loss stops improving ...

Final: Embeddings that satisfy all 3 rules
```

### SDNE Summary:

- ✓ High quality embeddings
- ✗ Slow (full adjacency matrix)
- ✗ High memory
- Best for: Small-medium graphs (< 100K nodes)

---

## 3. LINE (Large-Scale Network Embedding)

### The Key Problem with SDNE:

```
For 1 million nodes:
- Adjacency matrix = 1M × 1M = 1 TB RAM (impossible!)
- Processing all edges = too slow
```

### The Solution: Edge Sampling

**Don't process all edges. Sample random edges and learn from them.**

```
Instead of:        Do:
All edges      →   Random sample of edges
                   Learn from sample
                   Repeat many times
```

### LINE's Two Objectives:

#### Objective 1: First-Order Proximity (Edge Sampling)

```
Sample edge (Alice, Bob)
    
Make: similarity(Alice_embedding, Bob_embedding) HIGH

How? Dot product of embeddings
     Alice [0.1, 0.2, ...] · Bob [0.12, 0.19, ...] = high value ✓
     
If low: Update to increase similarity
```

#### Objective 2: Second-Order Proximity (Context Sampling)

```
Sample edge (Alice, Bob)

Alice's neighbors: {Charlie, David, Eve}
Bob's neighbors: {Frank, Grace}

Goal: Make Alice's embedding close to her neighbors' embeddings
      Make Bob's embedding close to his neighbors' embeddings

How? Update embeddings so each node attracts its neighbors
```

### Why it's Fast:

```
Processing:
- Sample 100K edges per iteration (not 1 trillion)
- Process those 100K
- Repeat until convergence

Memory:
- Only store sampled edges (much smaller than full matrix)

Result: 
- Much faster than SDNE
- Slightly lower quality (but still good)
```

### LINE Algorithm Simple View:

```
Step 1: Sample random edge (Alice, Bob)
        → Make their embeddings similar
        
Step 2: Sample random edge (Charlie, David)
        → Make their embeddings similar
        
Step 3: Sample edge (Alice, Frank)
        → Make Alice's context similar to Frank's context
        
... repeat 1000s of times ...

Final: All nodes have good embeddings
```

### LINE Summary:

- ✓ Scales to millions of nodes
- ✓ Fast (minutes instead of hours)
- ✓ Works with directed/weighted graphs
- ✗ Slightly lower quality than SDNE
- Best for: Large graphs (> 100K nodes)

---

## 4. SDNE vs LINE at a Glance

```
┌────────────────┬──────────────────────┬──────────────────────┐
│ Aspect         │ SDNE                 │ LINE                 │
├────────────────┼──────────────────────┼──────────────────────┤
│ What it does   │ Autoencoder + rules  │ Edge sampling + rules │
│ Graph size     │ Small-medium (100K)  │ Large (1M+)          │
│ Speed          │ Slow (hours)         │ Fast (minutes)       │
│ Quality        │ Highest              │ Good                 │
│ Memory         │ High                 │ Low                  │
│ When to use    │ Need best quality    │ Need speed/scale     │
└────────────────┴──────────────────────┴──────────────────────┘
```

### Choose Based On:

```
"Do I have millions of nodes?"
    ├─ Yes → Use LINE (SDNE can't handle it)
    └─ No → Use SDNE (better quality)

"Can I wait hours for better embeddings?"
    ├─ Yes → Use SDNE
    └─ No → Use LINE

"Do I need exact precision or approximate is OK?"
    ├─ Need exact → SDNE
    └─ Approximate OK → LINE
```

---

## 5. Visualizing Embeddings

After embedding, you have 64-dimensional vectors per node. Humans can't see 64D. Need 2D/3D.

### t-SNE (Show Clusters)

```
What: Keep nearby points nearby in 2D
Result: Beautiful clusters visible
Speed: Slow
Usefulness: Great for finding communities

Example:
    High-D: Alice [0.1, 0.2, 0.3, ...] close to Bob
    2D view after t-SNE: Alice ● Bob (still close) ✓
```

### PCA (Show Main Directions)

```
What: Find the 2 most important directions in data
Result: Can interpret what each axis means
Speed: Fast
Usefulness: Good for understanding overall patterns

Example:
    PC1 axis: "How connected is this node"
    PC2 axis: "What role does this node play"
```

### Which to use?

```
"I want to find communities/clusters?"
    → Use t-SNE

"I want fast results / interpretable axes?"
    → Use PCA

"I want to publish pretty visualizations?"
    → Use t-SNE
```

---

## Simple Summary

| Concept | Meaning |
|---------|---------|
| **Autoencoder** | Neural net that compresses and reconstructs data to learn representations |
| **SDNE** | Autoencoder that preserves first + second-order proximities (slow, high quality) |
| **LINE** | Edge sampling method that preserves first + second-order proximities (fast, scalable) |
| **t-SNE** | Visualization that shows clusters in 2D |
| **PCA** | Visualization that shows main variation directions in 2D |

---

## When to Use Each Algorithm

```
Small graph (< 100K nodes) → SDNE
Large graph (> 1M nodes) → LINE
Medium graph (100K - 1M) → Either (depends on your resources)

Need best quality → SDNE
Need to be fast → LINE
Need pretty visualization → t-SNE
Need to understand patterns → PCA
```