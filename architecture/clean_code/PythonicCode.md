
# Context Managers in Python — Detailed but Simple Guide

---

## 1. What is a Context Manager?

A **context manager** is Python’s way of saying:

> *“Run some setup code before a block, then always run cleanup code after the block — even if there’s an error.”*

We usually use it with the **`with`** keyword.

---

## 2. Real Life Analogy

Think of **renting a car**:

* **Before driving** → sign contract and get keys (setup)
* **Drive the car** → main work (your code block)
* **After returning** → give back keys, close contract (cleanup)

Even if you had an accident, you must still return the car. Python guarantees cleanup.

---

## 3. How It Works Under the Hood

When Python sees:

```python
with manager as thing:
    # do stuff
```

It does:

1. Call `manager.__enter__()` → runs setup. The return value goes into `thing`.
2. Run the code block.
3. Call `manager.__exit__(exc_type, exc_value, traceback)` → runs cleanup. Always runs.

If there’s an error in the block:

* Python passes info about the error into `__exit__`.
* If `__exit__` returns **True**, the error is swallowed.
* If `__exit__` returns **False** (default), the error continues normally.

---

## 4. Basic Class Example

```python
class MyContext:
    def __enter__(self):
        print("ENTER: setup")
        return "resource"

    def __exit__(self, exc_type, exc_value, traceback):
        print("EXIT: cleanup")

with MyContext() as x:
    print("Inside block with", x)
```

**Output:**

```
ENTER: setup
Inside block with resource
EXIT: cleanup
```

---

## 5. File Handling Example

This is the most common case:

```python
with open("data.txt", "r") as f:
    content = f.read()
# file is closed automatically ✅
```

* `__enter__` → open the file
* `__exit__` → close the file

---

## 6. Function Style with `@contextmanager`

Sometimes writing a whole class is too much. Python has a shortcut: `@contextmanager`.

```python
from contextlib import contextmanager

@contextmanager
def my_cm():
    print("ENTER: setup")
    yield "resource"  # gives value to the with-block
    print("EXIT: cleanup")

with my_cm() as x:
    print("Inside block with", x)
```

**Output:**

```
ENTER: setup
Inside block with resource
EXIT: cleanup
```

### How it works

* Code **before** `yield` = `__enter__`
* Code **after** `yield` = `__exit__`
* The value from `yield` = what `as x` gets

So `@contextmanager` is just a **shorter way** to write the same thing.

---

## 7. Decorator Style with `ContextDecorator`

You can also make a class that acts both as a context manager *and* a decorator.

```python
from contextlib import ContextDecorator

class MyCM(ContextDecorator):
    def __enter__(self):
        print("ENTER")
    def __exit__(self, exc_type, exc_value, tb):
        print("EXIT")

# Use as a context manager
with MyCM():
    print("Work inside")

# Use as a decorator
@MyCM()
def task():
    print("Work in function")

task()
```

**Output:**

```
ENTER
Work inside
EXIT
ENTER
Work in function
EXIT
```

---

## 8. Built-in Helper: `suppress`

Python has ready-to-use context managers. Example: `suppress` to ignore errors.

```python
from contextlib import suppress

with suppress(FileNotFoundError):
    open("missing.txt")  # no crash if file doesn’t exist
```

This is cleaner than `try/except/pass`.

---

## 9. Best Practices

✅ Use context managers whenever resources need cleanup (files, DB, sockets).
✅ Don’t swallow exceptions unless you really mean it.
✅ Use `@contextmanager` for small, simple helpers.
✅ Use `ContextDecorator` if you want to reuse the same setup/cleanup around many functions.

---

## 10. Key Sentence to Remember



# Comprehensions and Assignment Expressions — Beginner Friendly

## 1. Comprehensions

A short way to write loops.

```python
# Normal loop
squares = []
for n in range(5):
    squares.append(n * n)

# List comprehension
squares = [n * n for n in range(5)]
```

Both do the same thing, but the second is shorter.

---

## 2. Assignment Expression (`:=`) — Walrus Operator

The `:=` operator lets you **assign a value inside an expression**.

Think of it as: *“save this result, and use it right away.”*

### Without walrus

```python
import re
pattern = r"(\d+)"
text = "Order123"

result = re.search(pattern, text)
if result:
    print(result.group(1))  # 123
```

### With walrus

```python
import re
pattern = r"(\d+)"
text = "Order123"

if (result := re.search(pattern, text)):
    print(result.group(1))  # 123
```

Here `result` is created **inside the if**.

---

## 3. Combined Example

