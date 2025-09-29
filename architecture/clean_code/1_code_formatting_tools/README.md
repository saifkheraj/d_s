# Python Annotations and Docstrings

This document explains how annotations are used in Python for type hinting, how they complement docstrings, and how they can be applied step by step with examples.

---

## 1. What Are Annotations?

Annotations are metadata attached to function parameters and return values (and also variables, via PEP-526). They are most often used for **type hinting** but can hold *any valid Python expression*.

Example:

```python
from dataclasses import dataclass

@dataclass
class Point:
    lat: float
    lon: float

def locate(latitude: float, longitude: float) -> Point:
    """Convert latitude and longitude into a Point object."""
    return Point(lat=latitude, lon=longitude)

print(locate.__annotations__)
print(Point.__annotations__, "\n")
print(locate.__doc__)
```

### Output

```python
{'latitude': <class 'float'>, 'longitude': <class 'float'>, 'return': <class '__main__.Point'>}
{'lat': <class 'float'>, 'lon': <class 'float'>}
Convert latitude and longitude into a Point object.
```

* `locate.__annotations__` → shows types of parameters and return type.
* `Point.__annotations__` → shows types of dataclass fields.
* `locate.__doc__` → prints the function’s docstring.

---

## 2. Step-by-Step Evolution of Type Annotations

### Step 1: Generic List

```python
def process_clients(clients: list):
    for c in clients:
        print(c)
```

👉 No information about the contents of the list.

### Step 2: Tuple Structure

```python
def process_clients(clients: list[tuple[int, str]]):
    for client_id, client_name in clients:
        print(f"ID: {client_id}, Name: {client_name}")
```

👉 Slightly clearer, but verbose and harder to read.

### Step 3: Alias for Clarity

```python
from typing import Tuple
Client = Tuple[int, str]

def process_clients(clients: list[Client]):
    for client_id, client_name in clients:
        print(f"ID: {client_id}, Name: {client_name}")
```

👉 `Client` is now a meaningful abstraction. If the structure changes, update it in one place.

### Step 4: `@dataclass` for Richer Semantics

```python
from dataclasses import dataclass
from typing import List

@dataclass
class Client:
    id: int
    name: str

def process_clients(clients: List[Client]) -> None:
    for client in clients:
        print(f"ID: {client.id}, Name: {client.name}")
```

👉 `@dataclass` provides a compact way to define container objects and makes the code easier to extend.

---

## 3. Annotations vs Docstrings

A common question: **Do annotations replace docstrings?**

**Answer: No. They complement each other.**

* **Annotations** are for type information, which can be read by tools.
* **Docstrings** are for human readers, context, and examples.

### Example Without Docstring

```python
def data_from_response(response: dict) -> dict:
    if response["status"] != 200:
        raise ValueError
    return {"data": response["payload"]}
```

👉 We know it takes and returns a dict, but not *what kind of dict*.

### Example With Docstring

```python
def data_from_response(response: dict) -> dict:
    """If the response is OK, return its payload.

    Parameters
    ----------
    response : dict
        A dictionary like::

            {
                "status": 200,        # <int>
                "timestamp": "...",  # ISO datetime string
                "payload": { ... }   # dict with returned data
            }

    Returns
    -------
    dict
        A dictionary like::
            {"data": { ... }}

    Raises
    ------
    ValueError
        If the HTTP status is != 200.
    """
    if response["status"] != 200:
        raise ValueError
    return {"data": response["payload"]}

print(data_from_response.__doc__)
```

👉 Now we:

* Show expected structure of input.
* Document structure of output.
* Mention exceptions.
* Provide examples.

---

## 4. Key Takeaways

* **Annotations** improve readability and allow static analysis tools to catch errors early.
* **Docstrings** give detailed explanations, examples, and edge cases.
* Together, they:

  * Make code self-documenting.
  * Provide valuable input for tests.
  * Support maintainability and scalability.

---

✅ Use annotations for types.
✅ Use docstrings for meaning, context, and examples.
✅ Use both — and inspect them via `__annotations__` and `__doc__` for documentation, tooling, or validation.

# Tooling for Type Consistency and General Validations in Python

# Tooling for Type Consistency and General Validations in Python

This guide introduces **Python tooling** for ensuring type consistency, style compliance, and general code quality. These tools are widely used in professional development to catch bugs early, enforce coding standards, and maintain readable, maintainable code.

---

## 1. Introduction to Tools

Python is dynamically typed and flexible, but this flexibility can lead to hidden bugs if types are misused or if coding standards aren’t followed. To help with this, the Python ecosystem offers a range of tools:

