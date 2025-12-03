# Do You Trim Rows AND Columns When Removing Eigenvectors?

## Quick Answer

**Trim COLUMNS only. Keep ALL ROWS.**

```
Rows = Nodes (keep all)
Columns = Eigenvectors (trim weak ones)
```

---

## Visual Explanation

### Start: 4×4 Matrix with 4 Eigenvectors

```
     eig1   eig2   eig3   eig4
1  [ 0.5    0.5    0.5   -0.5]
2  [ 0.5   -0.5    0.5    0.5]
3  [ 0.5    0.5   -0.5    0.5]
4  [ 0.5   -0.5   -0.5   -0.5]

Rows = 4 nodes
Columns = 4 eigenvectors
```

### After Removing Weak Eigenvector 4

```
Remove column 4 (weakest eigenvector):

     eig1   eig2   eig3   
1  [ 0.5    0.5    0.5  ]
2  [ 0.5   -0.5    0.5  ]
3  [ 0.5    0.5   -0.5  ]
4  [ 0.5   -0.5   -0.5  ]

Rows = 4 nodes (SAME, kept all)
Columns = 3 eigenvectors (trimmed 1)

Matrix went from 4×4 to 4×3
```

---

## Understanding Row vs Column

### Rows = Nodes

```
Each row represents ONE NODE

Row 1 = Node 1 embedding
Row 2 = Node 2 embedding
Row 3 = Node 3 embedding
Row 4 = Node 4 embedding

You ALWAYS need embeddings for ALL nodes
Therefore: KEEP ALL ROWS
```

### Columns = Eigenvectors

```
Each column represents ONE EIGENVECTOR

Column 1 = Eigenvector 1 values
Column 2 = Eigenvector 2 values
Column 3 = Eigenvector 3 values
Column 4 = Eigenvector 4 values (weak, ignore)

You only want STRONG eigenvectors
Therefore: REMOVE WEAK COLUMNS
```

---

## Real Example: 4-Node Graph

### The Eigenvector Matrix

```
What it means:

     eig1   eig2   eig3   eig4
     ↓      ↓      ↓      ↓
1  [ 0.5    0.5    0.5   -0.5]  ← Node 1
2  [ 0.5   -0.5    0.5    0.5]  ← Node 2
3  [ 0.5    0.5   -0.5    0.5]  ← Node 3
4  [ 0.5   -0.5   -0.5   -0.5]  ← Node 4

Each row = complete embedding for one node
Each column = values from one eigenvector
```

### Eigenvalues

```
eig1: eigenvalue = 2.0   (STRONG) ✓✓✓
eig2: eigenvalue = 0.0   (MEDIUM) ✓✓
eig3: eigenvalue = 0.0   (MEDIUM) ✓✓
eig4: eigenvalue = -2.0  (WEAK)   ✗✗✗
```

### Decision: Keep Top 3, Remove eig4

```
Eigenvalues [2.0, 0.0, 0.0, -2.0]
                       ↓    ↓
Keep top 3:    [2.0, 0.0, 0.0]
Ignore last 1:        [-2.0]

Remove column 4 (eig4):

     eig1   eig2   eig3   
1  [ 0.5    0.5    0.5  ]
2  [ 0.5   -0.5    0.5  ]
3  [ 0.5    0.5   -0.5  ]
4  [ 0.5   -0.5   -0.5  ]
```

---

## Larger Example: 100-Node Graph

### Start: 100×100 Matrix

```
     eig1  eig2  eig3 ... eig99  eig100
n1  [ ...   ...   ...  ...  ...    ...  ]
n2  [ ...   ...   ...  ...  ...    ...  ]
n3  [ ...   ...   ...  ...  ...    ...  ]
...
n100[ ...   ...   ...  ...  ...    ...  ]

100 rows (nodes)
100 columns (eigenvectors)
```

### Eigenvalues Sorted

```
eig1:   λ = 5.2  (strong)
eig2:   λ = 3.1  (strong)
...
eig20:  λ = 0.8  (decent)
eig21:  λ = 0.3  (weak)  ← START IGNORING
eig22:  λ = 0.2  (weak)
...
eig100: λ = -0.1 (noise)
```

### Decision: Keep Top 20 Eigenvectors

Remove columns 21-100:

```
     eig1  eig2  eig3 ... eig20
n1  [ ...   ...   ...  ...  ...  ]
n2  [ ...   ...   ...  ...  ...  ]
n3  [ ...   ...   ...  ...  ...  ]
...
n100[ ...   ...   ...  ...  ...  ]

100 rows (nodes) - SAME, kept all
20 columns (eigenvectors) - trimmed to top 20

Matrix: 100×100 → 100×20

Removed 80 columns (weak eigenvectors)
Kept all 100 rows (all nodes)
```

