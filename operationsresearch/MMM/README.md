#  Understanding Adstock (β) and Diminishing Returns (α) in Marketing Mix Models

---

##  Overview

Marketing Mix Modeling (MMM) helps quantify **how advertising spend drives sales** over time. Two key parameters — **Adstock (β)** and **Diminishing Returns (α)** — capture memory and saturation effects in consumer behavior.

| Parameter     | Represents             | Real-world Meaning                                   |
| ------------- | ---------------------- | ---------------------------------------------------- |
| **β (Beta)**  | Time-based memory      | How long people remember your ads after seeing them. |
| **α (Alpha)** | Spend-based saturation | How quickly returns flatten as you spend more.       |

Together, they create a realistic model of how advertising works:

[
\text{Adstock}*t = X_t + \beta \times \text{Adstock}*{t-1}
]
[
\text{Response}_t = (\text{Adstock}_t)^{\alpha}
]

Where:

* (X_t): Current week's spend
* (\beta): Decay rate (0 < β < 1)
* (\alpha): Saturation factor (0 < α ≤ 1)
* (\text{Response}_t): Effective impact on sales

---

## Real-world Example: McDonald's Ramadan Campaign (Dubai)

| Week | Ad Spend (AED '000) | Adstock (β = 0.5) | Response (α = 0.7) | What Happens                              |
| ---- | ------------------- | ----------------- | ------------------ | ----------------------------------------- |
| 1    | 100                 | 100               | 25                 | First exposure – everyone sees it       |
| 2    | 100                 | 150               | 32                 | More exposure, but many already saw it  |
| 3    | 100                 | 175               | 35                 | Almost flat – market saturation         |
| 4    | 0                   | 87                | 19                 | Ads stop, but memory continues          |

**Formula breakdown:**

* Week 1 → (A_1 = 100)
* Week 2 → (A_2 = 100 + 0.5 × 100 = 150)
* Week 3 → (A_3 = 100 + 0.5 × 150 = 175)
* Week 4 → (A_4 = 0 + 0.5 × 175 = 87.5)

Then applying diminishing returns:
[
\text{Response}_t = (\text{Adstock}_t)^{0.7}
]

---

##  Scenario Analysis

| Scenario                      | β (Memory) | α (Saturation) | Description                                                  |
| ----------------------------- | ---------- | -------------- | ------------------------------------------------------------ |
| **1. Search Ads**             | 0.1        | 1.0            | No memory – effect ends instantly. Linear growth with spend. |
| **2. Social Ads (Instagram)** | 0.5        | 0.7            | Moderate memory and reach overlap. Best real-world balance.  |
| **3. TV Brand Ads**           | 0.8        | 0.5            | Strong memory; diminishing reach after heavy spending.       |
| **4. Big Brand (Coca-Cola)**  | 0.9        | 0.3            | People remember ads for months; new ads add little effect.   |

---

##  Intuition

| Dimension         | Controlled by | Example                                                                  |
| ----------------- | ------------- | ------------------------------------------------------------------------ |
| **Time (Memory)** | β             | People still remember the Ramadan meal offer even after ads stop.        |
| **Spend (Reach)** | α             | Showing the ad again reaches fewer *new* people – same audience overlap. |

* **β →** “How long the applause continues after the show.”
* **α →** “How crowded the theater already is.”

---

##  Product-level Intuition

| Product       | α (Reach Saturation) | β (Memory) | Explanation                                           |
| ------------- | -------------------- | ---------- | ----------------------------------------------------- |
| **Fast Food** | 0.9                  | 0.3        | People forget quickly; need frequent ads.             |
| **Car Brand** | 0.4                  | 0.8        | Fewer buyers, but long consideration memory.          |
| **Perfume**   | 0.7                  | 0.5        | Moderate recall and moderate saturation.              |
| **Coca-Cola** | 0.3                  | 0.9        | Everyone already knows it; brand recall lasts months. |

---

##  Full Model in Practice

Once we include both α and β, the full sales model becomes:

[
\text{Sales}*t = \text{Base Sales} + \theta × (X_t + \beta × X*{t-1} + \beta^2 × X_{t-2} + …)^{\alpha}
]

This means:

* Past ads (through β) keep affecting sales.
* Increasing spend (through α) yields smaller incremental returns.

---

##  Key Takeaways

| Question              | Answer                                          |
| --------------------- | ----------------------------------------------- |
| Why start from spend? | Because Adstock is spend *adjusted for memory*. |
| Does β reduce impact? | Yes, over time (memory fades).                  |
| Does α reduce impact? | Yes, with higher spend (reach saturates).       |
| What if α = 1?        | No diminishing returns → response = adstock.    |
| What if β = 0?        | No carry-over → only current week matters.      |

---

##  TL;DR

| Parameter     | Think of it as   | Acts On | Real-world Meaning                                  |
| ------------- | ---------------- | ------- | --------------------------------------------------- |
| **β (Beta)**  | Memory           | Time    | How long people remember ads after seeing them.     |
| **α (Alpha)** | Reach Efficiency | Spend   | How quickly new spending stops bringing new buyers. |

>  Example: During Ramadan, McDonald’s ads keep working (β), but extra airtime adds fewer new buyers (α).



- Beta (adstock/memory decay) is about timing, not individuals. It's saying: "A marketing exposure in week 1 still has some effect in week 2, week 3, etc." It doesn't matter if it's the same person seeing the ad again or a new person—beta is modeling the aggregate carryover effect of the campaign dollars spent. It's purely about how long the impact of that spend lingers.

- Alpha (diminishing returns) is about scale/saturation, also not tied to unique vs. repeat individuals specifically. It's saying: "When I increase my total spend in a given period, each incremental dollar is less efficient." This happens for many reasons—you might be reaching the same people repeatedly, you might be hitting less relevant audience segments, ad fatigue, etc. But alpha is an aggregate effect across your entire audience and spending level in that period.

So neither parameter is explicitly modeling "unique individuals" in the way you're thinking. Both are aggregate effects:

- Beta = carryover of spend effects across time periods
- Alpha = efficiency loss as you increase spend in a single period


#  Modeling Multiple Media Channels in Marketing Mix Models (MMM)

---

##  Objective

When you have **multiple advertising channels** (e.g., TV, Radio, Billboards, Social Media), you can extend the Adstock–α model for **each channel separately** and combine them in a **multiple regression framework**.

The goal is to estimate how much each channel contributes to sales, accounting for **time decay (β)** and **diminishing returns (α)**.

---

## Step 1: Transform Spend Data for Each Channel

For each medium ( i ):

[
\text{Adstock}*{i,t} = X*{i,t} + \beta_i × \text{Adstock}*{i,t-1}
]
[
\text{Response}*{i,t} = (\text{Adstock}_{i,t})^{\alpha_i}
]

Where:

* ( X_{i,t} ) = spend for medium *i* in week *t*
* ( \beta_i ) = memory (carryover) rate for that medium
* ( \alpha_i ) = diminishing return factor for that medium

 Example:

| Medium           | Typical β | Typical α | Explanation                           |
| ---------------- | --------- | --------- | ------------------------------------- |
| TV               | 0.8       | 0.6       | Long memory, broad reach saturation   |
| Radio            | 0.4       | 0.7       | Shorter memory, moderate saturation   |
| Billboards       | 0.7       | 0.5       | People see daily, effect lasts longer |
| Digital (Social) | 0.3       | 0.9       | Short memory, quick decay             |

---

##  Step 2: Create Regression-ready Variables

After transformation, each channel’s **Response variable** represents its *effective advertising pressure*.

Then we build a regression model:

[
\text{Sales}_t = b_0 + b_1(\text{TV}_t) + b_2(\text{Radio}_t) + b_3(\text{Billboards}_t) + b_4(\text{Social}_t) + ε_t
]

Each term (e.g., TVₜ) is the *adstock-transformed* and *α-adjusted* spend for that channel.

---

##  Step 3: Example Data

| Week | Sales | TV Spend | Radio Spend | Billboard Spend | Social Spend |
| ---- | ----- | -------- | ----------- | --------------- | ------------ |
| 1    | 200   | 100      | 50          | 30              | 20           |
| 2    | 230   | 100      | 30          | 40              | 30           |
| 3    | 260   | 150      | 20          | 50              | 40           |
| 4    | 240   | 80       | 20          | 30              | 25           |
| 5    | 210   | 60       | 10          | 20              | 15           |

Then apply β and α transformations separately:

Example (TV channel):

| Week | TV Spend | Adstock (β=0.8) | Response (α=0.6) |
| ---- | -------- | --------------- | ---------------- |
| 1    | 100      | 100             | 15.8             |
| 2    | 100      | 180             | 20.4             |
| 3    | 150      | 294             | 25.6             |
| 4    | 80       | 235             | 21.2             |
| 5    | 60       | 188             | 18.0             |

Repeat this for each channel and feed them into the regression.

---

##  Step 4: Run the Regression

In Python (example):

```python
import statsmodels.api as sm

# X = transformed adstock variables for each medium
X = df[['TV_response', 'Radio_response', 'Billboard_response', 'Social_response']]
X = sm.add_constant(X)

y = df['Sales']
model = sm.OLS(y, X).fit()
print(model.summary())
```

The coefficients (b₁–b₄) show the *incremental sales impact* per unit of transformed ad pressure.

---

##  Step 5: Interpretation

| Coefficient         | Meaning                                                   |
| ------------------- | --------------------------------------------------------- |
| **b₁ (TV)**         | Incremental sales from 1 unit of effective TV pressure    |
| **b₂ (Radio)**      | Incremental sales from 1 unit of effective Radio pressure |
| **b₃ (Billboards)** | Incremental sales from 1 unit of Billboard exposure       |
| **b₄ (Social)**     | Incremental sales from 1 unit of Social media activity    |

The larger the coefficient, the more powerful that channel’s influence on sales (after accounting for memory and saturation).

---

##  Step 6: Channel ROI & Optimization

Once you have coefficients, you can compute ROI per channel:

[
ROI_i = \frac{b_i × \text{mean(Response)}_i}{\text{mean(Spend)}_i}
]

Then, you can run **optimization** (using Linear or Quadratic Programming) to reallocate budgets toward higher-ROI channels.

---

## 🧭 Summary Table

| Step | What you do                              | Why                                   |
| ---- | ---------------------------------------- | ------------------------------------- |
| 1    | Transform spend with β and α             | Capture memory & diminishing effects  |
| 2    | Build regression with transformed spends | Estimate impact per channel           |
| 3    | Interpret coefficients                   | Quantify marginal contribution        |
| 4    | Calculate ROI                            | Compare performance across media      |
| 5    | Optimize budgets                         | Maximize total sales for fixed budget |

---

###  Example Intuition

> * **TV** builds slowly, stays long (high β, low α).
> * **Radio** fades fast (low β), but every new ad reaches different people (higher α).
> * **Billboards** are consistent, medium memory.
> * **Social Media** gives instant peaks but dies quickly.

By modeling each channel with its own β and α, you capture *real marketing dynamics* in one unified regression model.




