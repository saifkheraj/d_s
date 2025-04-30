# 📊 Statistics Mini-Series: Understanding Probability Distributions (CAP Prep)

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

Stochastic dominance helps in choosing optimal options under uncertainty by considering **both return and risk**. Use CDF plots and rules to make decisions aligned with different types of decision-makers.

---

