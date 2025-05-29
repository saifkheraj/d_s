# Airplane Overbooking Monte Carlo Simulation Tutorial

This project guides you through understanding and implementing a Monte Carlo simulation to solve a real-world problem: optimizing ticket sales for an airline to maximize profit while managing the uncertainty of passenger show-ups.

## Overview

Airlines often overbook flights, selling more tickets than available seats, betting that some passengers won’t show up. However, if too many do, the airline must bump passengers, incurring costs. This tutorial uses a Monte Carlo simulation to model this uncertainty and determine the optimal number of tickets to sell.

### Problem Statement
- **Plane Capacity**: 22 seats
- **Ticket Price**: $350 per ticket
- **Show-Up Probability**: 75% (25% no-show rate)
- **Bumping Cost**: $550 per bumped passenger
- **Goal**: Decide how many tickets to sell (e.g., 22 to 30) to maximize profit, balancing empty seats and bumping costs.

## Purpose
This code breaks down the logic behind Monte Carlo simulation, connects it to statistical concepts like the Central Limit Theorem and stochastic dominance, and provides an intuitive step-by-step approach to analyze the problem. It’s designed for learners interested in simulation techniques, probability, and decision-making under uncertainty.

## Steps to Understand the Simulation

### 1. Define the Problem and Randomness
- Each ticket sale introduces a random event: will the passenger show up (75% chance)?
- The total number of show-ups follows a binomial distribution (30 trials, 75% success rate for 30 tickets).
- Possible show-ups range from 0 to 30, though extremes are rare.

### 2. Simulate One Trial
- Generate a random number of show-ups (e.g., 23 out of 30).
- Calculate:
  - Revenue: $350 × number of tickets sold (e.g., $10,500 for 30 tickets).
  - Bumped passengers: Max(show-ups - 22, 0) (e.g., 23 - 22 = 1 bumped).
  - Bumping cost: $550 × bumped passengers (e.g., $550).
  - Profit: Revenue - Bumping cost (e.g., $10,500 - $550 = $9,950).

### 3. Run Multiple Trials (500 Times)
- Repeat the trial 500 times to capture a range of outcomes.
- Each trial uses new random show-ups, producing 500 different profit values.
- This reflects the variability of real-world flights, giving a sample of possible results.

### 4. Analyze the Results
- **Average Profit**: Calculate the mean of the 500 profits (e.g., ~$7,950) to estimate expected earnings.
- **Range**: Identify the lowest (e.g., $6,300) and highest (e.g., $10,500) profits to understand risk.
- **Cumulative Distribution**: Sort the 500 profits and compute the cumulative percentage (e.g., 0.2% at $6,300, 100% at $10,500). This shows the probability of achieving a profit level or less, visualized as a staircase curve.

### 5. Compare Decisions
- Test different ticket sales (22 to 30) with 500 trials each.
- Use **stochastic dominance**:
  - First-order: If one curve (e.g., 30 tickets) is always to the right of another (e.g., 22 tickets), it’s better.
  - Second-order: If curves cross, compare average profit and variability (standard deviation).
- Use the **Central Limit Theorem** to estimate confidence intervals for the average profit, enhancing decision reliability.

### 6. Make the Decision
- Based on 500 trials for 30 tickets (e.g., average $7,950, CI [$7,852, $8,048]), compare with other numbers.
- Choose 30 tickets if it offers the highest expected profit with acceptable risk.

## Key Insights
- **Not All Outcomes Are Seen**: With 500 trials, we likely miss rare show-ups (e.g., 0, 1, 29, 30) due to their low probability, but the sample still captures the typical range (e.g., 15 to 28).
- **Cumulative Importance**: The cumulative distribution helps visualize the profit distribution, aiding in risk assessment and comparison.
- **500 Trials**: This number balances accuracy and effort, providing a reliable estimate per the Central Limit Theorem.

## Learning Outcomes
- Understand how Monte Carlo simulation models uncertainty.
- Apply binomial distribution to random events.
- Use statistical tools (mean, cumulative distribution, confidence intervals) for decision-making.
- Recognize the trade-offs between profit and risk in overbooking.

