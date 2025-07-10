# README.md

## Understanding LLMs as Distributions and Sampling

This guide explains how large language models (LLMs), such as transformers, work as **distributions** and how we can generate different outputs by sampling from them. We break it down step by step.

---

### 1. LLMs as Distributions

LLMs do not generate a fixed answer. They generate responses by **sampling** from a **probability distribution** over possible words, given an input query.

> Example:
> For the query: **"Which is the largest ocean?"**
> Possible outputs:

* "Pacific Ocean"
* "Pacific Ocean is the largest ocean."
* "Atlantic Ocean"

These are sampled from the distribution $Y \sim \pi(Y|X)$, where $\pi$ is the probability distribution (policy) conditioned on input $X$.

---

### 2. How Transformers Generate Words

LLMs generate text **one token at a time**:

1. **Tokenize** the input (e.g., "Which is the largest ocean?").
2. Pass tokens through transformer layers.
3. Get **logits** (scores) for each word.
4. Apply **softmax** to convert logits into probabilities.
5. Sample a word from these probabilities.

> Example:
> Softmax might produce:

* "Pacific" = 60%
* "Atlantic" = 25%
* "Indian" = 15%

A word is sampled from this distribution instead of choosing the max (argmax).

---

### 3. Time-based Word Generation (t → t+1)

Each word depends on the previous words:

* At **time t**, the current word affects the next word's probability.
* This process is **causal** — past tokens influence future tokens.

> Example:
> “Pacific” at time t might lead to:

* “Ocean is”
* “Ocean covers”

This generates sequences like:

* “Pacific Ocean is the…”
* “Atlantic Sea is not…”
* “Indian Ocean if you…”

---

### 4. Visualizing with Bar Graphs

Each time step has a **bar graph**:

* **X-axis** = vocabulary words
* **Y-axis** = softmax probability for each word

Words are **sampled** based on their heights in the bar graph.

---

### 5. Generation Parameters

You can influence how the LLM generates output using these settings:

#### a. Temperature ($\tau$)

Controls randomness in the softmax function:

* Low $\tau$: sharp/peaky distribution (less random)
* High $\tau$: flat/uniform distribution (more random)

> Example:

* $\tau = 1$: Normal behavior
* $\tau = 10$: Almost all tokens equally likely

#### b. Top-K Sampling

Limits selection to the top K highest-probability words.

* Keeps only K best tokens
* Re-normalizes their probabilities

#### c. Top-p Sampling (Nucleus Sampling)

Selects the **smallest** group of words whose cumulative probability ≥ p.

* Dynamically adapts number of tokens
* Balances quality and diversity

#### d. Beam Search

Keeps **multiple best sequences** (beams) at each step:

* Expands them all
* Chooses the best final result

More coherent, but less diverse.

#### e. Repetition Penalty

Reduces probability of repeating previous words.

* Avoids loops like: "The ocean is big. The ocean is big."

#### f. Min/Max Tokens

Controls the length of output:

* **Min tokens** = at least this many words
* **Max tokens** = cut off after this many words

---

### Summary Table

| Concept              | Meaning                                  |
| -------------------- | ---------------------------------------- |
| LLM as distribution  | Sampled outputs based on probabilities   |
| Softmax              | Converts logits to probabilities         |
| Time-step generation | Each token depends on previous ones      |
| Temperature          | Controls randomness                      |
| Top-K Sampling       | Sample only from top-K tokens            |
| Top-p Sampling       | Sample from smallest cumulative p tokens |
| Beam Search          | Tracks top sequences at each step        |
| Repetition Penalty   | Penalizes repeated tokens                |
| Min/Max Tokens       | Limits output length                     |

---

### Final Note

The key idea is: **LLMs generate output by sampling from distributions**, not by selecting fixed outputs. You can customize the randomness and structure of generated sequences using parameters like temperature, top-k, and beam search.