* **mypy** → The most popular tool for **static type checking**. It checks that variables, parameters, and return values match the type hints in the code.
* **pytype** → A type checker from Google. Like mypy, it validates type hints, but it also analyzes the actual runtime behavior of the code to catch possible runtime type errors.
* **pycodestyle** → A simple tool that checks code style against the **PEP-8** standard.
* **flake8** → A wrapper around pycodestyle, plus extra linting and complexity checks.
* **pylint** → A more opinionated and comprehensive static analysis tool. It checks style, naming conventions, unused imports, complexity, and provides a numeric score for your code.

These tools can be run locally during development, or automatically in **Continuous Integration (CI)** pipelines to ensure the entire team adheres to the same standards.

---

## 2. Why Tooling Matters

Writing good code is about more than correct syntax. Code should be:

* **Easy to understand** by peers and new team members.
* **Expressive** of the domain problem it solves.
* **Consistent** in structure and style.

While formatting, indentation, and layout matter, they are not enough. Repetitive checks (like PEP-8 compliance) should be **automated** so reviews can focus on design, clarity, and problem-solving.

### Key principle

> Automate style and type checks, and make the **CI build fail** if they don’t pass.

---

## 3. Checking Type Consistency

Python allows optional type annotations. Tools like mypy and pytype use these annotations to validate type usage and catch errors.

### 3.1 Installing mypy and pytype

```bash
pip install mypy pytype
```

### 3.2 Running mypy

```bash
mypy my_project/
```

Reports type errors based on function signatures and annotations.

### 3.3 Running pytype

```bash
pytype my_project/
```

Performs deeper analysis, simulating runtime behavior.

---

### Example 1: Too Generic Annotation (Iterable)

```python
from typing import Iterable

def broadcast_notification(message: str, relevant_user_emails: Iterable[str]):
    for email in relevant_user_emails:
        print(f"Sending {message} to {email}")

# ❌ Wrong usage – iterates over characters in string
broadcast_notification("welcome", "user1@domain.com")
```

Run with mypy:

```bash
mypy broadcast1.py
```

Output:

```
Success: no issues found in 1 source file
```

⚠️ No issues found, because `Iterable[str]` accepts strings (but this is a bug in logic).

---

### Example 2: Restrictive Annotation (Union of List/Tuple)

```python
from typing import Union, List, Tuple

def broadcast_notification(message: str, relevant_user_emails: Union[List[str], Tuple[str, ...]]):
    for email in relevant_user_emails:
        print(f"Sending {message} to {email}")

# ❌ Wrong usage – string is not allowed now
broadcast_notification("welcome", "user1@domain.com")

# ✅ Correct usage
broadcast_notification("welcome", ["user1@domain.com", "user2@domain.com"])
```

Run with mypy:

```bash
mypy broadcast2.py
```

Output:

```
broadcast2.py:8: error: Argument 2 to "broadcast_notification" has incompatible type "str"; expected "Union[List[str], Tuple[str, ...]]"
Found 1 error in 1 file (checked 1 source file)
```

✅ The bug is now caught.

---

### Example 3: pytype Runtime Awareness

```python
def add_numbers(a: int, b: int) -> int:
    return a + b

# ❌ Wrong call
total = add_numbers("10", "20")
```

Run with pytype:

```bash
pytype main.py
```

Output:

```
File "main.py", line 5, in <module>:
  Function add_numbers was called with wrong argument types [wrong-arg-types]
    Expected: (a: int, b: int)
    Actually passed: (a: str, b: str)
```

✅ pytype interprets runtime behavior and reports the mismatch.

---

## 4. General Validations in Code

Beyond type checks, tools validate code style and enforce standards.

### 4.1 Installing Tools

```bash
pip install pycodestyle flake8 pylint
```

### 4.2 pycodestyle Example

```python
# bad_style.py

def add(a,b): print(a+b)   # no spacing, long line
```

Run:

```bash
pycodestyle bad_style.py
```

Output:

```
bad_style.py:3:11: E231 missing whitespace after ','
bad_style.py:3:19: E701 multiple statements on one line (colon)
```

---

### 4.3 flake8 Example

```python
# utils.py
import os   # unused import

def complex_function(a, b, c, d, e, f, g):
    return sum([a, b, c, d, e, f, g])
```

Run:

```bash
flake8 utils.py
```

Output:

```
utils.py:2:1: F401 'os' imported but unused
utils.py:4:4: R0913: Too many arguments (7/5) (too-many-arguments)
```

---

### 4.4 pylint Example

