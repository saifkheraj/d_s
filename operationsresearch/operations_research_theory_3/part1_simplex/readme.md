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

We want to solve this Linear Programming problem:

**Maximize:** `z = x₁ + 3x₂`

**Subject to:**
```
-x₁ +  x₂  ≤   3
-x₁ + 2x₂  ≤   8  
 3x₁ +  x₂  ≤  18
 x₁, x₂    ≥   0
```

## Step 1: Convert to Standard Form

Add slack variables s₁, s₂, s₃ to convert inequalities to equalities:

```
-x₁ +  x₂ + s₁ + 0s₂ + 0s₃ =  3
-x₁ + 2x₂ + 0s₁ + s₂ + 0s₃ =  8
 3x₁ +  x₂ + 0s₁ + 0s₂ + s₃ = 18
```

**All variables:** x₁, x₂, s₁, s₂, s₃ ≥ 0

**In matrix notation:**

**Matrix A** (constraint coefficients):
```
        x₁  x₂  s₁  s₂  s₃
Row 1  [-1   1   1   0   0]
Row 2  [-1   2   0   1   0]  
Row 3  [ 3   1   0   0   1]
```

**Vector b** (right-hand side):
```
b = [ 3]
    [ 8]
    [18]
```

**Vector c** (objective coefficients):
```
c = [ 1]  ← coefficient of x₁
    [ 3]  ← coefficient of x₂  
    [ 0]  ← coefficient of s₁
    [ 0]  ← coefficient of s₂
    [ 0]  ← coefficient of s₃
```

---

## Method 1: Tableau Method 📊

### Initial Tableau

| Basic Var | x₁ | x₂ | s₁ | s₂ | s₃ | RHS |
|-----------|----|----|----|----|----|----|
| s₁        | -1 |  1 |  1 |  0 |  0 |  3 |
| s₂        | -1 |  2 |  0 |  1 |  0 |  8 |
| s₃        |  3 |  1 |  0 |  0 |  1 | 18 |
| **z-row** | -1 | -3 |  0 |  0 |  0 |  0 |

### How Tableau Method Works:

**Step 1: Find Entering Variable**
- Look at z-row for most negative number
- Most negative = -3 (under x₂ column)
- **x₂ enters the basis**

**Step 2: Find Leaving Variable (Ratio Test)**
- For x₂ column, calculate: RHS ÷ positive coefficients
- Row 1: 3 ÷ 1 = 3
- Row 2: 8 ÷ 2 = 4  
- Row 3: 18 ÷ 1 = 18
- Minimum ratio = 3 → **s₁ leaves the basis**

**Step 3: Pivot Operation**
- Pivot element = 1 (intersection of x₂ column and s₁ row)
- Use row operations to make this element = 1 and others in column = 0
- Continue until no negative numbers in z-row

---

## Method 2: Matrix Method 🔢

The matrix method splits variables into two groups:

### Step 1: Identify Basic and Non-basic Variables

**Initial Setup:**
- **Basic variables** (in the solution): s₁, s₂, s₃
- **Non-basic variables** (set to zero): x₁, x₂

### Step 2: Split the Constraint Matrix

**A_B** (Basic variables part - columns for s₁, s₂, s₃):
```
A_B = [1  0  0]  ← This is a 3×3 identity matrix
      [0  1  0]
      [0  0  1]
```

**A_N** (Non-basic variables part - columns for x₁, x₂):
```
A_N = [-1   1]  ← Column 1: x₁ coefficients  
      [-1   2]  ← Column 2: x₂ coefficients
      [ 3   1]
```

**c_B** (costs of basic variables):
```
c_B = [0]  ← cost of s₁
      [0]  ← cost of s₂  
      [0]  ← cost of s₃
```

**c_N** (costs of non-basic variables):
```
c_N = [1]  ← cost of x₁
      [3]  ← cost of x₂
```

### Step 3: Solve for Basic Variables

Since A_B is identity matrix: **x_B = A_B⁻¹ × b = b**

**Current solution:**
```
s₁ = 3   (basic)
s₂ = 8   (basic)  
s₃ = 18  (basic)
x₁ = 0   (non-basic)
x₂ = 0   (non-basic)
```

### Step 4: Check if Optimal (Reduced Costs)

**Formula:** `reduced_costs = c_N - c_B^T × A_B⁻¹ × A_N`

**Calculation:**
```
c_N = [1, 3]
c_B^T × A_B⁻¹ × A_N = [0, 0, 0] × [1 0 0] × [-1  1] = [0, 0]
                                    [0 1 0]   [-1  2]
                                    [0 0 1]   [ 3  1]

reduced_costs = [1, 3] - [0, 0] = [1, 3]
```

