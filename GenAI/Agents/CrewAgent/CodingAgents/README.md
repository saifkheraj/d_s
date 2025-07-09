# CrewAI Coding Agents

Learn what coding agents are and how to create them with CrewAI for automated code generation and debugging.

## Table of Contents
- [What are Coding Agents?](#what-are-coding-agents)
- [Key Features](#key-features)
- [Getting Started](#getting-started)
- [Code Generation Example](#code-generation-example)
- [Code Debugging Example](#code-debugging-example)
- [Best Practices](#best-practices)
- [Requirements](#requirements)

## What are Coding Agents?

Coding agents are a special type of AI agent that goes beyond simple instruction-following or information gathering. While regular agents might tell you *how* to solve a problem, coding agents actually *solve* the problem by writing, executing, and testing code in real-time.

Think of it this way:
- **Regular Agent**: Finds a cake recipe and tells you the steps
- **Coding Agent**: Actually bakes the cake by writing and executing the recipe

This makes coding agents extremely powerful for:
- Data analysis
- Bug fixing
- Automation tasks
- Computational problem-solving

## Key Features

- **Code Generation**: Write code from natural language descriptions
- **Code Execution**: Run and test the generated code
- **Debugging**: Identify and fix issues in existing code
- **Real-time Problem Solving**: Move from planning to implementation automatically

## Getting Started

### Enabling Code Execution

To enable code execution capabilities in your CrewAI agents, you need to:

1. Set up your LLM
2. Create the agent with `allow_code_execution=True`
3. Assign the LLM to the agent

```python
import os
from crewai import Agent
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize your LLM
llm = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    temperature=0.1,
    api_key=os.environ["ANTHROPIC_API_KEY"]
)

# Create a coding agent with execution capabilities
coding_agent = Agent(
    role="Python Data Analyst",
    goal="Write and execute Python code to solve problems",
    backstory="You are an expert Python programmer with strong analytical skills.",
    allow_code_execution=True,  # This enables the coding capabilities
    llm=llm,  # Assign the LLM to the agent
    verbose=True  # Optional: for detailed output
)
```

> **Important**: By default, `allow_code_execution` is set to `False`. You must explicitly enable it for coding functionality.

## Code Generation Example

### Problem: Calculate Average Age

Instead of manually writing code to calculate the average of a list of ages, you can describe the problem to the agent and let it handle the implementation.

```python
import os
from crewai import Agent, Task, Crew
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the LLM
llm = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    temperature=0.1,
    api_key=os.environ["ANTHROPIC_API_KEY"]
)

# Create the coding agent
coding_agent = Agent(
    role="Python Data Analyst",
    goal="Write and execute Python code to solve problems",
    backstory="You are an expert Python programmer with strong analytical skills.",
    allow_code_execution=True,
    llm=llm,  # Assign the LLM to the agent
    verbose=True  # Optional: for detailed output
)

# Define the task
calculate_average_task = Task(
    description="Write Python code to calculate the average of this list of ages: [23, 35, 31, 29, 40].",
    expected_output="The calculated average age with the code used",
    agent=coding_agent
)

# Create and run the crew
crew = Crew(
    agents=[coding_agent],
    tasks=[calculate_average_task],
    verbose=True  # Optional: for detailed execution logs
)

# Execute the task
result = crew.kickoff()
print(result)
```

### Expected Output
```
The average age is: 31.6

Code executed:
ages = [23, 35, 31, 29, 40]
average_age = sum(ages) / len(ages)
print(f"The average age is: {average_age}")
```

## Code Debugging Example

### Problem: Fix Buggy Code

Coding agents can also debug existing code by identifying issues and providing fixes.

```python
import os
from crewai import Agent, Task, Crew
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the LLM
llm = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    temperature=0.1,
    api_key=os.environ["ANTHROPIC_API_KEY"]
)

# Create the debugging agent
debugging_agent = Agent(
    role="Python Code Debugger",
    goal="Debug and fix Python code issues",
    backstory="You are an expert at identifying and fixing bugs in Python code.",
    allow_code_execution=True,
    llm=llm,  # Assign the LLM to the agent
    verbose=True
)

# Define the debugging task
debug_task = Task(
    description="""
    Debug the following Python code that should calculate squares of numbers:
    
    ```python
    def square_numbers(numbers):
        squares = []
        for num in numbers:
            squares.append(num * num + 1)  # Bug: extra +1
        return squares
    
    numbers = [1, 2, 3, 4, 5]
    result = square_numbers(numbers)
    print(result)
    ```
    
    The code should return [1, 4, 9, 16, 25] but it's giving incorrect results.
    """,
    expected_output="Fixed code with explanation of the bug",
    agent=debugging_agent
)

# Create and run the crew
debug_crew = Crew(
    agents=[debugging_agent],
    tasks=[debug_task],
    verbose=True
)

# Execute the debugging task
result = debug_crew.kickoff()
print(result)
```

### Key Differences: Generation vs. Debugging

| Code Generation | Code Debugging |
|----------------|----------------|
| Starts from scratch | Works with existing code |
| Creates new solutions | Identifies and fixes problems |
| Follows clear instructions | Analyzes and improves code |
| Pure creation | Problem-solving with constraints |

## Advanced Configuration

### Custom LLM Settings

You can customize your LLM configuration for better performance:

```python
# For Claude - More conservative settings
llm = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    temperature=0.1,  # Lower temperature for more deterministic code
    max_tokens=4000,  # Adjust based on your needs
    timeout=60,  # Request timeout in seconds
    max_retries=3,  # Number of retries on failure
)

# For OpenAI - Similar configuration
llm = ChatOpenAI(
    model="gpt-4",
    temperature=0.1,
    max_tokens=4000,
    timeout=60,
    max_retries=3,
)
```

### Multiple Agents with Different LLMs

You can use different LLMs for different agents:

```python
# Claude for complex coding tasks
claude_llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0.1)

# GPT-4 for debugging tasks
openai_llm = ChatOpenAI(model="gpt-4", temperature=0.1)

# Create specialized agents
code_generator = Agent(
    role="Code Generator",
    goal="Generate clean, efficient Python code",
    backstory="Expert at writing new code from requirements",
    allow_code_execution=True,
    llm=claude_llm
)

debugger = Agent(
    role="Code Debugger", 
    goal="Find and fix bugs in existing code",
    backstory="Expert at debugging and code analysis",
    allow_code_execution=True,
    llm=openai_llm
)
```

### Error Handling and Logging

```python
import logging
from crewai import Agent, Task, Crew

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Your crew setup here
    crew = Crew(
        agents=[coding_agent],
        tasks=[task],
        verbose=True
    )
    
    result = crew.kickoff()
    logger.info(f"Task completed successfully: {result}")
    
except Exception as e:
    logger.error(f"Error executing crew: {str(e)}")
    # Handle the error appropriately
```

## Troubleshooting

### Common Issues and Solutions

#### 1. API Key Issues
```bash
# Error: "Authentication failed"
# Solution: Check your API key and environment variables
echo $ANTHROPIC_API_KEY  # Should display your key
```

#### 2. Import Errors
```bash
# Error: "No module named 'crewai'"
pip install --upgrade crewai

# Error: "No module named 'langchain_anthropic'"
pip install langchain-anthropic
```

#### 3. Code Execution Issues
```python
# If code execution fails, check permissions and environment
import sys
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
```

#### 4. Rate Limiting
```python
# Add delays between requests if you hit rate limits
import time

llm = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    temperature=0.1,
    request_timeout=120,  # Longer timeout
    max_retries=5  # More retries
)
```

### Performance Optimization

#### 1. Model Selection by Task Complexity
```python
# For simple coding tasks
simple_llm = ChatAnthropic(model="claude-3-haiku-20240307", temperature=0.1)

# For complex coding tasks
complex_llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0.1)

# For debugging tasks
debug_llm = ChatOpenAI(model="gpt-4", temperature=0.1)
```

#### 2. Task Optimization
```python
# Break complex tasks into smaller subtasks
task1 = Task(
    description="Write a function to read CSV data",
    expected_output="A working CSV reader function",
    agent=coding_agent
)

task2 = Task(
    description="Write a function to process the CSV data from task 1",
    expected_output="A data processing function",
    agent=coding_agent,
    context=[task1]  # Use output from previous task
)
```

### 1. Use Capable Models
For coding tasks, use more powerful models like:
- Claude 3.5 Sonnet
- GPT-4

These models have better coding understanding and are more likely to generate correct, efficient code.

### 2. Clear Task Descriptions
Provide specific, clear descriptions of what you want the agent to accomplish:

```python
# Good: Specific and clear
description = "Write Python code to read a CSV file, calculate the mean of the 'price' column, and save the result to a new file."

# Avoid: Vague and unclear
description = "Do something with data."
```

### 3. Handle Fuzzy Outputs
Since we're working with AI-generated code:
- Review the generated code before using in production
- Test thoroughly with different inputs
- Consider running the task multiple times if results don't meet expectations
- Adjust task descriptions based on output quality

### 4. Iterative Refinement
If the generated code doesn't meet your expectations:
1. Refine your task description
2. Provide more specific requirements
3. Include examples of expected input/output
4. Try running the task again

## Installation & Setup

### 1. Install Required Packages

```bash
pip install crewai
pip install crewai[tools]  # Optional: for additional tools
```

### 2. LLM Configuration

You'll need to configure your LLM provider. Here are examples for popular providers:

#### Option A: Claude (Anthropic)

```bash
pip install anthropic
```

```python
import os
from crewai import Agent, Task, Crew
from langchain_anthropic import ChatAnthropic

# Set your API key
os.environ["ANTHROPIC_API_KEY"] = "your-anthropic-api-key-here"

# Initialize Claude LLM
llm = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    temperature=0.1,
    api_key=os.environ["ANTHROPIC_API_KEY"]
)
```

#### Option B: OpenAI GPT

```bash
pip install openai
```

```python
import os
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI

# Set your API key
os.environ["OPENAI_API_KEY"] = "your-openai-api-key-here"

# Initialize OpenAI LLM
llm = ChatOpenAI(
    model="gpt-4",
    temperature=0.1,
    api_key=os.environ["OPENAI_API_KEY"]
)
```

#### Option C: Using Environment Variables

Create a `.env` file in your project root:

```env
ANTHROPIC_API_KEY=your-anthropic-api-key-here
OPENAI_API_KEY=your-openai-api-key-here
```

Then load it in your Python code:

```python
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file
```

### 3. System Requirements

- Python 3.8+
- CrewAI framework
- LLM provider package (anthropic, openai, etc.)
- API keys for your chosen LLM provider
- Internet connection for API calls

## Example Notebooks

Complete examples are available in Jupyter Notebooks:
- Code Generation Example: `CodingAgent1.ipynb`
- Code Debugging Example: `DebuggingAgent.ipynb`

> **Note**: Notebooks may show pre-executed outputs due to API key constraints. Replace placeholders with your own API keys to run the examples yourself.

## Conclusion

Coding agents transform AI assistants from simple advisors into active problem-solvers. They bridge the gap between understanding a problem and implementing a solution, making them invaluable for:

- Rapid prototyping
- Data analysis automation
- Code debugging and optimization
- Educational programming assistance

By enabling `allow_code_execution=True` and properly configuring your LLM, you unlock the full potential of CrewAI agents to not just think about problems, but to actively solve them through code.

The key to success with coding agents is:
1. **Proper setup**: Configure your LLM and API keys correctly
2. **Clear instructions**: Provide specific, detailed task descriptions
3. **Appropriate models**: Use capable models like Claude 3.5 Sonnet or GPT-4
4. **Iterative refinement**: Adjust and retry based on results

Start with simple examples and gradually build up to more complex use cases as you become familiar with the framework.

## Complete Working Example

Here's a full example you can run immediately (after setting up your API keys):

```python
# complete_example.py
import os
from crewai import Agent, Task, Crew
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv

def main():
    # Load environment variables
    load_dotenv()
    
    # Check if API key is available
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Please set your ANTHROPIC_API_KEY in your .env file")
        return
    
    # Initialize LLM
    llm = ChatAnthropic(
        model="claude-3-5-sonnet-20241022",
        temperature=0.1,
        api_key=os.environ["ANTHROPIC_API_KEY"]
    )
    
    # Create coding agent
    data_analyst = Agent(
        role="Senior Python Developer",
        goal="Write, execute, and debug Python code efficiently",
        backstory="""You are a senior Python developer with expertise in 
        data analysis, debugging, and writing clean, efficient code.""",
        allow_code_execution=True,
        llm=llm,
        verbose=True
    )
    
    # Create tasks
    analysis_task = Task(
        description="""
        Analyze the following sales data and provide insights:
        Sales data: [1500, 2300, 1800, 2100, 2500, 1900, 2200]
        
        1. Calculate the total sales
        2. Find the average sales
        3. Identify the highest and lowest sales
        4. Calculate the growth rate between first and last sale
        
        Write Python code to perform this analysis and display the results.
        """,
        expected_output="Complete analysis with calculations and insights",
        agent=data_analyst
    )
    
    # Create and run crew
    analysis_crew = Crew(
        agents=[data_analyst],
        tasks=[analysis_task],
        verbose=True
    )
    
    print("Starting sales data analysis...")
    result = analysis_crew.kickoff()
    print("\n" + "="*50)
    print("FINAL RESULT:")
    print("="*50)
    print(result)

if __name__ == "__main__":
    main()
```

To run this example:

1. Create a `.env` file with your API key:
   ```
   ANTHROPIC_API_KEY=your-api-key-here
   ```

2. Install dependencies:
   ```bash
   pip install crewai langchain-anthropic python-dotenv
   ```

3. Run the script:
   ```bash
   python complete_example.py
   ```

## Best Practices