```python
# models.py
class Client:
    def __init__(self, id, name, email, phone, address, age, active):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.age = age
        self.active = active
```

Run:

```bash
pylint models.py
```

Output:

```
************* Module models
models.py:1:0: C0114: Missing module docstring (missing-module-docstring)
models.py:2:0: C0115: Missing class docstring (missing-class-docstring)
models.py:3:4: R0913: Too many arguments (7/5) (too-many-arguments)
```

✅ Now we know what to fix.

---

## 5. CI/CD Integration

Example GitHub Actions pipeline:

```yaml
name: Lint and Type Check

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install mypy flake8 pylint pycodestyle

      - name: Run mypy
        run: mypy my_project/

      - name: Run flake8
        run: flake8 my_project/

      - name: Run pylint
        run: pylint my_project/
```

If any check fails, the build will fail automatically.

---

## 6. Key Takeaways

* **mypy / pytype** → enforce type correctness.
* **pycodestyle / flake8 / pylint** → enforce style, linting, and complexity rules.
* **CI/CD integration** → ensures team-wide consistency.

✅ Use annotations + mypy/pytype to catch type errors early.
✅ Use style tools to keep the code clean.
✅ Automate everything in CI/CD pipelines.


# Automatic Formatting in Python

This guide introduces tools for **automatic code formatting** in Python. These tools reduce style debates, enforce consistency, and ensure that code reviews focus on the logic and design rather than formatting issues.

---

## 1. Why Automatic Formatting Matters

Even if a team agrees on a style guide, manual enforcement often fails over time. Developers may unintentionally introduce style inconsistencies, and reviewers may waste time pointing out trivial formatting issues.

Automatic formatting solves this problem:

* Eliminates debates about personal style preferences.
* Keeps codebase consistent over time.
* Ensures pull requests highlight only meaningful changes.
* Integrates into CI/CD pipelines for team-wide enforcement.

---

## 2. Key Tools for Auto Formatting

### 2.1 **Black**

* Opinionated and deterministic formatter.
* Limited configuration (only key options like line length).
* Always formats strings with double quotes.
* Enforces a strict subset of PEP-8.
* Ensures consistent diffs in pull requests.

**Install Black:**

```bash
pip install black
```

**Format files:**

```bash
black my_project/
```

**Check without changing files (CI-friendly):**

```bash
black --check my_project/
```

### Example Before Black:

```python
def my_function(param1,param2):
  print('Hello',param1,param2)
```

### Example After Black:

```python
def my_function(param1, param2):
    print("Hello", param1, param2)
```

✅ Consistent spacing, indentation, and string quoting.

---

### 2.2 **YAPF (Yet Another Python Formatter)**

* Developed by Google.
* Highly configurable (style guides can be customized).
* Supports **partial formatting** (specific lines or regions).
* Useful for **legacy codebases** where full reformatting is disruptive.

**Install YAPF:**

```bash
pip install yapf
```

**Format files:**

```bash
yapf -i my_file.py
```

**Format specific lines only:**

```bash
yapf -i --lines 10-20 my_file.py
```

This allows gradual adoption in large projects.

---

## 3. Strategies for Adoption

### 3.1 New Repositories

* Adopt **Black** immediately.
* No history conflicts.
* Enforces consistent formatting from day one.

### 3.2 Legacy Repositories

Options:

1. **Milestone Pull Request**

   * Reformat all files at once.
   * Large diff but ensures consistency going forward.
2. **Rewrite Git History**

   * Apply Black retroactively to all past commits.
   * Cleaner history but requires force-push and team sync.
3. **Use YAPF Incrementally**

   * Apply formatting only to changed lines or files.
   * Lower risk, smoother transition.

---

## 4. Integration into Development Workflow

* **Pre-commit hooks:** Automatically format code before commits.

```bash
pip install pre-commit
pre-commit install
```

Example `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.9.1
    hooks:
      - id: black
```

* **CI/CD pipelines:** Add Black (or YAPF) checks in GitHub Actions, GitLab CI, etc.

GitHub Actions Example:

```yaml
name: Code Formatting

on: [push, pull_request]

jobs:
  black-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install Black
        run: pip install black
      - name: Run Black check
        run: black --check my_project/
```

---

## 5. Key Takeaways

* **Black** → Simple, opinionated, deterministic. Best for new projects.
* **YAPF** → Flexible, customizable, allows partial formatting. Best for legacy projects.
* **Automation** → Use pre-commit hooks and CI pipelines to enforce consistency.

✅ Focus on solving problems, not arguing over code style.
✅ Adopt automatic formatting to keep the codebase clean and maintainable.

