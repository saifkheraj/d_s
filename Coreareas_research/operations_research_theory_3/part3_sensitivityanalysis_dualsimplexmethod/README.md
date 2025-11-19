# Linear Programming: Evaluating New Variables
## Hospital Emergency Department Example

---

## Part 1: The Original Problem

### Simple Emergency Department Setup

A hospital's emergency department has **2 types of patient cases** and **2 limited resources** per day:

| Case Type | Revenue per Patient | Doctors Needed | Beds Needed |
|-----------|-------------------|----------------|------------|
| **Minor Injuries (MI)** | 100 | 1 doctor | 1 bed |
| **Urgent Care (UC)** | 200 | 1 doctor | 2 beds |

**Daily Resources Available:**
- Doctors: 4 available
- Beds: 6 available

### Mathematical Formulation (Part 1)

**Decision Variables:**

$$X_1 = \text{Number of Minor Injury patients per day}$$

$$X_2 = \text{Number of Urgent Care patients per day}$$

**Objective Function (What we want to maximize):**

$$\text{Maximize: } Z = 100X_1 + 200X_2$$

**Constraints (Limits we must respect):**

$$X_1 + X_2 \leq 4 \quad \text{(Doctors: only 4 available)}$$

$$X_1 + 2X_2 \leq 6 \quad \text{(Beds: only 6 available)}$$

$$X_1, X_2 \geq 0 \quad \text{(Non-negativity)}$$

### Current Solution (Using Simplex)

The hospital optimizes and finds:
- $X_1 = 2$ (Treat 2 Minor Injury patients)
- $X_2 = 2$ (Treat 2 Urgent Care patients)
- **Daily Revenue** $Z = 600$

**Resource Usage:**
- Doctors: $1(2) + 1(2) = 4$ ✓ Fully used
- Beds: $1(2) + 2(2) = 6$ ✓ Fully used

---

## Part 2: New Service Introduction

### A New Service Appears

The hospital wants to add **Observation Room (OR)** for monitoring cases:
- **Revenue per Patient:** 400 (high demand)
- **Resources Needed:** 0 doctors, 1 bed only (no doctor needed!)

### Mathematical Formulation (Part 2 - FULL RE-SOLVE from Scratch)

**Decision Variables (EXPANDED):**

$$X_1 = \text{Number of Minor Injury patients per day}$$

$$X_2 = \text{Number of Urgent Care patients per day}$$

$$X_3 = \text{Number of Observation Room patients per day} \quad \leftarrow \text{NEW!}$$

**NEW Objective Function (CHANGED):**

$$\text{Maximize: } Z = 100X_1 + 200X_2 + 400X_3$$

**Constraints (UNCHANGED LIMITS):**

$$X_1 + X_2 + 0X_3 \leq 4 \quad \text{(OR uses no doctors)}$$

$$X_1 + 2X_2 + X_3 \leq 6 \quad \text{(OR uses 1 bed per patient)}$$

$$X_1, X_2, X_3 \geq 0$$

**Important Points:**
- ✅ Resource LIMITS unchanged (still 4 doctors, 6 beds)
- ✅ Constraint STRUCTURE unchanged (still 2 constraints)
- ✅ Just add $X_3$ coefficients to each constraint
- ✅ Objective function EXPANDS with $400X_3$ term

### New Optimal Solution (If Solved from Scratch)

When solved completely fresh:
- $X_1 = 0$ (no Minor Injuries)
- $X_2 = 0$ (no Urgent Care)
- $X_3 = 6$ (all Observation Rooms)
- **Daily Revenue:** $Z = 2400$

**Check constraints:**
- Doctors: $1(0) + 1(0) + 0(6) = 0 \leq 4$ ✓
- Beds: $1(0) + 2(0) + 1(6) = 6 \leq 6$ ✓

---

## Part 3: The Problem & Smart Solution

### The Real Question

What if Observation Room isn't perfect? What if it needs **some doctor time** too? Then:
- We might NOT want to drop MI and UC completely
- We might want **a mix** of all three services
- We need to **decide carefully** without solving everything from scratch

### The Inefficient Way
```
Start from beginning → Run full simplex → Find mix → Takes hours/days
```

