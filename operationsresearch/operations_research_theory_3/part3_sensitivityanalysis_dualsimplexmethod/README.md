# Linear Programming: Evaluating New Variables
## Hospital Emergency Department Example

---

## Part 1: The Original Problem

### Simple Emergency Department Setup

A hospital's emergency department has **2 types of patient cases** and **2 limited resources** per day:

| Case Type | Revenue per Patient | Doctors Needed | Beds Needed |
|-----------|-------------------|----------------|------------|
| **Minor Injuries (MI)** | $100 | 1 doctor | 1 bed |
| **Urgent Care (UC)** | $200 | 1 doctor | 2 beds |

**Daily Resources Available:**
- Doctors: 4 available
- Beds: 6 available

### Mathematical Formulation (Part 1)

**Decision Variables:**
```
X1 = Number of Minor Injury patients per day
X2 = Number of Urgent Care patients per day
```

**Objective Function (What we want to maximize):**
```
Maximize: Z = 100·X1 + 200·X2
```

**Constraints (Limits we must respect):**
```
Doctors:      1·X1 + 1·X2 ≤ 4      (only 4 doctors available)
Beds:         1·X1 + 2·X2 ≤ 6      (only 6 beds available)
Non-negativity: X1 ≥ 0, X2 ≥ 0     (can't treat negative patients)
```

### Current Solution (Using Simplex)

The hospital optimizes and finds:
- **X1 = 2** (Treat 2 Minor Injury patients)
- **X2 = 2** (Treat 2 Urgent Care patients)
- **Daily Revenue Z = $600**

**Resource Usage:**
- Doctors: 1(2) + 1(2) = 4 ✓ Fully used
- Beds: 1(2) + 2(2) = 6 ✓ Fully used

---

## Part 2: New Service Introduction

### A New Service Appears

The hospital wants to add **Observation Room (OR)** for monitoring cases:
- **Revenue per Patient:** $400 (high demand)
- **Resources Needed:** 0 doctors, 1 bed only (no doctor needed!)

### Mathematical Formulation (Part 2 - FULL RE-SOLVE from Scratch)

**Decision Variables (EXPANDED - X3 IS NEW):**
```
X1 = Number of Minor Injury patients per day
X2 = Number of Urgent Care patients per day
X3 = Number of Observation Room patients per day ← NEW!
```

**NEW Objective Function (CHANGED - Added X3 term):**
```
Maximize: Z = 100·X1 + 200·X2 + 400·X3
                                  ↑
                        NEW coefficient for X3
```

**Constraints (UNCHANGED LIMITS - Same limits, just add X3 coefficients):**
```
Doctors:      1·X1 + 1·X2 + 0·X3 ≤ 4    (OR uses no doctors)
Beds:         1·X1 + 2·X2 + 1·X3 ≤ 6    (OR uses 1 bed per patient)
Non-negativity: X1 ≥ 0, X2 ≥ 0, X3 ≥ 0
```

**Important Points:**
- ✅ Resource LIMITS unchanged (still 4 doctors, 6 beds)
- ✅ Constraint STRUCTURE unchanged (still 2 constraints)
- ✅ Just add X3 coefficients to each constraint
- ✅ Objective function EXPANDS with 400·X3 term

### New Optimal Solution (If Solved from Scratch)

When solved completely fresh:
- **X1 = 0** (no Minor Injuries)
- **X2 = 0** (no Urgent Care)
- **X3 = 6** (all Observation Rooms)
- **Daily Revenue: Z = $2,400**

**Check constraints:**
- Doctors: 1(0) + 1(0) + 0(6) = 0 ≤ 4 ✓
- Beds: 1(0) + 2(0) + 1(6) = 6 ≤ 6 ✓

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
```
Maximize: Z = 100·X1 + 200·X2 + 400·X3
```

**Constraints (SAME - No change):**
```
Doctors:      1·X1 + 1·X2 + 0·X3 ≤ 4
Beds:         1·X1 + 2·X2 + 1·X3 ≤ 6
Non-negativity: X1 ≥ 0, X2 ≥ 0, X3 ≥ 0
```

**The Difference: Our STARTING POINT**

Instead of starting from scratch (X1=0, X2=0, X3=0), we use:

**STARTING POINT (Use Old Optimal + Set X3 = 0):**
```
X1 = 2  ← From original optimal (Part 1)
X2 = 2  ← From original optimal (Part 1)
X3 = 0  ← New variable, set to zero initially

Current Revenue: Z = 100(2) + 200(2) + 400(0) = $600
```

**Verify this starting point is feasible:**
- Doctors: 1(2) + 1(2) + 0(0) = 4 ≤ 4 ✓
- Beds: 1(2) + 2(2) + 1(0) = 6 ≤ 6 ✓
- All variables ≥ 0 ✓

**Why This Works:**
- The old solution still satisfies the new constraints!
- It's just missing the benefit of X3
- Perfect starting point for optimization

---

### Step 1: Check If X3 Should Increase from 0

**Question: Is it worth increasing X3 from 0?**

**Understanding the Reduced Cost - Detailed Explanation:**

#### What is Reduced Cost?

Reduced cost tells us: **If we force X3 to enter the solution (increase from 0 to 1), how much will our total profit change?**

#### Current Situation:
```
Current Plan:
X1 = 2 Minor Injuries  → Revenue: 2 × $100 = $200
X2 = 2 Urgent Care    → Revenue: 2 × $200 = $400
X3 = 0 Observation Rooms → Revenue: 0 × $400 = $0
─────────────────────────────────────────────
TOTAL REVENUE = $600
```

**Resource Usage:**
- Doctors: 1(2) + 1(2) = 4 ← **FULL! No room!**
- Beds: 1(2) + 2(2) = 6 ← **FULL! No room!**

