# 📊 Statistics Mini-Series: Understanding Probability Distributions (CAP Prep)

Welcome to our **Statistics Mini-Series**, the foundation of simulation modeling for data-driven decision-making. This class is the **core building block** of everything that follows — especially probability, uncertainty modeling, and simulation analysis in CAP.

---

## 📘 Table of Contents

1. [What is a Probability Distribution Function (PDF)?](#1-what-is-a-probability-distribution-function-pdf)
2. [Types of Random Variables](#2-types-of-random-variables)
3. [Probability Mass Function (PMF)](#3-probability-mass-function-pmf)
4. [Cumulative Distribution Function (CDF)](#4-cumulative-distribution-function-cdf)
5. [Continuous Probability Density Function (PDF)](#5-continuous-probability-density-function-pdf)
6. [Normal Distribution Preview](#6-normal-distribution-preview)
7. [Interval Probability](#7-interval-probability)
8. [Key Properties Summary](#8-key-properties-summary)

---

## 1. What is a Probability Distribution Function (PDF)?

A **Probability Distribution Function** maps a **random variable** (an uncertain event) to the **likelihood of its outcomes**.

- ✅ **Input**: Random variable (e.g., dice roll, height, time)
- ✅ **Output**: Probability or probability density

### Example:
Rolling a fair 6-sided die →  
Each number (1–6) has a probability of 1/6.

---

## 2. Types of Random Variables

| Type      | Description                  | Example                       | Related Function                 |
|-----------|------------------------------|-------------------------------|----------------------------------|
| Discrete  | Finite/countable outcomes    | Die roll, coin toss, rating   | PMF: Probability Mass Function   |
| Continuous| Infinite/uncountable outcomes| Height, weight, time          | PDF: Probability Density Function|

---

## 3. Probability Mass Function (PMF)

Used with **discrete variables** to assign probabilities to each individual outcome.

### Example:
Rolling a fair die:
- Outcomes: 1, 2, 3, 4, 5, 6
- Probability: Each = 1/6 = 0.167
- Graph: Vertical bars of equal height

---

## 4. Cumulative Distribution Function (CDF)

**CDF** = Probability that a random variable is less than or equal to a value (**P(X ≤ x)**)

### Discrete Case (PMF → CDF):
| Outcome | PMF       | CDF     |
|---------|-----------|---------|
| 1       | 0.10      | 0.10    |
| 2       | 0.20      | 0.30    |
| 3       | 0.30      | 0.60    |
| 4,5     | 0.00      | 0.60    |
| 6       | 0.40      | 1.00    |

- CDF **always increases**
- Maximum value of CDF = **1**

---

## 5. Continuous Probability Density Function (PDF)

Used with **continuous variables** like height or time.

### Key Points:
- You cannot calculate the probability of an exact value:  
  `P(X = 60) = 0`
- Instead, calculate **interval probability**:  
  `P(57 < X < 63)` = **Area under the curve**
- Total area under the PDF = **1**

---

## 6. Normal Distribution Preview

The **normal distribution** is a symmetric, bell-shaped curve.

- Mean = 60 → CDF(60) = 0.5
- PDF shows *density*, not point probability
- CDF gives cumulative probability from left

### Shape of CDF:
- Flat at tails (low probability density)
- Steepest at the mean (more probability mass)

---

## 7. Interval Probability

For **continuous distributions**, we calculate:

```text
P(a < X < b) = CDF(b) - CDF(a)
