**Best Practices for Exception Handling (Summary)**

* **Handle exceptions at the right level:** Keep exception handling consistent with the function’s responsibility. For example, `ConnectionError` should be handled inside the connection logic, not where data is decoded.
* **Do not expose tracebacks to users:** Log detailed errors internally, but show generic error messages like “Something went wrong” to prevent security risks.
* **Avoid empty `except` blocks:** Never silence errors with `pass`; instead, catch specific exceptions and handle them properly (e.g., log, retry, or raise a new one).
* **Catch specific exceptions:** Use targeted exceptions like `KeyError` or `ValueError` instead of a broad `Exception`.
* **Include the original exception:** When re-raising, use `raise NewError(...) from e` to preserve context for debugging.
* **Use `contextlib.suppress()`** explicitly if you need to ignore certain exceptions intentionally.

##  Best Practices for Exception Handling — Python Example

This example covers all 6 best practices:

```python
from contextlib import suppress

class CustomError(Exception):
    pass

def connect():
    raise ConnectionError("Failed to connect")

def decode():
    raise ValueError("Bad data format")

def main():
    try:
        connect()
    except ConnectionError as e:
        print("Retrying connection...")   # ✅ Handle exception at correct level

    try:
        decode()
    except ValueError:
        print("Something went wrong")     # ✅ Generic message, no traceback exposed

    try:
        raise KeyError("Missing key")
    except KeyError as e:
        print(f"Handled specific: {e}")   # ✅ Catch specific exception

    try:
        raise TypeError("Wrong type")
    except TypeError as e:
        raise CustomError("Custom wrapper") from e   # ✅ Include original exception

    with suppress(ZeroDivisionError):               # ✅ Explicitly ignore with suppress()
        1 / 0

    try:
        pass  # ✅ Avoid empty except block
    except Exception:
        pass
```

## 🧠 Using Assertions vs. Try/Except in Python

### 🔹 Key Points

* **Assertions** are for detecting *programming mistakes* or *impossible situations* that should never happen.
* **Exceptions (try/except)** are for handling *expected errors* — things that can go wrong due to user input or environment.
* **Do not wrap `assert` in try/except** to suppress it. Let it fail fast — it signals a logic bug.
* **You may catch AssertionError** only to log or debug internally, not to continue execution.
* **`assert` should not be used for input validation** — always use `raise` for that.
* **Assertions can be disabled** with `python -O`, so don’t rely on them for business logic.

---

### ✅ Example Code

```python
def divide(a, b):
    # Logic-level check (programmer mistake if b == 0)
    assert b != 0, "b should never be zero (check your logic)"
    return a / b


def safe_division(a, b):
    # User-level error handling using try/except
    try:
        result = divide(a, b)
        print(f"Result: {result}")
    except AssertionError as e:
        print(f"⚠️ Developer bug detected: {e}")  # For internal logs only
    except ZeroDivisionError:
        print("❌ User error: Division by zero!")


# --- Test Calls ---
safe_division(10, 2)   # Works fine
safe_division(10, 0)   # AssertionError (developer bug)
```

---

### 🧾 Output

```
Result: 5.0
⚠️ Developer bug detected: b should never be zero (check your logic)
```

---

### 💡 Summary

* Use **`assert`** to check that internal assumptions are correct.
* Use **`raise` + try/except** for expected user or runtime errors.
* Never silence assertion failures — they mean the code logic is broken.
* Fail fast → Fix logic → Deploy cleaner code ✅


## 🧩 Simple Explanation of Namespace Example

Let’s break down the `SimpleNamespace` part clearly 👇

### 🔹 What It’s Doing

In Python, every object has a built-in dictionary called `__dict__` that stores all its attributes.

When we do:

```python
self.__dict__.update(kwargs)
```

it simply **adds all key–value pairs from **``** into the object’s attributes**.

So if we create:

```python
obj = SimpleNamespace(name="Saif", age=30)
```

then inside `__init__`:

* `kwargs = {"name": "Saif", "age": 30}`
* `self.__dict__.update(kwargs)` turns that into → `self.name = "Saif"` and `self.age = 30`

✅ You can now access:

```python
print(obj.name)  # Saif
print(obj.age)   # 30
```

---

### 🔹 Full Example

```python
class SimpleNamespace:
    def __init__(self, **kwargs):
        # assign each keyword argument as an attribute
        self.__dict__.update(kwargs)

# Create an object easily
person = SimpleNamespace(name="Saif", age=30, city="Dubai")

print(person.name)   # Saif
print(person.city)   # Dubai
```

**Output:**

```
Saif
Dubai
```

---

### 💡 Why It’s Simpler

* No extra `@classmethod` or custom builder needed.
* `__dict__.update(kwargs)` copies keys directly as object attributes.
* Clean, short, and follows the **KIS (Keep It Simple)** principle.



main()