```python
import re
pattern = r"arn:.*:(\d+):.*"
resources = ["arn:aws:s3:12345:bucket", "arn:aws:s3:67890:bucket"]

ids = {m.group(1) for r in resources if (m := re.match(pattern, r))}
print(ids)  # {'12345', '67890'}
```

* Comprehension builds the set.
* `:=` stores the match as `m` and uses it immediately.

---

## 4. Key Idea

* **Comprehensions** = short loops for lists/sets/dicts.
* **Walrus (`:=`)** = assign + use at the same time.

✅ Great for short, clear code.
⚠ If it looks confusing, use a normal loop instead.


# Python Attributes, Properties, and Methods — Clear Guide

---

## 1. Attributes in Python

* In Python, all attributes are **public by default**.
* Python does not have strict private/protected like Java or C++.
* Instead, it uses **conventions**:

| Syntax   | Meaning (Convention) | Example Access                          |
| -------- | -------------------- | --------------------------------------- |
| `attr`   | Public               | `obj.attr` ✅                            |
| `_attr`  | Internal use only    | `obj._attr` (possible, but discouraged) |
| `__attr` | Name mangling        | Accessed as `obj._ClassName__attr`      |

### Example

```python
class Car:
    def __init__(self):
        self.color = "red"        # public
        self._engine_status = "off"  # private by convention
        self.__secret_code = 1234    # name-mangled

car = Car()
print(car.color)          # red (public)
print(car._engine_status) # off (works, but discouraged)
# print(car.__secret_code)  # ❌ AttributeError
print(car._Car__secret_code) # ✅ 1234 (name-mangled access)
```

🔑 **Rule:** Use a single underscore for private attributes. Avoid double underscores unless you specifically want name-mangling.

---

## 2. Properties

Properties let you **control attribute access** (read/write) with getters and setters.

```python
class Coordinate:
    def __init__(self, lat, lon):
        self.latitude = lat
        self.longitude = lon

    @property
    def latitude(self):
        return self._lat

    @latitude.setter
    def latitude(self, value):
        if not -90 <= value <= 90:
            raise ValueError("Invalid latitude")
        self._lat = value

    @property
    def longitude(self):
        return round(self._lon, 4)

    @longitude.setter
    def longitude(self, value):
        if not -180 <= value <= 180:
            raise ValueError("Invalid longitude")
        self._lon = value
```

Usage:

```python
c = Coordinate(10, 20.123456)
print(c.latitude)      # 10 (getter runs)
print(c.longitude)     # 20.1235 (rounded)

c.latitude = 95        # ❌ Error → setter validation failed
```

🔑 **Explanation:** Assigning `c.latitude = 95` automatically calls the setter. The setter checks if the value is valid; if not, it raises a `ValueError`.

---

## 3. Types of Methods

Python classes support **three main types of methods**:

### a) Instance Methods

* Default type of methods.
* First parameter is `self` (the object instance).
* Work on **one object**.

```python
class Example:
    def greet(self):
        return f"Hello from {self.__class__.__name__}"

obj = Example()
print(obj.greet())  # Hello from Example
```

---

### b) Class Methods

* Declared with `@classmethod`.
* First parameter is `cls` (the class itself).
* Work on the **class as a whole**.

```python
class Example:
    counter = 0

    @classmethod
    def increment(cls):
        cls.counter += 1
        return cls.counter

print(Example.increment())  # 1
print(Example.increment())  # 2
```

---

### c) Static Methods

* Declared with `@staticmethod`.
* Take no `self` or `cls`.
* Behave like plain functions inside the class.

```python
class Example:
    @staticmethod
    def add(a, b):
        return a + b

print(Example.add(2, 3))  # 5
```

---

## 4. Combined Example

```python
class User:
    all_users = []  # class-level attribute

    def __init__(self, name, email):
        self.name = name
        self._email = None
        self.email = email   # triggers property setter
        User.all_users.append(self)

    # Property for email
    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if "@" not in value:
            raise ValueError("Invalid email")
        self._email = value

    # Instance method
    def greet(self):
        return f"Hi, I'm {self.name}"

    # Class method
    @classmethod
    def count(cls):
        return len(cls.all_users)

    # Static method
    @staticmethod
    def is_valid_name(name):
        return name.isalpha()


# Usage
u1 = User("Alice", "alice@example.com")
u2 = User("Bob", "bob@example.com")

print(u1.greet())                  # Instance method → Hi, I'm Alice
print(User.count())                # Class method → 2
print(User.is_valid_name("Bob"))   # Static method → True

print(u1.email)                    # Property getter
u1.email = "new@site.com"          # Property setter with validation
```

---

## 5. Key Takeaways

