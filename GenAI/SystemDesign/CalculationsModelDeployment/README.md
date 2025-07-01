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

## ✨ Next Steps

In future lessons, we’ll:

* Apply these numbers to different model types (e.g., image, video)
* Explore batching, quantization, and serverless inference
* Optimize deployment costs

Stay tuned — BOTEC is just the start of system design!

---
