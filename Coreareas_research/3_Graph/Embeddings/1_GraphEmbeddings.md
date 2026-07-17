# Graph Embeddings: A Comprehensive Guide

## Introduction

Graphs are everywhere—social networks, recommendation systems, protein interactions, and patient care networks. But here's the challenge: **graphs are non-euclidean data structures**, meaning we can't feed them directly into machine learning algorithms. Graph embeddings solve this problem by converting graphs into numerical vectors.

---

## Part 1: Fundamentals

### What Gets Embedded?

Graph embeddings can work at different levels:

- **Node Embeddings** — Each individual node becomes a vector. Most common use case.
- **Edge Embeddings** — Each individual edge (connection) becomes a vector.
- **Graph-level Embeddings** — The entire graph becomes a single vector. Useful for comparing whole graphs.

### Why Do We Need Embeddings?

Machine learning algorithms expect clean numerical input. Graphs are visual and structural, but not directly numerical. Embeddings bridge this gap by converting graph structure into dense vectors that preserve important relationships.

### The ML Pipeline

```
Graph Data 
    ↓
Preprocessing
    ↓
Generate Embeddings (Convert to vectors)
    ↓
ML Task (Classification, Link Prediction, etc.)
    ↓
Results
```

### Popular Python Packages

- **karateclub** — Implements many graph embedding algorithms
- **graphvite** — Includes DeepWalk, LINE, and node2vec
- **GraphEmbedding** — Covers DeepWalk, LINE, node2vec, SDNE, and struc2vec
- **GEM** — Features Laplacian Eigenmaps, graph factorization, and more

---

## Part 2: Matrix Factorization Approach

### The Big Picture: What is Matrix Factorization?

**Intuition:** Imagine you have a huge spreadsheet showing which patients visited which departments in a hospital. Instead of storing this massive table, you represent each patient and each department as a small vector. When you multiply these vectors together, you can predict which departments each patient will likely visit.

**Mathematical Definition:**

Matrix factorization decomposes a large matrix into a product of smaller matrices:

$$A = U \times V^T$$

Where:
- **A** = Original matrix (dimensions: $n \times m$)
- **U** = First matrix (dimensions: $n \times k$)
- **V** = Second matrix (dimensions: $m \times k$)
- **k** = Embedding dimension (latent factors, where $k \ll n, m$)
- **V^T** = Transpose of V

**Why This Works:**

Memory efficiency comparison:
```
Without factorization:  Store n × m = 1000 × 1000 = 1,000,000 numbers
With factorization:     Store (n × k) + (m × k) = (1000 × 50) + (1000 × 50) = 100,000 numbers
                        → 90% memory savings!
```

**What Gets Learned Automatically:**
- All values in matrices U and V
- Values that best approximate the original matrix A

**What You Choose:**
- Embedding dimension k (e.g., 50, 100, 200)

---

### Graph Factorization (GF): A Special Case

**Intuition:** Think of a hospital patient referral network where doctors refer patients to each other. You want to learn embeddings that capture which doctors work together. Instead of a huge table showing all possible doctor pairs, represent each doctor as a vector. Multiplying two doctors' vectors predicts how likely they are to collaborate.

**Why It's Special for Graphs:**

Graphs are **symmetric** - if patient A visits department B, then department B is visited by patient A. This symmetry means we can use:

$$W \approx Y \times Y^T$$

Instead of two different matrices (U and V), we use ONE matrix Y repeated as itself transposed. This is more efficient.

**Comparison:**
```
General Matrix Factorization: A = U × V^T  (U and V are different)
Graph Factorization:          W = Y × Y^T  (Y is used twice)
```

**Mathematical Foundation:**

The adjacency matrix is:

$$W = \begin{bmatrix} 0 & 1 & 1 & 0 \\ 1 & 0 & 1 & 1 \\ 1 & 1 & 0 & 1 \\ 0 & 1 & 1 & 0 \end{bmatrix}$$

We learn embeddings Y such that:

$$W_{ij} \approx \langle Y_i, Y_j \rangle = Y_i \cdot Y_j^T$$

Where $\langle Y_i, Y_j \rangle$ is the dot product (prediction of connection).

**The Optimization Problem:**

Find embeddings Y that minimize:

$$\mathcal{L}(Y) = \sum_{(i,j) \in E} (W_{ij} - \langle Y_i, Y_j \rangle)^2 + \lambda \sum_{i} ||Y_i||^2$$

