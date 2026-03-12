# The Hospital That Fixed Its AI — By Asking Better Questions

*Everything you need to know about prompt engineering, explained through one real-world story*

---

A large hospital network — let's call it XYZ Health — deployed an AI assistant for its 70,000 staff. Nurses hated it. Doctors abandoned it after one try. The helpdesk got flooded with complaints.

The AI wasn't broken. The questions were.

That's the problem **prompt engineering** solves. And once XYZ fixed it, everything changed.

---

## What Is Prompt Engineering?

It's the skill of writing better instructions for AI — like briefing a new employee. The more precise you are, the better the result.

Bad prompt: `"chest pain treatment"` 

Good prompt:
```
List top 5 diagnoses for a 67-year-old male, history of heart 
surgery, diabetes, showing chest pressure and sweating. Rank by 
likelihood. Skip muscle-related causes. Numbered list, one-line 
reason each. Reader: on-call doctor.
```
Same AI. Completely different output.

---

## The 5 Building Blocks of Every Good Prompt

**1. Instruction** — what you want done
```
Summarize the patient's discharge notes.
```

**2. Context** — background the AI needs
```
Patient is 45, diabetic, discharged after knee surgery.
```

**3. Constraints** — limits on the response
```
Under 100 words. No medical jargon.
```

**4. Format** — how to structure the output
```
Output as 3 bullet points.
```

**5. Variables** — reusable placeholders
```
Patient: {{Name}}, Age: {{Age}}, Diagnosis: {{Diagnosis}}
Write a plain-English discharge summary for the above patient.
```
Swap the variables, reuse the same prompt for every patient. That's how XYZ Health sent AI-generated summaries to hundreds of patients daily without writing a new prompt each time.

---

## 6 Techniques XYZ's Team Used

### 1. Zero-Shot — Just Ask
No examples, no setup. Works for simple tasks.
```
Create a packing list for a 2-day business trip to Dubai.
```
Fast. Easy. Good enough for straightforward requests.

---

### 2. Few-Shot — Show an Example First
For complex tasks, give the AI one example of what you want, then ask for the real thing.
```
Example — Trip to San Francisco:
| Category  | Item          | Notes              |
|-----------|---------------|--------------------|
| Clothes   | Business suit | 2, for meetings    |
| Gadgets   | Laptop        | With charger       |

Now do the same for a 2-day business trip to Dubai, including 
beach activities in the evening.
```
The AI learns your format and follows it. Far better output than asking cold.

---

### 3. Chain-of-Thought — Break It Into Steps
For complex tasks like calculations or reasoning, spell out the steps.
```
Calculate total cost of a 3-day trip to Dubai for 2 people.
Step 1: Calculate flight cost (2,200 AED × 2 people)
Step 2: Calculate hotel cost (600 AED × 3 nights)
Step 3: Calculate food (200 AED × 2 people × 3 days)
Step 4: Add transport (100 AED × 3 days)
Step 5: Sum everything and show total.
```
Without the steps, XYZ's AI kept getting the math wrong. With them, it nailed it every time.

---

### 4. Self-Consistency — Run It Multiple Times, Pick the Winner
Run the same prompt 3–5 times. Pick the answer that appears most often.
```
Suggest 5 city-exploration sites for a business traveler 
visiting Dubai in the evening. [Run this 3 times]
```
If Burj Khalifa shows up in all 3 responses, it's probably the right answer. XYZ used this for clinical decision support where accuracy was non-negotiable.

---

### 5. Role-Based — Tell the AI Who to Be
```
Act as an experienced ER physician explaining this diagnosis 
to a worried patient in simple English.
```
The AI stays within the boundaries of that role — more focused, more relevant. XYZ used this so patient-facing summaries sounded like a caring doctor, not a textbook.

---

### 6. Iterative Prompting — Keep Refining Until It's Right
First attempt often isn't perfect. That's normal.

**Attempt 1:** AI gets the math wrong → tell it what's wrong
**Attempt 2:** AI overcorrects → ask it to recheck step by step
**Attempt 3:** Correct result ✓ → then add the missing detail
```
Good. Now add 300 AED per person per day for sightseeing 
and recalculate the total.
```
Think of it like editing a draft. You rarely get it perfect on the first go.

---

## Dials You Can Turn: AI Parameters

Beyond the words in your prompt, most AI systems let you tune these settings:

| Parameter | What It Does | Use Low When | Use High When |
|---|---|---|---|
| **Temperature** (0–2) | Controls creativity | You need facts, accuracy | You want creative writing |
| **Top-p** | Range of word choices | Focused, precise output | Diverse, exploratory output |
| **Top-k** | Number of word options | Consistent responses | Creative, varied responses |
| **Repetition Penalty** | Stops repeated phrases | Short outputs | Long documents |
| **Max Tokens** | Caps response length | Cost control, brevity | Full detailed responses |

XYZ set temperature to `0.2` for clinical summaries (accuracy matters) and `0.8` for patient communication drafts (tone and warmth matter).

---

## How to Know If Your Prompt Is Working

XYZ's team used three checks:

**Self-check before sending:**
- Did I give a clear instruction?
- Did I provide enough context?
- Did I set a format and constraints?
- Did I break complex tasks into steps?

**Automated metrics** their data team tracked:
- **BLEU / ROUGE** — how closely AI output matches expected answers (0 to 1; closer to 1 is better)
- **Perplexity** — how confident the model is in its output (lower = better)

**Human feedback** from the ground:
- Nurses and doctors rated usefulness after each interaction
- Department heads reviewed outputs weekly for accuracy and bias

---

## What XYZ Built in the End

They stopped asking staff to write better prompts. Instead, they embedded **340 pre-built prompt templates** directly into their hospital software. When a nurse opened a discharge form, the AI auto-loaded the patient's details into the template and generated the summary — no prompt writing required.

The results after 90 days:

| Metric | Before | After |
|---|---|---|
| Staff satisfied with AI output | 23% | 74% |
| Time to get a useful response | 4.2 min | 38 sec |
| Staff who quit the tool in 30 days | 68% | 19% |

**1,650 physician-hours recovered every single day.**

---

## The One Thing to Remember

The AI knows a lot. It just doesn't know what *you* need unless you tell it — with context, constraints, format, and the right technique for the job.

Prompt engineering is not a technical skill. It's clear communication.

**Better questions. Better answers. That's the whole game.**

---

*The XYZ Health scenario is a composite illustration based on real healthcare AI deployment patterns. Prompt engineering concepts sourced from Educative's AI curriculum.*