### The Smart Way (Sensitivity Analysis)
```
Use current solution (2 MI, 2 UC) as starting point → 
Check if OR is worth adding → Add OR column → Run just a few iterations → 
Get answer in minutes!
```

### Why This Saves Time

- Hospital already spent time finding the current plan (2 MI, 2 UC)
- New situation changed slightly (added OR service)
- Instead of starting over, **start from what you already know**
- Small adjustments to reach new optimum

---

## Part 4: How to Do It - The Reduced Cost Method

### Smart Approach: Use Old Solution as Starting Point

**Key Idea: We use the SAME formulation as Part 2, but with a smart starting point!**

**Mathematical Formulation (Part 4 - SAME as Part 2):**

**Objective Function (SAME - No change):**

$$\text{Maximize: } Z = 100X_1 + 200X_2 + 400X_3$$

**Constraints (SAME - No change):**

$$X_1 + X_2 + 0X_3 \leq 4$$

$$X_1 + 2X_2 + X_3 \leq 6$$

$$X_1, X_2, X_3 \geq 0$$

**The Difference: Our STARTING POINT**

Instead of starting from scratch $(X_1=0, X_2=0, X_3=0)$, we use:

**STARTING POINT (Use Old Optimal + Set $X_3 = 0$):**

$$X_1 = 2 \quad \text{(From original optimal)}$$

$$X_2 = 2 \quad \text{(From original optimal)}$$

$$X_3 = 0 \quad \text{(New variable, set to zero initially)}$$

**Current Revenue:** $Z = 100(2) + 200(2) + 400(0) = 600$

**Verify this starting point is feasible:**
- Doctors: $1(2) + 1(2) + 0(0) = 4 \leq 4$ ✓
- Beds: $1(2) + 2(2) + 1(0) = 6 \leq 6$ ✓
- All variables $\geq 0$ ✓

**Why This Works:**
- The old solution still satisfies the new constraints!
- It's just missing the benefit of $X_3$
- Perfect starting point for optimization

---

### Step 1: Check If $X_3$ Should Increase from 0

**Question: Is it worth increasing $X_3$ from 0?**

#### What is Reduced Cost?

**Reduced cost** tells us: **If we force $X_3$ to enter the solution (increase from 0 to 1), how much will our total profit change?**

#### Current Situation:

**Current Plan:**
- $X_1 = 2$ Minor Injuries → Revenue: $2 \times 100 = 200$
- $X_2 = 2$ Urgent Care → Revenue: $2 \times 200 = 400$
- $X_3 = 0$ Observation Rooms → Revenue: $0 \times 400 = 0$
- **TOTAL REVENUE = 600**

**Resource Usage:**
- Doctors: $1(2) + 1(2) = 4$ ← **FULL! No room!**
- Beds: $1(2) + 2(2) = 6$ ← **FULL! No room!**

#### What Happens If We Add 1 Observation Room Patient?

**We have NO FREE resources!** So we must remove an existing service.

**Option 1: Remove 1 Minor Injury Patient**

**BEFORE:**
- $X_1 = 2, \quad X_2 = 2, \quad X_3 = 0$
- Revenue = $200 + 400 + 0 = 600$
- Doctors used: $1(2) + 1(2) = 4$
- Beds used: $1(2) + 2(2) = 6$

**AFTER (Remove 1 MI, Add 1 OR):**
- $X_1 = 1, \quad X_2 = 2, \quad X_3 = 1$
- Revenue = $100 + 400 + 400 = 900$
- Doctors used: $1(1) + 1(2) + 0(1) = 3$ (Freed 1 doctor!)
- Beds used: $1(1) + 2(2) + 1(1) = 6$ (Still full)

**NET CHANGE: $900 - 600 = +300$**

**Why?**
- We lost: 1 MI patient = $-100$
- We gained: 1 OR patient = $+400$
- Net: $-100 + 400 = +300$

#### The Formula Makes Sense Now:

$$\text{Reduced Cost}(X_3) = \text{Revenue we gain} - \text{Revenue we lose}$$

$$= 400 - 100 = 300$$

**The 100 is the revenue of the CHEAPEST service we have to remove!**

---

#### Option 2: Remove 1 Urgent Care Patient

