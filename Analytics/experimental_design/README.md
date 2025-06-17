# Complete Experimental Design in Python (with Theory + Detailed Examples)

## 🎯 Objective

This document explains experimental design in Python step by step using theory, definitions, case studies, and real-world examples. It includes basic concepts like random assignment and advanced methods like block and stratified randomization, using an e-commerce use case with full Python examples.

---

## 🧪 What is Experimental Design?

Experimental design is the process of planning a research study to investigate a hypothesis in a controlled and objective way. It ensures that the results are not influenced by bias or external factors.

### Why is it Important?

It helps:

* Minimize bias
* Ensure reliable comparisons
* Enable quantified decision-making

Experimental design is widely used in:

* Medicine (clinical trials)
* Business (A/B testing)
* Agriculture (crop yield testing)
* Government policy (behavioral experiments)

---

## 🧠 Key Terms

| Term                 | Description                                                   |
| -------------------- | ------------------------------------------------------------- |
| Subjects             | Who/what is being tested (e.g., users)                        |
| Treatment            | The change or action being tested (e.g., new website layout)  |
| Control Group        | Receives no change, used for comparison                       |
| Treatment Group      | Receives the experimental change                              |
| Type I Error         | False positive – rejecting the null when it's true            |
| Covariate            | A variable that might affect results but is not the treatment |
| Confounding Variable | A covariate that can distort the treatment effect             |

---

## 🔄 Random Assignment

### Pros:

* Simple and effective
* Reduces selection bias

### Cons:

* Can create uneven group sizes in small datasets
* Might not balance covariates

### Example – 200 People Height Dataset

```python
group1 = heights.iloc[:100]         # Non-random split
group2 = heights.iloc[100:]

# Random assignment
group1 = heights.sample(frac=0.5, random_state=1)
group2 = heights.drop(group1.index)
```

Using `.describe()` helps compare means. Random assignment gives better balance in average height.

---

## 🔹 Case Study: E-commerce A/B Test (Detailed)

You want to test a new homepage layout to see if it improves spending.

### Dataset:

* 1000 users
* Features:

  * `basket_size` (in dollars)
  * `time_on_site` (in minutes)
  * `power_user` (True if time > 40 mins/day)

### Step 1: Create Data

```python
import pandas as pd
import numpy as np

np.random.seed(42)
df = pd.DataFrame({
    'user_id': range(1, 1001),
    'basket_size': np.random.normal(100, 15, 1000),
    'time_on_site': np.random.normal(35, 10, 1000)
})
df['power_user'] = df['time_on_site'] > 40
```

### Step 2: Pure Randomization

```python
random_treat = df.sample(frac=0.5, random_state=1)
random_control = df.drop(random_treat.index)

print("Treatment Power Users:", random_treat['power_user'].mean())
print("Control Power Users:", random_control['power_user'].mean())
```

❌ Power users are unbalanced → could affect results

---

## ✅ Block Randomization

To ensure equal group sizes:

### How It Works:

* Break data into blocks (e.g., 10 people)
* Randomly assign within each block

## 📦 How Block Randomization Works

You define a **block size**, e.g., `block_size = 10`

You divide **1000 users** into:

```
1000 / 10 = 100 blocks
```

### In Each Block:

* Half the users (**5**) are randomly assigned to **Treatment**
* The other half (**5**) to **Control**

### So You Get:

* **500 Treatment users**
* **500 Control users**

✅ Each block contributes equally to the two groups, which maintains balance **throughout the dataset**, not just at the end.


### Code:

```python
block_size = 10
blocks = [df.iloc[i:i+block_size] for i in range(0, len(df), block_size)]

results = []
for block in blocks:
    treat = block.sample(frac=0.5, random_state=1)
    treat['T_C'] = 'Treatment'
    control = block.drop(treat.index)
    control['T_C'] = 'Control'
    results.append(pd.concat([treat, control]))

block_df = pd.concat(results)
```

✅ Group sizes are even
⚠️ Covariates may still be unbalanced

---

## ✅ Stratified Randomization

Best when you want both:

* Even group sizes
* Balanced covariates (e.g. power\_user)

### Steps:

1. Split users by `power_user` (True/False)
2. Randomly assign treatment/control within each group


## 🔄 The Two Problems

### 1. Uneven Groups (Problem of Size)

When you assign users randomly (especially in small datasets), you might get 520 in treatment and 480 in control — not ideal.

This makes it hard to compare results fairly.

### 2. Confounding Variables (Problem of Bias)

A confounder like `power_user` (users who spend >40 mins/day on the site) might affect the outcome (like basket size).

If one group (say, treatment) has more power users than the control group, any observed effect might be due to this imbalance — not the treatment.

---

## ✅ How Stratified Randomization Solves Both

Let’s assume:

* **1000 users**
* **250 power users** (`power_user = True`)
* **750 non-power users**

### ➤ Step 1: Split dataset by the confounding variable (`power_user`)

| Stratum (group)         | Count |
| ----------------------- | ----- |
| Power Users (True)      | 250   |
| Non-Power Users (False) | 750   |