* **`attr`** = public, **`_attr`** = internal, **`__attr`** = name-mangled.
* **Properties** = control how attributes are read/written (validation, formatting).
* **Instance methods** = work on one object (`self`).
* **Class methods** = work on the class (`cls`).
* **Static methods** = independent helpers inside the class.
* Prefer clarity: use underscores by convention, and properties when you need extra control.


# Creating Classes with a More Compact Syntax — Dataclasses in Python

---

## 1. The Problem with Boilerplate

Traditionally, Python classes require an `__init__` method to initialize attributes:

```python
class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
```

This is repetitive when classes are mostly used to store data.

---

## 2. The `dataclasses` Module

Since **Python 3.7**, the `dataclasses` module makes this easier.

### `@dataclass` Decorator

* Automatically generates `__init__`, `__repr__`, and `__eq__` methods.
* You just declare attributes with type annotations.

```python
from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int

p = Person("Alice", 30)
print(p)  # Person(name='Alice', age=30)
```

Here, `name` and `age` are **instance attributes** → every object has its own separate values.

---

## 3. Class Attributes vs Instance Attributes

* **Class attributes**: Defined directly inside the class body *without type annotations*, or set equal to a value outside `__init__`. These are shared across all instances.
* **Instance attributes**: Declared with type annotations inside a dataclass (or assigned inside `__init__`). Each object gets its own copy.

Example:

```python
class Car:
    wheels = 4  # class attribute (shared)
    
    def __init__(self, color):
        self.color = color  # instance attribute (unique)

car1 = Car("red")
car2 = Car("blue")
print(car1.wheels, car2.wheels)  # both see 4 (shared)
print(car1.color, car2.color)    # red vs blue (different)
```

---

## 4. Mutable Defaults Problem

In dataclasses, **default values for fields are evaluated once, at class definition time.**

So if you do this:

```python
from dataclasses import dataclass

@dataclass
class Team:
    name: str                # instance attribute (unique per object)
    members: list[str] = []  # BAD: one list shared across all instances

team1 = Team("Dev Team")
team2 = Team("QA Team")
team1.members.append("Alice")
print(team2.members)  # ['Alice'] → same list used!
```

⚠ Why this happens:

* `name` is safe → each instance stores its own string.
* `members=[]` creates **one list at class definition**, so all objects point to it. It behaves like a shared class attribute, even though it looks like an instance field.

---

## 5. The Fix — `default_factory`

To ensure each instance gets its own list, use `field(default_factory=...)`.

```python
from dataclasses import dataclass, field

@dataclass
class Team:
    name: str
    members: list[str] = field(default_factory=list)

team1 = Team("Dev Team")
team2 = Team("QA Team")
team1.members.append("Alice")
print(team2.members)  # [] → different lists for each instance
```

👉 `field(default_factory=list)` means: *whenever a new `Team` is created, make a new empty list just for that object.*

So now:

* `name` → separate string for each instance.
* `members` → separate list for each instance.

---

## 6. Post-Initialization with `__post_init__`

If you need validation or adjustments after initialization, use `__post_init__`.

```python
from dataclasses import dataclass

@dataclass
class Product:
    name: str
    price: float

    def __post_init__(self):
        if self.price < 0:
            raise ValueError("Price cannot be negative")
```

---

## 7. Example: R-Trie Node

```python
from dataclasses import dataclass, field

R = 26  # Alphabet size

@dataclass
class RTrieNode:
    size = R  # class attribute, shared by all nodes
    value: int
    next_: list = field(default_factory=lambda: [None] * R)

    def __post_init__(self):
        if len(self.next_) != R:
            raise ValueError("Invalid next_ list length")
```

* `size` → class attribute (shared)
* `value` → instance attribute (different per node)
* `next_` → instance attribute, fresh list created per node

---

## 8. When to Use Dataclasses

✅ Use dataclasses when:

* Your class is mainly a **data container**
* You want compact syntax without boilerplate
* You don’t need complex initialization logic

⚠ Avoid when:

* You need strict type enforcement (dataclasses don’t convert types automatically)
* Your class has heavy validation or logic → write a custom `__init__`

---

## 9. Key Takeaway

* `name: str` in a dataclass = **instance attribute (unique per object)**.
* `members: list[str] = []` without `default_factory` = one shared object (buggy).
* ✅ Use `field(default_factory=...)` for mutable defaults.
* Class attributes (like `size=R`) = explicitly shared.

So: **`name` is not shared. Only mutable defaults behave like shared objects unless you fix them with `default_factory`.**




**A context manager = automatic setup and cleanup around a block of code.**