Where:
- First term = reconstruction error (actual vs predicted)
- Second term = regularization (prevents overfitting)
- $\lambda$ = regularization strength parameter

**Real Example with Numbers:**

Hospital network: 5 departments
Connections: Cardiology↔Radiology, Cardiology↔Emergency, Radiology↔Emergency, Emergency↔ICU, Radiology↔ICU

Adjacency matrix:
$$W = \begin{bmatrix} 0 & 1 & 1 & 0 & 0 \\ 1 & 0 & 1 & 1 & 0 \\ 1 & 1 & 0 & 1 & 1 \\ 0 & 1 & 1 & 0 & 1 \\ 0 & 0 & 1 & 1 & 0 \end{bmatrix}$$

Learned embeddings (k=2):
```
Cardiology:    [0.8, 0.3]
Radiology:     [0.7, 0.8]
Emergency:     [0.9, 0.6]
ICU:           [0.4, 0.8]
Orthopedics:   [0.2, 0.1]
```

Predictions (dot products):
```
Cardiology-Radiology = (0.8)(0.7) + (0.3)(0.8) = 0.56 + 0.24 = 0.80 ≈ 1 ✓
Cardiology-ICU = (0.8)(0.4) + (0.3)(0.8) = 0.32 + 0.24 = 0.56 ≈ 0 ✓
Radiology-ICU = (0.7)(0.4) + (0.8)(0.8) = 0.28 + 0.64 = 0.92 ≈ 1 ✓
```

**When to Use Graph Factorization:**

✓ Large graphs (millions of nodes)
✓ Memory efficiency critical
✓ Undirected graphs
✓ Link prediction needed
✓ Sparse graphs

**Parameters:**
```
YOU CHOOSE:
- k (embedding dimension, e.g., 50 or 100)

ALGORITHM LEARNS:
- All numbers in embedding matrix Y
```

---

## Part 3: Locally Linear Embedding (LLE)

### The Big Picture: What is LLE?

**Intuition:** Imagine a hospital workflow where each nurse works with a specific team of nurses. To understand a nurse's behavior, you only need to look at their immediate team, not the entire hospital. LLE learns embeddings by saying "each nurse is well-represented as a weighted combination of their team members."

**Core Principle:**

$$X_i = \sum_{j \in N_i} W_{ij} X_j$$

This says: "Node i can be reconstructed as a weighted sum of its K nearest neighbors."

**Step-by-Step Process:**

**Step 1: Find K-Nearest Neighbors**

For each node, identify K closest connected nodes:

$$N_i = \{j_1, j_2, ..., j_K\}$$

Example with K=3:
```
Nurse A's team: [Nurse B, Nurse C, Nurse D]
Nurse B's team: [Nurse A, Nurse C, Nurse E]
```

**Step 2: Compute Reconstruction Weights**

Find weights $W_{ij}$ that minimize reconstruction error:

$$\Phi(W) = \sum_{i=1}^{n} \left| X_i - \sum_{j \in N_i} W_{ij} X_j \right|^2$$

Subject to:
$$\sum_{j \in N_i} W_{ij} = 1 \quad \text{(weights sum to 1, like percentages)}$$

**Real Example:**

For Nurse A with team members B, C, D:
```
Nurse A = 50% Nurse B + 30% Nurse C + 20% Nurse D
Check: 0.5 + 0.3 + 0.2 = 1.0 ✓
```

These percentages show: "Nurse A's work style is mostly like B, somewhat like C, and a bit like D."

**Step 3: Learn Low-Dimensional Embeddings**

Use these weights to find embeddings in lower dimensions:

$$\Phi(Y) = \sum_{i=1}^{n} \left| Y_i - \sum_{j \in N_i} W_{ij} Y_j \right|^2$$

Subject to:
$$\frac{1}{n} \sum_{i=1}^{n} Y_i = 0 \quad \text{(centered)}$$
$$\frac{1}{n} \sum_{i=1}^{n} Y_i Y_i^T = I \quad \text{(unit variance)}$$

The result is embedding matrix Y where each row is a node's embedding.

**Hospital Example:**

Hospital workflow: 50 nurses
You decide: K=5 (each nurse considers 5 team members)
You decide: embedding dimension = 16

