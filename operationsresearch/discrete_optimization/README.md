# 🧠 Understanding "Value per Weight" in the Knapsack Problem

## 📦 What is the Knapsack Problem?

The **Knapsack Problem** is a classic optimization challenge in computer science and operations research.  
Given a set of items, each with a **weight** and **value**, and a bag (knapsack) with a **maximum weight capacity**,  
the goal is to **maximize the total value of items selected** without exceeding the knapsack's weight limit.

---

## ⚖️ What is "Value per Weight"?

**Value per Weight** (also called **value density**) is a simple yet powerful metric used in greedy algorithms  
for the knapsack problem. It tells you **how much value an item gives you per unit of weight**.

### 🧮 Formula:

value_per_weight = value / weight



---

## 📊 Example

Imagine you have the following items:

| Item           | Value ($) | Weight (kg) | Value/Weight |
|----------------|-----------|-------------|---------------|
| Gold Coin      | 100       | 2           | 50.0          |
| Bronze Statue  | 90        | 5           | 18.0          |
| Painting       | 60        | 1           | 60.0          |

If you're using a **greedy strategy based on value per weight**, you should pick the item with the **highest value density first**.  
In this case, the **Painting (60)** is the most efficient item per kg and would be selected first.

---

## 🤖 Why Use Value per Weight?

In greedy algorithms for the knapsack problem:

- Picking the **most valuable item** might give you less value if it’s too heavy.
- Picking the **lightest item** might not contribute enough value.
- But picking based on **value per weight** balances both, often leading to better solutions.

This strategy is fast and works well in many practical cases, even though it doesn't always guarantee the optimal result.

---

## 🚀 Summary

- **Value per Weight** = Value ÷ Weight
- Used in greedy algorithms to make efficient packing decisions.
- Helps choose items that give the **most value for the least weight**.
- A good **baseline approach** for solving knapsack-like problems quickly.

---

