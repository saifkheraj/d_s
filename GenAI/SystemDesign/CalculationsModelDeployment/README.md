# Back-of-the-Envelope Calculations (BOTEC) for Model Deployment

This README provides an intuitive understanding of resource estimation for deploying Large Language Models (LLMs) using back-of-the-envelope calculations. We'll break down storage, inference, and bandwidth needs using a relatable example: deploying an AI assistant in a mobile app used by 100 million daily active users (DAU).

---

## 📊 Goal

Estimate resources required to:

* Store the model and user data
* Run inference efficiently
* Manage bandwidth for requests and responses

---

## 🖼️ Case Study: Mobile AI Assistant App

Let’s walk through a step-by-step case study of a fictional mobile app called **SmartPal**, a personal AI assistant.

### ✅ Scenario

* SmartPal is expected to reach **100 million Daily Active Users (DAU)**
* Each user will interact with the model **10 times a day**
* Each response is **500 tokens**
* Model size: **3 billion parameters** using **FP16 precision**
* Inference will be handled by **NVIDIA A100 GPUs**

---

## 💾 Step 1: Storage Estimation

### ✅ 1. Model Storage

**Formula:**

```
Model Storage = Parameters × Precision
```

**Calculation:**

```
= 3B × 2 Bytes = 6 GB
```

### ✅ 2. User Profile Storage

Assume each user profile needs **10 KB**.

```
= 100M users × 10 KB = 1 TB
```

### ✅ 3. User Interaction Data

Each interaction takes **2 KB**.

```
= 100M × 10 × 2 KB = 2 TB/day
```

Add 25% for indexing:

```
= 2 TB + 0.5 TB = 2.5 TB/day
```

**Monthly storage**:

```
= 2.5 TB/day × 30 days = 75 TB/month
```

---

## 🤖 Step 2: Inference Server Estimation

### ✅ 4. TRPS (Total Requests Per Second)

```
= (100M × 10) / 86400 = 11,574 TRPS
```

### ✅ 5. Inference Time

```
T_inf = (3B × 2 × 500) / 312T = 9.6 ms
```

### ✅ 6. QPS (Queries per Second per GPU)

```
QPS = 1 / 9.6ms = 104
```

### ✅ 7. Number of GPUs Required

```
= TRPS / QPS = 11,574 / 104 = ≈ 112 GPUs
```

**Note:** With quantization or batching, this could reduce to around **56 GPUs**.

---

## 📡 Step 3: Bandwidth Estimation

### ✅ 8. Ingress Bandwidth

Each request = 2 KB

```
Ingress = 11,574 × 2 KB = 23.15 MBps = 186 Mbps
```

### ✅ 9. Egress Bandwidth

Each response = 10 KB

```
Egress = 11,574 × 10 KB = 115.74 MBps = 926 Mbps
```

---

## 📋 Summary of Key Metrics

| Component         | Value                   |
| ----------------- | ----------------------- |
| Model Size        | 6 GB (3B FP16)          |
| User Profile Data | 1 TB                    |
| Daily Interaction | 2.5 TB/day              |
| Monthly Storage   | 75 TB                   |
| Inference TRPS    | 11,574                  |
| Inference Time    | 9.6 ms                  |
| GPUs Required     | 112 (or \~56 optimized) |
| Ingress Bandwidth | 186 Mbps                |
| Egress Bandwidth  | 926 Mbps                |

---

## 🚀 Why BOTEC Matters

Quick estimations like these help you:

* Plan early-stage infrastructure
* Budget cloud costs
* Benchmark different model sizes
* Avoid surprises in scalability

---

## Using OpenAI

## RAG vs OpenAI API Deployment: Back-of-the-Envelope (BOTEC) Comparison

This README provides a summarized case study comparing two major approaches for deploying LLM-based applications at scale:

1. **Using OpenAI’s hosted API (e.g., GPT-4-turbo)**
2. **Combining OpenAI API with Retrieval-Augmented Generation (RAG)**

The goal is to understand their implications for storage, compute, bandwidth, and cost when serving 100 million daily active users (DAU).

---

## 📱 Case Study: SmartPal AI Assistant App

Assumptions:

* 100M DAU
* 10 interactions per user/day = 1B requests/day
* Each response = 500 tokens
* Model: GPT-4-turbo (hosted by OpenAI)

---

## 📊 Option 1: Using OpenAI API Directly

### ✅ Pros:

* No infra to manage
* High performance and reliability
* Fast to prototype and scale

### ❌ Cons:

* **Very expensive** at scale
* Vendor lock-in
* Limited context window

### 🔢 Token Cost Estimation

* Input tokens: 250/request → 250B/day
* Output tokens: 500/request → 500B/day

**Pricing (GPT-4-turbo)**:

* Input: \$0.01 / 1K tokens → \$2.5M/day
* Output: \$0.03 / 1K tokens → \$15M/day

📉 **Total: \$17.5M/day** (\~\$525M/month)

### 🚫 Not Feasible at 100M DAU Without Enterprise Licensing

---

## 📦 Option 2: RAG + OpenAI API

Retrieval-Augmented Generation (RAG) allows you to:

* Store user history, plans, or documents externally
* Retrieve relevant data per request
* Inject into prompt (shorter, more focused)

### ✅ Benefits:

* 50–75% token cost reduction
* Reduced hallucinations
* Personalization without context bloat

### Example:

* Input: 100 tokens (retrieved context)
* Output: 300 tokens
* Total/request = 400 tokens → \$0.004/request

**Cost/day = 1B × \$0.004 = \$4M/day**
📉 **Savings: >75% vs. direct API calls**

### Required Infrastructure:

* Vector DB (Pinecone, Weaviate, FAISS)
* Embedding model (OpenAI `text-embedding-3-small`)
* Orchestration layer (e.g., FastAPI, LangChain)

---

## 🧠 BOTEC Comparison Summary

| Component           | OpenAI API Only     | OpenAI API + RAG       |
| ------------------- | ------------------- | ---------------------- |
| Model Storage       | ✅ OpenAI hosted     | ✅ OpenAI hosted        |
| Compute (Inference) | ✅ Managed by OpenAI | ✅ Managed by OpenAI    |
| Token Usage         | High (750 tokens)   | Low (400 tokens)       |
| Cost per Request    | \~\$0.0175          | \~\$0.004              |
| Daily Cost          | \~\$17.5M           | \~\$4M                 |
| Personalization     | ❌ Stateless         | ✅ Context-aware        |
| Dev Complexity      | Low                 | Medium (add RAG infra) |

---

## 🧰 Final Recommendation

| You Are...                    | Best Approach               |
| ----------------------------- | --------------------------- |
| MVP builder or <10k users     | OpenAI API only             |
| Scaling to millions of users  | Use RAG + OpenAI            |
| Cost-sensitive at large scale | RAG + OpenAI or self-host   |
| Need long-term memory         | RAG or fine-tuned embedding |

---

