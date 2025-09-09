# Incremental Update Rule for Sample Average

In reinforcement learning (e.g., bandits), we estimate the value of an action by the **sample average** of rewards received.

---

## Step 1: Definition of the Average

The estimate after \$n\$ plays is:

$$
Q_{n+1} = \frac{1}{n}\sum_{i=1}^{n} R_i
$$

where:

* \$R\_i\$ = reward received on the \$i^{th}\$ play
* \$Q\_{n+1}\$ = estimated value after \$n\$ plays

---

## Step 2: Split the Sum

$$
Q_{n+1} = \frac{1}{n}\Big(R_n + \sum_{i=1}^{n-1} R_i\Big)
$$

---

## Step 3: Replace the Sum with the Old Average

We know that:

$$
Q_n = \frac{1}{n-1}\sum_{i=1}^{n-1} R_i
$$

So:

$$
\sum_{i=1}^{n-1} R_i = (n-1)Q_n
$$

Substitute:

$$
Q_{n+1} = \frac{1}{n}\Big(R_n + (n-1)Q_n\Big)
$$

---

## Step 4: Expand \$(n-1)Q\_n\$

$$
(n-1)Q_n = nQ_n - Q_n
$$

So:

$$
Q_{n+1} = \frac{1}{n}\Big(R_n + nQ_n - Q_n\Big)
$$

---

## Step 5: Break Into Separate Fractions

$$
Q_{n+1} = \frac{1}{n}R_n + \frac{1}{n}(nQ_n) - \frac{1}{n}Q_n
$$

---

## Step 6: Simplify the Middle Term

$$
\frac{1}{n}(nQ_n) = Q_n
$$

So:

$$
Q_{n+1} = Q_n + \frac{1}{n}R_n - \frac{1}{n}Q_n
$$

---

## Step 7: Factor the Last Two Terms

$$
Q_{n+1} = Q_n + \frac{1}{n}(R_n - Q_n)
$$

---

## ✅ Final Incremental Update Rule

$$
\boxed{Q_{n+1} = Q_n + \frac{1}{n}(R_n - Q_n)}
$$

---

### 🔎 Interpretation

* Start from old estimate \$Q\_n\$.
* Compare new reward \$R\_n\$ with it.
* Adjust a little (step size \$1/n\$) toward the new reward.

This avoids recalculating the whole average every time.

---

# Incremental Update with Constant Step Size (\$\alpha\$)

When rewards **change over time** (non-stationary problems), the sample average method (using \$1/n\$ as step size) is too slow to adapt.
Instead, we use a **fixed step size** \$\alpha\$.

---

## Update Rule

$$
Q_{n+1} = Q_n + \alpha (R_n - Q_n)
$$

* \$Q\_n\$: old estimate
* \$R\_n\$: new reward
* \$\alpha\$: step size (constant, e.g., 0.1)

---

## How It Works (Recursive Form)

Rearranging:

$$
Q_{n+1} = (1-\alpha)Q_n + \alpha R_n
$$

This shows a **weighted sum**:

* The old estimate \$Q\_n\$ keeps weight \$(1-\alpha)\$
* The new reward \$R\_n\$ has weight \$\alpha\$

Because the formula is recursive, older rewards keep getting multiplied by \$(1-\alpha)\$ each step → their influence fades **exponentially with time**.

---

## Unrolling the Equation Step by Step

1. Start with:
   $Q_{n+1} = (1-\alpha)Q_n + \alpha R_n$

2. Substitute for \$Q\_n\$:
   $Q_n = (1-\alpha)Q_{n-1} + \alpha R_{n-1}$

   So:
   $Q_{n+1} = (1-\alpha)[(1-\alpha)Q_{n-1} + \alpha R_{n-1}] + \alpha R_n$

3. Expand:
   $Q_{n+1} = (1-\alpha)^2 Q_{n-1} + (1-\alpha)\alpha R_{n-1} + \alpha R_n$

4. Substitute again for \$Q\_{n-1}\$:
   $Q_{n-1} = (1-\alpha)Q_{n-2} + \alpha R_{n-2}$

   So:
   $Q_{n+1} = (1-\alpha)^3 Q_{n-2} + (1-\alpha)^2\alpha R_{n-2} + (1-\alpha)\alpha R_{n-1} + \alpha R_n$

Continuing this way leads to:

$$
Q_{n+1} = (1-\alpha)^{n} Q_1 + \alpha \sum_{k=0}^{n-1} (1-\alpha)^k R_{n-k}
$$

This shows explicitly how weights decrease exponentially with time.

---

## Example Walkthrough

Suppose \$\alpha = 0.1\$ and the last three rewards were:

* \$R\_1 = 0.2\$, \$R\_2 = 0.8\$, \$R\_3 = 1.0\$

Then:

$$
Q_4 = 0.1(1.0) + 0.1(0.9)(0.8) + 0.1(0.9^2)(0.2) + \dots
$$

Calculating:

* \$0.1 \times 1.0 = 0.1\$
* \$0.1 \times 0.9 \times 0.8 = 0.072\$
* \$0.1 \times 0.9^2 \times 0.2 \approx 0.0162\$

Adding → \$Q\_4 \approx 0.188\$

✅ The most recent reward (\$1.0\$) dominates, older ones contribute much less.

---

## Why Use This?

* **Stationary problems** → use sample average (\$\alpha = 1/n\$).
* **Non-stationary problems** → use constant \$\alpha\$.

  * Older data fades away.
  * Estimates adapt quickly to the current reality.

---

## Example (\$\alpha = 0.1\$)

* Old estimate \$Q\_n = 0.5\$
* New reward \$R\_n = 1\$

$$
Q_{n+1} = 0.5 + 0.1(1 - 0.5) = 0.55
$$

✅ The estimate moves 10% closer to the new reward.


