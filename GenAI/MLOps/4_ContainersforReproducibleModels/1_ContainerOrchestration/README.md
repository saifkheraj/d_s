# Deploying a Fraud Detection Model - Concise Case Study

## The Problem

Your bank built a fraud detection ML model. It works perfectly on your laptop but needs to serve millions of customers 24/7. Your laptop can't handle this. You need:
- Multiple copies running simultaneously
- Auto-recovery if a copy crashes
- Auto-scaling for traffic spikes
- Intelligent traffic routing

## The Solution Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      USERS (Internet)                        │
│                   Submitting Transactions                    │
└────────────────────────┬──────────────────────────────────┘
                         │
           ┌─────────────▼─────────────┐
           │    LOAD BALANCER          │
           │  (Distributes Traffic)    │
           │  Which container is busy? │
           └─────────────┬─────────────┘
                         │
        ┌────────┬───────┴────────┬────────┐
        │        │                │        │
    ┌───▼──┐ ┌──▼──┐         ┌───▼──┐ ┌──▼──┐
    │Cont 1│ │Cont 2│ ...    │Cont 3│ │Cont 4│
    │(EC2) │ │(EC2) │        │(EC2) │ │(EC2) │
    └────┬─┘ └──┬───┘        └───┬──┘ └──┬───┘
         │      │                │       │
         └──────┴────────┬───────┴───────┘
                        │
              ┌─────────▼──────────┐
              │   ECS SERVICE      │
              │  Manages All 4     │
              │  Auto-restart      │
              │  Auto-scale        │
              └─────────┬──────────┘
                        │
         ┌──────────────┼──────────────┐
         │              │              │
    ┌────▼────┐   ┌────▼────┐   ┌────▼────┐
    │ ECR      │   │Task Def │   │ Cluster │
    │(Images)  │   │(Config) │   │(Space)  │
    └──────────┘   └─────────┘   └─────────┘
```

---

## Part 1: Docker & Containers

### The Core Concept

Docker packages your entire application into a sealed unit.

```
WITHOUT Docker:
Your Laptop:      Production Server:
✓ Python 3.9      ✗ Python 3.7
✓ TensorFlow 2.4  ✗ TensorFlow 2.3
✓ Flask 2.0       ✗ Flask 1.8
✓ Model Works!    ✗ Model Crashes!

WITH Docker:
Docker Image = Sealed Package
├─ Python 3.9 (locked)
├─ TensorFlow 2.4 (locked)
├─ Flask 2.0 (locked)
└─ Fraud Model Code

Result: Works IDENTICALLY everywhere!
```

### Containers Are Running Copies

```
Docker Image = Blueprint (like a recipe)
Container = Actual running app

1 Image → Many Containers:
├─ Container 1 (Processing transaction)
├─ Container 2 (Processing transaction)
├─ Container 3 (Processing transaction)
└─ Container 4 (Processing transaction)

If Container 2 crashes → Containers 1, 3, 4 still work ✓
```

---

## Part 2: ECR - The Warehouse

### What ECR Does

ECR is where Docker images are stored centrally so AWS can access them.

```
Your Laptop          ECR (AWS)              ECS (Orchestrator)
┌──────────┐        ┌──────────┐            ┌──────────┐
│Docker    │  Push  │ Image    │   Pull     │Creates   │
│Image     │───────→│Warehouse │───────────→│Container │
│500 MB    │        │Stored    │            │Instances │
└──────────┘        └──────────┘            └──────────┘

Process:
1. Build image on laptop: docker build -t fraud-detection .
2. Push to ECR: docker push to AWS
3. ECS pulls from ECR when needed
```

### Why This Matters

Without ECR, you'd manually copy your image to 4 different servers. With ECR, ECS automatically pulls the image whenever it needs a new container.

---

## Part 3: ECS - The Orchestrator

### The Three Components

```
┌─────────────────────────────────────────────────┐
│              ECS ORCHESTRATOR                   │
├─────────────────────────────────────────────────┤
│                                                 │
│  1. TASK DEFINITION (Recipe/Config)            │
│     "Use fraud-detection image"                │
│     "Allocate 256 CPU, 512 MB memory"          │
│     "Expose port 80"                           │
│     └─ Just a blueprint, nothing runs yet     │
│                                                 │
│  2. ECS CLUSTER (Workspace)                    │
│     Empty office building                      │
│     └─ Just a designated space                │
│                                                 │
│  3. ECS SERVICE (Manager - THE MAGIC!)         │
│     Desired Count = 4                          │
│     "Run 4 containers at all times"            │
│     └─ ECS automatically:                      │
│        ├─ Launches 2 EC2 instances             │
│        ├─ Pulls image from ECR (4 times)       │
│        ├─ Creates 4 containers                 │
│        ├─ Monitors 24/7                        │
│        ├─ Restarts if crash                    │
│        └─ Scales if needed                     │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Critical Understanding: Containers ≠ EC2