```
Algorithm learns:
Nurse 1 team: [2, 5, 7, 10, 15]
Weights: [0.40, 0.25, 0.20, 0.10, 0.05]

Nurse 1 embedding (learned): [0.2, -0.5, 0.1, 0.3, ..., -0.2] (16 numbers)
Nurse 2 embedding (learned): [0.3, 0.2, -0.4, 0.1, ..., 0.5] (16 numbers)
...

Result: 50 nurses × 16 dimensions = embedding matrix
```

**Key Properties:**

- Preserves local neighborhood structure
- Doesn't capture global patterns
- Sensitive to K parameter choice

**When to Use LLE:**

✓ Small to medium graphs (< 100K nodes)
✓ Local neighborhood structure important
✓ Interpretable results needed
✓ Undirected graphs

**Parameters:**
```
YOU CHOOSE:
- K (number of neighbors, e.g., 5 or 10)
- Embedding dimension (e.g., 16)

ALGORITHM LEARNS:
- Neighbor weights (percentages)
- Embedding vectors that preserve these weights
```

---

## Part 4: Relationship Between Approaches

**Conceptual Hierarchy:**

$$\text{Matrix Factorization (General)} \rightarrow \text{Graph Factorization (Special Case for Graphs)}$$

```
Matrix Factorization:
- Applies to ANY matrix
- Formula: A = U × V^T
- Two different matrices U and V

Graph Factorization:
- Specific to GRAPHS
- Formula: W = Y × Y^T
- One matrix Y (because graphs are symmetric)
- Special case of matrix factorization

LLE:
- Completely different approach
- NOT matrix factorization based
- Focuses on local neighborhoods
- Formula: X_i = Σ W_ij X_j
```

---

## Part 5: Healthcare Applications - Flow Optimization

### Application 1: Patient Journey Optimization - Hospital Department Network

**Problem:** Hospital wants to optimize patient flow through different departments to reduce wait times and identify bottlenecks where patients get stuck.

**Real Hospital Scenario:**

A mid-sized hospital has these departments:
- **ER** (Emergency Room) - Entry point for acute patients
- **Rad** (Radiology) - Imaging/diagnostic services
- **Card** (Cardiology) - Heart specialist care
- **ICU** (Intensive Care Unit) - Critical patients
- **Surg** (Surgery) - Operating rooms
- **Ward** (General Ward) - Recovery/observation

**Graph Structure:**
- **Nodes:** 6 hospital departments
- **Edges:** Patient referrals between departments
- **Edge Weight:** Number of patients transferred per month

**Real Patient Flow Data:**

```
Patient Transfer Flow (patients/month):
ER → Rad: 150 patients (diagnostic imaging needed)
ER → Card: 80 patients (cardiac symptoms)
ER → Surg: 120 patients (urgent surgery)
ER → ICU: 40 patients (critical condition)
ER → Ward: 90 patients (stable, need observation)

Rad → Card: 60 patients (cardiac imaging findings)
Rad → Surg: 50 patients (imaging confirms surgery needed)
Rad → ICU: 20 patients (critical findings)

Card → ICU: 70 patients (cardiac critical care)
Card → Surg: 40 patients (cardiac surgery needed)
Card → Ward: 85 patients (post-cardiology care)

Surg → ICU: 100 patients (post-surgery critical care)
Surg → Ward: 140 patients (post-surgery recovery)

ICU → Ward: 110 patients (stable enough to discharge from ICU)
```

**Adjacency Matrix (Patient Flow):**

$$W = \begin{bmatrix} 0 & 150 & 80 & 120 & 40 & 90 \\ 150 & 0 & 60 & 50 & 20 & 0 \\ 80 & 60 & 0 & 70 & 40 & 85 \\ 120 & 50 & 70 & 0 & 100 & 140 \\ 40 & 20 & 40 & 100 & 0 & 110 \\ 90 & 0 & 85 & 140 & 110 & 0 \end{bmatrix}$$

Where rows/columns = [ER, Rad, Card, Surg, ICU, Ward]

---

**Step 1: Learn Embeddings Using Graph Factorization**

We want to find embeddings for each department such that:

$$W_{ij} \approx \langle Y_i, Y_j \rangle = \text{embedding}_i \cdot \text{embedding}_j$$

Choose embedding dimension: **k = 3** (3 latent factors)

**The Algorithm Learns:**