---

## Why Not Trim Rows?

### Scenario: What if we trimmed rows?

```
WRONG approach:
Keep top 20 nodes, remove bottom 80 nodes

Resulting matrix: 20×100

Problem: Now you don't have embeddings for 80 nodes!
         They're missing from your analysis
         
This makes no sense. You need ALL nodes in your output.
```

### Correct Approach

```
CORRECT approach:
Keep all 100 nodes, remove bottom 80 eigenvectors

Resulting matrix: 100×20

Result: Every node has a 20D embedding (not missing any node)
```

---

## The Rule

```
ALWAYS:
- Keep ALL rows (all nodes)
- Trim COLUMNS (weak eigenvectors)

NEVER:
- Trim rows (you lose nodes from analysis)
```

---

## Matrix Dimension Changes

### 4-Node Graph Example

```
Start:        4×4  (4 nodes, 4 eigenvectors)
Use top 3:    4×3  (4 nodes, 3 eigenvectors)
Use top 2:    4×2  (4 nodes, 2 eigenvectors for visualization)

Pattern: n × k where n = nodes (fixed), k = eigenvectors (chosen)
```

### 100-Node Graph Example

```
Start:        100×100  (100 nodes, 100 eigenvectors)
Use top 20:   100×20   (100 nodes, 20 eigenvectors)
Use top 50:   100×50   (100 nodes, 50 eigenvectors)

Pattern: 100 × k where k is your choice
```

### 1000-Node Graph Example

```
Start:        1000×1000 (1000 nodes, 1000 eigenvectors)
Use top 100:  1000×100  (1000 nodes, 100 eigenvectors)

Pattern: 1000 × k where k is your choice
```

---

## Practical Implementation

### Step 1: Compute Eigenvectors

```
For 100-node graph:
Get 100 eigenvectors (100 columns)
Get 100 eigenvalues
```

### Step 2: Sort by Eigenvalue Strength

```
Sort eigenvalues (largest to smallest):
5.2, 3.1, 2.8, 1.5, 0.8, 0.3, 0.2, ...

Keep: 5.2, 3.1, 2.8, 1.5, 0.8 (top 5)
Ignore: 0.3, 0.2, ... (weak)
```

### Step 3: Trim Matrix

```
Original matrix: 100×100
Remove columns 6-100 (keep only columns for top 5 eigenvectors)
Trimmed matrix: 100×5

Each node now has 5D embedding
```

---

## Visual: Trimming Process

### Before

```
Matrix:
     col1  col2  col3  col4  col5  col6  ... col100
r1  [ ■     ■     ■     ■     ■     ■    ...  ■   ]
r2  [ ■     ■     ■     ■     ■     ■    ...  ■   ]
r3  [ ■     ■     ■     ■     ■     ■    ...  ■   ]
...
r100[ ■     ■     ■     ■     ■     ■    ...  ■   ]

100×100 matrix
```

### After (Keep Top 5)

```
Matrix:
     col1  col2  col3  col4  col5
r1  [ ■     ■     ■     ■     ■  ]
r2  [ ■     ■     ■     ■     ■  ]
r3  [ ■     ■     ■     ■     ■  ]
...
r100[ ■     ■     ■     ■     ■  ]

100×5 matrix

Removed: columns 6-100 (95 columns)
Kept: all 100 rows + top 5 columns
```

---

## Summary: Row vs Column Trimming

```
┌─────────────────┬──────────────────────┬─────────────────┐
│ Dimension       │ What It Represents   │ Keep or Trim?   │
├─────────────────┼──────────────────────┼─────────────────┤
│ Rows            │ Nodes                │ KEEP ALL        │
├─────────────────┼──────────────────────┼─────────────────┤
│ Columns         │ Eigenvectors         │ TRIM WEAK ONES  │
├─────────────────┼──────────────────────┼─────────────────┤
│ Result          │ n nodes × k eigs     │ All nodes kept  │
│                 │                      │ Weak eigs removed│
└─────────────────┴──────────────────────┴─────────────────┘
```

---

## Final Answer

**When you ignore weak eigenvectors:**

✓ **DO**: Remove those columns (eigenvectors)
✓ **DO**: Keep all rows (nodes)

✗ **DON'T**: Remove rows (you'd lose nodes)

**Result**: n × k matrix where:
- n = number of nodes (always the same)
- k = number of eigenvectors you keep (smaller than original)

---

## Example Output

### For 4-Node Graph (Keep Top 3)