```
WRONG: "Containers spin up EC2 machines"
CORRECT: "Containers run ON EC2. ECS spins up EC2 to hold containers"

Your App = Container (Person)
EC2 = Server (Chair)
ECS = Manager (Decides how many chairs to buy)

When you say "Desired Count = 4":
You're saying "I need 4 people working"
ECS calculates "4 people need 2 chairs"
ECS buys 2 chairs
NOT the other way around!
```

### Important Clarification: Image Pull vs Container Creation

**Key Question: "Why pull 4 times but only 2 EC2s?"**

**The Answer: Multiple Containers Run on ONE EC2, Sharing the Image**

```
Docker Image = Recipe book (stored once per EC2)
Container = Chef using that recipe (multiple chefs per EC2)

EC2-1:
├─ Image stored here (downloaded from ECR ONCE)
├─ Container 1 reads from this image (running)
└─ Container 2 reads from this image (running)
   Both containers share the same image file!

EC2-2:
├─ Image stored here (downloaded from ECR ONCE)
├─ Container 3 reads from this image (running)
└─ Container 4 reads from this image (running)
   Both containers share the same image file!

So:
- Pull 2 times (1 per EC2 instance)
- Create 4 containers (2 per EC2)
```

**Why 2 EC2s for 4 Containers?**

```
Task Definition says each container needs:
├─ 256 CPU
├─ 512 MB memory
└─ These resources needed by each container

EC2 t3.medium provides:
├─ 1024 CPU total
├─ 4 GB memory total

ECS calculates:
├─ 256 CPU × 4 containers = 1024 CPU needed
├─ 512 MB × 4 containers = 2 GB needed
├─ One t3.medium (1024 CPU, 4 GB) can fit 2 containers
├─ For 4 containers, need: 4 containers ÷ 2 per EC2 = 2 EC2 instances
└─ So launches 2 EC2 instances

Actual Usage:

EC2-1 (1024 CPU, 4 GB):
├─ Container 1: uses 256 CPU + 512 MB
├─ Container 2: uses 256 CPU + 512 MB
└─ Used: 512 CPU + 1 GB (plenty of space left)

EC2-2 (1024 CPU, 4 GB):
├─ Container 3: uses 256 CPU + 512 MB
├─ Container 4: uses 256 CPU + 512 MB
└─ Used: 512 CPU + 1 GB (plenty of space left)
```

**Visual Timeline:**

```
ECS Service: Desired Count = 4

1. ECS calculates resources needed
   └─ 4 containers × 256 CPU = 1024 CPU
   └─ 4 containers × 512 MB = 2 GB
   └─ Can fit 2 containers per t3.medium EC2

2. ECS launches EC2-1
   ├─ Pulls fraud-detection image from ECR (stored on EC2-1)
   ├─ Creates Container 1 (running on EC2-1, reads image)
   └─ Creates Container 2 (running on EC2-1, reads same image)

3. ECS launches EC2-2
   ├─ Pulls fraud-detection image from ECR (stored on EC2-2)
   ├─ Creates Container 3 (running on EC2-2, reads image)
   └─ Creates Container 4 (running on EC2-2, reads same image)

Result: 2 EC2s, 4 containers, 2 images (one per EC2)
```

**Simple Analogy:**

```
Docker Image = Restaurant Recipe
EC2 = Restaurant Kitchen
Container = Chef cooking using the recipe

Restaurant 1 (EC2-1):
├─ Recipe posted on wall (image pulled once)
├─ Chef 1 cooking (Container 1)
└─ Chef 2 cooking (Container 2)
   Both chefs read the SAME recipe, they don't need separate copies

Restaurant 2 (EC2-2):
├─ Recipe posted on wall (image pulled once)
├─ Chef 3 cooking (Container 3)
└─ Chef 4 cooking (Container 4)
   Both chefs read the SAME recipe

Result: 2 restaurants, 4 chefs, 2 recipe posts (one per restaurant)
NOT: 2 restaurants, 4 chefs, 4 recipe posts
```

**Bottom Line:**

When I said "pulls 4 times" - that was misleading. It's more accurate:

```
ECS:
├─ Pulls image 2 times (once per EC2)
├─ Creates 4 containers (2 per EC2)
└─ Each container uses the image on its own EC2

The image is a shared resource on each EC2.
Containers don't need individual copies of the image.
```

