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

# Details in depth

# Airplane Overbooking Monte Carlo Simulation Tutorial

This project guides you through understanding and implementing a Monte Carlo simulation to solve a real-world problem: optimizing ticket sales for an airline to maximize profit while managing the uncertainty of passenger show-ups.

## Overview

Airlines often overbook flights, selling more tickets than available seats, betting that some passengers won’t show up. However, if too many do, the airline must bump passengers, incurring costs. This tutorial uses a Monte Carlo simulation to model this uncertainty and determine the optimal number of tickets to sell.

### Problem Statement

* **Plane Capacity**: 22 seats
* **Ticket Price**: \$350 per ticket
* **Show-Up Probability**: 75% (25% no-show rate)
* **Bumping Cost**: \$550 per bumped passenger
* **Goal**: Decide how many tickets to sell (e.g., 22 to 30) to maximize profit, balancing empty seats and bumping costs.

## Purpose

This simulation framework demonstrates how to model stochastic processes, apply probability distributions, and evaluate outcomes using statistics. It connects Monte Carlo logic with key concepts like the Central Limit Theorem (CLT), stochastic dominance, binomial random variables, and confidence intervals to enable data-driven decision-making.

## Simulation Design and Steps

### 1. Define the Problem and Randomness

* The randomness lies in whether each ticketed passenger shows up (Bernoulli trial).

* For `n` tickets sold, the number of show-ups follows a **Binomial distribution**:
  $X \sim \text{Binomial}(n, p = 0.75)$
  where:

  * `n` is the number of tickets sold (a decision variable),
  * `p = 0.75` is the probability that a passenger shows up,
  * `X` is the random variable: the actual number of passengers who show up.

  So, you choose `n` (how many tickets to sell), and the simulation samples from $X$, the uncertain number of people who show up.

* The range of possible show-ups is from 0 to `n`, though extreme values are rare due to the nature of the binomial probability mass function.

### 2. Simulate One Trial

For one trial of selling `n` tickets:

* Randomly draw show-ups from $\text{Binomial}(n, 0.75)$
* Compute:

  * **Revenue**: $R = 350 \times n$
  * **Bumped Passengers**: $B = \max(0, \text{show\_ups} - 22)$
  * **Bumping Cost**: $C = 550 \times B$
  * **Profit**: $\Pi = R - C$

### 3. Run Multiple Trials (Monte Carlo Sampling)

* Run the above simulation **500 times** per ticket sale level (e.g., from 22 to 30).
* This produces a sample of 500 profit values $\{ \Pi_1, \Pi_2, \dots, \Pi_{500} \}$ for each `n`.
* These form an **empirical distribution** approximating the true outcome distribution under uncertainty.

### 4. Analyze the Results

For each ticket-sale level:

* **Sample Mean** (Expected Profit):
  $\bar{\Pi} = \frac{1}{500} \sum_{i=1}^{500} \Pi_i$
* **Sample Standard Deviation** (Spread):
  $s = \sqrt{\frac{1}{499} \sum_{i=1}^{500} (\Pi_i - \bar{\Pi})^2}$
* **Standard Error of the Mean (SEM)**:
  $\text{SE} = \frac{s}{\sqrt{500}}$
* **95% Confidence Interval (from CLT):**
  $\text{CI}_{95\%} = \bar{\Pi} \pm 1.96 \cdot \text{SE}$
  This interval estimates the range within which the true average profit lies with 95% confidence.

### 5. Visualize the Cumulative Distribution

* Sort the 500 profits in ascending order to compute the empirical cumulative distribution function (ECDF).
* ECDF helps evaluate the **risk** and **probability of achieving certain profit thresholds**.

### 6. Compare Strategies (22 to 30 tickets)

Use the following methods:

* **First-Order Stochastic Dominance**: A ticket level A dominates B if its cumulative profit distribution is always to the right.
* **Second-Order Dominance**: If distributions cross, compare both mean profit and standard deviation (risk-return tradeoff).
* Use CLT-based confidence intervals to ensure results are statistically significant.

## Statistical Insights

### Central Limit Theorem (CLT) in Action

Even though profit outcomes are not normally distributed (due to binomial inputs and max functions), the **sampling distribution of the sample mean profit** approaches normality thanks to the CLT. This enables:

* Building **confidence intervals** around the sample mean.
* Comparing strategies using mean differences with statistical rigor.

### Why 500 Simulations?

* By CLT, the error in estimating the mean decreases as $\frac{1}{\sqrt{n}}$.
* 500 samples provide a good tradeoff between computation and stability in the estimated mean and CI.

## Key Insights

* **Rare Events**: With 500 trials, rare show-ups (e.g., 0, 30) may not appear, but the typical range (e.g., 15–28) dominates the analysis.
* **Cumulative Distribution**: ECDF visualizes profit probabilities and risk profiles.
* **Confidence Intervals**: Offer statistically sound ranges for expected profit.
* **Optimization Strategy**: Select the ticket-sale level that maximizes expected profit while maintaining an acceptable risk profile.

## Learning Outcomes

* Understand the power of Monte Carlo simulation in modeling uncertainty.
* Apply binomial distributions and max logic in real-world problems.
* Use CLT to construct confidence intervals for expected values.
* Evaluate decision strategies using stochastic dominance and statistical rigor.

This code provides a foundation for simulation-based decision-making under uncertainty, applicable across finance, operations, and risk management.
