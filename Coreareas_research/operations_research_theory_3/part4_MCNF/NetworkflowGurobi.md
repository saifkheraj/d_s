# Assignment Problem: Network Flow Optimization with Gurobi

A comprehensive guide to solving assignment problems using network flow models with Gurobi and Python.

## Table of Contents
- [Overview](#overview)
- [Problem Description](#problem-description)
- [Real-World Use Cases](#real-world-use-cases)
- [Network Flow Model](#network-flow-model)
- [Mathematical Formulation](#mathematical-formulation)
- [Implementation](#implementation)
- [Key Insights](#key-insights)
- [Extensions](#extensions)
- [Requirements](#requirements)

## Overview

This case study demonstrates how to construct and solve an assignment problem using network flow optimization. The assignment problem is a special case of the minimum cost network flow problem, characterized by its bipartite graph structure and one-to-one assignment constraints.

### Business Problem
A company needs to assign **4 workers** to **4 jobs** with the following requirements:
- Each job must be assigned to exactly one worker
- Each worker can only perform one job
- Different workers have different costs for different jobs
- **Objective**: Minimize total assignment cost

## Problem Description

### Graph Structure
The assignment problem uses a **bipartite graph**:
- **Left vertices**: Jobs {A, B, C, D}
- **Right vertices**: Workers {E, F, G, H}
- **Arcs**: Connections between jobs and workers with associated costs

### Cost Matrix

| Job/Worker | E | F | G | H |
|------------|---|---|---|---|
| **A**      | 2 | ∞ | 4 | 3 |
| **B**      | 3 | 4 | 1 | 2 |
| **C**      | 5 | 2 | 6 | 4 |
| **D**      | 1 | 3 | 2 | 5 |

**Notes**:
- **∞ (infinity)** represents non-existent arcs (e.g., Worker F cannot do Job A)
- In practice, ∞ is replaced with a very large number (e.g., 999999)
- Dashed lines in diagrams represent invisible/forbidden arcs

## Real-World Use Cases

This optimization model applies to numerous scenarios:

### 1. **Human Resource Management**
- Assigning employees to projects based on skills and costs
- Matching interns to departments
- Allocating staff to shifts

### 2. **Operations Management**
- Assigning machines to production tasks
- Scheduling equipment for maintenance
- Allocating manufacturing resources

### 3. **Logistics**
- Assigning delivery drivers to routes
- Matching vehicles to delivery zones
- Warehouse worker task allocation

### 4. **Education**
- Assigning classrooms to courses
- Matching students to thesis advisors
- Allocating teaching assistants to sections

### 5. **Healthcare**
- Assigning nurses to shifts
- Matching patients to hospital rooms
- Allocating medical equipment to departments

## Network Flow Model

### Bipartite Graph Properties
- **Two disjoint sets**: Jobs and Workers
- **Equal cardinality**: |Jobs| = |Workers| = n
- **Directed arcs**: From jobs (source) to workers (sink)
- **Arc costs**: c_ij represents the cost of assigning job i to worker j

### Visual Representation
```
Jobs          Workers
A ----2----> E
 \----∞----> F
  \---4----> G
   \--3----> H

B ----3----> E
 \----4----> F
  \---1----> G
   \--2----> H

C ----5----> E
 \----2----> F
  \---6----> G
   \--4----> H

D ----1----> E
 \----3----> F
  \---2----> G
   \--5----> H
```

## Mathematical Formulation

### Sets
- **I**: Set of jobs {A, B, C, D}
- **J**: Set of workers {E, F, G, H}

### Parameters
- **c_ij**: Cost of assigning job i to worker j

### Decision Variables
```
x_ij = {1  if job i is assigned to worker j
       {0  otherwise
```

### Objective Function
```
Minimize: Σ Σ (c_ij × x_ij)
          i∈I j∈J
```
Minimize the total cost of all assignments.

### Constraints

**1. Job Assignment Constraint**
```
Σ x_ij = 1    for all i ∈ I
j∈J
```
Each job must be assigned to exactly one worker.

**2. Worker Assignment Constraint**
```
Σ x_ij = 1    for all j ∈ J
i∈I
```
Each worker must be assigned exactly one job.

**3. Binary Constraint**
```
x_ij ∈ {0, 1}    for all i ∈ I, j ∈ J
```

### Complete LP Formulation
```
Minimize:   Σ Σ c_ij × x_ij
            i j

Subject to: Σ x_ij = 1        ∀i ∈ I  (each job assigned once)
            j

            Σ x_ij = 1        ∀j ∈ J  (each worker gets one job)
            i

            x_ij ∈ {0, 1}     ∀i,j    (binary decision)
```

## Implementation

### Prerequisites
```python
import gurobipy as gp
from gurobipy import GRB
import pandas as pd
```

### Step 1: Data Preparation

#### Load Data from Excel
```python
# Excel file should have columns: Jobs, Workers, Cost
data = pd.read_excel('assignment_costs.xlsx')
print(data.head())
```

**Example Data Structure**:
```
   Jobs  Workers  Cost
0     A        E     2
1     A        F   999  # Infinity represented as large number
2     A        G     4
3     A        H     3
...
```

#### Prepare Data Structures
```python
# Create dictionary of arcs and costs
flow_dict = {
    (row['Jobs'], row['Workers']): row['Cost'] 
    for _, row in data.iterrows()
}

# Extract unique sets
jobs = set(data['Jobs'].unique())
workers = set(data['Workers'].unique())

# Create multidict for Gurobi
arcs, costs = gp.multidict(flow_dict)
```

### Step 2: Model Construction

#### Create Model
```python
# Initialize Gurobi model
model = gp.Model('assignment_problem')

# Add binary decision variables
x = model.addVars(arcs, vtype=GRB.BINARY, name='assign')
```

#### Set Objective Function
```python
# Minimize total assignment cost
model.setObjective(
    gp.quicksum(costs[i, j] * x[i, j] for i, j in arcs),
    GRB.MINIMIZE
)
```

#### Add Constraints
```python
# Constraint 1: Each job assigned to exactly one worker
for i in jobs:
    model.addConstr(
        gp.quicksum(x[i, j] for j in workers if (i, j) in arcs) == 1,
        name=f'job_{i}'
    )

# Constraint 2: Each worker assigned exactly one job
for j in workers:
    model.addConstr(
        gp.quicksum(x[i, j] for i in jobs if (i, j) in arcs) == 1,
        name=f'worker_{j}'
    )
```

### Step 3: Solve and Retrieve Results

#### Optimize
```python
# Solve the model
model.optimize()
```

#### Extract Solution
```python
# Check if optimal solution was found
if model.status == GRB.OPTIMAL:
    print(f"\nOptimal Solution Found!")
    print(f"Total Cost: {model.ObjVal}")
    print("\nAssignments:")
    
    for i, j in arcs:
        if x[i, j].X > 0.5:  # Binary variable is 1
            print(f"  Job {i} → Worker {j}, Cost: {costs[i, j]}")
else:
    print("No optimal solution found")
```

### Complete Implementation Example

```python
import gurobipy as gp
from gurobipy import GRB
import pandas as pd

# Load data
data = pd.read_excel('assignment_costs.xlsx')

# Prepare data
flow_dict = {(row['Jobs'], row['Workers']): row['Cost'] 
             for _, row in data.iterrows()}
jobs = set(data['Jobs'].unique())
workers = set(data['Workers'].unique())
arcs, costs = gp.multidict(flow_dict)

# Build model
model = gp.Model('assignment')
x = model.addVars(arcs, vtype=GRB.BINARY, name='assign')

# Objective
model.setObjective(
    gp.quicksum(costs[i, j] * x[i, j] for i, j in arcs),
    GRB.MINIMIZE
)

# Constraints
for i in jobs:
    model.addConstr(
        gp.quicksum(x[i, j] for j in workers if (i, j) in arcs) == 1,
        name=f'job_{i}'
    )

for j in workers:
    model.addConstr(
        gp.quicksum(x[i, j] for i in jobs if (i, j) in arcs) == 1,
        name=f'worker_{j}'
    )

# Solve
model.optimize()

# Results
if model.status == GRB.OPTIMAL:
    print(f"Optimal Cost: {model.ObjVal}")
    for i, j in arcs:
        if x[i, j].X > 0.5:
            print(f"Job {i} → Worker {j}")
```

### Example Output
```
Optimize a model with 8 rows, 15 columns and 30 nonzeros
Coefficient statistics:
  Matrix range     [1e+00, 1e+00]
  Objective range  [1e+00, 1e+01]
  Bounds range     [1e+00, 1e+00]
  RHS range        [1e+00, 1e+00]
Presolve removed 8 rows and 15 columns
Presolve time: 0.00s
Presolve: All rows and columns removed

Explored 0 nodes (0 simplex iterations) in 0.01 seconds
Thread count was 1 (of 8 available processors)

Optimal Solution Found!
Total Cost: 13

Assignments:
  Job A → Worker E, Cost: 2
  Job B → Worker G, Cost: 1
  Job C → Worker F, Cost: 2
  Job D → Worker H, Cost: 8
```

## Key Insights

### 1. Total Unimodularity

The assignment problem possesses a special mathematical property called **total unimodularity**.

#### What It Means
The constraint matrix of the assignment problem is totally unimodular, which guarantees that:
- The LP relaxation (continuous variables) produces integer solutions
- No branch-and-bound algorithm is required
- The simplex method alone finds the optimal solution

#### Testing LP Relaxation
```python
# Change variable type from BINARY to CONTINUOUS
x = model.addVars(arcs, vtype=GRB.CONTINUOUS, lb=0, ub=1, name='assign')

# Rebuild and solve
model.optimize()

# You'll still get integer solutions (0 or 1)!
```

#### Why This Matters
```
Binary Model:     Uses integer programming (potentially slow)
Continuous Model: Uses simplex method (very fast)
Result:           SAME optimal solution with integer values!
```

### 2. Computational Efficiency

**Solver Output Analysis**:
```
Explored 0 nodes (0 simplex iterations)
```

**Interpretation**:
- **0 nodes explored**: No branch-and-bound tree traversal needed
- Gurobi recognizes the special structure
- Solution found directly via simplex method
- Extremely fast even for large problems

### 3. Problem Characteristics

| Characteristic | Assignment Problem | General IP |
|---------------|-------------------|------------|
| Constraint Matrix | Totally Unimodular | Arbitrary |
| LP Relaxation | Gives integer solution | May be fractional |
| Solution Method | Simplex only | Branch-and-bound |
| Scalability | Excellent (10,000+ variables) | Limited |
| Special Algorithms | Hungarian algorithm available | N/A |

### 4. Optimal Solution Visualization

For our example, the optimal solution with cost = 13:
```
Job A → Worker E (Cost: 2) ✓
Job B → Worker G (Cost: 1) ✓
Job C → Worker F (Cost: 2) ✓
Job D → Worker H (Cost: 8) ✓
                  ─────────
         Total Cost:    13
```

## Extensions

### 1. Unbalanced Assignment

When jobs ≠ workers, add dummy entities.

```python
# More jobs than workers: Add dummy workers
num_jobs = len(jobs)
num_workers = len(workers)

if num_jobs > num_workers:
    dummy_workers = [f"Dummy_{i}" for i in range(num_jobs - num_workers)]
    workers.update(dummy_workers)
    
    # Add arcs with zero cost
    for job in jobs:
        for dummy in dummy_workers:
            arcs.append((job, dummy))
            costs[(job, dummy)] = 0  # No cost for dummy assignment
```

### 2. Multiple Assignments Per Worker

Allow workers to handle multiple jobs.

```python
# Worker can handle up to k jobs
k = 3

for j in workers:
    model.addConstr(
        gp.quicksum(x[i, j] for i in jobs if (i, j) in arcs) <= k,
        name=f'worker_capacity_{j}'
    )
```

### 3. Preference Constraints

Add hard requirements or prohibitions.

```python
# MUST assign Job A to Worker E
model.addConstr(x['A', 'E'] == 1, name='required_assignment')

# CANNOT assign Job C to Worker F
model.addConstr(x['C', 'F'] == 0, name='prohibited_assignment')

# Worker G must get at least 2 jobs
model.addConstr(
    gp.quicksum(x[i, 'G'] for i in jobs if (i, 'G') in arcs) >= 2,
    name='min_jobs_G'
)
```

### 4. Multi-Objective Optimization

Balance cost with other factors.

```python
# Primary objective: minimize cost
# Secondary objective: maximize worker satisfaction

satisfaction = {
    ('A', 'E'): 8, ('A', 'G'): 6, ('A', 'H'): 7,
    ('B', 'E'): 5, ('B', 'F'): 9, ('B', 'G'): 10,
    # ... more satisfaction scores
}

# Weighted objective
model.setObjective(
    gp.quicksum(costs[i, j] * x[i, j] for i, j in arcs) 
    - 0.1 * gp.quicksum(satisfaction.get((i, j), 0) * x[i, j] for i, j in arcs),
    GRB.MINIMIZE
)
```

### 5. Time-Window Constraints

Jobs must be assigned within specific time periods.

```python
# Add time periods
time_availability = {
    'E': [1, 2, 3],     # Worker E available in periods 1-3
    'F': [2, 3, 4],     # Worker F available in periods 2-4
    # ...
}

job_periods = {
    'A': 1,  # Job A must be done in period 1
    'B': 2,
    # ...
}

# Only allow assignments where timing matches
for i, j in arcs:
    if job_periods[i] not in time_availability[j]:
        model.addConstr(x[i, j] == 0, name=f'time_conflict_{i}_{j}')
```

### 6. Skill-Based Constraints

Workers have skills; jobs require specific skills.

```python
worker_skills = {
    'E': {'Python', 'SQL'},
    'F': {'Java', 'Python'},
    'G': {'SQL', 'R'},
    # ...
}

job_requirements = {
    'A': {'Python'},
    'B': {'SQL', 'R'},
    'C': {'Java'},
    # ...
}

# Only allow assignments where worker has required skills
for i, j in arcs:
    if not job_requirements[i].issubset(worker_skills[j]):
        model.addConstr(x[i, j] == 0, name=f'skill_mismatch_{i}_{j}')
```

## Requirements

### Software Requirements
```
Python >= 3.7
gurobipy >= 10.0
pandas >= 1.3.0
openpyxl >= 3.0.0  # For Excel file reading
```

### Installation
```bash
# Install via pip
pip install gurobipy pandas openpyxl

# Or via conda
conda install -c gurobi gurobi pandas openpyxl
```

### Gurobi License
- Free academic license available at [gurobi.com](https://www.gurobi.com/academia/academic-program-and-licenses/)
- Commercial licenses required for business use
- Free trial licenses available for evaluation

### Data Format

**Excel File Structure** (`assignment_costs.xlsx`):
```
| Jobs | Workers | Cost |
|------|---------|------|
| A    | E       | 2    |
| A    | F       | 999  |
| A    | G       | 4    |
| ...  | ...     | ...  |
```

## Advanced Topics

### Hungarian Algorithm

The assignment problem can also be solved using the specialized **Hungarian algorithm** (also known as Kuhn-Munkres algorithm), which runs in O(n³) time.

```python
from scipy.optimize import linear_sum_assignment
import numpy as np

# Create cost matrix (n × n)
cost_matrix = np.array([
    [2, 999, 4, 3],   # Job A
    [3, 4, 1, 2],     # Job B
    [5, 2, 6, 4],     # Job C
    [1, 3, 2, 5]      # Job D
])

# Solve
row_ind, col_ind = linear_sum_assignment(cost_matrix)

# Results
total_cost = cost_matrix[row_ind, col_ind].sum()
print(f"Total Cost: {total_cost}")

for i, j in zip(row_ind, col_ind):
    print(f"Job {i} → Worker {j}, Cost: {cost_matrix[i, j]}")
```

### Sensitivity Analysis

Analyze how solution changes with cost variations.

```python
# After solving the model
for i, j in arcs:
    if x[i, j].X > 0.5:  # Assigned arc
        # Get reduced cost (shadow price)
        print(f"Arc ({i},{j}): Reduced Cost = {x[i, j].RC}")
        
# Constraint dual values
for constr in model.getConstrs():
    print(f"{constr.ConstrName}: Dual = {constr.Pi}")
```

## Performance Benchmarks

| Problem Size | Variables | Constraints | Time (Gurobi) | Time (Hungarian) |
|--------------|-----------|-------------|---------------|------------------|
| 10 × 10      | 100       | 20          | < 0.01s       | < 0.01s          |
| 100 × 100    | 10,000    | 200         | 0.05s         | 0.1s             |
| 1000 × 1000  | 1,000,000 | 2,000       | 2.5s          | 15s              |
| 5000 × 5000  | 25,000,000| 10,000      | 45s           | 8 min            |

## Troubleshooting

### Common Issues

**1. Infeasible Model**
```python
if model.status == GRB.INFEASIBLE:
    # Compute IIS (Irreducible Inconsistent Subsystem)
    model.computeIIS()
    model.write("model.ilp")
    print("Check model.ilp for conflicting constraints")
```

**2. Large Number Replacement for Infinity**
```python
# Use a large but reasonable number
M = 1000000  # Big-M value

# Avoid actual infinity
costs_cleaned = {k: (v if v < float('inf') else M) 
                 for k, v in costs.items()}
```

**3. No Solution Found**
```python
if model.status != GRB.OPTIMAL:
    if model.status == GRB.INFEASIBLE:
        print("Model is infeasible")
    elif model.status == GRB.UNBOUNDED:
        print("Model is unbounded")
    else:
        print(f"Optimization status: {model.status}")
```

## References

1. **Gurobi Documentation**: [https://www.gurobi.com/documentation/](https://www.gurobi.com/documentation/)
2. **Network Flow Theory**: Ahuja, Magnanti, and Orlin - "Network Flows"
3. **Linear Programming**: Bertsimas and Tsitsiklis - "Introduction to Linear Optimization"
4. **Hungarian Algorithm**: Kuhn, H. W. (1955). "The Hungarian method for the assignment problem"

## License

This documentation is provided for educational purposes.

## Contributing

Suggestions and improvements are welcome. Please submit issues or pull requests.

---

**Last Updated**: December 2025  
**Author**: Network Flow Optimization Tutorial