# Iterable Objects and Sequences in Python

---

## 1. What Does Iterable Mean?

An **iterable** is any Python object that can be used in a `for` loop.

* Built-in examples: `list`, `tuple`, `set`, `dict`.
* You can also create your **own iterable** objects.

Python follows the **iterator protocol** when you do:

```python
for x in myobject:
    ...
```

It checks:

1. Does the object have `__iter__` or `__next__`?
2. If not, is it a sequence with `__len__` and `__getitem__`?
3. If neither → raises `TypeError`.

---

## 2. Creating a Custom Iterable

When you call `iter(obj)`, Python looks for the `__iter__` method.

* `__iter__`: returns an iterator object (often `self`).
* `__next__`: returns the next item or raises `StopIteration` when done.

### Example: DateRangeIterable

```python
from datetime import date, timedelta

class DateRangeIterable:
    def __init__(self, start_date, end_date):
        self.current = start_date
        self.end_date = end_date

    def __iter__(self):
        return self  # the object itself is the iterator

    def __next__(self):
        if self.current > self.end_date:
            raise StopIteration
        today = self.current
        self.current += timedelta(days=1)
        return today

# Usage
for d in DateRangeIterable(date(2023, 1, 1), date(2023, 1, 3)):
    print(d)
```

Output:

```
2023-01-01
2023-01-02
2023-01-03
```

### Problem

Once used, the iterable is **exhausted**:

```python
rng = DateRangeIterable(date(2023,1,1), date(2023,1,2))
for d in rng: print(d)  # works
for d in rng: print(d)  # empty, already exhausted
```

---

## 3. Fixing with Container Iterables

Instead of returning `self` in `__iter__`, return a **fresh iterator** each time. A generator is perfect here.

```python
class DateRangeIterable:
    def __init__(self, start_date, end_date):
        self.start = start_date
        self.end = end_date

    def __iter__(self):
        current = self.start
        while current <= self.end:
            yield current
            current += timedelta(days=1)

# Now works in multiple loops
rng = DateRangeIterable(date(2023,1,1), date(2023,1,2))
for d in rng: print(d)
for d in rng: print(d)
```

👉 This design is called a **container iterable**. Each `for` loop calls `__iter__`, which makes a new generator.

---

## 4. Creating a Sequence

If `__iter__` is missing, Python checks for `__getitem__`. If that works with indices, the object is also iterable.

A **sequence** must:

* Implement `__len__`
* Implement `__getitem__` (with integer indices)

### Example: DateRangeSequence

```python
class DateRangeSequence:
    def __init__(self, start_date, end_date):
        self._dates = []
        current = start_date
        while current <= end_date:
            self._dates.append(current)
            current += timedelta(days=1)

    def __len__(self):
        return len(self._dates)

    def __getitem__(self, index):
        return self._dates[index]

# Usage
rng = DateRangeSequence(date(2023,1,1), date(2023,1,3))
print(rng[0])       # 2023-01-01
print(rng[-1])      # 2023-01-03
for d in rng: print(d)
```

---

## 5. Trade-Offs: Iterable vs Sequence

* **Iterable (with generator)**:

  * Uses less memory (stores only one item at a time).
  * To access nth item, must loop n times → O(n).
* **Sequence (with list)**:

  * Uses more memory (stores all items).
  * Can access any item directly by index → O(1).

This is the classic **memory vs speed trade-off**.

---

## 6. Key Takeaways

* **Iterable protocol**: `__iter__` + `__next__`.
* **Sequence protocol**: `__len__` + `__getitem__`.
* Use **generators/container iterables** for efficiency.
* Use **sequences** when you need random access and indexing.
* Always raise `StopIteration` when iteration is complete.

👉 Rule of thumb: prefer **iterables (generators)** for large data, and **sequences** when you need indexing support.


# Other Properties, Attributes, and Methods in Python

In this guide, we’ll cover three powerful object-oriented features in Python:

* **Container objects** (`__contains__`)
* **Dynamic attributes** (`__getattr__`)
* **Callable objects** (`__call__`)

Each of these relies on Python’s **magic methods** to give objects special behaviors.

---

## 1. Container Objects (`__contains__`)

A **container object** is one that can answer the question: *Does this object contain X?*
This is what allows the use of the `in` keyword.

```python
class Boundaries:
    def __init__(self, x_min, x_max, y_min, y_max):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

    def __contains__(self, coord):
        x, y = coord
        return self.x_min <= x <= self.x_max and self.y_min <= y <= self.y_max

class Grid:
    def __init__(self, limits):
        self.limits = limits

    def __contains__(self, coord):
        return coord in self.limits

# Example usage
grid = Grid(Boundaries(0, 10, 0, 10))
print((5, 5) in grid)   # ✅ True
print((15, 5) in grid)  # ❌ False
```

