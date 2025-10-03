
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





**A context manager = automatic setup and cleanup around a block of code.**
