# Measuring Similarity Between Embeddings

Vector embeddings represent data as points in multi-dimensional space. We use distance metrics to measure how similar or different two embeddings are.

## Euclidean Distance

**What it measures:** The straight-line distance between two points in space.

![alt text](<Screenshot 2025-11-02 at 5.43.58 PM.png>)

**Formula:**

$$d(u, v) = \sqrt{\sum_{i=1}^{n} (u_i - v_i)^2}$$

**How it works:** Calculates how far apart two vectors are, considering both direction and magnitude.

**Real-world example:** Finding the nearest store location to your current position. If two stores are in different directions but one is closer overall, Euclidean distance identifies it correctly.

**Key trait:** Magnitude-sensitive. A long vector pointing left differs significantly from a short vector pointing left.

**Best for:** Clustering locations, regression tasks, or scenarios where absolute differences matter.

---

## Cosine Similarity

**What it measures:** The angle between two vectors, regardless of their length.

![alt text](<Screenshot 2025-11-02 at 5.51.43 PM.png>)

**Formula:**

$$\text{similarity}(u, v) = \cos(\theta) = \frac{u \cdot v}{\|u\| \times \|v\|} = \frac{\sum_{i=1}^{n} (u_i \times v_i)}{\sqrt{\sum_{i=1}^{n} u_i^2} \times \sqrt{\sum_{i=1}^{n} v_i^2}}$$

**How it works:** Compares direction only. Two vectors pointing the same way have high similarity, even if one is longer.

**Real-world example:** Comparing product reviews. A short review saying "great product" and a long review saying "absolutely fantastic product" both express similar sentiment, even though they differ in length.

**Key trait:** Magnitude-invariant and scale-independent. Perfect for text and high-dimensional data.

**Best for:** Text analysis, recommendation systems, document similarity, plagiarism detection.

**Range:** -1 to 1 (1 = identical direction, 0 = unrelated, -1 = opposite).

---

## Dot Product

**What it measures:** Both the direction and magnitude of vectors combined.

![alt text](<Screenshot 2025-11-02 at 6.05.41 PM.png>)

The diagram shows:

- Vector u (black arrow)

- Vector v (black arrow)

- Projection of u onto v (shorter arrow on v)

- The dashed line dropping u onto v

- Angle  between u and v

This projection represents how much of u points along v.

**Dot Product Formula**



Where:

|u| = magnitude of u

|v| = magnitude of v

θ = directional alignment

**Formula:**

Geometric representation:
$$u \cdot v = \|u\| \times \|v\| \times \cos(\theta)$$

Algebraic representation:
$$u \cdot v = \sum_{i=1}^{n} (u_i \times v_i)$$

**How it works:** Reflects how much two vectors align in both direction and strength.

**Real-world example:** Movie recommendations. Two users with similar tastes (direction) and similar engagement levels (magnitude) receive higher scores than users who just share tastes but one is barely active.

**Key trait:** Unbounded and sensitive to vector size. Larger values indicate stronger alignment.

**Best for:** Machine learning models, relevance ranking, correlation analysis.

---

## Why Dot Product and Cosine Similarity are Different

Both use cosine, but they measure fundamentally different things:

### The Mathematical Difference

**Cosine Similarity** removes the magnitude by normalizing:
$$\text{similarity}(u, v) = \frac{u \cdot v}{\|u\| \times \|v\|}$$

**Dot Product** keeps the magnitude:
$$u \cdot v = \|u\| \times \|v\| \times \cos(\theta)$$

Notice: Cosine similarity = (Dot product) / (magnitudes)

### The Practical Difference

**Example:** Comparing two movie ratings

User A rates: [5, 5, 5] (loved 3 movies)  
User B rates: [10, 10, 10] (loved same 3 movies, but rated higher)

| Metric | Result | Interpretation |
|--------|--------|-----------------|
| **Cosine Similarity** | 1.0 | Perfectly similar taste (same direction) |
| **Dot Product** | 150 | User B's engagement is stronger |

**Cosine similarity** says: "They like the same movies" (direction only)  
**Dot product** says: "They like the same movies AND User B is way more engaged" (direction + magnitude)

### When to Use Each

- **Cosine Similarity:** When you only care about *what* they like, not *how much*
  - Example: Finding similar documents regardless of length
  
- **Dot Product:** When magnitude matters as much as direction
  - Example: Ranking by both preference alignment AND engagement level
  - Example: Neural network layer operations where signal strength matters

---

| Metric | Considers Magnitude | Considers Direction | Best Use Case |
|--------|-------------------|-------------------|---------------|
| Euclidean Distance | ✓ | ✓ | Spatial clustering, regression |
| Cosine Similarity | ✗ | ✓ | Text analysis, recommendations |
| Dot Product | ✓ | ✓ | ML models, ranking systems |