Now you have 2 balanced strata. This solves the confounding issue — because you isolate the variable that could bias results.

### ➤ Step 2: Randomly assign 50% of each stratum to treatment and 50% to control

From **250 power users**:

* 125 → Treatment
* 125 → Control

From **750 non-power users**:

* 375 → Treatment
* 375 → Control

| Group     | Power Users | Non-Power Users | Total |
| --------- | ----------- | --------------- | ----- |
| Treatment | 125         | 375             | 500   |
| Control   | 125         | 375             | 500   |

This solves the uneven group size problem and keeps confounders evenly distributed.

---

## ✅ Why This Is Powerful

By stratifying:

* You lock in **fairness by design**
* Every subgroup (e.g., power users vs. non-power users) is fairly represented in both treatment and control
* You preserve **statistical power** and avoid biased conclusions


### Code:

```python
power_users = df[df['power_user'] == True]
non_power_users = df[df['power_user'] == False]

pu_treat = power_users.sample(frac=0.5, random_state=42)
pu_treat['T_C'] = 'Treatment'
pu_control = power_users.drop(pu_treat.index)
pu_control['T_C'] = 'Control'

npu_treat = non_power_users.sample(frac=0.5, random_state=42)
npu_treat['T_C'] = 'Treatment'
npu_control = non_power_users.drop(npu_treat.index)
npu_control['T_C'] = 'Control'

stratified_df = pd.concat([pu_treat, pu_control, npu_treat, npu_control])
```

### Confirm Balance:

```python
stratified_df.groupby(['power_user', 'T_C']).size()
```

✅ Perfectly balanced by power user status

---

## 📊 Visualization (Optional)

```python
import seaborn as sns
import matplotlib.pyplot as plt

sns.displot(df, x='basket_size', hue='power_user', kind='kde', height=5)
plt.title("Basket Size by Power User")
plt.show()
```

---

## 🔚 Summary Table

| Method                   | Even Groups? | Balanced Covariates? | Complexity |
| ------------------------ | ------------ | -------------------- | ---------- |
| Pure Randomization       | ❌            | ❌                    | Low        |
| Block Randomization      | ✅            | ❌                    | Medium     |
| Stratified Randomization | ✅            | ✅                    | High       |

---

## ✅ Best Practices

* Always check covariate balance
* Use `.describe()` and `.groupby()` to summarize differences
* Use seaborn to visualize distributions
* Prefer **stratified randomization** when important variables (like gender, location, or engagement) could bias results

---

## 📚 References

