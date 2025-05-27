# 📊 Statistics Mini-Series: Understanding Probability Distributions 

Welcome to our **Statistics Mini-Series**, the foundation of simulation modeling for data-driven decision-making. This class is the **core building block** of everything that follows — especially probability, uncertainty modeling, and simulation analysis in CAP.

---

## 📘 Table of Contents

1. [What is a Probability Distribution Function (PDF)?](#1-what-is-a-probability-distribution-function-pdf)
2. [Types of Random Variables](#2-types-of-random-variables)
3. [Probability Mass Function (PMF)](#3-probability-mass-function-pmf)
4. [Cumulative Distribution Function (CDF)](#4-cumulative-distribution-function-cdf)
5. [Continuous Probability Density Function (PDF)](#5-continuous-probability-density-function-pdf)
6. [Normal Distribution (with Excel & Real-World Example)](#6-normal-distribution-with-excel--real-world-example)
7. [Interval Probability](#7-interval-probability)
8. [Key Properties Summary](#8-key-properties-summary)
9. [Comparing Distributions Using Stochastic Dominance](#9-comparing-distributions-using-stochastic-dominance)
10. [Central Limit Theorem (CLT) — Explained with Simulation] (## 10. 📊 Central Limit Theorem (CLT) — Explained with Simulation)

---

## 1. What is a Probability Distribution Function (PDF)?

A **Probability Distribution Function** maps a **random variable** (an uncertain event) to the **likelihood of its outcomes**.

- ✅ **Input**: Random variable (e.g., dice roll, height, time)
- ✅ **Output**: Probability or probability density

### 🎲 Example:
Rolling a fair 6-sided die:  
Each number (1–6) has a probability of 1/6.

---

## 2. Types of Random Variables

| Type       | Description                   | Example                     | Related Function                 |
|------------|-------------------------------|-----------------------------|----------------------------------|
| Discrete   | Finite/countable outcomes     | Die roll, coin toss         | PMF: Probability Mass Function   |
| Continuous | Infinite/uncountable outcomes | Height, weight, time        | PDF: Probability Density Function|

---

## 3. Probability Mass Function (PMF)

Used with **discrete variables** to assign probabilities to each individual outcome.

### 🎲 Example:
Rolling a fair die:
- Outcomes: 1, 2, 3, 4, 5, 6
- Probability: Each = 1/6 = 0.167
- Visual: Vertical bars of equal height (bar plot)

---

## 4. Cumulative Distribution Function (CDF)

**CDF** = Probability that a random variable is less than or equal to a value (**P(X ≤ x)**)

### 📊 Discrete Case Example:
| Outcome | PMF   | CDF  |
|---------|-------|------|
| 1       | 0.10  | 0.10 |
| 2       | 0.20  | 0.30 |
| 3       | 0.30  | 0.60 |
| 4,5     | 0.00  | 0.60 |
| 6       | 0.40  | 1.00 |

- CDF is **non-decreasing**
- Max value = **1**

---

## 5. Continuous Probability Density Function (PDF)

Used with **continuous variables** like height or time.

### Key Concepts:
- `P(X = exact value)` = **0**
- Instead, calculate interval probabilities:  
  `P(57 < X < 63)` = **Area under the curve**
- **Total area under PDF = 1**

---

## 6. 🔔 Normal Distribution (with Excel & Real-World Example)

The **normal distribution**, or bell curve, is the most widely used continuous probability distribution in statistics, business, and science.

### 🎯 Real-Life Example: Food Delivery Times

Imagine you're a data scientist working at a food delivery company. You collect delivery time data from 1,000 completed orders.

- Most deliveries take **around 30 minutes**
- Fewer deliveries take **very short (<10 min)** or **very long (>50 min)** times

When you plot a histogram of these delivery times, you notice a **symmetric, bell-shaped curve** forming — this is a hallmark of the **normal distribution**.

### 📊 Characteristics of the Normal Distribution

| Feature               | Description                                                |
|-----------------------|------------------------------------------------------------|
| Shape                | Bell-shaped, symmetric around the mean                     |
| Mean (μ)             | Location of the center (peak of the curve)                |
| Standard Deviation (σ)| Spread of the curve — wider means more variability        |
| Total Area           | Equals **1** under the curve (i.e., total probability)     |
| Tails                | Extend to ±∞ but rapidly approach zero probability density |

### 📃 Formula

```math
f(x) = \frac{1}{\sqrt{2\pi\sigma^2}} \cdot \exp\left(-\frac{(x - \mu)^2}{2\sigma^2}\right)
```

### 📘 Excel Implementation

- Use `=NORM.DIST(x, mean, std_dev, FALSE)` for PDF
- Use `=NORM.DIST(x, mean, std_dev, TRUE)` for CDF

### ⚙ Changing Parameters

| Curve | Mean (μ) | Std. Dev. (σ) | Shape Insight                        |
|-------|----------|---------------|--------------------------------------|
| A     | 30       | 5             | Centered at 30, moderately narrow    |
| B     | 30       | 10            | Same center, but wider               |
| C     | 40       | 5             | Shifted right                        |

### 🛡 Confidence Interval (95%) in Excel

```excel
=NORM.INV(0.025, 30, 5)  // Lower Bound
=NORM.INV(0.975, 30, 5)  // Upper Bound
```

---

## 7. Interval Probability

For **continuous variables**:
```text
P(a < X < b) = CDF(b) - CDF(a)
```
This represents the **area under the PDF curve** between `a` and `b`.

---

## 8. Key Properties Summary

| Concept | Applies To | Description                             |
|---------|------------|-----------------------------------------|
| PMF     | Discrete   | Probability of each outcome             |
| PDF     | Continuous | Density function (not exact probability)|
| CDF     | Both       | Cumulative probability ≤ x             |
| Area    | Continuous | Represents probability between values   |
| Total   | All        | Must always sum to 1                    |

---

## 9. 🌟 Comparing Distributions Using Stochastic Dominance

![image](https://github.com/user-attachments/assets/20728273-4cc7-4429-bc82-cc6034d0856e)
![image](https://github.com/user-attachments/assets/a88ebb07-17ff-4feb-9dff-f6ef3d5e7664)


# 📊 Stochastic Dominance: Portfolio Comparison with Visuals

This README explains **stochastic dominance** using 5 simulated investment portfolios. Each portfolio is modeled as a **normal distribution** defined by its mean (expected return) and standard deviation (risk).

We’ll use both **Probability Density Function (PDF)** and **Cumulative Distribution Function (CDF)** plots to determine which portfolio is preferred under different decision-making criteria.

---

## 📘 Portfolios Overview

| Portfolio    | Mean Return (%) | Std. Deviation (%) | Comment                          |
|--------------|------------------|---------------------|----------------------------------|
| Portfolio 1  | 10               | 5                   | Baseline                         |
| Portfolio 2  | 7                | 5                   | Lower return, same risk          |
| Portfolio 3  | 8                | 2                   | Lower return, less risk          |
| Portfolio 4  | 10               | 10                  | Same return, higher risk         |
| Portfolio 5  | 12               | 12                  | Higher return, much higher risk  |

---

## 📈 Probability Density Functions (PDF)

This shows how the probability mass is distributed across return outcomes:

![PDF Plot](pdf_plot.png)

---

## 📊 Cumulative Distribution Functions (CDF)

This is used to determine **stochastic dominance** by comparing the full probability spread up to each point:

![CDF Plot](cdf_plot.png)

---

## 🔍 Analysis Using CDF

| Comparison   | Dominance Type | Who Prefers It?       | Reason                                    |
|--------------|----------------|------------------------|-------------------------------------------|
| P1 vs P2     | FSD            | Everyone               | Same risk, P1 has higher return           |
| P1 vs P3     | FSD            | Everyone               | P1’s CDF always below P3                  |
| P1 vs P4     | SSD            | Risk-averse people     | P1 has lower risk, same return            |
| P1 vs P5     | ❌ None         | Depends on preference  | P5 has higher return, but higher risk     |

---

## 🧠 Stochastic Dominance Rules

### ✅ First-Order Stochastic Dominance (FSD)
- A’s CDF is always below B’s CDF
- Everyone prefers A

### ✅ Second-Order Stochastic Dominance (SSD)
- A’s CDF crosses B’s once from below
- Risk-averse people prefer A

### ❌ No Dominance
- CDFs cross multiple times
- Preference depends on utility functions

---

## 📦 Conclusion

Stochastic dominance helps in choosing optimal options under uncertainty by considering **both return and risk**. Use CDF plots and rules to make decisions aligned with different 
types of decision-makers.

 

## 10. 📊 Central Limit Theorem (CLT) — Explained with Simulation

Welcome to the most powerful concept in statistics: the **Central Limit Theorem (CLT)**. Whether you're building forecasts, running simulations, or constructing confidence intervals, **CLT is the reason we can trust the normal distribution**.

---

## 🧠 What is the Central Limit Theorem?

The **Central Limit Theorem (CLT)** states:

> *If you take many samples from a population and compute their means, the distribution of those sample means will approximate a normal distribution — even if the original population is not normal.*

---

## 📘 Key Definitions

| Concept           | Symbol | Meaning                                     |
|------------------|--------|---------------------------------------------|
| Population Mean  | μ      | True average of the entire population       |
| Population Std Dev| σ      | True spread of the population               |
| Sample Mean      | x̄      | Average from one sample                     |
| Sample Std Dev   | s      | Spread in one sample                        |
| Sample Size      | n      | How many observations in each sample        |
| Standard Error   | SE     | Spread of the sample means: σ / √n          |

---

## 📦 Real-World Example: Delivery Times

### 🎯 Scenario:
You work at a food delivery company. You want to estimate the **average delivery time**.

- The delivery times vary a lot: weather, traffic, driver availability
- You don’t have access to all delivery data ever made (the population)
- But you can take **multiple samples** of delivery times (say, 50 orders at a time)

### 🎲 Here's What You Do:
1. Randomly take many samples of 50 delivery times each
2. Calculate the average delivery time of each sample
3. Plot the distribution of those **sample averages**

### 📈 CLT Guarantees:
- That distribution of averages will **look normal** (bell curve)
- The **mean of these averages = true population mean (μ)**
- The **spread = σ / √n** (smaller than population spread)

---

## 🔍 What CLT Tells Us

| Rule | Statement                                                                                   |
|------|----------------------------------------------------------------------------------------------|
| 1    | The average of sample means = population mean: `E[x̄] = μ`                                   |
| 2    | The std dev of sample means = standard error: `SE = σ / √n`                                 |
| 3    | If population is normal, then sample mean distribution is also normal (for any n)           |
| 4    | If sample size `n ≥ 30`, sample mean follows normal distribution regardless of population   |

---

## 🧪 Simulation: Proving CLT with Dice Rolls

Let’s simulate the Central Limit Theorem using Python or Excel:

### 🎯 Setup:
- Population = rolling a fair 6-sided die (outcomes: 1 to 6)
- Population Mean = 3.5
- Population Std Dev ≈ 1.71

### 🎲 Plan:
- Simulate 1,000 samples of 50 dice rolls each
- Calculate mean of each sample
- Plot histogram of sample means

### 🧠 Expectation from CLT:
- Histogram of sample means ≈ Normal Distribution
- Mean of sample means ≈ 3.5
- Std Dev of sample means ≈ 1.71 / √50 ≈ 0.24

---

## 📊 Result from Simulation

| Metric                      | Value           |
|-----------------------------|------------------|
| Mean of Sample Means        | 3.4996           |
| Standard Error (simulated)  | 0.2369           |
| Standard Error (theoretical)| 0.2414           |

✅ **Match confirmed!** CLT holds — the sample means form a normal distribution centered around the population mean.

---

## 🎓 Why CLT Is So Useful

- Makes **sampling powerful** — you don't need the entire population
- Enables construction of **confidence intervals**
- Lets you use **z-scores, t-tests, regression** confidently
- Turns complex data into manageable problems

---

## 💡 Final Takeaways

- CLT lets you use normal distribution tools even when the population isn't normal
- More samples or larger sample sizes = better approximations
- It underpins nearly all inferential statistics used in forecasting, business analytics, and simulation modeling

---

## 📁 Try It Yourself

Simulate dice rolls or delivery time data in Excel or Python:
- Take 30+ samples of size ≥ 30
- Plot the sample means
- Watch the normal curve emerge

CLT isn't just theory — it's a practical, powerful engine behind almost every decision made with data.

---


#  Understanding Probability Distributions in Simulations

This guide is your final checkpoint before diving into real-world simulations. Think of this as loading your GPS and charting the route. To run simulations effectively, we must understand the types of **probability distributions** that describe random variables.

---


![output (2)](https://github.com/user-attachments/assets/ffa40ed5-fc8f-4c65-a783-39964c3ec47e)


## 1. **Types of Distributions**

There are two broad types:

### A. Discrete Distributions

* Used when outcomes are **countable** (e.g., number of dice rolls, success/failure in a trial).

#### i. **Discrete Uniform Distribution**

* **Use Case**: When all possible outcomes are equally likely.
* **Example**: Rolling a fair six-sided die. Each face (1 through 6) has a 1/6 chance.
* **Why It Matters**: It models "complete fairness." Good starting point when nothing is biased.
* **Visual**: A bar chart with equal heights.

#### ii. **Custom Discrete Distribution**

* **Use Case**: When outcomes are known but probabilities differ.
* **Example**: Biased die where face 3 has 30% chance, and others vary.
* **Why It Matters**: It allows domain-specific customization (e.g., modeling customer behavior skewed toward certain choices).
* **Visual**: A bar chart with uneven heights per face.

#### iii. **Bernoulli Distribution**

* **Use Case**: Single event with binary outcome (Success or Failure).
* **Example**: You roll the biased die once. Define success as getting a 3 (P = 0.3).
* **Why It Matters**: It forms the base of many complex distributions like Binomial.
* **Visual**: Two bars (at 0 and 1). Height depends on probability.

#### iv. **Binomial Distribution**

* **Use Case**: Repeated independent Bernoulli trials.
* **Example**: You roll the biased die 10 times. What’s the chance of getting exactly three 3s?
* **Why It Matters**: It helps model how frequently an event occurs in repeated trials (e.g., success in campaigns).
* **Visual**: A histogram peaking near expected number of successes.

---

### B. Continuous Distributions

* Used when values can take **any number in a range** (e.g., weight, height).

#### i. **Continuous Uniform Distribution**

* **Use Case**: All values in a range are equally likely.
* **Example**: Tomato weight is somewhere between 30g and 90g with no more info.
* **Why It Matters**: A good fallback when only the range is known.
* **Visual**: Flat line between 30 and 90.

#### ii. **Triangular Distribution**

* **Use Case**: You know the min, max, and the most likely value.
* **Example**: Tomatoes are 30g–90g but most are around 60g.
* **Why It Matters**: Offers a simple model with a peak—more informative than uniform.
* **Visual**: Triangle with peak at 60.

#### iii. **PERT (Beta-PERT) Distribution**

* **Use Case**: Like triangular, but with a smoother, more natural curve.
* **Example**: Same 30g–60g–90g tomato assumption.
* **Why It Matters**: Produces more realistic and less extreme samples.
* **Visual**: Smooth hump-shaped curve.

#### iv. **Normal (Gaussian) Distribution**

* **Use Case**: When values naturally cluster around a mean.
* **Example**: Tomato weights are measured and found to center around 60g with 5g variation.
* **Why It Matters**: Many natural and business processes follow this distribution.
* **Visual**: Bell curve centered at 60.

---

## 2. **How to Use These Distributions in Simulation**

Simulations are about generating many random values from these distributions and studying their behavior.

* Choose **discrete** for binary/limited outcomes.
* Choose **continuous** when working with measurements.

**Example**: You’re modeling how many premium tomatoes (weight > 65g) come in a batch.

* Use Normal distribution for tomato weights
* Run simulation for 1000 tomatoes
* Count how many exceed 65g

This will give you a realistic estimate of expected quality.

---

## 3. **Histogram vs. PDF (Probability Density Function)**

* **Histogram**: A bar graph created from simulation samples. It tells us how often values occurred.
* **PDF**: A mathematical function describing how a value is theoretically expected to behave.

> Histograms approximate the shape of PDFs when sample sizes are large.

Example:

* A normal distribution PDF is a smooth curve.
* A histogram built from 5000 normal samples will look like a bell shape with discrete bars.

---

## 4. **Visual Summary of Distributions**

| Distribution       | Use Case         | Shape         | Tomato/Dice Example          |
| ------------------ | ---------------- | ------------- | ---------------------------- |
| Discrete Uniform   | Equal outcomes   | Equal bars    | Fair dice (1–6)              |
| Custom Discrete    | Unequal outcomes | Uneven bars   | Biased dice (30% on 3)       |
| Bernoulli          | One success/fail | Two bars      | Roll 3 or not (P=0.3)        |
| Binomial           | Multiple trials  | Discrete bell | # of 3s in 10 rolls          |
| Continuous Uniform | Known range      | Flat line     | Weight between 30–90g        |
| Triangular         | Known mode       | Triangle      | Most tomatoes \~60g          |
| PERT               | Smooth triangle  | Hump          | Same as triangular, smoother |
| Normal             | Natural process  | Bell curve    | Avg. tomato weight = 60g     |

---

## 5. **Final Note**

Understanding these distributions is essential for simulating real-world scenarios. You now have:

* Distributions for modeling both countable and measurable uncertainty
* Clear examples tied to relatable cases (dice & tomatoes)
* Visual intuition from graphs to distinguish each distribution

In the next step, you’ll connect these distributions with real outcomes through simulation.






---

