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



# CronJobs

# Cron & Workflow Scheduling for Model Pipelines

---

## Quick Recap: Real-Time Models (Already Covered in Detail)

### The Real-Time Approach

Real-time models need instant responses (milliseconds).

```
Docker (Package model)
  ↓
ECR (Store image)
  ↓
ECS (Manage multiple copies)
  ↓
Load Balancer (Route traffic)
  ↓
Users get instant response ✓

Example: Fraud detection (need answer in 200ms)
```

**Key Points:**
- Docker: Package model + dependencies
- ECS: Manages 4+ containers, auto-recovery, auto-scaling
- Load Balancer: Routes traffic intelligently
- Cost: Always running

**See detailed documentation for full explanation.**

---

## Real-Time vs Batch: The Key Difference

### Real-Time Pipeline

```
User Request
    ↓
Instant Processing (milliseconds)
    ↓
User sees result immediately

Example: Fraud detection, recommendation systems, chatbots
```

### Batch Pipeline

```
Scheduled Trigger (e.g., daily at 2 AM)
    ↓
Process data (can take hours)
    ↓
Store results in database
    ↓
Other services query results later

Example: Churn prediction, customer scoring, ranking
```

### Comparison Table

| Aspect | Real-Time | Batch |
|--------|-----------|-------|
| Response Needed | Instantly (milliseconds) | Later (hours acceptable) |
| When | Continuous | On schedule |
| Example | Fraud detection | Churn prediction |
| Tools | Docker + ECS + LB | Cron + EventBridge + Airflow |
| Scaling | Auto with traffic | Manual or scheduled |
| Cost | Always running | Run when needed |
| Infrastructure | Multiple EC2 instances | Single or few EC2 instances |

---

# BATCH PIPELINES: THE FOCUS

Batch pipelines run on a schedule to process data and store results.

---

## The Problem: Gaming Company Scenario

Your gaming company built a model predicting player churn (likely to quit). This prediction must run **every day at 2 AM**.

```
Pipeline Steps:
1. Fetch player data from warehouse
2. Train churn prediction model
3. Generate predictions for all players
4. Save results to database

At 9 AM:
5. Game servers query predictions
6. Identify 5,000 at-risk players
7. Send each personalized offer
8. Result: 1,000 players stay, $50K revenue saved
```

**Challenge:** How do you make this run automatically every day?

---

## Part 1: Docker Container (Brief Overview)

### Build Container for Pipeline

```dockerfile
FROM python:3.9
RUN pip install pandas sklearn google-cloud-bigquery
COPY pipeline.py /app/
COPY credentials.json /app/
CMD ["python", "/app/pipeline.py"]
```

Build command:
```bash
docker build -t churn-pipeline:latest .
docker push to ECR (storage)
```

Result: Container that runs your pipeline script.

**Purpose:** Package pipeline script with dependencies so it runs identically everywhere.

---

## Part 2: Cron - Simple Scheduling

### What is Cron?

Cron is a Linux utility that runs tasks on a schedule. Like your phone's alarm, but for computers.

Think of it as: "Every day at 2 AM, wake up and run this command"

### Cron Expressions

Cron uses a specific format to define when things run:

```
Format: Minute Hour Day Month DayOfWeek

Example: 0 2 * * *

Breakdown:
┌─ Minute (0)
│ ┌─ Hour (2)
│ │ ┌─ Day of month (* = every day)
│ │ │ ┌─ Month (* = every month)
│ │ │ │ ┌─ Day of week (* = every day)
│ │ │ │ │
0 2 * * *  = Run at 2:00 AM every day
```

### Common Cron Expressions

```
0 2 * * *      = Daily at 2:00 AM
30 9 * * *     = Daily at 9:30 AM
0 0 * * 0      = Every Sunday at midnight
0 0 1 * *      = 1st of every month at midnight
0 */4 * * *    = Every 4 hours (0, 4, 8, 12, 16, 20)
*/15 * * * *   = Every 15 minutes
0 9-17 * * *   = Every hour from 9 AM to 5 PM
```

