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

## License

This guide is provided for educational purposes. Feel free to use, modify, and distribute for learning and teaching.

## Contributing

Found an error or want to improve the explanation? Please open an issue or submit a pull request!
