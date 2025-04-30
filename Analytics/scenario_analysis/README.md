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

## 6. Normal Distribution (with Excel & Real-World Example)

The **Normal Distribution**, or bell curve, is the most common continuous probability distribution. It appears frequently in nature, business, and data science.

### 🚴 Real-Life Example: Delivery Ride Times

Let’s say you’re a data scientist working at a logistics company, and you’re interested in analyzing delivery times for food orders.

- You track **delivery times** for 100 rides.
- You notice most deliveries fall around **30 minutes**, with fewer deliveries taking very short or very long times.
- You group times into buckets: 0–10, 10–20, ..., 60–70 mins.
- As you plot the histogram, it begins to resemble a **bell-shaped curve**, centered around 30 mins.

If you collected 1000 or more samples, you’d likely find:
- Most delivery times fall within 20 to 40 minutes
- Very few take less than 10 or more than 50 minutes

### 🔍 Theoretical Insight

This is the essence of the **normal distribution**:  
A symmetric distribution where:
- Mean = 30 mins  
- Standard Deviation (SD) = 5 mins  
- Shape is defined fully by these two parameters

**Mathematically**, the normal distribution is expressed as:  
```math
f(x) = \frac{1}{\sqrt{2\pi\sigma^2}} \cdot e^{-(x-\mu)^2 / (2\sigma^2)}
