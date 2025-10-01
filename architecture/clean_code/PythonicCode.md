
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

**A context manager = automatic setup and cleanup around a block of code.**
