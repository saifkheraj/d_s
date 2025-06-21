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


# Randomized Block Design

![image](https://github.com/user-attachments/assets/f4c76d2a-ffb0-445a-a50f-554ec9c7c229)

Goal: To measure each exercise’s true effect on muscle gain by removing the influence of athletes’ starting fitness level.

Group similar athletes into blocks (Beginner, Intermediate, Advanced).

Randomly assign all treatments (Cardio, Strength, Yoga) within each block so every block sees each exercise.

Use replicates (multiple athletes per block–treatment) to capture natural variability.

Perform ANOVA to test treatment differences while accounting for block (fitness) effects.


## 📌 Conclusion

* Check normality **before using parametric tests**
* Use **visual + statistical methods** together
* Choose the test based on **sample size** and **interpretation needs**

Let me know if you want a Jupyter Notebook version for practice!



# Covariate Adjustment and OLS: Complete Understanding Guide

## Table of Contents
1. [What is OLS?](#what-is-ols)
2. [Understanding Linear Regression](#understanding-linear-regression)
3. [Introduction to Covariates](#introduction-to-covariates)
4. [Why Covariate Adjustment Matters](#why-covariate-adjustment-matters)
5. [When to Remove Covariates](#when-to-remove-covariates)
6. [Step-by-Step Covariate Removal Process](#step-by-step-covariate-removal-process)
7. [Interpreting Results](#interpreting-results)
8. [Real-World Applications](#real-world-applications)
9. [Best Practices](#best-practices)
10. [Common Pitfalls](#common-pitfalls)

---

## What is OLS?

**Ordinary Least Squares (OLS)** is a statistical method used to find the best-fitting line through a set of data points. It's the foundation of linear regression analysis.

### The Core Concept
Imagine you have a scatter plot with points representing data. OLS finds the straight line that minimizes the total distance between all points and the line. The "least squares" part refers to minimizing the sum of squared distances from each point to the line.

### Why It's Important
OLS allows us to:
- Understand relationships between variables
- Make predictions based on data
- Quantify the strength and direction of relationships
- Control for multiple factors simultaneously

---

## Understanding Linear Regression

### Simple Linear Regression
This examines the relationship between one input variable and one output variable. For example, studying how hours of study time affects test scores.

**The Relationship**: As study hours increase, test scores tend to increase in a predictable pattern.

### Multiple Linear Regression
This examines how multiple input variables together affect one output variable. For example, how study hours, sleep quality, and previous GPA all influence current test scores.

**The Advantage**: We can understand the individual effect of each factor while controlling for the others.

---

## Introduction to Covariates

### What Are Covariates?
Covariates are variables that:
- Influence the outcome you're measuring
- Are not your primary focus of study
- Need to be "controlled for" to get accurate results

### Examples in Different Contexts

**Medical Research**
- Primary interest: Does a new drug reduce blood pressure?
- Covariates: Patient age, weight, existing health conditions, diet

**Education Research**
- Primary interest: Does a new teaching method improve learning?
- Covariates: Student prior knowledge, socioeconomic status, school resources

**Business Research**
- Primary interest: Does a new website design increase sales?
- Covariates: Customer age, purchase history, device type, time of day

---

## Why Covariate Adjustment Matters

### The Problem of Confounding
Without controlling for covariates, you might mistake correlation for causation. For example:

**Scenario**: A study finds that people who drink more coffee have higher income.
**Wrong Conclusion**: Coffee drinking causes higher income.
**Real Explanation**: Education level affects both coffee preferences and income potential.

### Benefits of Covariate Adjustment
1. **Reduces Bias**: Isolates the true effect of your variable of interest
2. **Increases Precision**: Reduces unexplained variation in your results
3. **Improves Validity**: Leads to more accurate conclusions
4. **Controls Confounding**: Prevents misleading relationships

### The Control Mechanism
When you include covariates, you're essentially asking: "Among people with similar characteristics (age, education, etc.), what is the effect of the treatment?"

---

## When to Remove Covariates

### Reasons for Removal

#### Statistical Reasons
- **Non-significance**: The covariate doesn't show a meaningful relationship with the outcome
- **Multicollinearity**: Two covariates measure essentially the same thing
- **Model Complexity**: Too many variables relative to sample size

#### Practical Reasons
- **Simplicity**: Easier model interpretation and communication
- **Data Availability**: Covariate data is difficult or expensive to collect
- **Theoretical Irrelevance**: The variable doesn't make logical sense to include

### When to Keep Covariates
Even if not statistically significant, keep covariates that:
- Are theoretically important
- Control for known confounders
- Are standard in your field of research
- Substantially change other coefficients when removed

---

## Step-by-Step Covariate Removal Process

### Phase 1: Initial Assessment
1. **Start Comprehensive**: Include all potentially relevant covariates
2. **Examine Significance**: Look at p-values for each variable
3. **Check Model Fit**: Assess how well the model explains the data
4. **Review Theory**: Consider which variables should logically be included

### Phase 2: Systematic Removal
1. **Identify Candidates**: Variables with p-values > 0.05
2. **Remove Gradually**: Start with the least significant (highest p-value)
3. **Reassess After Each Removal**: Check how it affects other variables
4. **Compare Models**: Evaluate changes in model performance

### Phase 3: Final Validation
1. **Check Remaining Variables**: Ensure all are significant or theoretically important
2. **Validate Assumptions**: Confirm the model meets statistical requirements
3. **Test Predictions**: See how well the final model predicts new data
4. **Interpret Results**: Understand what the final model tells you

### Decision Criteria
Remove a covariate if:
- P-value > 0.05 AND theoretically unimportant
- Removal doesn't substantially change other coefficients
- Model performance doesn't significantly decrease
- Simplification aids interpretation without losing validity

---

## Interpreting Results

### Understanding Coefficients
Each coefficient tells you the expected change in the outcome for a one-unit increase in that variable, **holding all other variables constant**.

### Statistical Significance
- **P-value < 0.01**: Strong evidence of a relationship
- **P-value < 0.05**: Moderate evidence of a relationship  
- **P-value > 0.05**: Weak evidence of a relationship

### Practical Significance
A statistically significant result might not be practically meaningful if:
- The effect size is very small
- The cost of implementation is high
- The variable is difficult to influence

### Model Quality Indicators
- **R-squared**: Percentage of variation explained by the model
- **Adjusted R-squared**: R-squared adjusted for number of variables
- **Residual patterns**: Whether the model fits the data well

---

## Real-World Applications

### Healthcare
**Scenario**: Testing a new treatment's effectiveness
- **Primary Variable**: Treatment type (new vs. standard)
- **Outcome**: Patient recovery time
- **Covariates**: Age, severity of condition, other medications, lifestyle factors

**Covariate Removal**: Remove factors like "favorite color" (irrelevant) but keep "age" (affects recovery regardless of treatment).

### Education
**Scenario**: Evaluating online vs. in-person learning
- **Primary Variable**: Learning format
- **Outcome**: Course completion rates
- **Covariates**: Student age, prior experience, technical skills, motivation level

**Covariate Removal**: Remove "shoe size" (irrelevant) but keep "prior experience" (affects learning regardless of format).

### Business
**Scenario**: Testing marketing campaign effectiveness
- **Primary Variable**: Campaign type (email vs. social media)
- **Outcome**: Purchase conversion rate
- **Covariates**: Customer age, purchase history, device type, season

**Covariate Removal**: Remove "zodiac sign" (irrelevant) but keep "purchase history" (affects buying behavior regardless of campaign type).

### E-commerce
**Scenario**: A/B testing website layouts
- **Primary Variable**: Website design (A vs. B)
- **Outcome**: Time spent on site
- **Covariates**: User device, time of day, returning vs. new visitor, referral source

**Covariate Removal**: Remove "browser version" (if not significant) but keep "device type" (affects user experience regardless of design).

---

## Best Practices

### Design Phase
1. **Plan Covariates Early**: Identify important control variables before data collection
2. **Collect Quality Data**: Ensure covariate measurements are accurate and complete
3. **Consider Sample Size**: Ensure adequate observations relative to number of variables
4. **Document Decisions**: Record why specific covariates were included or excluded

### Analysis Phase
1. **Start Simple**: Begin with a basic model and add complexity gradually
2. **Check Assumptions**: Verify that your data meets the requirements for OLS
3. **Use Domain Knowledge**: Let theoretical understanding guide statistical decisions
4. **Test Robustness**: See if results hold under different model specifications

### Reporting Phase
1. **Be Transparent**: Report which covariates were removed and why
2. **Show Comparisons**: Display results with and without key covariates
3. **Discuss Limitations**: Acknowledge what the model can and cannot tell you
4. **Focus on Interpretation**: Explain what results mean in practical terms

---

## Common Pitfalls

### Statistical Pitfalls
1. **Overfitting**: Including too many variables relative to sample size
2. **Underfitting**: Removing important control variables
3. **Data Snooping**: Choosing covariates based on results rather than theory
4. **Assumption Violations**: Ignoring requirements for valid OLS results

### Interpretation Pitfalls
1. **Causal Claims**: Assuming correlation implies causation
2. **Extrapolation**: Applying results beyond the data range
3. **Precision Illusion**: Thinking more decimal places mean more accuracy
4. **Significance Misunderstanding**: Confusing statistical and practical significance

### Practical Pitfalls
1. **Kitchen Sink Approach**: Including every available variable without thought
2. **Arbitrary Cutoffs**: Using rigid p-value thresholds without considering context
3. **Model Shopping**: Trying many specifications until finding desired results
4. **Ignoring Theory**: Making purely statistical decisions without domain knowledge

---

## Key Takeaways

### Fundamental Principles
1. **OLS is a tool for understanding relationships** between variables while controlling for multiple factors
2. **Covariates help isolate true effects** by controlling for confounding variables
3. **Model simplicity is valuable** but not at the expense of validity
4. **Statistical significance is not the only criterion** for variable inclusion

### Decision Framework
- Include covariates that are theoretically important or empirically significant
- Remove covariates that add complexity without improving understanding
- Always consider the practical implications of your modeling choices
- Document and justify your decisions for transparency

### Quality Indicators
A good model balances:
- **Accuracy**: Explains the data well
- **Simplicity**: Is interpretable and communicable  
- **Validity**: Meets statistical assumptions
- **Relevance**: Addresses the research question meaningfully

---

## Conclusion

Understanding covariate adjustment and OLS is essential for making valid inferences from data. The key is finding the right balance between model complexity and interpretability while ensuring that your conclusions are both statistically sound and practically meaningful.

Whether you're analyzing business metrics, research data, or experimental results, the principles of thoughtful covariate selection will help you draw more accurate and actionable insights from your analyses.

Remember: the goal is not just to find statistically significant results, but to understand the true relationships in your data and make better decisions based on that understanding.