**Interpretation:** 
- For tableau: we use negative of these → [-1, -3]
- Since -3 < 0, **x₂ should enter** (can improve objective)

### Step 5: Find Leaving Variable

**Direction vector** (what happens when x₂ enters):
```
d = A_B⁻¹ × (x₂ column from A_N) = [1 0 0] × [1] = [1]
                                   [0 1 0]   [2]   [2]
                                   [0 0 1]   [1]   [1]
```

**Ratio test:**
```
Current basic values: [3, 8, 18]
Direction vector:     [1, 2,  1]
Ratios:              [3/1, 8/2, 18/1] = [3, 4, 18]
```

**Minimum ratio = 3 → s₁ leaves**

### Step 6: Update Basis and Repeat

**New basic variables:** x₂, s₂, s₃  
**New non-basic variables:** x₁, s₁

Repeat steps 2-5 until all reduced costs ≥ 0.

---

## Side-by-Side Comparison

| Aspect | Tableau Method | Matrix Method |
|--------|----------------|---------------|
| **Visual** | Easy to see all steps in table format | More compact, requires matrix calculations |
| **Manual Calculation** | ✅ Great for hand solving | ❌ Needs calculator/computer for matrices |
| **Large Problems** | ❌ Table gets huge and messy | ✅ Stays organized and efficient |
| **Computer Implementation** | ❌ Inefficient memory usage | ✅ Used by all professional solvers |
| **Learning** | ✅ Shows exactly what's happening | ❌ Hides some geometric intuition |
| **Speed** | ❌ Slow for big problems | ✅ Much faster with good linear algebra |

---

## Final Answer for Our Example

Both methods give the same result:

**Optimal Solution:**
```
x₁ = 2
x₂ = 5
Maximum z = 1(2) + 3(5) = 17
```

**Verification (check all constraints):**
```
Constraint 1: -2 + 5 = 3 ≤ 3 ✅
Constraint 2: -2 + 10 = 8 ≤ 8 ✅  
Constraint 3: 6 + 5 = 11 ≤ 18 ✅
```

**Path taken:**
```
Start: (0,0) with z = 0
Step 1: (0,3) with z = 9  
Step 2: (2,5) with z = 17 ← OPTIMAL
```

---

## When to Use Each Method

### 🎓 Use Tableau Method When:
- Learning the simplex method for the first time
- Solving small problems by hand (≤ 4 variables)
- Taking exams or homework
- Want to see every step clearly

### 💻 Use Matrix Method When:
- Programming a solver
- Dealing with large problems (≥ 10 variables)
- Need computational efficiency
- Building commercial optimization software

---

## Quick Implementation Guide

### Python - Tableau Method
```python
import numpy as np

# Simple tableau structure
tableau = np.array([
    [-1,  1,  1,  0,  0,  3],   # s₁ row
    [-1,  2,  0,  1,  0,  8],   # s₂ row  
    [ 3,  1,  0,  0,  1, 18],   # s₃ row
    [-1, -3,  0,  0,  0,  0]    # z row
])

# Main loop: find entering/leaving variables and pivot
# (Full implementation would be ~50 lines)
```

### Python - Matrix Method
```python
import numpy as np

# Define problem
A = np.array([[-1, 1, 1, 0, 0], 
              [-1, 2, 0, 1, 0], 
              [3, 1, 0, 0, 1]])
b = np.array([3, 8, 18])
c = np.array([1, 3, 0, 0, 0])

# Initial basis: columns 2, 3, 4 (s₁, s₂, s₃)
basis = [2, 3, 4]

# Solve using scipy or custom matrix operations
# (Professional solvers use this approach)
```

---

## Additional Resources

### 📚 **Best Textbooks:**
- **Beginner:** "Linear Programming" by Chvátal
- **Advanced:** "Linear and Nonlinear Programming" by Luenberger & Ye
- **Applied:** "Model Building in Mathematical Programming" by Williams

### 🔧 **Software to Try:**
- **Learning:** Excel Solver, LINGO
- **Open Source:** GLPK, CBC, SciPy
- **Commercial:** Gurobi, CPLEX, Xpress

### 🎯 **Practice Problems:**
- Start with 2-variable problems you can graph
- Move to transportation/assignment problems  
- Try portfolio optimization examples

---

*This guide should make the simplex method much clearer! Both approaches solve the same problems - tableau is better for learning, matrix is better for computing.* 🚀
