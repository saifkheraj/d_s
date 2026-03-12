# Semantic Routing for LLMs

## Overview

Semantic routing is an intelligent query distribution system for Large Language Models (LLMs) that directs user queries to the most appropriate domain-specific prompt or sub-model. Instead of using a one-size-fits-all approach, semantic routing analyzes the semantic meaning of a query and matches it with specialized prompts designed for specific domains like finance, health, travel, or literature.

## Intuition: How It Works

Think of semantic routing as a smart receptionist in a large hospital. When a patient arrives with a complaint, the receptionist doesn't send everyone to the same doctor. Instead, they listen to the symptoms and direct the patient to the specialist best equipped to help—cardiology for heart issues, orthopedics for bone problems, and so on.

Similarly, semantic routing:
1. **Listens** to the user's query by converting it into a numerical representation (embedding)
2. **Understands** the meaning by comparing it against pre-defined domain-specific questions
3. **Directs** the query to the most semantically similar domain
4. **Responds** using a specialized prompt tailored for that domain

The magic happens through **cosine similarity**—a mathematical way to measure how "close" two pieces of text are in meaning, even if they use different words.

## How Semantic Routing Works: Step-by-Step

### Step 1: Define Domain-Specific Prompts
Create specialized prompts for each domain you want to support. Each prompt sets the context and expertise level for that domain.

```python
book_review_template = """You are an expert literary critic..."""
health_fitness_template = """You are a certified health and fitness expert..."""
travel_guide_template = """You are an experienced travel consultant..."""
personal_finance_template = """You are a financial advisor..."""
```

### Step 2: Create Representative Questions
For each domain, define a set of typical questions that users might ask. These serve as semantic anchors.

```python
book_review_questions = [
    "What are the main themes in this novel?",
    "Can you recommend books similar to...",
    # More questions...
]
```

### Step 3: Generate Embeddings
Convert all representative questions into numerical vectors (embeddings) that capture their semantic meaning.

```python
embeddings = OpenAIEmbeddings()
book_review_question_embeddings = embeddings.embed_documents(book_review_questions)
```

### Step 4: Process User Query
When a user query arrives, convert it into an embedding using the same model.

```python
query_embedding = embeddings.embed_query(user_query)
```

### Step 5: Calculate Similarity Scores
Compute cosine similarity between the query embedding and each domain's question embeddings.

```python
book_review_similarity = cosine_similarity([query_embedding], book_review_question_embeddings)
health_fitness_similarity = cosine_similarity([query_embedding], health_fitness_question_embeddings)
# Calculate for all domains...
```

### Step 6: Route to Best Match
Select the domain with the highest similarity score and use its specialized prompt.

```python
max_similarity = max(book_review_similarity, health_fitness_similarity, ...)
if max_similarity == book_review_similarity:
    return book_review_template
```

### Step 7: Generate Response
Feed the selected prompt along with the user query to the LLM to generate a domain-specific response.

```python
chain = RunnablePassthrough() | RunnableLambda(prompt_router) | ChatOpenAI() | StrOutputParser()
response = chain.invoke({"query": user_query})
```

## Advantages

### 1. **Improved Response Quality**
Queries are handled by domain-specific prompts, leading to more accurate and contextually relevant responses.

### 2. **Efficient Resource Utilization**
Instead of maintaining separate models for each domain, you can use a single LLM with multiple specialized prompts.

### 3. **Easy to Extend**
Adding new domains is straightforward—just define new prompts and representative questions.

### 4. **No Additional Training Required**
Unlike training separate classifiers, semantic routing leverages pre-trained embedding models.

### 5. **Transparent and Debuggable**
You can inspect similarity scores to understand why a query was routed to a particular domain.

### 6. **Flexible and Adaptive**
Works well even with queries that don't perfectly match the training examples, thanks to semantic understanding.

## Disadvantages

### 1. **Dependency on Embedding Quality**
The effectiveness heavily relies on the quality of the embedding model. Poor embeddings lead to incorrect routing.

### 2. **Computational Overhead**
Calculating embeddings and similarity scores for every query adds latency, especially with many domains.

### 3. **Limited to Pre-Defined Domains**
Struggles with queries that don't fit neatly into any existing domain or span multiple domains.

### 4. **Embedding API Costs**
Using commercial embedding APIs (like OpenAI) can accumulate costs at scale.

### 5. **Cold Start Problem**
Requires careful selection of representative questions for each domain. Poor question selection leads to misrouting.

### 6. **No Multi-Domain Support**
If a query legitimately belongs to multiple domains, the system will only route to one.

## Practical Tips

### Design Representative Questions Carefully
- Include diverse phrasings and question types for each domain
- Cover edge cases and common variations
- Test with real user queries to identify gaps
- Aim for 10-20 representative questions per domain

### Optimize for Performance
- Cache embeddings for representative questions (they don't change)
- Use batch embedding when processing multiple queries
- Consider using lighter, faster embedding models for real-time applications
- Implement similarity score thresholds to detect out-of-domain queries

### Handle Edge Cases
```python
if max_similarity < THRESHOLD:
    return generic_fallback_template  # Query doesn't fit any domain
```

### Monitor and Iterate
- Log routing decisions and similarity scores
- Track misrouted queries through user feedback
- Regularly update representative questions based on actual usage patterns
- A/B test different prompt formulations

### Consider Hybrid Approaches
- Combine semantic routing with keyword-based filters for certain domains
- Use semantic routing as a first pass, followed by a classifier for ambiguous cases
- Implement multi-level routing for complex domain hierarchies

### Domain Design Best Practices
- Keep domains distinct and non-overlapping where possible
- Avoid domains that are too broad or too narrow
- Consider user intent, not just topic (e.g., "learning about X" vs "troubleshooting X")
- Group related sub-domains under umbrella prompts when they share similar expertise

### Testing Strategy
```python
# Create a test suite with known queries
test_cases = [
    ("What's the best investment strategy?", "personal_finance"),
    ("Review of '1984' by Orwell", "book_review"),
    # Add edge cases and ambiguous queries
]

# Validate routing accuracy
for query, expected_domain in test_cases:
    routed_domain = test_routing(query)
    assert routed_domain == expected_domain
```

## When to Use Semantic Routing

**Good fit for:**
- Systems with clearly defined, distinct domains
- Applications where response quality is more important than latency
- Scenarios with 3-10 different domains (sweet spot)
- Projects with limited training data for domain classification

**Not ideal for:**
- Real-time, latency-critical applications
- Systems with highly overlapping domains
- Applications requiring multi-domain responses
- Scenarios with hundreds of micro-domains

## Conclusion

Semantic routing offers an elegant, maintainable solution for directing queries in multi-domain LLM applications. While it has limitations, its simplicity and effectiveness make it an excellent choice for many production use cases. Start simple, monitor performance, and iterate based on real-world usage patterns.