```
Node embeddings:

Node 1: [0.5, 0.5, 0.5]      ← 3D embedding
Node 2: [0.5, -0.5, 0.5]     ← 3D embedding
Node 3: [0.5, 0.5, -0.5]     ← 3D embedding
Node 4: [0.5, -0.5, -0.5]    ← 3D embedding

Represented as table:

     dim1  dim2  dim3
n1  [ 0.5   0.5   0.5  ]
n2  [ 0.5  -0.5   0.5  ]
n3  [ 0.5   0.5  -0.5  ]
n4  [ 0.5  -0.5  -0.5  ]

4×3 matrix
(4 nodes, 3 eigenvectors)
```

---

# Laplacian Matrix: What It Is

## Adjacency vs Laplacian

You've seen **Adjacency Matrix** (who connects to whom).

**Laplacian Matrix** is a modified version that captures MORE information:

```
Laplacian = Degree Matrix - Adjacency Matrix

Example (4-node graph):

Adjacency Matrix A:
     1  2  3  4
1  [ 0  1  1  0 ]
2  [ 1  0  0  1 ]
3  [ 1  0  0  1 ]
4  [ 0  1  1  0 ]

Degree Matrix D (how many connections each node has):
     1  2  3  4
1  [ 2  0  0  0 ]  ← Node 1 has 2 connections
2  [ 0  2  0  0 ]  ← Node 2 has 2 connections
3  [ 0  0  2  0 ]  ← Node 3 has 2 connections
4  [ 0  0  0  2 ]  ← Node 4 has 2 connections

Laplacian L = D - A:
     1  2  3  4
1  [ 2 -1 -1  0 ]
2  [-1  2  0 -1 ]
3  [-1  0  2 -1 ]
4  [ 0 -1 -1  2 ]
```

### What Laplacian Tells You

```
Diagonal (top-left to bottom-right):
- Shows degree of each node
- Higher number = more connections

Off-diagonal:
- Negative values where edges exist
- Zero where no connection
- Represents "smoothness" constraint
```

---

## Why Laplacian Matters for Graphs

### The Problem with Adjacency

```
Adjacency matrix tells: "Who is connected"

But it doesn't tell:
- How important are connections?
- How similar are neighborhoods?
- What's the global structure?
```

### What Laplacian Solves

```
Laplacian tells:
- Global structure (degree matters)
- Neighborhood similarity (smooth transitions)
- Community boundaries (where Laplacian changes)
```

---

## Laplacian Eigenvectors: The Key

### Why Laplacian Eigenvectors are Better

```
Eigenvectors of Laplacian automatically:
- Keep similar nodes close
- Respect graph structure
- Reveal communities

WHY? Because Laplacian encodes "neighborhood similarity"
in its mathematical structure.
```

### Example: 4-Node Graph

```
Adjacency eigenvectors:
eig1: [0.5, 0.5, 0.5, 0.5]    (all same)
eig2: [0.5, -0.5, 0.5, -0.5]  (left vs right)

Laplacian eigenvectors:
eig1: [0.5, 0.5, 0.5, 0.5]    (same overall)
eig2: [0.1, -0.4, 0.3, -0.2]  (smoother separation!)

Notice: Laplacian eigenvectors show SMOOTHER transitions
        between communities, not hard boundaries
```

---

# Application: Matrix Factorization in Graphs

## What is Matrix Factorization?

Matrix factorization breaks down a matrix into smaller pieces:

```
Large Matrix = Small Matrix 1 × Small Matrix 2

Example:
100×100 matrix = 100×10 matrix × 10×100 matrix
(full)           (compressed)   (basis)

This helps:
- Reduce dimensionality
- Denoise data
- Find latent patterns
```

---

## How Laplacian is Used in Matrix Factorization

### Step 1: Start with Laplacian

```
L = Laplacian matrix (n × n)

For 100-node graph:
L = 100×100 matrix
```

### Step 2: Compute Eigenvectors

```
Get eigenvectors of L:
100 eigenvectors (one per row/column)

Each eigenvector = one pattern in the graph
```

### Step 3: Keep Top k Eigenvectors

```
Sort by eigenvalue strength
Keep top k (usually 10-20)

Discard weak ones
```

### Step 4: Create Factor Matrices

```
Original Laplacian: L (100×100)
                     ↓
Top k eigenvectors → V (100×k)
Top k eigenvalues  → Λ (k×k, diagonal matrix)

Reconstruction:
L ≈ V × Λ × V^T

Where:
V = eigenvector matrix (100×k)
Λ = eigenvalue matrix (k×k)
V^T = transpose of V (k×100)

This is matrix factorization!
```