```
ER embedding:      [0.8, 0.5, 0.2]
Radiology:         [0.7, 0.6, 0.3]
Cardiology:        [0.6, 0.8, 0.4]
Surgery:           [0.9, 0.4, 0.7]
ICU:               [0.5, 0.7, 0.9]
Ward:              [0.4, 0.3, 0.8]
```

**What These Numbers Mean:**

- **First dimension (0.8, 0.7, ...)** = "Diagnostic/Initial Assessment"
  - ER (0.8) - highest, main entry point
  - Rad (0.7) - diagnostic imaging
  - Card (0.6) - specialized diagnosis
  
- **Second dimension (0.5, 0.6, ...)** = "Specialist Consultation"
  - Card (0.8) - cardiac specialist
  - ICU (0.7) - critical care specialist
  
- **Third dimension (0.2, 0.3, ...)** = "Post-Care/Recovery"
  - ICU (0.9) - critical patients after acute care
  - Ward (0.8) - recovery ward
  - Surg (0.7) - post-surgical patients

---

**Step 2: Verify Predictions Against Real Data**

Let's verify the learned embeddings can predict actual patient flows:

**Prediction 1: ER → Radiology**
```
Actual flow:     150 patients/month
Predicted score: (0.8)(0.7) + (0.5)(0.6) + (0.2)(0.3) 
               = 0.56 + 0.30 + 0.06 = 0.92 ✓
(High score = high traffic ✓)
```

**Prediction 2: ER → Ward** 
```
Actual flow:     90 patients/month
Predicted score: (0.8)(0.4) + (0.5)(0.3) + (0.2)(0.8)
               = 0.32 + 0.15 + 0.16 = 0.63 ✓
(Medium score = medium traffic ✓)
```

**Prediction 3: Radiology → ICU** 
```
Actual flow:     20 patients/month (LOW)
Predicted score: (0.7)(0.5) + (0.6)(0.7) + (0.3)(0.9)
               = 0.35 + 0.42 + 0.27 = 1.04
Expected:       20 patients/month ✗
(This seems high for actual traffic!)
```

**Prediction 4: Surgery → ICU**
```
Actual flow:     100 patients/month (HIGH)
Predicted score: (0.9)(0.5) + (0.4)(0.7) + (0.7)(0.9)
               = 0.45 + 0.28 + 0.63 = 1.36 ✓
(High score = high traffic ✓)
```

---

**Step 3: Identify Bottlenecks**

**Method: Embedding Similarity & Congestion Analysis**

Calculate congestion for each department by examining incoming traffic:

**Department Connectivity Matrix (Incoming Patients):**

```
ER:        150(from Rad) = 150 patients/month INCOMING
Radiology: 150(from ER) = 150 patients/month INCOMING
Cardiology: 80(from ER) + 60(from Rad) = 140 patients/month INCOMING
Surgery:    120(from ER) + 50(from Rad) + 70(from Card) = 240 patients/month INCOMING
ICU:        40(from ER) + 20(from Rad) + 70(from Card) + 100(from Surg) = 230 patients/month INCOMING
Ward:       90(from ER) + 85(from Card) + 140(from Surg) + 110(from ICU) = 425 patients/month INCOMING
```

**Congestion Ratio = Incoming Traffic / Typical Capacity:**

Assume each department has capacity:
```
ER capacity:     300 patients/month
Radiology:       200 patients/month
Cardiology:      150 patients/month
Surgery:         250 patients/month
ICU:             100 patients/month
Ward:            500 patients/month
```

**Bottleneck Analysis:**

```
ER:        150/300 = 50%   ✓ OK
Radiology: 150/200 = 75%   ✓ OK
Cardiology: 140/150 = 93%   ⚠ NEAR CAPACITY
Surgery:    240/250 = 96%   ⚠⚠ CRITICAL BOTTLENECK
ICU:        230/100 = 230% ❌ SEVERELY OVERLOADED
Ward:       425/500 = 85%   ✓ OK
```

**Top Bottlenecks (by severity):**

1. **ICU (230% capacity)** - CRITICAL
   - Needs 130 extra beds
   - Main source: 100 from Surgery, 70 from Cardiology
   
2. **Surgery (96% capacity)** - HIGH RISK
   - Operating at 96% - little room for emergencies
   - Main source: 120 from ER, 50 from Radiology, 70 from Cardiology
   
3. **Cardiology (93% capacity)** - MEDIUM RISK
   - Main source: 80 from ER, 60 from Radiology

