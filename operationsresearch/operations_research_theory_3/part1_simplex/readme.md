# Simplex Method — Beginner Friendly Guide

A comprehensive, step-by-step explanation of the Simplex Method for solving Linear Programming problems, designed for beginners who want to understand not just the "how" but also the "why" behind each step.

## Table of Contents

- [What is the Simplex Method?](#what-is-the-simplex-method)
- [Prerequisites](#prerequisites)
- [Key Concepts](#key-concepts)
- [Step-by-Step Example](#step-by-step-example)
- [Visual Walkthrough](#visual-walkthrough)
- [Understanding the Algorithm](#understanding-the-algorithm)
- [Common Questions](#common-questions)
- [Further Reading](#further-reading)

## What is the Simplex Method?

The Simplex Method is an algorithm for solving **Linear Programming (LP)** problems:
- **Maximize** or **minimize** a linear objective function
- Subject to linear constraints (inequalities/equalities)
- All variables are non-negative

### Key Insight
The optimal solution to any LP problem always occurs at a **corner point** (vertex) of the feasible region. The Simplex Method efficiently walks from one corner to another, always improving the objective function, until no further improvement is possible.

<img width="780" height="706" alt="image" src="https://github.com/user-attachments/assets/2c972800-5303-45b0-8b63-7fba916ed8e7" />


## Prerequisites

- Basic linear algebra (systems of equations)
- Understanding of inequalities and graphing
- Familiarity with mathematical optimization concepts

## Key Concepts

### 1. Slack Variables
Convert inequality constraints (≤) into equalities by adding slack variables.

**Example:** `2x₁ - x₂ ≤ 4` becomes `2x₁ - x₂ + s₁ = 4` where `s₁ ≥ 0`

**Interpretation:** Slack represents "leftover room" in a constraint. When slack = 0, the constraint is tight (exactly satisfied).

### 2. Basis and Basic Variables

- **Basic Variables**: Variables currently in the solution (have positive values)
- **Non-Basic Variables**: Variables set to zero
- **Basis**: The set of basic variables at any iteration

The basis changes as we move from one corner point to another:
- One non-basic variable **enters** the basis (becomes > 0)
- One basic variable **leaves** the basis (becomes 0)

### 3. Tableau Structure

The simplex tableau organizes all information needed for the algorithm:

| Basis | x₁ | x₂ | s₁ | s₂ | s₃ | RHS |
|-------|----|----|----|----|----|----|
| s₁    | 2  | -1 | 1  | 0  | 0  | 4   |
| s₂    | 2  | 1  | 0  | 1  | 0  | 8   |
| s₃    | 0  | 1  | 0  | 0  | 1  | 3   |
| z     | -1 | 0  | 0  | 0  | 0  | 0   |

## Step-by-Step Example

### Problem Statement
```
Maximize: z = x₁

Subject to:
  2x₁ - x₂ ≤ 4
  2x₁ + x₂ ≤ 8  
  x₂ ≤ 3
  x₁, x₂ ≥ 0
```

### Step 1: Add Slack Variables
```
Maximize: z = x₁

Subject to:
  2x₁ - x₂ + s₁ = 4
  2x₁ + x₂ + s₂ = 8
  x₂ + s₃ = 3
  x₁, x₂, s₁, s₂, s₃ ≥ 0
```

**Initial Solution:** x₁ = 0, x₂ = 0, s₁ = 4, s₂ = 8, s₃ = 3, z = 0  
**Initial Basis:** {s₁, s₂, s₃}

## Visual Walkthrough

### Iteration 0 (Starting Point)
**Location:** (0, 0)  
**Basis:** {s₁, s₂, s₃}  
**Objective:** z = 0

### Iteration 1
**Entering Variable:** x₁ (most negative reduced cost: -1)  
**Leaving Variable:** s₁ (ratio test: min{4/2, 8/2} = 2)  
**New Location:** (2, 0)  
**New Basis:** {x₁, s₂, s₃}  
**Objective:** z = 2

### Iteration 2 (Optimal)
**Entering Variable:** x₂ (negative reduced cost: -0.5)  
**Leaving Variable:** s₂ (ratio test: min{4/2, 3/1} = 2)  
**Final Location:** (3, 2)  
**Final Basis:** {x₁, x₂, s₃}  
**Optimal Objective:** z = 3

## Understanding the Algorithm

### How to Choose the Entering Variable
Look at the **z-row** (bottom row) for **reduced costs**:
- **Negative reduced cost** → Increasing this variable improves z
- **Zero reduced cost** → No effect on z
- **Positive reduced cost** → Would make z worse

Choose the variable with the **most negative** reduced cost.

### How to Choose the Leaving Variable (Ratio Test)
1. Look at the column of the entering variable
2. For each **positive** entry, calculate: `RHS ÷ column entry`
3. The row with the **smallest ratio** determines the leaving variable

**Why?** This variable will hit zero first as we increase the entering variable.

### When to Stop
The algorithm terminates when the z-row has **no negative reduced costs**. This means no variable can further improve the objective function.

## Common Questions

### Q: Why does the basis change?
**A:** As we move from one corner of the feasible region to another, different constraints become "tight" (active). This changes which variables are basic (positive) vs non-basic (zero).

### Q: What if there are multiple negative reduced costs?
**A:** Choose the most negative one. This is the steepest ascent rule and typically leads to faster convergence.

### Q: What does it mean geometrically when a variable enters/leaves?
**A:** We're moving along an edge of the feasible region polygon. The entering variable determines the direction, and the leaving variable determines how far we can go before hitting the next corner.

### Q: Can the algorithm fail?
**A:** The algorithm can encounter two special cases:
- **Unbounded solution**: The objective can be increased indefinitely
- **Degeneracy**: Multiple optimal solutions exist

## Algorithm Summary

1. **Setup**: Convert to standard form with slack variables
2. **Initialize**: Start at origin with all slacks basic
3. **Iterate**:
   - Choose entering variable (most negative reduced cost)
   - Choose leaving variable (ratio test)
   - Pivot to new basic solution
4. **Terminate**: When no negative reduced costs remain

## Further Reading

- **Linear Programming Theory**: Dantzig, G.B. "Linear Programming and Extensions"
- **Optimization Methods**: Nocedal, J. & Wright, S. "Numerical Optimization"
- **Online Resources**: 
  - [MIT OpenCourseWare - Linear Programming](https://ocw.mit.edu)
  - [Khan Academy - Linear Programming](https://www.khanacademy.org)

---



# Simplex Method: Tableau vs Matrix Form

This document explains and compares the two main ways of implementing the Simplex method:

1. **Tableau Method** — the traditional row-operations approach
2. **Matrix Method** — the algebraic/linear algebra approach used in solvers

## Problem Setup (Example)

We want to solve:

**Maximize:**
```
z = x₁ + 3x₂
```

**Subject to:**
```
-x₁ +  x₂ ≤  3
-x₁ + 2x₂ ≤  8
 3x₁ +  x₂ ≤ 18
 x₁, x₂ ≥  0
```

### Step 1: Standard Form

Add slack variables s₁, s₂, s₃:

```
-x₁ +  x₂ + s₁      =  3
-x₁ + 2x₂      + s₂ =  8
 3x₁ +  x₂           + s₃ = 18
```

**Variables:** (x₁, x₂, s₁, s₂, s₃)

**Matrix form:**
```
     [-1   1   1   0   0]
A =  [-1   2   0   1   0]
     [ 3   1   0   0   1]

     [ 3]       [1]
b =  [ 8],  c = [3]
     [18]       [0]
                [0]
                [0]
```

## Tableau Method

### Initial Tableau

| Basis | x₁ | x₂ | s₁ | s₂ | s₃ | RHS |
|-------|----|----|----|----|----|----|
| s₁    | -1 |  1 |  1 |  0 |  0 |  3 |
| s₂    | -1 |  2 |  0 |  1 |  0 |  8 |
| s₃    |  3 |  1 |  0 |  0 |  1 | 18 |
| z     | -1 | -3 |  0 |  0 |  0 |  0 |

### Process

1. **Entering variable:** Most negative in z row = **-3** → x₂ enters
2. **Leaving variable:** Ratio test → min(3/1, 8/2, 18/1) = **3** → s₁ leaves
3. **Pivot:** Perform row operations to update tableau
4. **Repeat** until all reduced costs ≥ 0

## Matrix Method

### Step 1: Split Basis/Nonbasis

- **Basis (initial):** s₁, s₂, s₃
- **Nonbasis:** x₁, x₂

So:
```
A_B = I₃ (3×3 identity matrix) = [1  0  0]
                                 [0  1  0]
                                 [0  0  1]

A_N = [-1  1]     c_B = [0]     c_N = [1]
      [-1  2]           [0]           [3]
      [ 3  1]           [0]
```

### Step 2: Compute Basic Solution

```
x_B = A_B⁻¹ × b = I₃ × b = b = [3]
                               [8]
                               [18]
```

Therefore: s₁ = 3, s₂ = 8, s₃ = 18, x₁ = 0, x₂ = 0

### Step 3: Reduced Costs

```
r_N^T = c_N^T - c_B^T × A_B⁻¹ × A_N
      = [1  3] - [0  0  0] × [-1  1]
                              [-1  2]
                              [ 3  1]
      = [1  3] - [0  0] = [1  3]
```

In tableau convention → (-1, -3). Since -3 < 0, variable x₂ enters the basis.

### Step 4: Ratio Test

Direction vector for entering variable x₂:
```
d = A_B⁻¹ × A_x₂ = I₃ × [1] = [1]
                         [2]   [2]
                         [1]   [1]
```

Ratio test:
```
min{x_Bᵢ/dᵢ : dᵢ > 0} = min{3/1, 8/2, 18/1} = min{3, 4, 18} = 3
```

→ s₁ leaves the basis (first constraint becomes tight)

### Step 5: Update Basis

**New basis:** (x₂, s₂, s₃)

Update basis matrix:
```
A_B^new = [1  1  0]  (columns for x₂, s₂, s₃)
          [2  0  1]
          [1  0  0]
```

Compute new basic solution: x_B^new = (A_B^new)⁻¹ × b

Repeat until all reduced costs ≥ 0.

## Comparison

| Aspect | Tableau Method | Matrix Method |
|--------|----------------|---------------|
| **What you do** | Pivot with row operations on a tableau | Compute x_B = A_B⁻¹×b, reduced costs, ratios |
| **Good for** | Learning, small problems, manual solving | Computer implementations, large LPs |
| **Pros** | Visual, intuitive, easy step tracking | Efficient, compact, avoids giant tableaux |
| **Cons** | Gets messy for large LPs | Requires linear algebra (inverses/factorizations) |

## Which Method to Use?

### 📚 Learning/Exams → Use **Tableau Method**
- Easy to understand entering/leaving variables
- Clear visualization of how pivots work  
- Step-by-step process is transparent
- Good for hand calculations

### 💻 Coding/Real-World LP Solving → Use **Matrix Method**
- All professional solvers (CPLEX, Gurobi, GLPK) use matrix-based implementations
- More efficient for large problems
- Better numerical stability control
- Easier to implement advanced techniques (dual simplex, primal-dual, etc.)

## Final Result

For this example:

**Optimal solution:**
```
x₁* = 2
x₂* = 5  
z*  = 17
```

**Solution path:**
```
(x₁, x₂): (0,0) → (0,3) → (2,5)
```

**Verification:**
```
z* = 1×2 + 3×5 = 2 + 15 = 17 ✓

Constraint check:
-2 + 5  =  3 ≤  3 ✓
-2 + 10 =  8 ≤  8 ✓  
 6 + 5  = 11 ≤ 18 ✓
```

## Implementation Examples

### Tableau Method (Python)
```python
import numpy as np

def simplex_tableau(c, A, b):
    """
    Solve LP using tableau method
    min c^T x subject to Ax = b, x >= 0
    """
    m, n = A.shape
    
    # Create initial tableau [A b; c^T 0]
    tableau = np.zeros((m+1, n+1))
    tableau[:m, :n] = A
    tableau[:m, n] = b
    tableau[m, :n] = c
    
    while True:
        # Find entering variable (most negative in bottom row)
        entering_col = np.argmin(tableau[m, :n])
        if tableau[m, entering_col] >= 0:
            break  # Optimal solution found
            
        # Find leaving variable (minimum ratio test)
        ratios = []
        for i in range(m):
            if tableau[i, entering_col] > 0:
                ratios.append(tableau[i, n] / tableau[i, entering_col])
            else:
                ratios.append(float('inf'))
        
        leaving_row = np.argmin(ratios)
        
        # Pivot operation
        pivot_element = tableau[leaving_row, entering_col]
        tableau[leaving_row] /= pivot_element





## License

This guide is provided for educational purposes. Feel free to use, modify, and distribute for learning and teaching.

## Contributing

Found an error or want to improve the explanation? Please open an issue or submit a pull request!
