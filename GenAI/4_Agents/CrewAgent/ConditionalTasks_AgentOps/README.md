# CrewAI Conditional Tasks & Smart Multi-Agent Systems

Build intelligent, self-correcting multi-agent systems with conditional task execution that adapt and ensure quality results.

## Table of Contents
- [What are Conditional Tasks?](#what-are-conditional-tasks)
- [Why Use Conditional Tasks?](#why-use-conditional-tasks)
- [Installation & Setup](#installation--setup)
- [Core Concepts](#core-concepts)
- [Complete Example: Event Data Collection](#complete-example-event-data-collection)
- [Advanced Conditional Patterns](#advanced-conditional-patterns)
- [Production Use Cases](#production-use-cases)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Related Guides](#related-guides)

## What are Conditional Tasks?

Conditional tasks are intelligent checkpoints in your multi-agent workflows that execute **only when specific conditions are met**. Think of them as quality control agents that automatically kick in when something isn't quite right.

### Simple Analogy
Imagine you ask someone to buy groceries and bring back "enough food for dinner." A conditional task is like saying: **"If you didn't get enough ingredients, go back to the store and get more."** The task only runs if the condition (not enough food) is true.

### In Multi-Agent Systems
```
Agent 1: Collect Data → Check: Is data sufficient? 
                       ↳ If NO → Agent 2: Collect More Data
                       ↳ If YES → Continue to Next Step
```

## Why Use Conditional Tasks?

### The Problem with Traditional Workflows
- **Agents aren't perfect**: They might miss data, return incomplete results, or fail to meet requirements
- **No quality control**: Workflows continue with insufficient data
- **Manual intervention**: You have to manually check and restart processes

### The Solution: Conditional Intelligence
- **Automatic quality checks**: Built-in validation of results
- **Self-correcting workflows**: Agents automatically retry or fetch more data
- **Reliable outcomes**: Ensure minimum quality standards are met
- **Reduced manual oversight**: Let the system handle common failure scenarios

## Installation & Setup

### 1. Install Required Packages

```bash
pip install crewai
pip install crewai[tools]
pip install pydantic
pip install python-dotenv
```

### 2. For Web Search Capabilities (Optional)

```bash
pip install google-search-results  # For SerperDevTool
```

### 3. LLM Configuration

```python
import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

# Load environment variables
load_dotenv()

# Initialize LLM
llm = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    temperature=0.1,
    api_key=os.environ["ANTHROPIC_API_KEY"]
)
```

### 4. Environment Setup

Create a `.env` file:
```env
ANTHROPIC_API_KEY=your-api-key-here
SERPER_API_KEY=your-serper-api-key-here  # For web search
```

## Core Concepts

### 1. ConditionalTask Structure

```python
from crewai import ConditionalTask

conditional_task = ConditionalTask(
    description="Task description",
    expected_output="Expected output format",
    condition=condition_function,  # Function that returns True/False
    agent=agent_to_execute
)
```

### 2. Condition Functions

Condition functions determine when a conditional task should execute:

```python
def should_execute_task(output):
    """
    Args:
        output: TaskOutput from the previous task
    
    Returns:
        bool: True if conditional task should execute, False otherwise
    """
    # Your condition logic here
    return True  # or False
```

### 3. Data Validation with Pydantic

```python
from pydantic import BaseModel
from typing import List

class DataModel(BaseModel):
    items: List[str]
    count: int

# Use in tasks for structured output
task = Task(
    description="Collect data",
    output_pydantic=DataModel,  # Ensures structured output
    agent=collector_agent
)
```

## Complete Example: Event Data Collection

This example builds a system that collects event data and automatically fetches more if insufficient data is found.

### Step 1: Define Data Models

```python
from pydantic import BaseModel
from typing import List

class EventsData(BaseModel):
    """Structured format for event data"""
    events: List[str]
    
    def __len__(self):
        return len(self.events)
```

### Step 2: Create Specialized Agents

```python
import os
from crewai import Agent
from crewai_tools import SerperDevTool
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv

# Setup
load_dotenv()
llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0.1)

# Initialize web search tool
search_tool = SerperDevTool()

# Data Collection Agent
data_collector = Agent(
    role="Event Data Collector",
    goal="Collect comprehensive event information from reliable sources",
    backstory="""You are an expert at finding and gathering event information. 
    You search thoroughly and provide detailed, accurate event listings.""",
    tools=[search_tool],
    llm=llm,
    verbose=True
)

# Data Quality Analyzer
data_analyzer = Agent(
    role="Data Quality Analyst", 
    goal="Analyze collected data and determine if additional collection is needed",
    backstory="""You are meticulous about data quality and completeness. 
    You ensure that data collection meets specified requirements and standards.""",
    tools=[search_tool],
    llm=llm,
    verbose=True
)

# Summary Creator
summary_creator = Agent(
    role="Event Summary Writer",
    goal="Create clear, engaging summaries of event collections", 
    backstory="""You excel at taking raw event data and crafting compelling, 
    informative summaries that highlight the most important details.""",
    llm=llm,
    verbose=True
)
```

### Step 3: Define Tasks with Conditional Logic

```python
from crewai import Task, ConditionalTask

# Primary data collection task
fetch_task = Task(
    description="""
    Search for and collect information about 8 interesting events happening in New York City.
    
    Requirements:
    - Find diverse types of events (cultural, entertainment, sports, business, etc.)
    - Include event names, dates, and brief descriptions
    - Ensure events are current and upcoming
    - Provide accurate, verified information
    """,
    expected_output="A structured list of exactly 8 events with details",
    output_pydantic=EventsData,
    agent=data_collector
)

# Condition function for data sufficiency
def should_fetch_more_data(output):
    """
    Check if we have enough events collected.
    
    Args:
        output: TaskOutput containing EventsData
        
    Returns:
        bool: True if we need more data (< 8 events), False if sufficient
    """
    events_count = len(output.pydantic.events)
    print(f"📊 Data Quality Check: Found {events_count} events, need 8 minimum")
    
    if events_count < 8:
        print("⚠️  Insufficient data detected - triggering additional collection")
        return True
    else:
        print("✅ Sufficient data collected - proceeding to summary")
        return False

# Conditional task - only runs if we need more data
fetch_more_task = ConditionalTask(
    description="""
    The initial data collection was insufficient. Perform additional searches to find more events.
    
    Current situation: Less than 8 events were found in the first collection.
    Your task: Find additional NYC events to reach the target of 8 total events.
    
    Focus on:
    - Different event categories not covered in the first search
    - Alternative date ranges or venues
    - Niche or specialized events that might have been missed
    """,
    expected_output="Additional events to supplement the original collection",
    condition=should_fetch_more_data,
    agent=data_analyzer
)

# Summary task - runs after data collection is complete
summary_task = Task(
    description="""
    Create an engaging summary of the collected NYC events.
    
    Include:
    - Brief overview of the event variety and appeal
    - Highlight the most interesting or unique events
    - Organize by categories or themes if applicable
    - Make it compelling for people planning to visit NYC
    """,
    expected_output="A well-organized, engaging summary of NYC events",
    agent=summary_creator,
    context=[fetch_task, fetch_more_task]  # Use data from both collection tasks
)
```

### Step 4: Create and Execute the Crew

```python
from crewai import Crew

# Create the intelligent crew
event_crew = Crew(
    agents=[data_collector, data_analyzer, summary_creator],
    tasks=[fetch_task, fetch_more_task, summary_task],
    planning=True,  # Enable intelligent planning
    verbose=True
)

def run_event_collection():
    """Execute the event collection workflow with conditional logic"""
    
    print("🚀 Starting intelligent event collection workflow...")
    print("="*60)
    
    try:
        result = event_crew.kickoff()
        
        print("\n" + "="*60)
        print("🎉 EVENT COLLECTION COMPLETE!")
        print("="*60)
        print(result)
        
        return result
        
    except Exception as e:
        print(f"❌ Error in workflow: {str(e)}")
        return None

# Run the example
if __name__ == "__main__":
    result = run_event_collection()
```

### Understanding the Workflow

```
1. 📥 Data Collector searches for 8 NYC events
   ↓
2. 🔍 Quality Check: Are there 8+ events?
   ├─ YES → Skip to Summary ✅
   └─ NO → Trigger Additional Collection ⚠️
        ↓
3. 🔄 Data Analyzer finds more events  
   ↓
4. ✍️ Summary Creator compiles final results
```

## Advanced Conditional Patterns

### 1. Multiple Condition Checks

```python
def complex_data_validation(output):
    """Multiple validation criteria"""
    events = output.pydantic.events
    
    # Check quantity
    if len(events) < 8:
        print("❌ Not enough events")
        return True
    
    # Check quality - ensure events have sufficient detail
    detailed_events = [e for e in events if len(e.split()) > 5]
    if len(detailed_events) < 6:
        print("❌ Events lack sufficient detail")
        return True
        
    # Check diversity - basic keyword variety check
    keywords = set()
    for event in events:
        keywords.update(event.lower().split())
    
    if len(keywords) < 20:  # Ensure some diversity in event types
        print("❌ Events lack diversity")
        return True
    
    print("✅ All validation criteria met")
    return False

enhanced_conditional_task = ConditionalTask(
    description="Enhance data collection based on multiple quality criteria",
    condition=complex_data_validation,
    agent=data_analyzer
)
```

### 2. Nested Conditional Logic

```python
# First level: Check basic requirements
def basic_validation(output):
    return len(output.pydantic.events) < 5

# Second level: Check advanced requirements  
def advanced_validation(output):
    return len(output.pydantic.events) < 10

basic_collection = ConditionalTask(
    description="Collect basic minimum events",
    condition=basic_validation,
    agent=basic_collector
)

advanced_collection = ConditionalTask(
    description="Collect comprehensive event listing", 
    condition=advanced_validation,
    agent=advanced_collector,
    context=[basic_collection]  # Depends on basic collection
)
```

### 3. Error Recovery Patterns

```python
def error_recovery_condition(output):
    """Check if previous task failed or returned errors"""
    try:
        if hasattr(output, 'pydantic') and output.pydantic:
            return False  # Success case
        else:
            return True   # Need recovery
    except Exception:
        return True       # Error case

recovery_task = ConditionalTask(
    description="Recover from failed data collection using alternative methods",
    condition=error_recovery_condition,
    agent=backup_collector
)
```

### 4. Dynamic Threshold Adjustment

```python
class AdaptiveQualityChecker:
    """Adaptive quality checker that adjusts thresholds based on context"""
    
    def __init__(self, base_threshold=8):
        self.base_threshold = base_threshold
        self.attempt_count = 0
        self.max_attempts = 3
    
    def check_quality(self, output):
        """Dynamic quality checking with adaptive thresholds"""
        
        self.attempt_count += 1
        events_count = len(output.pydantic.events)
        
        # Adjust threshold based on attempts
        if self.attempt_count >= self.max_attempts:
            # Lower threshold after multiple attempts
            threshold = max(5, self.base_threshold - 2)
            print(f"🔄 Attempt {self.attempt_count}: Lowered threshold to {threshold}")
        else:
            threshold = self.base_threshold
        
        if events_count < threshold:
            print(f"⚠️  Need more data: {events_count}/{threshold} events found")
            return True
        
        print(f"✅ Quality threshold met: {events_count}/{threshold} events")
        return False

# Usage
quality_checker = AdaptiveQualityChecker(base_threshold=8)

adaptive_conditional = ConditionalTask(
    description="Collect additional data with adaptive quality thresholds",
    condition=quality_checker.check_quality,
    agent=data_analyzer
)
```

### 5. Time-Based Conditions

```python
import time
from datetime import datetime, timedelta

def time_based_condition(output, max_execution_time=300):
    """Conditional execution based on time constraints"""
    
    # Check if we have a start time stored
    if not hasattr(output, 'start_time'):
        output.start_time = time.time()
    
    elapsed_time = time.time() - output.start_time
    events_count = len(output.pydantic.events)
    
    # If we're running out of time, accept lower quality
    if elapsed_time > max_execution_time:
        print(f"⏰ Time limit reached ({elapsed_time:.1f}s). Accepting current data.")
        return False
    
    # Otherwise, apply normal quality checks
    if events_count < 8:
        print(f"🔄 Time remaining: {max_execution_time - elapsed_time:.1f}s. Collecting more data.")
        return True
    
    return False

time_aware_task = ConditionalTask(
    description="Collect data with time awareness",
    condition=time_based_condition,
    agent=data_analyzer
)
```

## Production Use Cases

### 1. Financial Data Validation

```python
from decimal import Decimal
from typing import Dict, Any

class FinancialData(BaseModel):
    """Financial data model with validation"""
    revenue_figures: List[Decimal]
    profit_margins: List[float]
    market_data: Dict[str, Any]
    
    @validator('profit_margins')
    def validate_margins(cls, v):
        if any(margin < 0 or margin > 1 for margin in v):
            raise ValueError("Profit margins must be between 0 and 1")
        return v

def financial_validation_condition(output):
    """Validate financial data completeness and accuracy"""
    
    try:
        financial_data = output.pydantic
        
        # Check data completeness
        required_fields = ['revenue_figures', 'profit_margins', 'market_data']
        missing_fields = [field for field in required_fields 
                         if not getattr(financial_data, field, None)]
        
        if missing_fields:
            print(f"❌ Missing financial data: {missing_fields}")
            return True
        
        # Check data quality
        if len(financial_data.revenue_figures) < 4:  # Need quarterly data
            print("❌ Insufficient revenue data (need quarterly figures)")
            return True
        
        # Check market data completeness
        required_market_data = ['sector_performance', 'competitor_analysis', 'market_trends']
        missing_market_data = [key for key in required_market_data 
                              if key not in financial_data.market_data]
        
        if missing_market_data:
            print(f"❌ Missing market data: {missing_market_data}")
            return True
        
        print("✅ Financial data validation passed")
        return False
        
    except Exception as e:
        print(f"❌ Financial data validation error: {str(e)}")
        return True

financial_enhancement_task = ConditionalTask(
    description="""
    Enhance financial data collection to meet regulatory and analysis requirements.
    
    Focus on:
    - Complete quarterly revenue figures
    - Accurate profit margin calculations
    - Comprehensive market analysis
    - Competitor benchmarking data
    """,
    condition=financial_validation_condition,
    agent=financial_analyst
)
```

### 2. Content Quality Assurance

```python
import re
from typing import List

class ContentData(BaseModel):
    """Content data model"""
    articles: List[str]
    word_count: int
    readability_score: float
    
    @validator('readability_score')
    def validate_readability(cls, v):
        if v < 0 or v > 100:
            raise ValueError("Readability score must be between 0 and 100")
        return v

def content_quality_condition(output):
    """Check content quality and completeness"""
    
    content_data = output.pydantic
    
    # Check article count
    if len(content_data.articles) < 5:
        print(f"❌ Need more articles: {len(content_data.articles)}/5")
        return True
    
    # Check word count distribution
    word_counts = [len(article.split()) for article in content_data.articles]
    avg_word_count = sum(word_counts) / len(word_counts)
    
    if avg_word_count < 500:
        print(f"❌ Articles too short: average {avg_word_count} words")
        return True
    
    # Check readability
    if content_data.readability_score < 60:
        print(f"❌ Poor readability: {content_data.readability_score}/100")
        return True
    
    # Check for duplicate content
    unique_articles = set(content_data.articles)
    if len(unique_articles) < len(content_data.articles):
        print("❌ Duplicate content detected")
        return True
    
    # Check for keyword diversity
    all_text = ' '.join(content_data.articles).lower()
    unique_words = set(re.findall(r'\b\w+\b', all_text))
    
    if len(unique_words) < 200:  # Expect good vocabulary diversity
        print(f"❌ Limited vocabulary: {len(unique_words)} unique words")
        return True
    
    print("✅ Content quality standards met")
    return False

content_improvement_task = ConditionalTask(
    description="""
    Improve content collection to meet quality standards.
    
    Requirements:
    - Minimum 5 articles with 500+ words each
    - Readability score above 60
    - No duplicate content
    - Rich vocabulary diversity
    - Engaging and informative content
    """,
    condition=content_quality_condition,
    agent=content_creator
)
```

### 3. E-commerce Inventory Management

```python
class InventoryData(BaseModel):
    """Inventory data model"""
    products: List[Dict[str, Any]]
    stock_levels: Dict[str, int]
    pricing_data: Dict[str, float]
    supplier_info: Dict[str, Any]

def inventory_completeness_condition(output):
    """Validate inventory data completeness"""
    
    inventory = output.pydantic
    
    # Check product data completeness
    required_product_fields = ['name', 'sku', 'category', 'description', 'price']
    incomplete_products = []
    
    for product in inventory.products:
        missing_fields = [field for field in required_product_fields 
                         if field not in product or not product[field]]
        if missing_fields:
            incomplete_products.append({
                'sku': product.get('sku', 'unknown'),
                'missing': missing_fields
            })
    
    if incomplete_products:
        print(f"❌ Incomplete product data: {len(incomplete_products)} products")
        return True
    
    # Check stock level data
    products_with_stock = set(product['sku'] for product in inventory.products)
    stock_data_skus = set(inventory.stock_levels.keys())
    
    missing_stock_data = products_with_stock - stock_data_skus
    if missing_stock_data:
        print(f"❌ Missing stock data for {len(missing_stock_data)} products")
        return True
    
    # Check for low stock items
    low_stock_items = [sku for sku, level in inventory.stock_levels.items() 
                      if level < 10]
    
    if len(low_stock_items) > len(inventory.products) * 0.3:  # More than 30% low stock
        print(f"⚠️  High number of low-stock items: {len(low_stock_items)}")
        return True
    
    # Check supplier information
    if not inventory.supplier_info or len(inventory.supplier_info) < 3:
        print("❌ Insufficient supplier information")
        return True
    
    print("✅ Inventory data validation passed")
    return False

inventory_enhancement_task = ConditionalTask(
    description="""
    Enhance inventory data collection and validation.
    
    Tasks:
    - Complete missing product information
    - Update stock levels for all products
    - Gather supplier contact and pricing information
    - Identify and flag low-stock items
    - Validate pricing data consistency
    """,
    condition=inventory_completeness_condition,
    agent=inventory_manager
)
```

## Best Practices

### 1. Clear Condition Logic

```python
# ✅ Good: Clear, descriptive condition
def needs_more_financial_data(output):
    """Check if financial analysis has sufficient data points"""
    data_points = len(output.pydantic.financial_metrics)
    required_minimum = 10
    
    if data_points < required_minimum:
        print(f"Need {required_minimum - data_points} more financial metrics")
        return True
    return False

# ❌ Avoid: Unclear condition logic
def check_stuff(output):
    return len(output.pydantic.stuff) < 5  # What stuff? What's the threshold based on?
```

### 2. Structured Output Validation

```python
from pydantic import BaseModel, Field, validator
from typing import List, Optional

class QualityEventData(BaseModel):
    events: List[str] = Field(..., min_items=1, description="List of event descriptions")
    total_count: int = Field(..., ge=0, description="Total number of events")
    data_quality_score: Optional[float] = Field(None, ge=0, le=1, description="Quality score 0-1")
    
    @validator('events')
    def validate_event_quality(cls, v):
        """Ensure each event has minimum detail"""
        for event in v:
            if len(event.split()) < 3:
                raise ValueError(f"Event description too short: {event}")
        return v
    
    @validator('total_count')
    def validate_count_matches(cls, v, values):
        """Ensure count matches actual events"""
        if 'events' in values and v != len(values['events']):
            raise ValueError("Count doesn't match events list length")
        return v
```

### 3. Informative Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def comprehensive_validation(output):
    """Well-logged validation with detailed feedback"""
    events = output.pydantic.events
    event_count = len(events)
    
    logger.info(f"🔍 Validating data collection: {event_count} events found")
    
    # Check minimum threshold
    min_required = 8
    if event_count < min_required:
        logger.warning(f"⚠️  Below minimum threshold: {event_count}/{min_required}")
        return True
    
    # Check for duplicate events
    unique_events = set(events)
    if len(unique_events) < event_count:
        logger.warning(f"⚠️  Duplicate events detected: {event_count - len(unique_events)} duplicates")
        return True
    
    # Check event detail quality
    avg_length = sum(len(event.split()) for event in events) / event_count
    if avg_length < 6:
        logger.warning(f"⚠️  Events lack detail: average {avg_length:.1f} words per event")
        return True
    
    logger.info("✅ All validation checks passed")
    return False
```

### 4. Performance Optimization

```python
# Cache validation results to avoid redundant checks
from functools import lru_cache

@lru_cache(maxsize=128)
def cached_validation(output_hash):
    """Cache validation results for identical outputs"""
    # Implementation would go here
    pass

def optimized_condition(output):
    """Use caching for expensive validation operations"""
    # Create a hash of the output for caching
    output_hash = hash(str(output.pydantic.dict()))
    return cached_validation(output_hash)
```

### 5. Graceful Degradation

```python
def graceful_condition(output, max_attempts=3):
    """Implement graceful degradation for conditional tasks"""
    
    # Track attempts (in real implementation, store this persistently)
    attempt_count = getattr(output, '_attempt_count', 0)
    output._attempt_count = attempt_count + 1
    
    events_count = len(output.pydantic.events)
    base_threshold = 8
    
    # Adjust expectations based on attempts
    if attempt_count >= max_attempts:
        adjusted_threshold = max(3, base_threshold - attempt_count)
        print(f"🔄 Final attempt: accepting {adjusted_threshold}+ events")
        return events_count < adjusted_threshold
    
    # Normal threshold for early attempts
    if events_count < base_threshold:
        print(f"⚠️  Attempt {attempt_count}: need more data ({events_count}/{base_threshold})")
        return True
    
    print(f"✅ Quality threshold met on attempt {attempt_count}")
    return False
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Condition Function Not Triggering

```python
# Problem: Condition always returns False
def debug_condition(output):
    print(f"DEBUG: Output type: {type(output)}")
    print(f"DEBUG: Has pydantic attr: {hasattr(output, 'pydantic')}")
    
    if hasattr(output, 'pydantic'):
        print(f"DEBUG: Pydantic data: {output.pydantic}")
        return len(output.pydantic.events) < 8
    else:
        print("DEBUG: No pydantic data found")
        return True  # Trigger task if no structured data
```

#### 2. Pydantic Validation Errors

```python
# Problem: Output doesn't match expected Pydantic model
from pydantic import ValidationError

def safe_condition(output):
    try:
        events = output.pydantic.events
        return len(events) < 8
    except (AttributeError, ValidationError) as e:
        print(f"Validation error: {e}")
        return True  # Trigger conditional task to fix data
```

#### 3. Infinite Loops in Conditional Tasks

```python
# Problem: Conditional task keeps triggering itself
def loop_safe_condition(output, max_attempts=3):
    """Prevent infinite loops with attempt tracking"""
    
    # Track attempts (you might store this in a class or external state)
    attempts = getattr(output, 'collection_attempts', 0)
    
    if attempts >= max_attempts:
        print(f"⚠️  Max attempts reached ({max_attempts}), proceeding with available data")
        return False
    
    if len(output.pydantic.events) < 8:
        print(f"Attempt {attempts + 1}/{max_attempts}: Need more data")
        # Increment attempt counter
        output.collection_attempts = attempts + 1
        return True
    
    return False
```

#### 4. Task Dependencies Issues

```python
# Problem: Conditional task doesn't have access to previous results
summary_task = Task(
    description="Summarize all collected events",
    agent=summary_agent,
    context=[fetch_task, fetch_more_task],  # Include both collection tasks
    expected_output="Complete event summary"
)
```

#### 5. Complex Condition Logic

```python
# Problem: Overly complex condition functions
class ConditionManager:
    """Manage complex conditional logic"""
    
    def __init__(self, min_items=8, quality_threshold=0.8):
        self.min_items = min_items
        self.quality_threshold = quality_threshold
        self.validators = []
    
    def add_validator(self, validator_func):
        """Add a validation function"""
        self.validators.append(validator_func)
    
    def evaluate(self, output):
        """Evaluate all conditions"""
        
        results = []
        for validator in self.validators:
            try:
                result = validator(output)
                results.append(result)
            except Exception as e:
                print(f"Validator error: {e}")
                results.append(True)  # Assume needs improvement on error
        
        # Return True if any validator indicates improvement needed
        needs_improvement = any(results)
        
        if needs_improvement:
            failed_checks = sum(results)
            print(f"⚠️  {failed_checks}/{len(results)} validation checks failed")
        else:
            print("✅ All validation checks passed")
        
        return needs_improvement

# Usage
condition_manager = ConditionManager()
condition_manager.add_validator(lambda x: len(x.pydantic.events) < 8)
condition_manager.add_validator(lambda x: any(len(e.split()) < 5 for e in x.pydantic.events))

manageable_conditional = ConditionalTask(
    description="Improve data based on multiple criteria",
    condition=condition_manager.evaluate,
    agent=data_improver
)
```

## Related Guides

### 🔧 [CrewAI Coding Agents Guide](./CrewAI-Coding-Agents-README.md)
**Build agents that write, execute, and debug code**
- Code generation from natural language
- Automated debugging and error fixing
- Advanced execution patterns (async, batch processing)
- **When to use**: For data analysis, automation, and code generation tasks

### 📊 [Testing & Monitoring Guide](./CrewAI-Testing-Monitoring-README.md)
**Ensure reliability with comprehensive testing and monitoring**
- Automated testing frameworks with scoring
- Real-time monitoring with AgentOps
- Production deployment strategies
- **When to use**: Before production deployment and ongoing operations

### 🚀 [Advanced Multi-Agent Patterns](./CrewAI-Advanced-Patterns-README.md)
**Master complex multi-agent workflows and architectures**
- Hierarchical agent structures
- Cross-crew communication
- Scalable agent orchestration
- **When to use**: For enterprise-scale multi-agent systems

---

## Conclusion

Conditional tasks transform your multi-agent systems from simple linear workflows into intelligent, adaptive processes. They provide:

- **Automatic Quality Control**: Built-in validation and correction
- **Resilient Workflows**: Handle incomplete or failed tasks gracefully  
- **Reduced Manual Oversight**: Let the system self-correct common issues
- **Flexible Execution**: Adapt to different data conditions and requirements

### Key Success Factors

1. **Clear Condition Logic**: Write explicit, well-documented condition functions
2. **Structured Data**: Use Pydantic models for consistent data validation
3. **Comprehensive Logging**: Track workflow decisions for debugging
4. **Graceful Degradation**: Handle edge cases and prevent infinite loops
5. **Testing**: Validate your conditional logic with various scenarios

Start with simple conditions and gradually build more sophisticated validation logic as your system requirements grow. Remember: the goal is to make your agents not just intelligent, but **reliable**.

### Getting Started Checklist

**🚀 Quick Start (10 minutes):**
- [ ] Install CrewAI and dependencies
- [ ] Run the [Event Data Collection example](#complete-example-event-data-collection)
- [ ] Modify the condition function for your use case

**📈 Intermediate (30 minutes):**
- [ ] Implement [multiple validation criteria](#multiple-condition-checks)
- [ ] Add structured data models with Pydantic
- [ ] Test edge cases and error scenarios

**🏗️ Production Ready:**
- [ ] Add comprehensive logging and monitoring
- [ ] Implement graceful degradation patterns
- [ ] Create production-specific validation rules
- [ ] Set up automated testing for conditional logic

**Ready to build your first self-correcting workflow?** Start with the complete example above and customize it for your specific quality control needs. Your multi-agent systems will thank you for the reliability! 🎉