### How Cron Works

```
Every minute, cron checks its schedule.
When the time matches, it executes the command.

Example Timeline:

1:59 AM - Waiting...
2:00 AM - TIME MATCHES! Execute:
         docker run churn-pipeline:latest
         └─ Container starts
         └─ Pipeline runs
         └─ Predictions generated
         └─ Results saved
2:05 AM - Pipeline done, container stops
3:00 AM - Still waiting for next trigger...
...
Next day at 2:00 AM - MATCHES AGAIN! Repeats.
```

### Setting Up a Cron Job

#### Step 1: Open Cron Editor

```bash
crontab -e
```

This opens a text editor where you can add cron jobs.

#### Step 2: Add Your Job

Add this line:
```
0 2 * * * docker run churn-pipeline:latest
```

This says: "Every day at 2 AM, run the churn-pipeline container"

#### Step 3: Save and Exit

Save the file (in vi: press Esc, then :wq)

Result: Job scheduled ✓

### Real Timeline: One Day with Cron

```
2:00 AM - Cron trigger
├─ Docker container starts
├─ Python script begins
├─ Loads 10,000 players (10 seconds)
├─ Trains model (30 seconds)
├─ Generates predictions (10 seconds)
├─ Saves to database (10 seconds)
└─ Container stops (total: ~60 seconds)

2:02 AM - Pipeline complete, results in database

9:00 AM - Game servers query results
├─ Query: "Show players with churn_score > 0.8"
├─ Results: 5,000 at-risk players
├─ Send each a special offer
└─ 1,000 of those players now stay

Result: $50,000 revenue saved ✓
```

### Verify Cron Job Is Set

```bash
crontab -l    # List all cron jobs
```

You should see your job in the list.

### Logs: Checking If Job Ran

```bash
# Check system logs
sudo tail -f /var/log/syslog | grep CRON

# Or check specific command logs
# Most services log to: /var/log/
```

---

## Part 3: Limitations of Cron

### Problem 1: Single Machine Dependency

```
Your Laptop (has cron job set up)
    ↓
At 2 AM, laptop wakes cron to run job
    ↓
But what if:
├─ Laptop is turned off? → Job doesn't run ✗
├─ Laptop loses power? → Job doesn't run ✗
├─ Network connection drops? → Job fails ✗
└─ Laptop crashes? → Job never runs again ✗

Result: No predictions generated that day
        Game servers use stale data
        Wrong offers sent to players
        Revenue lost ✗
```

### Problem 2: No Monitoring or Alerts

```
2 AM - Pipeline fails (database connection error)
    └─ Cron runs silently, doesn't notify anyone

9 AM - Game servers query predictions
    └─ No results (pipeline failed)
    └─ Use old predictions

Afternoon - You discover problem
    └─ By then, day is mostly lost

With monitoring:
2:05 AM - Would alert: "Pipeline failed!"
2:10 AM - You could investigate and fix
Result: Much less damage
```

### Problem 3: No Dependency Management

```
Your data warehouse has maintenance on Tuesday
├─ Pipeline runs at 2 AM
├─ Tries to fetch data
├─ Data warehouse unavailable
├─ Pipeline fails silently
└─ No one knows until morning

With dependency checks:
├─ Pipeline checks: "Is warehouse ready?"
├─ Warehouse returns: "No, maintenance in progress"
├─ Pipeline automatically retries in 1 hour
├─ When warehouse comes back, pipeline succeeds
└─ Fresh data available by morning
```

### Problem 4: No Easy Recovery

```
Tuesday 2 AM - Pipeline fails for some reason
Wednesday morning - You discover problem
    └─ Need to manually restart pipeline
    └─ Need to backfill Tuesday's missing predictions
    └─ Manual work, error-prone

With proper workflow tool:
├─ Immediate notification of failure
├─ Easy click-to-retry
├─ Automatic backfilling
└─ Much simpler recovery
```

---