#### What Happens If We Add 1 Observation Room Patient?

**We have NO FREE resources!** So we must remove an existing service.

**Option 1: Remove 1 Minor Injury Patient**

```
BEFORE:
X1 = 2, X2 = 2, X3 = 0
Revenue = $200 + $400 + $0 = $600
Doctors used: 1(2) + 1(2) = 4
Beds used: 1(2) + 2(2) = 6

AFTER (Remove 1 MI, Add 1 OR):
X1 = 1, X2 = 2, X3 = 1
Revenue = $100 + $400 + $400 = $900
Doctors used: 1(1) + 1(2) + 0(1) = 3 ← Freed 1 doctor!
Beds used: 1(1) + 2(2) + 1(1) = 6 ← Still full

NET CHANGE: $900 - $600 = +$300
```

**Why?**
- We lost: 1 MI patient = -$100
- We gained: 1 OR patient = +$400
- Net: -$100 + $400 = **+$300**

#### The Formula Makes Sense Now:

```
Reduced Cost(X3) = What we GAIN - What we LOSE

                 = (Revenue we add) - (Revenue we give up)
                 
                 = $400 - $100
                 
                 = $300
```

**The $100 is the revenue of the CHEAPEST service we have to remove!**

---

#### Let's Try Option 2: Remove 1 Urgent Care Patient

```
BEFORE:
X1 = 2, X2 = 2, X3 = 0
Revenue = $600
Doctors used: 4
Beds used: 6

AFTER (Remove 1 UC, Add 1 OR):
X1 = 2, X2 = 1, X3 = 1
Revenue = $200 + $200 + $400 = $800
Doctors used: 1(2) + 1(1) + 0(1) = 3
Beds used: 1(2) + 2(1) + 1(1) = 5 ← Now we freed 1 bed!

NET CHANGE: $800 - $600 = +$200
```

**Why lower than Option 1?**
- We lost: 1 UC patient = -$200 (MORE expensive!)
- We gained: 1 OR patient = +$400
- Net: -$200 + $400 = **+$200** (worse than removing MI!)

**So we should remove the CHEAPEST option (MI at $100), not the expensive one (UC at $200)**

---

#### IMPORTANT: Why Remove MI? (Looking at BOTH Revenue AND Resources!)

**This is the KEY insight! We must consider BOTH:**
1. **Revenue impact** (what we lose in dollars)
2. **Resource consumption** (what resources each service uses)

**Let me show the detailed comparison:**

---

#### What Resources Does Each Service Use?

```
Minor Injury (MI):
├─ Needs: 1 doctor + 1 bed
└─ Revenue: $100

Urgent Care (UC):
├─ Needs: 1 doctor + 2 beds
└─ Revenue: $200

Observation Room (OR):
├─ Needs: 0 doctors + 1 bed ← KEY: Doesn't need doctors!
└─ Revenue: $400
```

#### Current Resource Status:

```
Available:
- Doctors: 4 (WE USE ALL 4 - FULLY USED!)
- Beds: 6 (WE USE ALL 6 - FULLY USED!)

Current plan uses:
- Doctors: 1(MI) + 1(UC) = 2 doctors used out of 4... WAIT!
- Actually: 1(2 MI) + 1(2 UC) = 4 doctors total ✓
- Beds: 1(2 MI) + 2(2 UC) = 6 beds total ✓
```

---

#### Now Here's the Critical Question:

**What does OR need? 0 doctors + 1 bed**

**This means:**
- We DON'T need to free up doctors (OR uses 0!)
- We ONLY need to free up beds!

---

#### Comparison: Remove MI vs Remove UC

**Option 1: Remove 1 MI**

```
What we LOSE:
- Revenue: -$100
- Resources freed: 1 doctor + 1 bed

What we GAIN:
- Revenue: +$400 (from 1 OR)
- OR needs: 0 doctors + 1 bed

ANALYSIS:
- We free 1 doctor BUT OR needs 0 doctors → 1 doctor WASTED!
- We free 1 bed AND OR needs 1 bed → 1 bed USED! ✓
- Net revenue: -$100 + $400 = +$300
```

**Option 2: Remove 1 UC**

```
What we LOSE:
- Revenue: -$200
- Resources freed: 1 doctor + 2 beds

What we GAIN:
- Revenue: +$400 (from 1 OR)
- OR needs: 0 doctors + 1 bed

ANALYSIS:
- We free 1 doctor BUT OR needs 0 doctors → 1 doctor WASTED!
- We free 2 beds BUT OR needs 1 bed → 1 bed WASTED!
- Net revenue: -$200 + $400 = +$200
```

---

#### The Key Comparison Table:

```
                    Revenue    Doctors   Beds      Net        Efficiency
                    Loss       Freed     Freed     Gain       (Waste?)
────────────────────────────────────────────────────────────────────────
Remove MI:          -$100      1 (wasted) 1 (used) +$300      Less waste
Remove UC:          -$200      1 (wasted) 2 (1 wasted) +$200  More waste
────────────────────────────────────────────────────────────────────────
```

**Why Remove MI is Better:**