---

**Step 4: Using Embeddings to Identify Bottleneck Causes**

**Question:** Which departments are "too close" in embedding space?

Calculate distance between department embeddings:

$$\text{Distance}(i,j) = ||Y_i - Y_j||$$

```
Surgery vs ICU:
Distance = ||(0.9-0.5, 0.4-0.7, 0.7-0.9)||
         = ||(0.4, -0.3, -0.2)||
         = √(0.16 + 0.09 + 0.04) = √0.29 = 0.54 (CLOSE)

Interpretation: Surgery and ICU are CLOSELY RELATED
→ Many post-surgery patients go to ICU
→ This causes ICU bottleneck
```

**Step 5: Solutions Based on Analysis**

**Solution A: Expand ICU Capacity**
```
Current ICU beds: 100
Required for 230 patients: ~230 beds (but 100 is max realistic)
Option: Expand to 150 beds
Cost: High, but necessary
```

**Solution B: Reduce Surgery→ICU Flow**
```
Current: 100 patients/month from Surgery to ICU
Goal: Reduce to 70 patients/month
Method: 
- Improve surgery success rates
- Send more stable post-op patients directly to Ward
- Implement better recovery protocols
```

**Solution C: Parallel Routes**
```
Create alternative pathways:
ER → Cardiology (direct, skip Radiology) = 30 patients/month
Surgery → Ward (direct post-op, skip ICU) = 30 patients/month
Result: Reduces ICU load by 30 patients/month
```

**Solution D: Radiology Load Balancing**
```
Current Radiology flow: 150 patients/month
Distribute some imaging:
- Ultra-sound: portable to bedside in Ward
- CT scans: schedule off-peak hours
- MRI: rotate usage with other facilities
Result: Reduces Rad congestion, improves ER→Rad flow
```

---

**Step 6: Embedding Interpretation - What Do Dimensions Mean?**

Using clustering on the embeddings:

```
Dimension 1 (Entry-Level Function):
High:  ER (0.8), Surgery (0.9)      - Acute intervention points
Low:   Ward (0.4), ICU (0.5)        - Recovery focus

Dimension 2 (Specialty Level):
High:  Cardiology (0.8), ICU (0.7)  - Specialist intensive
Low:   ER (0.5), Ward (0.3)         - General care

Dimension 3 (Post-Care Function):
High:  ICU (0.9), Ward (0.8)        - Post-acute recovery
Low:   ER (0.2), Radiology (0.3)    - Diagnostic focus
```

**Visualization Insight:**

If we could visualize these embeddings in 3D space:
```
        (Specialist)
              ↑
              | Card(0.8)
              | ICU(0.7)
              |
              |
         Rad  |  Surg
        (0.6) |  (0.4)
              |
        ER --- Ward ---- (Recovery Focus)
       (0.5)  (0.3)
        (General Entry)
```

Departments close together → high patient flow
Departments far apart → low patient flow

---

**Step 7: Predictive Bottleneck Detection**

**If hospital adds 50 new cardiac patients per month:**

New flow would be:
```
ER → Card: 80 + 20 = 100 patients/month
Card → ICU: 70 + 15 = 85 patients/month
Card → Surg: 40 + 8 = 48 patients/month
```

**Using embedding predictions:**

```
New Cardiology load:
Current: 140 patients/month (93% capacity)
Increase: 20 + 15 + 8 = 43 patients/month
New total: 183 patients/month (122% OVERLOAD!)

Prediction: Cardiology becomes a NEW bottleneck
→ Hospital should increase Cardiology capacity BEFORE adding new services
```

---

**Step 8: Real-World Optimization Results**

**Scenario: Hospital implements recommendations**

**Before Optimization:**
```
Max congestion: ICU at 230%
Patient wait time: 4-6 hours average
Surgery cancellations: 15% due to no ICU beds
```

**After Optimization (implementing all solutions):**

1. Expand ICU to 120 beds (20% increase)
2. Route 30 post-op patients directly to Ward
3. Optimize Surgery→ICU direct ratio
4. Distribute Radiology load

```
New congestion levels:
ER:        150/300 = 50%   ✓
Radiology: 130/200 = 65%   ✓
Cardiology: 140/150 = 93%  ✓
Surgery:    210/250 = 84%  ✓
ICU:        170/120 = 142% ⚠ Improved from 230%
Ward:       455/500 = 91%  ✓

Patient wait time: 1-2 hours (50% reduction)
Surgery cancellations: 2% (80% improvement)
```