### What ECS Does Automatically

```
Event 1: Container Crashes (3 AM)
├─ ECS detects: "Expected 4, have 3"
├─ ECS action: Pulls fresh image, starts new container
└─ Result: Back to 4 containers ✓ (Users see nothing)

Event 2: Traffic Spike (Black Friday)
├─ ECS detects: "Containers at 90% capacity"
├─ ECS action: Increases Desired Count to 12
├─ ECS launches more EC2s, creates more containers
└─ Result: System remains responsive ✓

Event 3: Traffic Returns to Normal
├─ ECS detects: "Containers at 20% capacity"
├─ ECS action: Decreases Desired Count to 4
├─ ECS terminates extra containers and EC2s
└─ Result: Saves money ✓
```

---

## Part 4: Load Balancer - Traffic Director

### The Core Concept

Load Balancer sits in front of containers and decides which one should process each request.

```
Without Load Balancer:
User A gets routed to Container 1 (busy with 100 transactions)
User B gets routed to Container 3 (busy with 95 transactions)
Both wait forever
Result: Slow system ✗

With Load Balancer:
LB checks container status:
├─ Container 1: 100 transactions (BUSY)
├─ Container 2: 10 transactions ← PICK THIS ONE
├─ Container 3: 95 transactions (BUSY)
└─ Container 4: 20 transactions

Routes both users to Container 2
Result: Fast processing ✓
```

### The Connection: Desired Count ↔ Load Balancer

```
Desired Count = How many containers
Load Balancer = Distributes traffic among them

Desired Count = 1:
├─ 1 container × 100 transactions/sec = 100 total capacity
├─ Get 500 transactions/sec → OVERLOADED ✗
└─ Users experience slow response

Desired Count = 4:
├─ 4 containers × 100 transactions/sec = 400 total capacity
├─ Get 400 transactions/sec → PERFECT ✓
├─ LB distributes evenly across all 4
└─ Users experience fast response

More containers = More capacity = LB can distribute better
```

### A Transaction's Journey

```
Step 1: User submits $5000 transfer
        ↓
Step 2: Request hits Load Balancer
        ↓
Step 3: LB checks: Container 2 is least busy
        ↓
Step 4: Routes to Container 2
        ↓
Step 5: Container 2 runs fraud model (50ms)
        ↓
Step 6: Decision: APPROVED
        ↓
Step 7: Response back through LB
        ↓
Step 8: User sees ✓ Transfer Approved (200ms total)
```

---

## Part 5: Complete Workflow

### Step-by-Step Setup

```
Step 1: Build Docker Image
        └─ Your code + Python + TensorFlow + Flask
        └─ Result: fraud-detection image (500 MB)

Step 2: Push to ECR
        └─ Image now in AWS warehouse
        └─ ECS can access it anytime

Step 3: Create Task Definition
        └─ Config: image, CPU, memory, port
        └─ This is just a recipe

Step 4: Create ECS Cluster
        └─ Empty workspace created
        └─ Nothing happens yet

Step 5: Create ECS Service
        ├─ Set Desired Count = 4
        └─ AUTOMATIC:
           ├─ ECS launches EC2 instances
           ├─ Pulls image from ECR
           ├─ Creates 4 containers
           └─ All running ✓

Step 6: Create Load Balancer
        └─ Routes traffic to 4 containers

Step 7: Users Access
        └─ LB distributes traffic
        └─ Containers process transactions
        └─ System auto-recovers from failures
        └─ System auto-scales under load
```

### Real Numbers

```
Problem: Bank processes 1M transactions/day
Fraud loss: 0.1% = 1000 frauds × $500 = $500K/day

Solution: Fraud detection model with 95% accuracy
Actual fraud: 5% of 1000 = 50 frauds × $500 = $25K/day
Savings: $475K/day

Cost: 2 EC2s + Load Balancer = ~$2,300/month

ROI: Saves bank $475K/day
     Costs $2,300/month
     Pays for itself in hours, not months ✓
```

---

## Part 6: Failure & Recovery

### When a Container Crashes

```
Current State:
├─ Container 1: ✓ Running
├─ Container 2: ✓ Running
├─ Container 3: ✓ Running
└─ Container 4: ✓ Running

Container 2 crashes (bug in code)
     ↓
ECS detects: "Desired 4, have 3"
     ↓
ECS pulls fresh image from ECR
     ↓
ECS starts new Container 2
     ↓
Load Balancer notices:
├─ Routes traffic to 1, 3, 4 (temporarily)
├─ When 2 comes online, routes to it again
└─ Users see ZERO downtime ✓
```

---

## Part 7: Auto-Scaling in Action