1. ✅ **Lower revenue loss** ($100 vs $200)
2. ✅ **Less resource waste** (free exactly what we need!)
3. ✅ **Higher profit gain** (+$300 vs +$200)
4. ✅ **More efficient** (don't overfree resources)

**Why NOT remove UC:**
- ❌ Higher revenue loss ($200 is more than $100)
- ❌ More resource waste (free 2 beds when we only need 1)
- ❌ Lower profit gain (+$200 is less than +$300)

---

#### The Real Logic (Why Remove MI - DETAILED):

**Step 1: What does the new service need?**
```
OR needs: 0 doctors + 1 bed

CONSTRAINT STATUS:
- Doctor constraint: NOT the bottleneck for OR (OR needs 0 doctors)
- Bed constraint: IS the bottleneck for OR (OR needs 1 bed)
```

**Step 2: Which service should we remove to free beds efficiently?**

For every bed freed, how much revenue do we lose?

```
MI: $100 revenue ÷ 1 bed = $100 per bed ← LOWEST!
UC: $200 revenue ÷ 2 beds = $100 per bed
```

**Both have same ratio! So we remove MI because:**
- We only need 1 bed freed
- MI frees exactly 1 bed (no waste)
- UC frees 2 beds (1 wasted)

**Step 3: Remove MI**
```
Old plan: 2 MI + 2 UC + 0 OR = $600
New plan: 1 MI + 2 UC + 1 OR = $900 ✓
```

---

#### IMPORTANT: The Tradeoff You Should Consider!

**You're absolutely correct to question this!** There IS a real tradeoff:

**Two competing concerns:**
1. **Minimize resource waste** → Remove service using least resources per unit
2. **Minimize profit loss** → Remove service with least revenue

**In our example, both point the same way:**
- Remove MI: Lowest revenue ($100) AND least resource waste
- Remove UC: Higher revenue ($250) AND more resource waste

**But they could conflict!** Let me show you:

---

#### When the Tradeoff Actually Conflicts

**Different scenario:**

| Service | Revenue | Doctors | Beds |
|---------|---------|---------|------|
| Service A | $50 | 1 | 5 |
| Service B | $300 | 1 | 1 |
| New Service | $400 | 0 | 1 |

Current: 1A + 1B = $350

**Remove Service A?**
- Lose revenue: $50 (LEAST!)
- Free: 1 doctor + 5 beds
- Need for new: 0 doctors + 1 bed
- **Waste: 1 doctor + 4 beds** (huge waste!)
- **Net gain: -$50 + $400 = +$350**

**Remove Service B?**
- Lose revenue: $300 (MORE!)
- Free: 1 doctor + 1 bed
- Need for new: 0 doctors + 1 bed
- **Waste: 1 doctor only** (less waste)
- **Net gain: -$300 + $400 = +$100**

**The Dilemma:**
- Service A has lowest revenue (good to remove) but wastes most resources (bad!)
- Service B has highest revenue (bad to remove) but wastes least resources (good!)

**Answer?** 
- **Remove A** because the net gain is higher (+$350 > +$100)
- Even though it wastes more resources!
- The huge profit difference ($300 vs $50 = $250) outweighs the waste consideration

**The Reduced Cost formula captures this automatically:**

$$\text{Reduced Cost}(A) = 400 - 50 = 350 \quad \text{(BEST)}$$
$$\text{Reduced Cost}(B) = 400 - 300 = 100 \quad \text{(WORSE)}$$

---

#### Why the Formula Handles Your Tradeoff

**The reduced cost formula is:**

$$\text{Net Benefit} = C_{\text{new service}} - C_{\text{removed service}}$$

**This formula considers:**
- ✓ Revenue of new service ($400)
- ✓ Revenue of removed service ($50 or $300)
- ✓ Resource constraints (implicitly through what we CAN remove)
- ✓ **The profit difference between them** (this is where your tradeoff matters!)

**It automatically balances:**
- Profit gained from new service
- Profit lost from removed service
- Resource efficiency

**All in one simple formula!**

---

#### Real Hospital Examples of Your Tradeoff

**Example 1: Should we add Basic Physio when we might remove Surgery?**

```
Current: 2 Emergency ($200 each) + 1 Major Surgery ($600)
New: Physical Therapy ($300, uses 2 nurses, 0 beds)

Remove Emergency?
- Lose: $200 (cheap service)
- Net: -$200 + $300 = +$100

Remove Surgery?
- Lose: $600 (expensive service!)
- Net: -$600 + $300 = -$300 (NEGATIVE! Don't do this!)
```

**Answer:** Only remove Emergency care (not Surgery), because Physio ($300) isn't valuable enough to justify losing Surgery revenue ($600).

**Example 2: Should we add Premium Surgery when we might remove basic services?**

```
Current: 2 Minor Injuries ($100) + 1 Urgent Care ($200)
New: Premium Surgery ($900, uses 3 doctors, 1 bed)

Remove Minor Injury?
- Lose: $100 (cheap!)
- Net: -$100 + $900 = +$800 ✓ GREAT

Remove Urgent Care?
- Lose: $200 (more expensive)
- Net: -$200 + $900 = +$700 ✓ Still great, but less

Remove Both?
- Lose: $300
- Net: -$300 + $900 = +$600 ✓ Still positive
```

**Answer:** Remove Minor Injuries first (+$800), then Urgent Care (+$700) if needed. The enormous value of Premium Surgery justifies removing even expensive services!

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

$$\text{Which service to remove?} = \arg\max(\text{Reduced Cost})$$

**In plain English:** Remove whichever service gives you the biggest net profit improvement!

#### Simple Summary - The Decision Logic:

**We remove MI (not UC) because:**

| Criteria | MI | UC |
|----------|----|----|
| Revenue per bed sacrificed | $100 | $100 |
| Beds freed when we remove 1 | 1 | 2 |
| Doctors freed when we remove 1 | 1 | 1 |
| Do we NEED those doctors? | No | No |
| Do we need those beds? | 1 out of 1 | 1 out of 2 |
| **Waste level** | **None** | **50% waste (1 bed wasted)** |
| **Better choice?** | **✓ YES** | No |

**Bottom line:** Remove the service that wastes the LEAST resources when we remove it!

---

#### The Reduced Cost Formula Explained:

```
Reduced Cost(X3) = Revenue from X3 - Revenue of cheapest service to remove

Reduced Cost(X3) = $400 - $100 = $300
                          ↑
                    This is X1 (Minor Injuries)
                    the cheapest service ($100)
```

**Decision Rule:**
- If Reduced Cost > 0 → **YES, add X3!** (We gain money)
- If Reduced Cost < 0 → **NO, don't add X3!** (We lose money)
- If Reduced Cost = 0 → **NEUTRAL** (No change)

**Our case:** $300 > 0, so **YES, we should add Observation Rooms!**

---

#### Real-World Analogy:

Imagine you have a restaurant:
- Table A: Customers spend $100
- Table B: Customers spend $200
- New Table C: Customers would spend $400

You only have 6 tables total and all are full.

If you want to add Table C, you must remove a table. Which one?
- Remove Table A (loses $100) → Net gain = $400 - $100 = **+$300** ✓ BEST!
- Remove Table B (loses $200) → Net gain = $400 - $200 = **+$200**

**The reduced cost of $300 tells us: "By adding Table C, net gain is $300"**

### Step 2: How Many X3 Can We Add?

**The Trade-off Calculation:**

Current setup:
- 6 beds total
- Each X3 (Observation Room) uses 1 bed
- Each X2 (Urgent Care) uses 2 beds

**If we remove 1 Urgent Care patient:**
- Frees up: 2 beds
- Can add: 2 Observation Rooms
- Revenue change: -$200 (lost UC) + $800 (gained 2 OR) = **+$600 improvement!**

### Step 3: New Solution Found

**Updated Plan:**
```
X1 = 2  (Minor Injuries - unchanged)
X2 = 1  (Urgent Care - reduced from 2)
X3 = 2  (Observation Rooms - added)

New Revenue: Z = 100(2) + 200(1) + 400(2) = $200 + $200 + $800 = $1,200
```

**Progress: From $600 → $1,200 by adjusting existing solution!**

**Verify constraints still satisfied:**
- Doctors: 1(2) + 1(1) + 0(2) = 3 ≤ 4 ✓
- Beds: 1(2) + 2(1) + 1(2) = 6 ≤ 6 ✓

### Step 4: Continue Checking for Improvements

**Can we improve further?**

Check: Can we swap another Minor Injury for Observation Rooms?
- Remove 1 MI (X1): Frees 1 bed
- Add 1 more OR: Revenue change: -$100 + $400 = +$300

**New improved solution:**
```
X1 = 1  (Minor Injuries - reduced to 1)
X2 = 1  (Urgent Care - stays at 1)
X3 = 3  (Observation Rooms - increased)

New Revenue: Z = 100(1) + 200(1) + 400(3) = $100 + $200 + $1,200 = $1,500
```

**Keep improving until no more beneficial swaps exist!**

---

## What CHANGES vs What STAYS SAME

### What STAYS SAME (No change):
- ✅ **Constraint Limits** (still 4 doctors, 6 beds)
- ✅ **Constraint Structure** (still 2 constraints)
- ✅ **Resource Requirements for Old Services** (X1 and X2 coefficients unchanged)
- ✅ **Old Variables X1, X2** (their coefficients in objective)

### What CHANGES (When new variable added):
- ❌ **Decision Variables** (add X3)
- ❌ **Objective Function** (add 400·X3 term)
- ❌ **Constraint Coefficients** (add X3 column: [0, 1])
- ❌ **Optimal Solution** (will change from X1=2, X2=2 to new values)
- ❌ **Maximum Revenue** (changed from $600 to higher value)

---

## Complete Process Comparison

```
PART 1: Original Problem
├─ Variables: X1, X2
├─ Objective: Z = 100X1 + 200X2
├─ Doctors constraint: 1X1 + 1X2 ≤ 4
├─ Beds constraint: 1X1 + 2X2 ≤ 6
└─ Solution: X1=2, X2=2, Z=$600

PART 2: New Service (Solving COMPLETELY from scratch)
├─ Variables: X1, X2, X3 ← ADDED
├─ Objective: Z = 100X1 + 200X2 + 400X3 ← CHANGED
├─ Doctors constraint: 1X1 + 1X2 + 0X3 ≤ 4 ← X3 added
├─ Beds constraint: 1X1 + 2X2 + 1X3 ≤ 6 ← X3 added
├─ Run full simplex from X1=0, X2=0, X3=0
└─ Solution: X1=0, X2=0, X3=6, Z=$2,400 (many iterations)

PART 3-4: SMART Way (Using old solution as starting point)
├─ Variables: X1, X2, X3 ← SAME as Part 2
├─ Objective: Z = 100X1 + 200X2 + 400X3 ← SAME as Part 2
├─ Doctors constraint: 1X1 + 1X2 + 0X3 ≤ 4 ← SAME as Part 2
├─ Beds constraint: 1X1 + 2X2 + 1X3 ≤ 6 ← SAME as Part 2
├─ START from: X1=2, X2=2, X3=0 ← Use old optimal as starting point!
├─ Calculate reduced cost of X3 = 300 (worth adding!)
├─ Run ONLY a few iterations (not from scratch!)
└─ Solution: X1=1, X2=1, X3=3, Z=$1,500 (QUICK!)
```

---

## Part 5: Solving Using Matrix and Tableau Methods

### Understanding Basic and Non-Basic Variables

**From the original problem:**

```
Basic Variables (in the solution):
- X1 = 2 (Minor Injuries)
- X2 = 2 (Urgent Care)

Non-Basic Variables (not used):
- None in original (we only had 2 variables)
```

**After adding X3:**

```
Basic Variables (in the solution):
- X1 = 2
- X2 = 2

Non-Basic Variables (not in the solution):
- X3 = 0 ← NEW! Currently zero, we want to check if it should enter

With 2 constraints (doctors, beds), we can only have 2 basic variables!
So X3 MUST be non-basic at first.
```

---

### The Simplex Tableau Method

#### What is the Simplex Tableau?

It's a table that shows the current solution with:
- **Objective row** (bottom): The reduced costs
- **Constraint rows** (top): The coefficients
- **Identity matrix columns**: Show which variables are basic

#### Original Optimal Tableau (With 2 Variables)

```
Basic  | X1  | X2  | RHS (Result)
───────┼─────┼─────┼──────────
s1     | 1   | 1   | 4    (doctor constraint, s1 = slack)
s2     | 1   | 2   | 6    (bed constraint, s2 = slack)
───────┼─────┼─────┼──────────
Z      |-100 |-200 | 0    (objective row, negated)
```

Wait, let me show this more clearly. At optimality for the original problem:

```
       | X1  | X2  | s1  | s2  | RHS
───────┼─────┼─────┼─────┼─────┼──────
X1     | 1   | 0   | 2   |-1   | 2     ← X1 is basic = 2
X2     | 0   | 1   |-1   | 1   | 2     ← X2 is basic = 2
───────┼─────┼─────┼─────┼─────┼──────
Z      | 0   | 0   | 100 | 100 | 600   ← All non-negative, OPTIMAL!
```

**Read this tableau:**
- X1 is basic (has 1 in X1 column, 0 elsewhere) = 2
- X2 is basic (has 0 in X1 column, 1 in X2 column) = 2
- s1, s2 are non-basic = 0
- All reduced costs (bottom row) are ≥ 0 → OPTIMAL!
- Objective value = 600

---

#### Adding New Variable X3 to the Tableau

**Now we add X3 column:**

```
       | X1  | X2  | X3  | s1  | s2  | RHS
───────┼─────┼─────┼─────┼─────┼─────┼──────
X1     | 1   | 0   | ?   | 2   |-1   | 2
X2     | 0   | 1   | ?   |-1   | 1   | 2
───────┼─────┼─────┼─────┼─────┼─────┼──────
Z      | 0   | 0   | ?   | 100 | 100 | 600
                    ↑
            We need to calculate
            these question marks!
```

---

Maximize: $Z = 100X_1 + 200X_2 + 400X_3$

Subject to:
$$1 \cdot X_1 + 1 \cdot X_2 + 0 \cdot X_3 \leq 4 \quad \text{(Doctors)}$$
$$1 \cdot X_1 + 2 \cdot X_2 + 1 \cdot X_3 \leq 6 \quad \text{(Beds)}$$

**Extract data for X₃:**

$$C_3 = 400 \quad \text{(Revenue from one OR patient)}$$

$$A_3 = \begin{bmatrix} 0 \\ 1 \end{bmatrix} \quad \text{(Resources needed: 0 doctors, 1 bed)}$$

**What do these mean?**
- $C_3 = 400$: Each Observation Room patient brings $400 in revenue
- $A_3 = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$: Each OR patient needs 0 doctor hours and 1 bed hour

---

#### Step 2: Define the Basis Matrix and Calculate Its Inverse

**Current basic variables:** $X_1 = 2, X_2 = 2$

#### Step 2: Define the Basis Matrix and Calculate Its Inverse

**FIRST: What is a Basis Matrix B?**

A basis matrix contains the **coefficients of the current basic variables** from the constraints.

**Remember:** In our hospital example, we have:
- **2 constraints** (Doctors and Beds)
- **2 basic variables** (X₁ and X₂ currently in the solution)
- **Rule:** Number of basic variables = Number of constraints

**The constraints from the original problem:**

$$1 \cdot X_1 + 1 \cdot X_2 + 0 \cdot X_3 \leq 4 \quad \text{(Doctors constraint)}$$
$$1 \cdot X_1 + 2 \cdot X_2 + 1 \cdot X_3 \leq 6 \quad \text{(Beds constraint)}$$

**Which variables are currently basic?**

From our optimal solution:
- $X_1 = 2$ ✓ (currently IN the solution - BASIC)
- $X_2 = 2$ ✓ (currently IN the solution - BASIC)
- $X_3 = 0$ ✗ (currently NOT in solution - NON-BASIC)

---

**Where does B come from?**

**Step 1: Look at the constraint coefficients**

Write out the full constraint matrix A (all variables):

$$A = \begin{bmatrix} 1 & 1 & 0 \\ 1 & 2 & 1 \end{bmatrix}$$

**Reading this matrix:**
- Row 1 (Doctors): Coefficients are [1, 1, 0] for [X₁, X₂, X₃]
- Row 2 (Beds): Coefficients are [1, 2, 1] for [X₁, X₂, X₃]

**Step 2: Extract ONLY the columns for basic variables**

Basic variables are X₁ and X₂, so we take columns 1 and 2:

$$B = \begin{bmatrix} 1 & 1 \\ 1 & 2 \end{bmatrix}$$

**That's it! This is the Basis Matrix!**

---

**Visual Explanation:**

```
Original Constraint Matrix A:
       X₁  X₂  X₃
       ─────────────
Doc:   1   1   0
Bed:   1   2   1

Basic variables: X₁ and X₂
So we take columns 1 and 2:

       X₁  X₂
       ─────────
Doc:   1   1     ← This is B!
Bed:   1   2
```

---

**Why do we only use basic variables?**

Because in an optimal solution:
- **Basic variables** = Variables that are non-zero (actually in use)
- **Non-basic variables** = Variables that are zero (not used)

At optimality:
- $X_1 = 2$ (basic, non-zero)
- $X_2 = 2$ (basic, non-zero)
- $X_3 = 0$ (non-basic, zero)

The basic variables form an "identity" pattern in the optimal tableau, which is why we can invert them!

---

**Another way to think about it:**

**Imagine you're running the hospital with current plan:**
- You USE 4 doctors (all from X₁ and X₂)
- You USE 6 beds (all from X₁ and X₂)

**The basis matrix B tells us:**
"With the 4 doctors and 6 beds currently used, how much does X₁ and X₂ consume them?"

$$\begin{bmatrix} 1 & 1 \\ 1 & 2 \end{bmatrix} \begin{bmatrix} X_1 \\ X_2 \end{bmatrix} = \begin{bmatrix} 4 \\ 6 \end{bmatrix}$$

This says:
- Doctors: $1 \cdot X_1 + 1 \cdot X_2 = 4$
- Beds: $1 \cdot X_1 + 2 \cdot X_2 = 6$

And we know $X_1 = 2, X_2 = 2$ satisfies this perfectly!

---

**Formula notation:**

$$B \cdot X_B = b$$

Where:
- $B$ = Basis matrix (coefficients of basic variables)
- $X_B$ = Basic variables [X₁, X₂]ᵀ = [2, 2]ᵀ
- $b$ = Resource limits (right-hand side) = [4, 6]ᵀ

---

**Now calculate $B^{-1}$:**

Why do we invert B?

**If** $B \cdot X_B = b$

**Then** $X_B = B^{-1} \cdot b$

**This gives us:** What values should basic variables have given the resources?

$$B^{-1} = \begin{bmatrix} 2 & -1 \\ -1 & 1 \end{bmatrix}$$

**Verify it works:**

$$\begin{bmatrix} 2 & -1 \\ -1 & 1 \end{bmatrix} \begin{bmatrix} 4 \\ 6 \end{bmatrix} = \begin{bmatrix} 2(4) + (-1)(6) \\ (-1)(4) + 1(6) \end{bmatrix} = \begin{bmatrix} 8-6 \\ -4+6 \end{bmatrix} = \begin{bmatrix} 2 \\ 2 \end{bmatrix}$$

**Perfect!** We get $X_1 = 2, X_2 = 2$ ✓

---

**Summary: Where B Comes From**

```
STEP 1: Identify basic variables from current solution
        Current: X₁ = 2, X₂ = 2 (these are BASIC)
        
STEP 2: Look at constraint coefficients for basic variables only
        Constraint matrix A = [1 1 0]
                               [1 2 1]
        
STEP 3: Extract columns for X₁ and X₂
        B = [1 1]  ← These are the coefficients of X₁, X₂
            [1 2]
        
STEP 4: Invert B to get B⁻¹
        B⁻¹ = [ 2 -1]
              [-1  1]
```

---

**Real Example: What if X₂ and X₃ were basic instead?**

If the solution was: $X_1 = 0, X_2 = 1, X_3 = 2$

Then basic matrix would be (columns 2 and 3 only):

$$A = \begin{bmatrix} 1 & 1 & 0 \\ 1 & 2 & 1 \end{bmatrix}$$

$$B = \begin{bmatrix} 1 & 0 \\ 2 & 1 \end{bmatrix} \quad \text{(columns for X₂ and X₃)}$$

**Different basis = Different B matrix!**

---

**Key Takeaway:**

| Concept | Meaning |
|---------|---------|
| **B** | Matrix of coefficients for CURRENT basic variables only |
| **Where B comes from** | Extract columns from constraint matrix A that correspond to basic variables |
| **B⁻¹** | The inverse tells us how resources map to basic variables |
| **Changes when** | Different variables become basic (after each pivot) |

**Calculate $B^{-1}$ (inverse of matrix B):**

For a 2×2 matrix $\begin{bmatrix} a & b \\ c & d \end{bmatrix}$, the inverse formula is:

$$B^{-1} = \frac{1}{ad-bc} \begin{bmatrix} d & -b \\ -c & a \end{bmatrix}$$

**Our calculation:**

$$\text{Determinant} = (1)(2) - (1)(1) = 2 - 1 = 1$$

$$B^{-1} = \frac{1}{1} \begin{bmatrix} 2 & -1 \\ -1 & 1 \end{bmatrix} = \begin{bmatrix} 2 & -1 \\ -1 & 1 \end{bmatrix}$$

---

#### Step 3: Calculate $B^{-1} \times A_j$ for NON-BASIC Variables

**IMPORTANT RULE:** 

$$\boxed{\text{We ALWAYS check } B^{-1} \times A_j \text{ where } j = \text{NON-BASIC variable}}$$

**NOT always A₃!** The subscript changes based on which variable is non-basic.

**In CURRENT iteration:**
- Basic variables: X₁, X₂
- Non-basic variables: X₃

Therefore, check: $B^{-1} \times A_3$ (because X₃ is non-basic)

**Formula:**
$$\text{Impact of X}_3 \text{ entering} = B^{-1} \times A_3$$

**Calculation:**

$$B^{-1} \times A_3 = \begin{bmatrix} 2 & -1 \\ -1 & 1 \end{bmatrix} \times \begin{bmatrix} 0 \\ 1 \end{bmatrix}$$

**Matrix multiplication (2×2 × 2×1 = 2×1):**

$$\begin{bmatrix} 2 & -1 \\ -1 & 1 \end{bmatrix} \times \begin{bmatrix} 0 \\ 1 \end{bmatrix} = \begin{bmatrix} (2)(0) + (-1)(1) \\ (-1)(0) + (1)(1) \end{bmatrix} = \begin{bmatrix} 0 - 1 \\ 0 + 1 \end{bmatrix} = \begin{bmatrix} -1 \\ 1 \end{bmatrix}$$

**Result:**
$$\text{X}_3 \text{ column in tableau} = \begin{bmatrix} -1 \\ 1 \end{bmatrix}$$

**Interpretation:**
- When we increase $X_3$ by 1 unit, $X_1$ changes by -1 (decreases by 1)
- When we increase $X_3$ by 1 unit, $X_2$ changes by +1 (increases by 1)

**Why?** Because we're substituting $X_3$ into the current basis ($X_1, X_2$).

---

**CRITICAL: When Basis Changes - Non-Basic Variable Changes Too!**

**Rule:** The subscript in $B^{-1} \times A_j$ ALWAYS corresponds to the NON-BASIC variable!

**If after the next iteration, X₂ and X₃ become basic:**

```
New basic: X₂, X₃
New non-basic: X₁ (changed!)

Then we calculate: B_new⁻¹ × A₁ (check X₁ now, NOT X₃!)
```

**Timeline showing which variable is checked each iteration:**

```
Iteration 1: Basic = {X₁,X₂}  Non-basic = {X₃}  → Check: B⁻¹ × A₃
Iteration 2: Basic = {X₂,X₃}  Non-basic = {X₁}  → Check: B_new⁻¹ × A₁
Iteration 3: Basic = {X₁,X₃}  Non-basic = {X₂}  → Check: B_new2⁻¹ × A₂
```

**Don't always check A₃!** Check whichever variable is non-basic!

---

#### Step 4: Calculate Reduced Cost

**Define $C_B$** (the objective coefficients of basic variables):

$$C_B = \begin{bmatrix} C_1 \\ C_2 \end{bmatrix} = \begin{bmatrix} 100 \\ 200 \end{bmatrix}$$

**The Reduced Cost Formula:**

$$\text{Reduced Cost}(X_3) = C_B^T \times B^{-1} \times A_3 - C_3$$

**Breaking down each operation:**

**Step 4a:** Transpose $C_B$ to get $C_B^T$ (convert column vector to row vector)

$$C_B^T = \begin{bmatrix} 100 & 200 \end{bmatrix} \quad \text{(now a row vector)}$$

**Step 4b:** Calculate $C_B^T \times B^{-1}$ (row × matrix)

$$C_B^T \times B^{-1} = \begin{bmatrix} 100 & 200 \end{bmatrix} \times \begin{bmatrix} 2 & -1 \\ -1 & 1 \end{bmatrix}$$

$$= \begin{bmatrix} (100)(2) + (200)(-1) & (100)(-1) + (200)(1) \end{bmatrix}$$

$$= \begin{bmatrix} 200 - 200 & -100 + 200 \end{bmatrix} = \begin{bmatrix} 0 & 100 \end{bmatrix}$$

**Step 4c:** Multiply the result by $A_3$ (row × column)

$$C_B^T \times B^{-1} \times A_3 = \begin{bmatrix} 0 & 100 \end{bmatrix} \times \begin{bmatrix} 0 \\ 1 \end{bmatrix}$$

$$= (0)(0) + (100)(1) = 100$$

**Step 4d:** Subtract $C_3$ to get reduced cost

$$\text{Reduced Cost}(X_3) = 100 - 400 = -300$$

---

#### What Does Reduced Cost = -300 Mean?

**Decision Rule for MAXIMIZATION:**
- If Reduced Cost $< 0$ → Variable **SHOULD ENTER** the basis ✓ (improves objective)
- If Reduced Cost $> 0$ → Variable should NOT enter ✗ (worsens objective)
- If Reduced Cost $= 0$ → Neutral (no change)

**In our case:**

$$\text{Reduced Cost}(X_3) = -300 < 0 \implies \boxed{\text{X}_3 \text{ SHOULD ENTER}}$$

**Interpretation:**
- For every 1 unit of $X_3$ we add, profit increases by 300
- This is equivalent to our intuitive calculation: Remove 1 MI ($-100$) + Add 1 OR ($+400$) = Net gain $+300$

**The negative sign:** In LP formulation, the negative means "beneficial" in a maximization problem.

---

#### Complete Matrix Formula Summary

| Formula | Calculation | Meaning |
|---------|------------|---------|
| $A_3 = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$ | From problem | Resource needs of X₃ |
| $C_3 = 400$ | From problem | Revenue coefficient of X₃ |
| $B = \begin{bmatrix} 1 & 1 \\ 1 & 2 \end{bmatrix}$ | Basis matrix | Current basic variables' coefficients |
| $B^{-1} = \begin{bmatrix} 2 & -1 \\ -1 & 1 \end{bmatrix}$ | Matrix inversion | How to transform variables |
| $B^{-1} \times A_3 = \begin{bmatrix} -1 \\ 1 \end{bmatrix}$ | Matrix multiply | X₃'s effect on current basis |
| $C_B^T \times B^{-1} \times A_3 - C_3 = -300$ | Full formula | Net benefit per unit X₃ |

---

#### Updated Tableau with X3 Column

```
       | X1  | X2  | X3  | s1  | s2  | RHS
───────┼─────┼─────┼─────┼─────┼─────┼──────
X1     | 1   | 0   |-1   | 2   |-1   | 2      ← Means X1 decreases if X3 enters
X2     | 0   | 1   | 1   |-1   | 1   | 2      ← Means X2 increases if X3 enters
───────┼─────┼─────┼─────┼─────┼─────┼──────
Z      | 0   | 0   |-300 | 100 | 100 | 600   ← Reduced cost is NEGATIVE!
                    ↑
            NEGATIVE means we should
            increase X3 (enter the basis)!
```

---

### Ratio Test: Which Variable Leaves?

**We want to increase X3 from 0. But how much?**

**Ratio test formula:**
```
Minimum of: RHS / |coefficient in X3 column|  (for positive coefficients)

For X1: 2 / |-1| = 2 / 1 = 2  ← But coefficient is negative! Skip this.
For X2: 2 / |1| = 2 / 1 = 2   ← Positive coefficient, include this!
```

**Result:** X2 can increase X3 by at most 2 units before X2 becomes 0.

**Decision:** X2 leaves, X3 enters, with X3 increasing to 2.

---

### New Solution After One Iteration

**After pivoting (row operations):**

```
New values:
X1 = 2 - 1(2) = 0  ← X1 decreased
X2 → becomes non-basic (leaves)
X3 = 2  ← X3 entered at value 2

New revenue: Z = 100(0) + 200(0) + 400(2) = $800
```

---

### Complete Tableau Process Summary

```
ORIGINAL OPTIMAL TABLEAU (2 variables):
       | X1  | X2  | s1  | s2  | RHS
───────┼─────┼─────┼─────┼─────┼──────
X1     | 1   | 0   | 2   |-1   | 2
X2     | 0   | 1   |-1   | 1   | 2
───────┼─────┼─────┼─────┼─────┼──────
Z      | 0   | 0   | 100 | 100 | 600
       └──────────────────────────────
         All reduced costs ≥ 0 ✓ OPTIMAL

STEP 1: Add X3 column using B^(-1) × A_j
       | X1  | X2  | X3  | s1  | s2  | RHS
───────┼─────┼─────┼─────┼─────┼─────┼──────
X1     | 1   | 0   |-1   | 2   |-1   | 2
X2     | 0   | 1   | 1   |-1   | 1   | 2
───────┼─────┼─────┼─────┼─────┼─────┼──────
Z      | 0   | 0   |-300 | 100 | 100 | 600
                    ↑
            NEGATIVE! Should enter!

STEP 2: Ratio test → X3 enters, X2 leaves with value 2

STEP 3: Pivot and get NEW tableau
       | X1  | X2  | X3  | s1  | s2  | RHS
───────┼─────┼─────┼─────┼─────┼─────┼──────
X1     | 1   |-1   | 0   | 1   | 0   | 0     ← X1 = 0
X3     | 0   | 1   | 1   |-1   | 1   | 2     ← X3 = 2
───────┼─────┼─────┼─────┼─────┼─────┼──────
Z      | 0   | 300 | 0   |-200 | 200 | 800
                        ↑
            All reduced costs ≥ 0? 
            Check the -200... STILL NEGATIVE!
```

**Continue iterating until ALL reduced costs are ≥ 0...**

---

### Key Formulas Used

```
1. B^(-1) × A_j  
   = Constraint coefficients for new variable in tableau

2. C_B^T × B^(-1) × A_j - C_j
   = Reduced cost of new variable

3. Ratio test: min(RHS_i / Coefficient_i)  for positive coefficients
   = How much the entering variable can increase
```

---

### When to Use Each Method

**Intuitive Method (What we did first):**
- ✅ Easy to understand the logic
- ✅ Good for simple problems
- ✅ Shows why decisions make sense
- ❌ Hard to scale to many variables

**Tableau Method (Using formulas):**
- ✅ Systematic and organized
- ✅ Easy to implement on computer
- ✅ Works for any size problem
- ❌ Less intuitive at first

**Matrix Method (Pure formulas):**
- ✅ Mathematically elegant
- ✅ Easiest for computer programming
- ✅ Most efficient for large problems
- ❌ Requires linear algebra knowledge

---

## Key Takeaway

**Both methods solve the SAME problem:**
1. Add new variable X3 with coefficient 0
2. Calculate using B^(-1) × A_j what happens when X3 enters
3. Calculate reduced cost to check if it's worth entering
4. Do ratio test to find which variable leaves
5. Update solution with new basis

**The intuitive reasoning:** Why we remove MI (lowest resource waste)
**The tableau/matrix calculation:** How much we can improve and where exactly to pivot

**Both lead to the same answer - just different ways of thinking about it!**

### When Adding a New Variable (Service X3):

**Objective Function becomes:**
```
Z = (old objective) + (new coefficient)·X3
Z = 100X1 + 200X2 + 400X3
```

**Each Constraint becomes:**
```
(old constraint) + (X3 coefficient)·X3 ≤ (limit)
1X1 + 1X2 + 0X3 ≤ 4  (X3 coefficient for doctors is 0)
1X1 + 2X2 + 1X3 ≤ 6  (X3 coefficient for beds is 1)
```

**Reduced Cost (Should we add X3?):**
```
Reduced Cost = (Revenue from X3) - (Resource impact)
Reduced Cost > 0 → YES, increase X3
Reduced Cost < 0 → NO, keep X3 = 0
```

---

## Summary: The Two Approaches

### Approach 1: Solve from Scratch (Inefficient)
```
Remove old solution (X1=2, X2=2)
Start from nothing: X1=0, X2=0, X3=0
Add new constraints with X3
Run full simplex algorithm
Many iterations... find solution
Time: Hours or Days
```

### Approach 2: Use Old Solution (Efficient - What We Do)
```
Keep old solution: X1=2, X2=2
Add new variable: X3=0
Add new constraints with X3 (same limits!)
Calculate reduced cost of X3 (one formula!)
Run only a few iterations
Time: Minutes
```

**Both solve the EXACT SAME problem with SAME constraints, just different starting points!**

---

## The Bottom Line

✅ **When adding a new service to an existing plan:**

1. **Objective Function:** Add the new revenue term (400·X3)
2. **Constraints:** Add new variable coefficients, but LIMITS STAY THE SAME
3. **Starting Point:** Use previous optimal solution, set new X3=0
4. **Iterate:** Only a few iterations needed instead of full re-solve

**No changing constraint limits! No starting from zero! Just add one column and iterate.**