---

**Key Insights from Hospital Example:**

1. **Embeddings capture hidden patterns** - Surgery→ICU relationship (0.54 distance)
2. **Bottlenecks are emergent** - ICU overload comes from Surgery + Cardiology combined
3. **Predictions enable proactive planning** - Add 50 cardiac patients → need more Cardiology capacity
4. **Multiple solutions available** - Can expand, redistribute, or create alternatives
5. **Optimization is data-driven** - Use patient flow data + embeddings for decisions

---

### Application 2: Staff Workflow Coordination

**Problem:** Hospital wants to understand how different staff members collaborate and predict optimal team composition.

**Graph Structure:**
- **Nodes:** Healthcare workers (doctors, nurses, technicians)
- **Edges:** Collaborations/referrals between workers
- **Edge Weight:** Number of joint patient interactions

**Using LLE (K-Nearest Neighbors):**

Each worker is represented as a combination of their K closest collaborators:

$$\text{Worker}_i = \sum_{j \in \text{Team}_i} W_{ij} \times \text{Worker}_j$$

**Application Steps:**

1. **Identify core teams** - K nearest collaborators for each worker
2. **Compute team weights** - who contributes most to workflow
3. **Learn embeddings** - capture each worker's role in collaboration network
4. **Optimize assignments** - assign new hires to teams with similar structures

**Example:**

For Surgeon A with K=5 closest collaborators:
```
Surgeon A = 40% Anesthesiologist B + 30% Nurse C + 20% Technician D + 10% Surgeon E + 0% Other

This means: Surgeon A primarily works with:
- Anesthesiologist B (most critical)
- Nurse C (important support)
- Technician D (regular collaboration)
- Surgeon E (occasional)
```

---

### Application 3: Disease Progression Network

**Problem:** Hospital wants to predict which patients are at risk based on their current condition and position in disease progression network.

**Graph Structure:**
- **Nodes:** Patient health states (disease stages, conditions)
- **Edges:** Patient transitions from one state to another
- **Edge Weight:** Number of patients transitioning

**Using Graph Factorization:**

Learn embeddings that capture disease progression patterns:

$$P(\text{next\_state}_{ij}) \approx \langle Y_i, Y_j \rangle$$

**Application Steps:**

1. **Create health state graph** from historical patient data
2. **Learn embeddings** of each health state
3. **Predict transitions** - which patients will progress to which states
4. **Identify risk clusters** - states that lead to critical outcomes
5. **Intervene early** - catch high-risk patients before progression

**Mathematical Formulation:**

Transition probability matrix:
$$T = \begin{bmatrix} 0 & 0.7 & 0.2 & 0.1 \\ 0.3 & 0 & 0.6 & 0.1 \\ 0.1 & 0.2 & 0 & 0.7 \\ 0.2 & 0.1 & 0.3 & 0 \end{bmatrix}$$

Where rows/columns = [Healthy, Early Disease, Advanced Disease, Critical]

After learning embeddings:
```
Healthy:           [0.2, 0.1, 0.0]
Early Disease:     [0.6, 0.4, 0.1]
Advanced Disease:  [0.9, 0.7, 0.5]
Critical:          [0.3, 0.9, 0.9]
```

Predictions (dot products):
```
Healthy → Early Disease: (0.2)(0.6) + (0.1)(0.4) + (0.0)(0.1) = 0.16 ≈ 0.7 ✓
Advanced → Critical: (0.9)(0.3) + (0.7)(0.9) + (0.5)(0.9) = 1.17 ≈ 0.7 ✓
```

---

### Application 4: Hospital Resource Allocation

**Problem:** Allocate limited resources (beds, equipment, staff) across departments based on actual workflow patterns.

**Graph Structure:**
- **Nodes:** Hospital resources/departments
- **Edges:** Resource sharing/transfers
- **Edge Weight:** Frequency of resource requests

**Using Graph Factorization:**

$$\text{Resource\_allocation}_{ij} = \langle Y_i, Y_j \rangle$$

**Optimization Steps:**

1. **Learn embeddings** of resource-department relationships
2. **Identify critical dependencies** - which departments need which resources
3. **Predict bottlenecks** - when shortages will occur
4. **Optimize allocation** - distribute resources efficiently