---

## Real Example: 4-Node Graph Factorization

### Original Laplacian L (4×4)

```
     1   2   3   4
1  [ 2  -1  -1   0 ]
2  [-1   2   0  -1 ]
3  [-1   0   2  -1 ]
4  [ 0  -1  -1   2 ]
```

### Compute Eigenvectors and Eigenvalues

```
Eigenvalue 1: λ₁ = 4.0
Eigenvalue 2: λ₂ = 2.0
Eigenvalue 3: λ₃ = 2.0
Eigenvalue 4: λ₄ = 0.0

Eigenvectors:
v₁ = [0.5, 0.5, 0.5, 0.5]
v₂ = [0.5, -0.5, 0.5, -0.5]
v₃ = [0.5, 0.5, -0.5, -0.5]
v₄ = [-0.5, 0.5, 0.5, -0.5]
```

### Keep Top 3 Eigenvectors

```
Discard eigenvalue 0.0 (it's weak)

V = [0.5   0.5   0.5  ]
    [0.5  -0.5   0.5  ]
    [0.5   0.5  -0.5  ]
    [0.5  -0.5  -0.5  ]

(4×3 matrix)

Λ = [4.0   0    0  ]
    [ 0   2.0   0  ]
    [ 0    0   2.0 ]

(3×3 matrix)
```

### Reconstruction

```
L ≈ V × Λ × V^T

V (4×3) × Λ (3×3) × V^T (3×4) = L_reconstructed (4×4)

This reconstructs (approximately) the original Laplacian!
```

---

## Why This Matters: SDNE Connection

### SDNE Uses Laplacian Factorization

```
SDNE Algorithm:

1. Compute Laplacian L
2. Get eigenvectors V (top k)
3. Use V as initial node embeddings
4. Train neural network to refine them

Step 2 = Matrix Factorization!
```

### The Flow

```
Graph (adjacency)
    ↓
Laplacian Matrix
    ↓
Eigenvectors (matrix factorization)
    ↓
Initial Embeddings (V matrix)
    ↓
SDNE Neural Network
    ↓
Final Refined Embeddings
```

---

## Practical Application Example

### Use Case: Community Detection via Matrix Factorization

```
Graph with 100 nodes:

Step 1: Create Laplacian (100×100)
Step 2: Compute top 5 eigenvectors
Step 3: Create V matrix (100×5)
Step 4: Apply k-means on V
Step 5: Assign nodes to clusters

Result: 5 communities detected!

Why work?
- V captures community structure (from Laplacian eigenvectors)
- Top eigenvectors = strongest community patterns
- Weak eigenvectors ignored (noise)
```

---

## Key Insight: Laplacian vs Adjacency for Factorization

### Adjacency Factorization

```
A = U × Σ × V^T

Problem: Just captures "who connects to whom"
Doesn't capture global structure well
```

### Laplacian Factorization

```
L = V × Λ × V^T

Advantage: Captures neighborhood similarity
Captures community structure
Better for clustering and embedding
```

### Why Laplacian Better?

```
Adjacency matrix:
[0  1  0  0]  ← Says "node 1 connects to node 2"
[1  0  0  1]
[0  0  0  1]
[0  1  1  0]

Laplacian matrix:
[1  -1  0   0]  ← Says "node 1 has 1 connection"
[-1  2  0  -1]  ← "Node 2 has 2 connections"
[0   0  1  -1]  ← "Degree matters!"
[0  -1 -1   2]  ← "Structure matters!"

Laplacian encodes MORE information!
```

---

## Summary: Laplacian and Matrix Factorization

```
Laplacian Matrix:
- Modified version of adjacency
- Degree Matrix - Adjacency Matrix
- Captures neighborhood information

Eigenvectors of Laplacian:
- Reveal graph structure
- Separate communities
- Smooth transitions (no hard boundaries)

Matrix Factorization:
- Break L into component pieces
- L ≈ V × Λ × V^T
- V = eigenvector matrix (compressed representation)
- Λ = eigenvalue matrix (strength of patterns)

Application in Graphs:
- Community detection
- Node clustering
- Dimensionality reduction
- Initialization for deep learning (like SDNE)
```

---

## Why This Matters for SDNE

```
SDNE uses Laplacian Eigenmaps:

1. Laplacian factorization gives initial embeddings
2. These embeddings already respect graph structure
3. Neural network refines them further
4. Result: High-quality embeddings!

Without Laplacian:
- Random initialization (no structure)
- Slow convergence
- Lower quality results

With Laplacian:
- Informed initialization (has structure)
- Fast convergence
- Higher quality results
```