**BEFORE:**
- $X_1 = 2, \quad X_2 = 2, \quad X_3 = 0$
- Revenue = 600
- Doctors used: 4
- Beds used: 6

**AFTER (Remove 1 UC, Add 1 OR):**
- $X_1 = 2, \quad X_2 = 1, \quad X_3 = 1$
- Revenue = $200 + 200 + 400 = 800$
- Doctors used: $1(2) + 1(1) + 0(1) = 3$
- Beds used: $1(2) + 2(1) + 1(1) = 5$ (Freed 1 bed!)

**NET CHANGE: $800 - 600 = +200$**

**Why lower than Option 1?**
- We lost: 1 UC patient = $-200$ (MORE expensive!)
- We gained: 1 OR patient = $+400$
- Net: $-200 + 400 = +200$ (worse than removing MI!)

**So we should remove the CHEAPEST option (MI at 100), not the expensive one (UC at 200)**

---

#### IMPORTANT: Why Remove MI? (Looking at BOTH Revenue AND Resources!)

**This is the KEY insight! We must consider BOTH:**
1. **Revenue impact** (what we lose in dollars)
2. **Resource consumption** (what resources each service uses)

#### What Resources Does Each Service Use?

**Minor Injury (MI):**
- Needs: 1 doctor + 1 bed
- Revenue: 100

**Urgent Care (UC):**
- Needs: 1 doctor + 2 beds
- Revenue: 200

**Observation Room (OR):**
- Needs: 0 doctors + 1 bed ← KEY!
- Revenue: 400

#### Current Resource Status:

- Doctors: 4 (WE USE ALL 4 - FULLY USED!)
- Beds: 6 (WE USE ALL 6 - FULLY USED!)

---

#### Now Here's the Critical Question:

**What does OR need?** 0 doctors + 1 bed

**This means:**
- We DON'T need to free up doctors (OR uses 0!)
- We ONLY need to free up beds!

---

#### Comparison: Remove MI vs Remove UC

**Option 1: Remove 1 MI**

**What we LOSE:**
- Revenue: $-100$
- Resources freed: 1 doctor + 1 bed

**What we GAIN:**
- Revenue: $+400$ (from 1 OR)
- OR needs: 0 doctors + 1 bed

**ANALYSIS:**
- Doctors: Free 1, need 0 → 1 WASTED
- Beds: Free 1, need 1 → PERFECT! ✓
- Net revenue: $-100 + 400 = +300$

---

**Option 2: Remove 1 UC**

**What we LOSE:**
- Revenue: $-200$
- Resources freed: 1 doctor + 2 beds

**What we GAIN:**
- Revenue: $+400$ (from 1 OR)
- OR needs: 0 doctors + 1 bed

**ANALYSIS:**
- Doctors: Free 1, need 0 → 1 WASTED
- Beds: Free 2, need 1 → 1 WASTED
- Net revenue: $-200 + 400 = +200$

---

#### The Key Comparison Table:

| | Revenue Loss | Doctors Freed | Beds Freed | Net Gain | Efficiency |
|---|---|---|---|---|---|
| **Remove MI** | -100 | 1 (wasted) | 1 (used) | +300 | ✓ Less waste |
| **Remove UC** | -200 | 1 (wasted) | 2 (1 wasted) | +200 | ✗ More waste |

**Why Remove MI is Better:**