✨ This makes the code more **Pythonic** and expressive:

```python
if coord in grid:
    print("Inside the grid!")
```

Instead of writing a long conditional manually.

---

## 2. Dynamic Attributes (`__getattr__`)

Python lets you control what happens when an attribute is accessed but not found. This is done with `__getattr__`.

```python
class DynamicAttributes:
    def __init__(self):
        self.existing = "I exist!"

    def __getattr__(self, name):
        if name.startswith("fallback_"):
            return f"Generated attribute for {name}"
        raise AttributeError(f"{name} not found")

obj = DynamicAttributes()
print(obj.existing)           # ✅ "I exist!"
print(obj.fallback_test)      # ✅ "Generated attribute for fallback_test"
# print(obj.unknown)          # ❌ Raises AttributeError
```

🔑 Key points:

* If an attribute is **already defined**, `__getattr__` is not called.
* If it’s missing, Python calls `__getattr__` with the attribute name.
* Always raise **AttributeError** for missing cases — this keeps Python consistent with built-ins like `getattr(obj, "missing", default)`.

📌 **Use cases:**

* Delegating calls in wrappers/proxies
* Avoiding boilerplate for repeated attributes
* On-demand attribute generation

⚠️ **Warning:** Overusing `__getattr__` can make code confusing because attributes may “appear magically.” Use with caution.

---

## 3. Callable Objects (`__call__`)

In Python, even objects can behave like functions. This is possible with the `__call__` magic method.

```python
class CallCount:
    def __init__(self):
        self.counts = {}

    def __call__(self, value):
        self.counts[value] = self.counts.get(value, 0) + 1
        return self.counts[value]

counter = CallCount()
print(counter("apple"))   # 1
print(counter("apple"))   # 2
print(counter("banana"))  # 1
print(counter("apple"))   # 3
```

Here, `counter("apple")` calls `counter.__call__("apple")`.
Each call updates the internal state.

📌 **Use cases:**

* **Memoization** (caching results)
* **Decorators** (wrapping functions)
* **Objects as functions** with internal state

---

## Summary

* `__contains__`: Makes objects usable with `in` for clean membership checks.
* `__getattr__`: Lets objects handle missing attributes dynamically.
* `__call__`: Allows objects to behave like functions and hold state across calls.

Together, these magic methods let you design objects that are **expressive, flexible, and Pythonic**.

# Magic Methods in Python – Summary Cheat Sheet

This document provides a quick overview of the most common **magic methods** (also called *dunder methods*) in Python, their purpose, and how they connect to Python’s special syntax.

---

## 🔑 Key Magic Methods and Their Behaviors

* **Indexing & slicing**

  * `obj[key]` → `__getitem__(key)` → makes objects *subscriptable*
  * `obj[i:j]`, `obj[i:j:k]` → handled by `__getitem__` with slice objects

* **Context Managers**

  * `with obj:` → `__enter__()` and `__exit__()`
  * Used for resources that need setup & cleanup (files, DB connections)

* **Iteration & Sequences**

  * `for i in obj:` → `__iter__()` + `__next__()` (iterator protocol)
  * As fallback: `__len__()` + `__getitem__()` → makes it a *sequence*

* **Dynamic Attributes**

  * `obj.attr` → If not found, Python calls `__getattr__(name)`
  * Useful for proxies, dynamic properties, or fallback attributes

* **Callable Objects**

  * `obj(*args, **kwargs)` → `__call__(*args, **kwargs)`
  * Lets objects behave like functions, often used for decorators or stateful functions

---

## 🧰 Best Practices

* Use **`collections.abc`** base classes:

  * Example: `collections.abc.Iterable`, `collections.abc.Sequence`, etc.
  * These enforce which methods must be implemented and ensure correct typing with `isinstance()`

* Always:

  * Raise `StopIteration` in `__next__()` when iteration is done
  * Raise `AttributeError` in `__getattr__()` for missing attributes
  * Use `__exit__()` for cleanup in context managers, even on exceptions

---

## 🎯 Final Notes

* Magic methods let us integrate *our own classes* seamlessly with Python syntax.
* They enable Pythonic expressions like:

  * `with MyResource(): ...`
  * `if item in my_container:`
  * `for x in my_range:`
* Learning and practicing these will make your code more **natural, compact, and expressive**.

👉 With time, writing clean abstractions using magic methods becomes second nature — even in other languages that don’t support them natively.