* [ScienceDirect: Experimental Design](https://www.sciencedirect.com/topics/earth-and-planetary-sciences/experimental-design)
* [Pandas Documentation](https://pandas.pydata.org/)
* [Seaborn Displot](https://seaborn.pydata.org/generated/seaborn.displot.html)



# Understanding Normal Data in Experimental Design

## 🎯 Objective

This document provides a comprehensive explanation of **normal data** and how it plays a critical role in experimental design and hypothesis testing. You'll learn about:

* The concept of normal distribution
* Its connection to z-scores and alpha
* Visual and statistical tests for assessing normality

---

## 1. 📈 What is Normal Data?

Normal data refers to data drawn from a **normal distribution**, also known as the **Gaussian distribution**. It has the classic "bell-shaped" curve, which is symmetric around the mean.

### Features:

* Mean (μ) at the center
* Standard deviation (σ) determines spread
* 68% of values fall within ±1σ, 95% within ±2σ, and 99.7% within ±3σ

### Why It Matters:

Many statistical methods (called **parametric tests**) assume that the data is normally distributed. Examples include:

* t-tests
* ANOVA
* Linear regression

If the data isn’t normal, these tests might give misleading results.

---

## 2. 📐 Z-Scores and the Normal Distribution

A **z-score** standardizes any data point based on the population mean and standard deviation:

```math
z = (x - μ) / σ
```

This allows us to:

* Understand how extreme a value is
* Compare across datasets with different units

### Standard Normal Distribution

* Mean = 0
* Std dev = 1

It’s used to calculate **p-values** and assess **statistical significance** in hypothesis testing.

---

## 3. 🔬 Hypothesis Testing and Alpha

In hypothesis testing:

* **Null Hypothesis (H₀):** The data is normal (or no effect)
* **Alternative Hypothesis (H₁):** The data is not normal (or there is an effect)

### Significance Level (α)

* Common alpha = 0.05
* Represents 5% chance of making a **Type I error** (false positive)
* In a two-tailed test, 2.5% lies in each tail of the normal curve

You compare the **p-value** (from test) to **alpha**:

* If **p < α** → reject H₀
* If **p ≥ α** → fail to reject H₀

---

## 4. 📊 Visual Tests for Normality

### KDE Plot (Kernel Density Estimate)

Use Seaborn’s `displot()` with `kind='kde'`:

```python
import seaborn as sns
sns.displot(df['salary'], kind='kde')
```

If the curve is smooth and symmetric like a bell, the data is likely normal.

---

## 5. 📉 QQ Plot (Quantile-Quantile)

![alt text](<output (3).png>)

Plots the quantiles of your data against the quantiles of a normal distribution:

```python
import statsmodels.api as sm
import scipy.stats as stats
import matplotlib.pyplot as plt

sm.qqplot(df['salary'], line='45', dist=stats.norm)
plt.show()
```

* If points lie on the 45° line → normal
* If points bow outward or inward → non-normal

---

## 6. 🧪 Statistical Tests for Normality

### 1. Shapiro-Wilk Test

* Good for small datasets
* Tests whether sample comes from normal distribution

```python
from scipy.stats import shapiro
stat, p = shapiro(df['salary'])
```

* If **p > 0.05** → data is normal

### 2. D'Agostino and Pearson’s Test (K²)

* Tests skewness and kurtosis
* Good for medium-large samples

```python
from scipy.stats import normaltest
stat, p = normaltest(df['salary'])
```

if p > 0.05 → Data appears normal

if p ≤ 0.05 → Data likely not normal

### 3. Anderson-Darling Test

* Provides critical values for multiple alpha levels

```python
from scipy.stats import anderson
result = anderson(df['salary'], dist='norm')
```

* Compare result.statistic to result.critical\_values
* If statistic < critical → data is normal

## 🤔 Why Does Anderson-Darling Give Many Alphas?

### Because:

* It **does not give a p-value**.
* Instead, it gives you a **test number** (called the "statistic") and a **table with critical values** for different alpha levels.

---

## ✅ What Do You Do With It?

You **look at your test number** and **compare** it to each alpha's **critical value**.

| Alpha | Critical Value | Is your test statistic smaller? | Then...                              |
| ----- | -------------- | ------------------------------- | ------------------------------------ |
| 15%   | 0.574          | Yes                             | ✅ Data is probably normal            |
| 5%    | 0.784          | Yes                             | ✅ Still normal at stricter level     |
| 1%    | 1.088          | Yes                             | ✅ Even very strict check says normal |

---

## 🎯 Why This Is Helpful:

* It tells you **how strong your evidence** is for normality.
* You can choose the **alpha level** that fits your situation:

  * Casual test? → **10%**
  * Serious test? → **1%**

---

## 🧠 Simple Summary

| Think of it like...         | Why it's useful                               |
| --------------------------- | --------------------------------------------- |
| A report card with 5 grades | Shows how confident we are the data is normal |
| One test, many cutoffs      | You choose how strict you want to be          |


---

## 7. ✅ Example: Shapiro-Wilk Test

```python
from scipy.stats import shapiro
stat, p = shapiro(df['salary'])
alpha = 0.05
if p > alpha:
    print("Data looks normal (fail to reject H₀)")
else:
    print("Data not normal (reject H₀)")
```

### Output:

```
Test Statistic: 0.985
p-value: 0.184
```

✅ Since p > 0.05, we **fail to reject** the null → the data is likely normal.

---

## 8. ✅ Example: Anderson-Darling Test

```python
from scipy.stats import anderson
result = anderson(df['salary'], dist='norm')
print(f"Statistic: {result.statistic}")
for i in range(len(result.critical_values)):
    sl, cv = result.significance_level[i], result.critical_values[i]
    print(f"At {sl:.1f}%: critical={cv:.3f}, {'Fail to reject' if result.statistic < cv else 'Reject'}")
```

### Output:

```
Statistic: 0.2748
At 15.0%: critical=0.563, Fail to reject
At 10.0%: critical=0.642, Fail to reject
At 5.0%: critical=0.762, Fail to reject
At 2.5%: critical=0.873, Fail to reject
At 1.0%: critical=1.035, Fail to reject
```

✅ Since the statistic is **less than all critical values**, we **fail to reject** the null hypothesis at all alpha levels → the data is likely normal.

---

## 🔁 Summary

| Test                 | Best For      | Output         | Decision Rule (α=0.05)   |
| -------------------- | ------------- | -------------- | ------------------------ |
| **Shapiro-Wilk**     | Small samples | stat, p-value  | p > α = normal           |
| **D’Agostino K²**    | Large samples | stat, p-value  | p > α = normal           |
| **Anderson-Darling** | All sizes     | stat, critical | stat < critical = normal |

🔍 Two Common Approaches in Hypothesis Testing:

1. Tests Using p-values (e.g., t-test, Shapiro-Wilk, KS test):
You get a p-value.

You compare the p-value to alpha (significance level, e.g., 0.05):

If p-value < α → Reject the null hypothesis.

If p-value ≥ α → Fail to reject the null hypothesis.

2. Anderson-Darling Test (and some others):
   
You do not get a p-value.

Instead, you get a test statistic and a set of critical values at various significance levels.

You compare the test statistic directly to the critical values:

If statistic > critical value → Reject the null hypothesis at that alpha level.

If statistic < critical value → Fail to reject the null hypothesis at that alpha level.

✅ So yes, it’s not about p-values here — you just compare the statistic to critical values.

---

## 📌 Conclusion

* Check normality **before using parametric tests**
* Use **visual + statistical methods** together
* Choose the test based on **sample size** and **interpretation needs**

Let me know if you want a Jupyter Notebook version for practice!