1. ✅ **Lower revenue loss** (100 vs 200)
2. ✅ **Less resource waste** (free exactly what we need!)
3. ✅ **Higher profit gain** (+300 vs +200)
4. ✅ **More efficient** (don't overfree resources)

---

#### The Real Logic (Why Remove MI - DETAILED):

**Step 1: What does the new service need?**

OR needs: 0 doctors + 1 bed

**CONSTRAINT STATUS:**
- Doctor constraint: NOT bottleneck for OR (needs 0)
- Bed constraint: IS bottleneck for OR (needs 1)

**Step 2: Which service should we remove to free beds efficiently?**

For every bed freed, how much revenue do we lose?

$$\text{MI: } \frac{100}{1 \text{ bed}} = 100 \text{ per bed} \quad \leftarrow \text{LOWEST!}$$

$$\text{UC: } \frac{200}{2 \text{ beds}} = 100 \text{ per bed}$$

**Both have same ratio! So we remove MI because:**
- We only need 1 bed freed
- MI frees exactly 1 bed (no waste)
- UC frees 2 beds (1 wasted)

**Step 3: Remove MI**

Old plan: $2 \text{MI} + 2 \text{UC} + 0 \text{OR} = 600$

New plan: $1 \text{MI} + 2 \text{UC} + 1 \text{OR} = 900$ ✓

---

#### Summary: Your Tradeoff Concern is VALID

**You're right that:**
- Removing low-profit services (like MI) seems wasteful because they're efficient
- But removing high-profit services (like UC) also wastes resources

**The resolution:**
- **Always calculate the net benefit** (new revenue - old revenue)
- **The service giving HIGHEST net benefit should be removed**
- This automatically balances your tradeoff!

**The formula does this for you:**

**Decision Rule:**

$$\text{Remove service} = \text{Argmax(Reduced Cost)}$$

**In plain English:** Remove whichever service gives you the biggest net profit improvement!

---

#### Simple Summary - The Decision Logic:

| Criteria | MI | UC |
|----------|----|----|
| Revenue per bed sacrificed | 100 | 100 |
| Beds freed when we remove 1 | 1 | 2 |
| Doctors freed when we remove 1 | 1 | 1 |
| Do we NEED those doctors? | No | No |
| Do we need those beds? | 1 out of 1 | 1 out of 2 |
| **Waste level** | **None** | **50% waste** |
| **Better choice?** | **✓ YES** | No |

**Bottom line:** Remove the service that wastes the LEAST resources when we remove it!

---

#### The Reduced Cost Formula Explained:

$$\text{Reduced Cost}(X_3) = \text{Revenue from } X_3 - \text{Revenue of cheapest service to remove}$$

$$= 400 - 100 = 300$$

**Decision Rule:**
- If Reduced Cost $> 0$ → **YES, add $X_3$!** (We gain money)
- If Reduced Cost $< 0$ → **NO, don't add $X_3$!** (We lose money)
- If Reduced Cost $= 0$ → **NEUTRAL** (No change)

**Our case:** $300 > 0$, so **YES, we should add Observation Rooms!**

---

### Step 2: How Many $X_3$ Can We Add?

**The Trade-off Calculation:**

Current setup:
- 6 beds total
- Each $X_3$ (Observation Room) uses 1 bed
- Each $X_2$ (Urgent Care) uses 2 beds

**If we remove 1 Urgent Care patient:**
- Frees up: 2 beds
- Can add: 2 Observation Rooms
- Revenue change: $-200 + 800 = +600$ improvement!

### Step 3: New Solution Found

**Updated Plan:**

$$X_1 = 2, \quad X_2 = 1, \quad X_3 = 2$$

$$Z = 100(2) + 200(1) + 400(2) = 200 + 200 + 800 = 1200$$

**Progress: From 600 to 1200 by adjusting existing solution!**

**Verify constraints:**
- Doctors: $1(2) + 1(1) + 0(2) = 3 \leq 4$ ✓
- Beds: $1(2) + 2(1) + 1(2) = 6 \leq 6$ ✓

### Step 4: Continue Checking for Improvements

**Can we improve further?**

Check: Can we swap another Minor Injury for Observation Rooms?
- Remove 1 MI: Frees 1 bed
- Add 1 more OR: Revenue change $= -100 + 400 = +300$

**New improved solution:**

$$X_1 = 1, \quad X_2 = 1, \quad X_3 = 3$$

$$Z = 100(1) + 200(1) + 400(3) = 100 + 200 + 1200 = 1500$$

**Keep improving until no more beneficial swaps exist!**

---

## Part 5: Solving Using Matrix and Tableau Methods

### Understanding Basic and Non-Basic Variables

**From the original problem:**

**Basic Variables (in the solution):**
$$X_1 = 2, \quad X_2 = 2$$

**Non-Basic Variables (not used):**
- None in original (we only had 2 variables)

**After adding $X_3$:**

**Basic Variables (in the solution):**
$$X_1 = 2, \quad X_2 = 2$$

**Non-Basic Variables (not in the solution):**
$$X_3 = 0 \quad \leftarrow \text{NEW! Currently zero}$$

With 2 constraints (doctors, beds), we can only have 2 basic variables!
So $X_3$ MUST be non-basic at first.

---

### The Simplex Tableau Method

#### What is the Simplex Tableau?

It's a table that shows the current solution with:
- **Objective row** (bottom): The reduced costs
- **Constraint rows** (top): The coefficients
- **Identity matrix columns**: Show which variables are basic

#### Original Optimal Tableau (With 2 Variables)

At optimality for the original problem:

| | $X_1$ | $X_2$ | $s_1$ | $s_2$ | RHS |
|---|---|---|---|---|---|
| $X_1$ | 1 | 0 | 2 | -1 | 2 |
| $X_2$ | 0 | 1 | -1 | 1 | 2 |
| $Z$ | 0 | 0 | 100 | 100 | 600 |

**Read this tableau:**
- $X_1$ is basic (identity pattern) $= 2$
- $X_2$ is basic (identity pattern) $= 2$
- $s_1, s_2$ are non-basic $= 0$
- All reduced costs (bottom row) are $\geq 0$ → OPTIMAL! ✓
- Objective value $= 600$

---

#### Adding New Variable $X_3$ to the Tableau

**Now we add $X_3$ column:**

| | $X_1$ | $X_2$ | $X_3$ | $s_1$ | $s_2$ | RHS |
|---|---|---|---|---|---|---|
| $X_1$ | 1 | 0 | ? | 2 | -1 | 2 |
| $X_2$ | 0 | 1 | ? | -1 | 1 | 2 |
| $Z$ | 0 | 0 | ? | 100 | 100 | 600 |

We need to calculate the question marks!

---

### Step 1: Extract Problem Data

**Maximize:** $Z = 100X_1 + 200X_2 + 400X_3$

**Subject to:**

$$1 \cdot X_1 + 1 \cdot X_2 + 0 \cdot X_3 \leq 4 \quad \text{(Doctors)}$$

$$1 \cdot X_1 + 2 \cdot X_2 + 1 \cdot X_3 \leq 6 \quad \text{(Beds)}$$

**Extract data for $X_3$:**

$$C_3 = 400 \quad \text{(Revenue from one OR patient)}$$

$$\mathbf{A}_3 = \begin{pmatrix} 0 \\ 1 \end{pmatrix} \quad \text{(Resources needed by } X_3 \text{)}$$

**What do these mean?**
- $C_3 = 400$: Each OR patient brings 400 in revenue
- $\mathbf{A}_3 = [0, 1]^T$: Each OR patient needs 0 doctor hours and 1 bed hour

---

### Step 2: Define the Basis Matrix and Calculate Its Inverse

#### What is a Basis Matrix $B$?

A basis matrix contains the **coefficients of the current basic variables** from the constraints.

**Remember:** In our hospital example:
- **2 constraints** (Doctors and Beds)
- **2 basic variables** ($X_1$ and $X_2$ currently in the solution)
- **Rule:** Number of basic variables = Number of constraints

#### The Constraints from the Original Problem:

$$1 \cdot X_1 + 1 \cdot X_2 + 0 \cdot X_3 \leq 4 \quad \text{(Doctors)}$$

$$1 \cdot X_1 + 2 \cdot X_2 + 1 \cdot X_3 \leq 6 \quad \text{(Beds)}$$

#### Which variables are currently basic?

From our optimal solution:
- $X_1 = 2$ ✓ (BASIC - in the solution)
- $X_2 = 2$ ✓ (BASIC - in the solution)
- $X_3 = 0$ ✗ (NON-BASIC - not in solution)

---

#### Building the Basis Matrix $B$

**Constraint Matrix $A$ (all variables):**

$$\mathbf{A} = \begin{pmatrix} 1 & 1 & 0 \\ 1 & 2 & 1 \end{pmatrix}$$

Reading this matrix:
- Row 1 (Doctors): $[1, 1, 0]$ for $[X_1, X_2, X_3]$
- Row 2 (Beds): $[1, 2, 1]$ for $[X_1, X_2, X_3]$

**Extract ONLY the columns for basic variables** $X_1$ and $X_2$:

$$\mathbf{B} = \begin{pmatrix} 1 & 1 \\ 1 & 2 \end{pmatrix}$$

This is the **Basis Matrix!**

---

#### Calculate $B^{-1}$ (Inverse of Basis Matrix)

For a $2 \times 2$ matrix:

$$\begin{pmatrix} a & b \\ c & d \end{pmatrix}^{-1} = \frac{1}{ad-bc} \begin{pmatrix} d & -b \\ -c & a \end{pmatrix}$$

**Our calculation:**

$$\det(B) = (1)(2) - (1)(1) = 2 - 1 = 1$$

$$\mathbf{B}^{-1} = \frac{1}{1} \begin{pmatrix} 2 & -1 \\ -1 & 1 \end{pmatrix} = \begin{pmatrix} 2 & -1 \\ -1 & 1 \end{pmatrix}$$

---

#### Verify $B^{-1}$ Works

$$\mathbf{B}^{-1} \times \mathbf{b} = \mathbf{X}_B$$

$$\begin{pmatrix} 2 & -1 \\ -1 & 1 \end{pmatrix} \times \begin{pmatrix} 4 \\ 6 \end{pmatrix} = \begin{pmatrix} 2(4) + (-1)(6) \\ (-1)(4) + 1(6) \end{pmatrix} = \begin{pmatrix} 8-6 \\ -4+6 \end{pmatrix} = \begin{pmatrix} 2 \\ 2 \end{pmatrix}$$

Perfect! We get $X_1 = 2, X_2 = 2$ ✓

---

### Step 3: Calculate $B^{-1} \times A_j$ for NON-BASIC Variables

**IMPORTANT RULE:** We ALWAYS check $B^{-1} \times A_j$ where $j$ = NON-BASIC variable

In the **CURRENT iteration:**
- Basic variables: $X_1, X_2$
- Non-basic variables: $X_3$

Therefore, check: $B^{-1} \times A_3$

**Matrix multiplication:**

$$\begin{pmatrix} 2 & -1 \\ -1 & 1 \end{pmatrix} \times \begin{pmatrix} 0 \\ 1 \end{pmatrix} = \begin{pmatrix} 2(0) + (-1)(1) \\ (-1)(0) + 1(1) \end{pmatrix} = \begin{pmatrix} -1 \\ 1 \end{pmatrix}$$

**Result:**

$$\mathbf{B}^{-1} \times \mathbf{A}_3 = \begin{pmatrix} -1 \\ 1 \end{pmatrix}$$

**Interpretation:**
- When we increase $X_3$ by 1 unit, $X_1$ changes by -1 (decreases by 1)
- When we increase $X_3$ by 1 unit, $X_2$ changes by +1 (increases by 1)

---

### Step 4: Calculate Reduced Cost

**Define $\mathbf{C}_B$** (the objective coefficients of basic variables):

$$\mathbf{C}_B = \begin{pmatrix} C_1 \\ C_2 \end{pmatrix} = \begin{pmatrix} 100 \\ 200 \end{pmatrix}$$

#### The Reduced Cost Formula:

**Standard Form:**

$$RC_j = \mathbf{C}_B^T \times \mathbf{B}^{-1} \times \mathbf{A}_j - C_j$$

**Alternative Form (showing components):**

$$RC_j = \mathbf{C}_B^T \times \mathbf{B}^{-1} \times \mathbf{A}_N - \mathbf{C}_N^T$$

**For our problem with $X_3$:**

$$RC_3 = \mathbf{C}_B^T \times \mathbf{B}^{-1} \times \mathbf{A}_3 - C_3$$

Where:
- $\mathbf{C}_B$ = Coefficients of basic variables = $[100, 200]^T$
- $\mathbf{B}^{-1}$ = Inverse of basis matrix
- $\mathbf{A}_3$ = Column coefficients for new variable $X_3$ = $[0, 1]^T$
- $C_3$ = Direct objective coefficient for $X_3$ = 400

**What These Components Mean:**

1. **$\mathbf{C}_B^T \times \mathbf{B}^{-1} \times \mathbf{A}_j$** = Shadow price / opportunity cost
   - This calculates the "cost" to the current basis if we introduce variable $j$
   - It's the value lost from the current basic variables

2. **$C_j$** = Direct benefit of new variable
   - This is the direct contribution to profit if we add variable $j$

3. **$RC_j = \text{Direct benefit} - \text{Opportunity cost}$**
   - If positive: Cost of displacing basic variables is high, don't add
   - If negative: Benefit outweighs cost, add this variable! ✓

#### Step 4a: Transpose $\mathbf{C}_B$

$$\mathbf{C}_B^T = \begin{pmatrix} 100 & 200 \end{pmatrix}$$

#### Step 4b: Calculate $\mathbf{C}_B^T \times \mathbf{B}^{-1}$

$$\begin{pmatrix} 100 & 200 \end{pmatrix} \times \begin{pmatrix} 2 & -1 \\ -1 & 1 \end{pmatrix}$$

$$= \begin{pmatrix} 100(2) + 200(-1) & 100(-1) + 200(1) \end{pmatrix}$$

$$= \begin{pmatrix} 200 - 200 & -100 + 200 \end{pmatrix} = \begin{pmatrix} 0 & 100 \end{pmatrix}$$

#### Step 4c: Multiply by $\mathbf{A}_3$

$$\begin{pmatrix} 0 & 100 \end{pmatrix} \times \begin{pmatrix} 0 \\ 1 \end{pmatrix} = 0(0) + 100(1) = 100$$

#### Step 4d: Subtract $C_3$

$$\text{Reduced Cost}(X_3) = 100 - 400 = -300$$

---

#### Notation Reference: Understanding the Formula

**You pointed out the complete standard form:**

$$RC = c_B^T B^{-1} A_N - c_N^T$$

**This is equivalent to what we calculated:**

$$RC_j = c_B^T B^{-1} A_j - c_j$$

**Breaking down the notation:**

| Notation | Meaning | In Our Problem | Value |
|----------|---------|---|---|
| $c_B^T$ | Transpose of basic variable costs | $[100, 200]$ | $[100, 200]$ |
| $B^{-1}$ | Inverse of basis matrix | $\begin{pmatrix} 2 & -1 \\ -1 & 1 \end{pmatrix}$ | Given |
| $A_j$ or $A_N$ | Column of constraint coefficients for new variable | $\begin{pmatrix} 0 \\ 1 \end{pmatrix}$ | $\begin{pmatrix} 0 \\ 1 \end{pmatrix}$ |
| $c_j$ or $c_N^T$ | Objective coefficient of new variable | 400 | 400 |

**What the formula calculates:**
1. **$c_B^T B^{-1} A_N = 100$** = Shadow cost / opportunity cost
   - Cost to current basis if we introduce the new variable
   
2. **$-c_N^T = -400$** = Negative of new variable's benefit

3. **Total = $100 - 400 = -300$** = Net reduced cost
   - Negative means we gain 300 in profit by adding this variable ✓

---

#### What Does Reduced Cost = -300 Mean?

**Decision Rule for MAXIMIZATION:**
- If Reduced Cost $< 0$ → Variable **SHOULD ENTER** the basis ✓ (improves objective)
- If Reduced Cost $> 0$ → Variable should NOT enter ✗ (worsens objective)
- If Reduced Cost $= 0$ → Neutral (no change)

**In our case:**

$$\text{Reduced Cost}(X_3) = -300 < 0 \quad \Rightarrow \quad X_3 \text{ SHOULD ENTER!} \checkmark$$

**Interpretation:**
- For every 1 unit of $X_3$ we add, profit increases by 300
- This matches our intuitive calculation: Remove 1 MI (-100) + Add 1 OR (+400) = Net gain +300

---

#### Updated Tableau with $X_3$ Column

| | $X_1$ | $X_2$ | $X_3$ | $s_1$ | $s_2$ | RHS |
|---|---|---|---|---|---|---|
| $X_1$ | 1 | 0 | -1 | 2 | -1 | 2 |
| $X_2$ | 0 | 1 | 1 | -1 | 1 | 2 |
| $Z$ | 0 | 0 | **-300** | 100 | 100 | 600 |

**NEGATIVE reduced cost means we should increase $X_3$ (enter the basis)!**

---

### Ratio Test: Which Variable Leaves?

**We want to increase $X_3$ from 0. But how much?**

**Ratio test:**

$$\text{Maximum } X_3 = \min\left(\frac{\text{RHS}_i}{\text{Coefficient in } X_3 \text{ column}}\right)$$

**For positive coefficients only:**
- $X_1$: Coefficient is -1 (negative, skip)
- $X_2$: $\frac{2}{1} = 2$ (positive, include)

**Result:** $X_3$ can increase to 2 units before $X_2$ becomes 0.

**Decision:** $X_2$ leaves, $X_3$ enters with value 2.

---

### New Solution After One Iteration

**After pivoting (row operations):**

$$X_1 = 2 - 1(2) = 0$$

$$X_3 = 2$$

$$\text{Revenue: } Z = 100(0) + 200(0) + 400(2) = 800$$

**Progress: From 600 to 800**

Continue iterating until all reduced costs are $\geq 0$ (OPTIMAL).

---

## Complete Process Comparison

```
PART 1: Original Problem
├─ Variables: X₁, X₂
├─ Objective: Z = 100X₁ + 200X₂
├─ Doctors constraint: X₁ + X₂ ≤ 4
├─ Beds constraint: X₁ + 2X₂ ≤ 6
└─ Solution: X₁=2, X₂=2, Z=600

PART 2: New Service (FULL RE-SOLVE)
├─ Variables: X₁, X₂, X₃
├─ Objective: Z = 100X₁ + 200X₂ + 400X₃
├─ Doctors constraint: X₁ + X₂ + 0X₃ ≤ 4
├─ Beds constraint: X₁ + 2X₂ + X₃ ≤ 6
├─ Start from: X₁=0, X₂=0, X₃=0
└─ Solution: X₁=0, X₂=0, X₃=6, Z=2400 (many iterations)

PARTS 3-4: SMART WAY (Using old solution as starting point)
├─ Same formulation as Part 2
├─ START from: X₁=2, X₂=2, X₃=0 (use old optimal!)
├─ Calculate reduced cost: -300
├─ Run ONLY a few iterations
└─ Solution: X₁=1, X₂=1, X₃=3, Z=1500 (QUICK!)
```

---

## What CHANGES vs What STAYS SAME

### What STAYS SAME:
- ✅ **Constraint Limits** (still 4 doctors, 6 beds)
- ✅ **Constraint Structure** (still 2 constraints)
- ✅ **Resource Requirements for Old Services** ($X_1$ and $X_2$ coefficients unchanged)
- ✅ **Old Variables Coefficients** in objective function

### What CHANGES:
- ❌ **Decision Variables** (add $X_3$)
- ❌ **Objective Function** (add $400X_3$ term)
- ❌ **Constraint Coefficients** (add $X_3$ column)
- ❌ **Optimal Solution** (will change from $X_1=2, X_2=2$ to new values)
- ❌ **Maximum Revenue** (changed from 600 to higher value)

---

## Key Formulas Reference

| Formula | Purpose |
|---------|---------|
| $\mathbf{B}^{-1} \times \mathbf{A}_j$ | $X_3$ effect on current basis |
| $\mathbf{C}_B^T \times \mathbf{B}^{-1} \times \mathbf{A}_j - C_j$ | Reduced cost of new variable |
| $\min(\text{RHS}_i / \text{Coefficient}_i)$ for positive coefficients | Ratio test (entering variable limit) |

---

## When to Use Each Method

| Method | Pros | Cons |
|--------|------|------|
| **Intuitive Method** | Easy to understand; shows why decisions make sense | Hard to scale to many variables |
| **Tableau Method** | Systematic and organized; works for any size | Less intuitive initially |
| **Matrix Method** | Mathematically elegant; easiest for programming | Requires linear algebra knowledge |

**All three methods solve the SAME problem - just different ways of thinking about it!**

---

## Key Takeaway

✅ **When adding a new service to an existing plan:**

1. **Objective Function:** Add the new revenue term ($400X_3$)
2. **Constraints:** Add new variable coefficients, but **LIMITS STAY THE SAME**
3. **Starting Point:** Use previous optimal solution, set new $X_3=0$
4. **Iterate:** Only a few iterations needed instead of full re-solve

**No changing constraint limits! No starting from zero! Just add one column and iterate.**