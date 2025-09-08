
# Incremental Update Rule for Sample Average

In reinforcement learning (e.g., bandits), we estimate the value of an action by the **sample average** of rewards received.

---

## Step 1: Definition of the Average

The estimate after `n` plays is:

\[
Q_{n+1} = \frac{1}{n}\sum_{i=1}^{n} R_i
\]

where:
- \( R_i \) = reward received on the \( i^{th} \) play  
- \( Q_{n+1} \) = estimated value after \( n \) plays  

---

## Step 2: Split the Sum

\[
Q_{n+1} = \frac{1}{n}\Big(R_n + \sum_{i=1}^{n-1} R_i\Big)
\]

---

## Step 3: Replace the Sum with the Old Average

We know that:

\[
Q_n = \frac{1}{n-1}\sum_{i=1}^{n-1} R_i
\]

So:

\[
\sum_{i=1}^{n-1} R_i = (n-1)Q_n
\]

Substitute:

\[
Q_{n+1} = \frac{1}{n}\Big(R_n + (n-1)Q_n\Big)
\]

---

## Step 4: Expand \((n-1)Q_n\)

\[
(n-1)Q_n = nQ_n - Q_n
\]

So:

\[
Q_{n+1} = \frac{1}{n}\Big(R_n + nQ_n - Q_n\Big)
\]

---

## Step 5: Break Into Separate Fractions

\[
Q_{n+1} = \frac{1}{n}R_n + \frac{1}{n}(nQ_n) - \frac{1}{n}Q_n
\]

---

## Step 6: Simplify the Middle Term

\[
\frac{1}{n}(nQ_n) = Q_n
\]

So:

\[
Q_{n+1} = Q_n + \frac{1}{n}R_n - \frac{1}{n}Q_n
\]

---

## Step 7: Factor the Last Two Terms

\[
Q_{n+1} = Q_n + \frac{1}{n}(R_n - Q_n)
\]

---

## ✅ Final Incremental Update Rule

\[
\boxed{Q_{n+1} = Q_n + \frac{1}{n}(R_n - Q_n)}
\]

---

### 🔎 Interpretation
- Start from old estimate \( Q_n \).  
- Compare new reward \( R_n \) with it.  
- Adjust a little (step size \( \frac{1}{n} \)) toward the new reward.  

This avoids recalculating the whole average every time.


# Incremental Update with Constant Step Size (α)

When rewards **change over time** (non-stationary problems), the sample average method
(using `1/n` as step size) is too slow to adapt.  
Instead, we use a **fixed step size** α.

---

## Update Rule

\[
Q_{n+1} = Q_n + \alpha (R_n - Q_n)
\]

- \( Q_n \): old estimate  
- \( R_n \): new reward  
- \( \alpha \): step size (constant, e.g., 0.1)  

---

## How It Works

- The new reward pulls the estimate by **α × error**.  
- The old estimate keeps weight \(1 - \alpha\).  

Example with α = 0.1:
- New reward weight = 0.1 (10%)  
- Old estimate weight = 0.9 (90%)  

---

## Why Recent Rewards Matter More

If you expand (unroll) the formula:

\[
Q_{n+1} = 0.1R_n + 0.1(0.9)R_{n-1} + 0.1(0.9^2)R_{n-2} + \dots
\]

- Latest reward \(R_n\) → weight = 0.1  
- Previous reward \(R_{n-1}\) → weight = 0.09  
- Earlier reward \(R_{n-2}\) → weight = 0.081  
- …and so on.  

👉 Influence of old rewards **decays exponentially**.  
👉 Most recent rewards dominate the estimate.

---

## Why Use This?

- **Stationary problems** → use sample average (α = 1/n).  
- **Non-stationary problems** → use constant α.  
  - Older data fades away.  
  - Estimates adapt quickly to the current reality.  

---

## Example (α = 0.1)

- Old estimate \(Q_n = 0.5\)  
- New reward \(R_n = 1\)  

\[
Q_{n+1} = 0.5 + 0.1(1 - 0.5) = 0.55
\]

✅ The estimate moves 10% closer to the new reward.