## Part 4: Cloud Scheduling - Cron in the Cloud

As your pipeline grows, you need reliability. Cloud providers offer better solutions.

### Two Main Options

#### Option 1: AWS EventBridge

AWS's native scheduling service.

```
EventBridge Rule:
├─ Schedule: 0 2 * * * (same cron syntax!)
├─ Target: ECS Service
└─ Action: Run docker container

When 2 AM arrives:
├─ EventBridge triggers
├─ Tells ECS to run the task
├─ ECS pulls image from ECR
├─ ECS creates container
├─ Pipeline runs
├─ ECS cleans up when done
```

**Setup:**
```
1. Push churn-pipeline image to ECR
2. Create ECS Task Definition
3. Create EventBridge Rule
   ├─ Name: daily-churn-prediction
   ├─ Schedule: 0 2 * * *
   ├─ Target: ECS Service
   └─ Done!
```

**Advantages:**
- Simple setup
- AWS-native
- CloudWatch monitoring
- Email alerts via SNS
- Automatic retries
- Cost: ~$0.35/month

**Disadvantages:**
- AWS-only (not portable to other clouds)
- Limited for complex workflows

#### Option 2: Kubernetes CronJob

Google Cloud's approach (works on any cloud).

```
YAML Configuration:

apiVersion: batch/v1beta1
kind: CronJob
metadata:
  name: churn-prediction
spec:
  schedule: "0 2 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: churn-pipeline
            image: churn-pipeline:latest
```

**Setup:**
```
1. Push image to Container Registry
2. Create cluster
3. Apply YAML file
4. Done!
```

**Advantages:**
- Cloud-agnostic (works on AWS, GCP, Azure, on-premises)
- Kubernetes is industry standard
- Automatic monitoring
- Automatic retries
- Highly reliable

**Disadvantages:**
- Requires Kubernetes knowledge
- More complex than EventBridge

---

## Part 5: Airflow - Complex Workflows

When your pipeline has dependencies and complexity, use Airflow.

### Real-World Complexity

```
Simple view: "Run pipeline at 2 AM"

Reality:
├─ Task 1: Check if data warehouse is ready
│  ├─ If not ready, retry in 30 minutes
│  └─ If still not ready, alert team
├─ Task 2: Only if Task 1 succeeds, train model
├─ Task 3: Only if Task 2 succeeds, generate predictions
├─ Task 4: Only if Task 3 succeeds, save to database
├─ Task 5: Notify stakeholders
├─ Task 6: If any task fails, send detailed alert
└─ Task 7: Allow manual retry of just failed task
```

EventBridge and CronJob can't express this complexity.

### What Airflow Does

```
Airflow DAG (Directed Acyclic Graph):

Check Warehouse
       ↓
    Train Model (only if check succeeds)
       ↓
Generate Predictions (only if training succeeds)
       ↓
    Save Results (only if generation succeeds)
       ↓
  Send Notifications

Each task:
├─ Runs independently
├─ Has retry logic
├─ Logs everything
├─ Can be rerun individually
└─ Depends on previous tasks
```

### Real Benefit

```
SCENARIO: Data warehouse maintenance Tuesday

With Cron:
├─ 2 AM: Pipeline tries to fetch data
├─ Database unavailable
├─ Pipeline fails silently
├─ 9 AM: No predictions, stale data used
├─ Day is largely lost ✗

With Airflow:
├─ 2 AM: Task 1 checks warehouse
├─ Database unavailable
├─ Airflow immediately notifies team
├─ Task 1 fails, other tasks don't run
├─ 2:05 AM: Team gets alert
├─ 2:15 AM: Warehouse back online
├─ Airflow automatically retries Task 1
├─ Task 1 succeeds
├─ Remaining tasks execute
├─ 2:30 AM: Pipeline complete
├─ Fresh predictions available
└─ Result: Minimal impact ✓
```

### When to Use Airflow