**Cost Function to Minimize:**

$$\mathcal{L} = \sum_{(i,j)} (W_{ij} - \langle Y_i, Y_j \rangle)^2 + \lambda \sum_i ||Y_i||^2 + \text{Cost}(Y)$$

Where Cost(Y) represents resource allocation constraints.

---

### Application 5: Patient Readmission Risk Prediction

**Problem:** Predict which patients are likely to be readmitted by analyzing their position in patient similarity network.

**Graph Structure:**
- **Nodes:** Patients
- **Edges:** Similarity between patients (age, diagnosis, treatment similarity)
- **Edge Weight:** Similarity score

**Using LLE:**

Each patient is represented as a combination of K most similar patients:

$$\text{Patient}_i = \sum_{j \in \text{Similar}} W_{ij} \times \text{Patient}_j$$

**Process:**

1. **Build patient similarity network** from medical records
2. **For each patient, find K nearest neighbors** (most similar patients)
3. **Learn K-neighbor embeddings** - capture patient risk profiles
4. **Identify high-risk patterns** - which types of patient combinations predict readmission
5. **Flag similar patients** - alert clinicians for high-risk patients

**Example:**

Patient A with K=3 similar patients:
```
Patient A = 50% Patient B + 30% Patient C + 20% Patient D

Patient B → Readmitted (50% influence)
Patient C → Readmitted (30% influence)
Patient D → Not readmitted (20% influence)

Predicted readmission risk for A = 50% + 30% = 80%
```

---

## Part 6: Comparison and Selection Guide

### Quick Reference Table

| Aspect | Matrix Factorization | Graph Factorization | LLE |
|--------|---------------------|---------------------|-----|
| **Formula** | $A = U \times V^T$ | $W \approx Y \times Y^T$ | $X_i = \sum W_{ij} X_j$ |
| **Type** | General technique | Special case for graphs | Local-based |
| **Best for** | Any large matrix | Large graphs | Small-medium graphs |
| **Node scale** | N/A | Millions | Hundreds of thousands |
| **Graph type** | N/A | Undirected | Undirected |
| **Memory** | Very efficient | Very efficient | Moderate |
| **Speed** | Fast | Fast | Moderate |
| **Interpretability** | Low-Medium | Low-Medium | High |
| **What captures** | Global structure | Global connections | Local neighborhoods |
| **Main advantage** | Scalable | Scalable + efficient | Interpretable |
| **Main disadvantage** | Information loss | Can't capture complex patterns | Slow for large graphs |

### Healthcare Application Selection

| Problem | Best Approach | Why |
|---------|---------------|-----|
| **Patient flow optimization** | Graph Factorization | Captures overall department relationships |
| **Staff team composition** | LLE | Focuses on immediate team collaborations |
| **Disease progression** | Graph Factorization | Needs to predict global transitions |
| **Resource allocation** | Graph Factorization | Captures all resource dependencies |
| **Readmission risk** | LLE | Similar patients → similar outcomes |
| **Infection transmission** | Graph Factorization | Needs to model spread across entire facility |
| **Care pathway optimization** | LLE | Local care steps matter most |

---

## Part 7: Summary

**The Hierarchy:**

```
Matrix Factorization (General Principle)
├─ Graph Factorization (For undirected graphs)
│  └ Formula: W = Y × Y^T
└─ Recommendation Systems, Image Compression, etc.

LLE (Different Approach)
├─ Based on K-nearest neighbors
├─ Formula: X_i = Σ W_ij X_j
└─ Preserves local structure
```

**Key Takeaways:**

1. **Matrix Factorization** = general technique to break large matrices into smaller ones
2. **Graph Factorization** = matrix factorization applied to graphs (special case with symmetry)
3. **LLE** = completely different approach focusing on local neighborhoods

4. **What you choose:** Embedding dimension (k or d)
5. **What algorithm learns:** All values in embedding vectors

6. **Healthcare applications:** Patient flow, staff coordination, disease progression, resource allocation, readmission risk

---

## Further Reading

- Matrix Factorization Theory: SVD (Singular Value Decomposition)
- Graph Embedding Papers: "Graph Factorization" (Menon & Elkan, 2011)
- LLE Paper: "Nonlinear Dimensionality Reduction by Locally Linear Embedding" (Roweis & Saul, 2000)

---