### Black Friday Traffic Spike

```
Normal Day:
├─ 4 containers running
├─ Each handles 100 transactions/sec
├─ Total: 400 transactions/sec capacity

Black Friday:
├─ Traffic suddenly 10x normal
├─ ECS detects: "Containers at 90% capacity"
├─ ECS action: Increase Desired Count to 40
     └─ Launches more EC2 instances
     └─ Creates 36 more containers
     └─ Total: 40 containers
     └─ New capacity: 4000 transactions/sec ✓

After Black Friday:
├─ Traffic back to normal
├─ ECS decreases Desired Count to 4
├─ Extra containers & EC2s terminated
├─ Cost reduced ✓
```

---

## Part 8: AWS vs GCP

### Same Problem, Different Solutions

```
AWS (ECS) Approach:
1. Build image
2. Push to ECR
3. Create Task Definition
4. Create Cluster
5. Create Service (Desired Count = 4)
6. Create Load Balancer
7. Connect them

GCP (Kubernetes) Approach:
1. Build image
2. Push to Container Registry
3. Create Deployment (Replicas = 4)
4. Expose Load Balancer

Difference: ECS requires more steps, Kubernetes more automated
Same Result: 4 containers, auto-recovery, auto-scaling, load-balanced
```

---

## Quick Revision Guide

### 5 Key Concepts

| Concept | What It Is | Purpose |
|---------|-----------|---------|
| **Docker Image** | Sealed package of app + dependencies | Portability |
| **ECR** | Central warehouse for images | Accessibility |
| **Task Definition** | Configuration for running one container | Blueprint |
| **ECS Service** | Manager (Desired Count = 4) | Orchestration |
| **Load Balancer** | Traffic router | Efficient distribution |

### The Flow

```
Image → ECR → Task Def → Cluster → Service (Desired=4)
  ↓
ECS creates EC2s + Containers
  ↓
Load Balancer routes traffic
  ↓
Auto-recovery + Auto-scaling happen automatically
```

### Critical Points to Remember

1. **Containers are your app, not servers**
   - Containers run ON EC2s
   - ECS decides how many EC2s to create

2. **Desired Count = Capacity**
   - 1 container = 100 req/sec capacity
   - 4 containers = 400 req/sec capacity
   - More containers needed → Set higher Desired Count

3. **Load Balancer distributes across containers**
   - Always routes to least busy
   - If container crashes, reroutes automatically
   - Users see no downtime

4. **ECS automates everything**
   - You set Desired Count once
   - ECS handles: launching, monitoring, recovery, scaling
   - No manual intervention needed

5. **Both AWS and GCP solve same problem**
   - Different implementation
   - Same concepts apply

---

## Interview Answer (2 minutes)

**Q: Explain your deployment architecture for the fraud detection model**

**A:**

"I containerize the fraud detection model using Docker, packaging the code with Python, TensorFlow, and all dependencies. This Docker image is stored in ECR.

I create a Task Definition that specifies: use this image, allocate 256 CPU and 512 MB memory. This is just a configuration.

I create an ECS Cluster as a workspace, and then create an ECS Service with Desired Count = 4. ECS automatically launches EC2 instances and creates 4 containers from the image.

I set up a Load Balancer that intelligently routes all user requests to the least busy container.

ECS continuously monitors the containers. If one crashes, it automatically restarts it. The load balancer reroutes traffic during this time, so users see zero downtime.

If fraud traffic spikes on a holiday, ECS detects the high load and automatically scales to more containers. When traffic returns to normal, it scales back down.

This architecture provides high availability, automatic recovery, and automatic scaling—all critical for production."

---

## Diagram: Complete System

```
                        USERS
                         │
                   ┌─────▼─────┐
                   │   LOAD     │
                   │ BALANCER   │
                   └─────┬─────┘
                   ┌─────┴─────┬─────────┐
                   │           │         │
            ┌──────▼──┐  ┌────▼───┐  ┌─▼──────┐
            │Container│  │Container│  │Container│  ...
            │    1    │  │   2    │  │   3    │
            └─────────┘  └────────┘  └────────┘
                │            │           │
            ┌───┴────────────┴───────────┘
            │
        ┌───▼───────────────┐
        │  ECS SERVICE      │
        │ Desired Count = 4 │
        │ Auto-recovery     │
        │ Auto-scaling      │
        └───┬───────────────┘
            │
    ┌───────┼───────┐
    │       │       │
┌───▼──┐ ┌──▼──┐ ┌──▼──┐
│ECR   │ │Task │ │Clust│
│Images│ │Def  │ │er   │
└──────┘ └─────┘ └─────┘
```