```
Use Airflow when:
├─ Multiple dependent tasks
├─ Need complex logic between tasks
├─ Multiple teams depend on results
├─ Need to backfill historical data
├─ Production-grade reliability critical
└─ Need visibility into what's happening
```

---

## Part 6: Scheduling Evolution

### How Companies Progress

```
MONTH 1: Learning Phase
├─ Use: Cron on laptop
├─ Problem: Unreliable
├─ Cost: Free

MONTH 3: Growing Phase
├─ Use: Kubernetes CronJob (if multi-cloud)
│   or EventBridge (if AWS-only)
├─ Benefit: Reliable, monitored, alerts
├─ Cost: Minimal (~$0.35/month)

MONTH 6: Scaling Phase
├─ Use: Airflow
├─ Benefit: Complex workflows, dependencies
├─ Cost: More infrastructure but worth it
```

---

## Comparison: All Options

| Aspect | Cron | EventBridge | CronJob | Airflow |
|--------|------|-------------|---------|---------|
| Setup | Simple | Easy | Medium | Complex |
| Runs On | Single machine | AWS Cloud | Any cloud | Any cloud |
| Reliability | Low | High | High | Very High |
| Monitoring | None | CloudWatch | Built-in | Complete |
| Alerts | Manual | SNS/Email | Yes | Yes |
| Retries | None | Yes | Yes | Yes |
| Dependencies | Manual | Limited | Limited | Full |
| Cost | Free | $0.35/mo | Similar | More |
| Best For | Learning | AWS tasks | Cloud-agnostic | Complex |

---

## Making the Choice

### Choose Cron When:
- Learning cron syntax (educational)
- Simple one-off task
- Single machine is fine

### Choose EventBridge When:
- AWS-only infrastructure
- Simple scheduled task
- Want AWS-native monitoring
- Need reliable cloud execution

### Choose Kubernetes CronJob When:
- Multi-cloud or might switch clouds
- Want portable solution
- Need Kubernetes infrastructure anyway
- Simple scheduled containerized task

### Choose Airflow When:
- Multiple dependent tasks
- Complex pipeline logic
- Multiple teams using pipeline
- Need production-grade reliability
- Business-critical pipeline

---

## Real-World Architecture

```
Churn Prediction Pipeline

┌─────────────────────────────────┐
│  2 AM: Scheduler Trigger        │
├─────────────────────────────────┤
│                                 │
│  Option 1: Cron                 │
│  ├─ Unreliable                  │
│  └─ No monitoring               │
│                                 │
│  Option 2: EventBridge/CronJob  │
│  ├─ Reliable                    │
│  ├─ Monitoring                  │
│  └─ Alerts                      │
│                                 │
│  Option 3: Airflow              │
│  ├─ Reliable                    │
│  ├─ Complex logic               │
│  └─ Full visibility             │
│                                 │
└─────────────────────────────────┘
           ↓
┌─────────────────────────────────┐
│  Docker Container               │
│  (Runs pipeline script)         │
└─────────────────────────────────┘
           ↓
┌─────────────────────────────────┐
│  Pipeline Execution             │
│  1. Fetch data                  │
│  2. Train model                 │
│  3. Generate predictions        │
│  4. Save to database            │
└─────────────────────────────────┘
           ↓
┌─────────────────────────────────┐
│  9 AM: Game Servers Query       │
│  Results available for           │
│  targeting at-risk players      │
└─────────────────────────────────┘
```

---

## Summary

```
Real-Time Models:
├─ Always running
├─ Need instant response
├─ Use: Docker + ECS + Load Balancer
└─ Example: Fraud detection

Batch Models:
├─ Run on schedule
├─ Store results for later use
├─ Evolution:
│  ├─ Start: Cron (simple, unreliable)
│  ├─ Grow: EventBridge/CronJob (reliable)
│  └─ Scale: Airflow (complex, enterprise)
└─ Example: Churn prediction

Choice depends on:
├─ Complexity of workflow
├─ Cloud provider (AWS vs multi-cloud)
├─ Reliability requirements
├─ Team expertise
└─ Budget
```

---
