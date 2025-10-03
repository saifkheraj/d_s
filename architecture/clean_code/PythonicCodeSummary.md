# Python Concepts Reference Table

## Context Managers

| Aspect | Details |
|--------|---------|
| **Purpose** | Automatic setup and cleanup around code blocks |
| **Syntax** | `with manager as thing:` |
| **How to Implement (Class)** | Define `__enter__()` and `__exit__(exc_type, exc_value, traceback)` |
| **How to Implement (Function)** | Use `@contextmanager` decorator with `yield` |
| **Use Cases** | File handling, database connections, locks, resource management |
| **Code Snippet** | ```python<br>from contextlib import contextmanager<br><br>@contextmanager<br>def my_cm():<br>    print("Setup")<br>    yield "resource"<br>    print("Cleanup")<br><br>with my_cm() as x:<br>    print(f"Using {x}")``` |
| **Key Point** | Cleanup always runs, even on errors |

---

## List/Set/Dict Comprehensions

| Aspect | Details |
|--------|---------|
| **Purpose** | Concise way to create collections from loops |
| **Syntax** | `[expr for item in iterable if condition]` |
| **Types** | List `[]`, Set `{}`, Dict `{k:v}`, Generator `()` |
| **Use Cases** | Transforming lists, filtering data, creating mappings |
| **Code Snippet** | ```python<br># List comprehension<br>squares = [n**2 for n in range(5)]<br><br># Dict comprehension<br>square_dict = {n: n**2 for n in range(5)}<br><br># Set comprehension<br>unique = {x for x in [1,2,2,3]}``` |
| **Key Point** | More readable than traditional loops for simple operations |

---

## Walrus Operator (`:=`)

| Aspect | Details |
|--------|---------|
| **Purpose** | Assign and use value in same expression |
| **Syntax** | `(var := expression)` |
| **Use Cases** | Avoiding repeated function calls, combining assignment with conditionals |
| **Code Snippet** | ```python<br>import re<br><br># Without walrus<br>match = re.search(r'\d+', text)<br>if match:<br>    print(match.group())<br><br># With walrus<br>if (match := re.search(r'\d+', text)):<br>    print(match.group())``` |
| **Key Point** | Reduces code duplication, especially in comprehensions and conditions |

---

## Attributes & Access Control

| Aspect | Details |
|--------|---------|
| **Public** | `self.attr` - Accessible everywhere |
| **Private (Convention)** | `self._attr` - Internal use (not enforced) |
| **Name Mangling** | `self.__attr` - Becomes `_ClassName__attr` |
| **Use Cases** | Encapsulation, internal state management |
| **Code Snippet** | ```python<br>class Example:<br>    def __init__(self):<br>        self.public = 1<br>        self._internal = 2<br>        self.__private = 3<br><br>obj = Example()<br>print(obj.public)  # 1<br>print(obj._internal)  # 2 (discouraged)<br>print(obj._Example__private)  # 3``` |
| **Key Point** | Python relies on conventions, not strict enforcement |

---

## Properties

| Aspect | Details |
|--------|---------|
| **Purpose** | Control attribute access with getter/setter logic |
| **Syntax** | `@property` for getter, `@attr.setter` for setter |
| **Use Cases** | Validation, computed attributes, read-only fields |
| **Code Snippet** | ```python<br>class Circle:<br>    def __init__(self, radius):<br>        self._radius = radius<br><br>    @property<br>    def radius(self):<br>        return self._radius<br><br>    @radius.setter<br>    def radius(self, value):<br>        if value < 0:<br>            raise ValueError("Negative!")<br>        self._radius = value<br><br>c = Circle(5)<br>c.radius = 10  # setter called``` |
| **Key Point** | Access like an attribute, but with method logic |

---

## Method Types

| Type | Decorator | First Parameter | Access | Use Case |
|------|-----------|-----------------|--------|----------|
| **Instance** | None | `self` | `obj.method()` | Work with instance data |
| **Class** | `@classmethod` | `cls` | `Class.method()` | Factory methods, class-level operations |
| **Static** | `@staticmethod` | None | `Class.method()` | Utility functions related to class |

**Code Snippet:**
```python
class Example:
    count = 0
    
    def instance_method(self):
        return f"Instance: {self}"
    
    @classmethod
    def class_method(cls):
        cls.count += 1
        return cls.count
    
    @staticmethod
    def static_method(x, y):
        return x + y
```

---

## Dataclasses

| Aspect | Details |
|--------|---------|
| **Purpose** | Reduce boilerplate for data-holding classes |
| **Syntax** | `@dataclass` decorator |
| **Auto-Generated** | `__init__`, `__repr__`, `__eq__` |
| **Mutable Defaults** | Use `field(default_factory=list)` for lists/dicts |
| **Use Cases** | Configuration objects, DTOs, simple data containers |
| **Code Snippet** | ```python<br>from dataclasses import dataclass, field<br><br>@dataclass<br>class Person:<br>    name: str<br>    age: int<br>    hobbies: list = field(default_factory=list)<br><br>    def __post_init__(self):<br>        if self.age < 0:<br>            raise ValueError("Invalid age")<br><br>p = Person("Alice", 30)``` |
| **Key Point** | Always use `default_factory` for mutable defaults |

---

## Iterables

| Aspect | Details |
|--------|---------|
| **Purpose** | Objects that can be looped over |
| **Methods Required** | `__iter__()` returns iterator with `__next__()` |
| **Use Cases** | Custom data structures, lazy evaluation |
| **Code Snippet** | ```python<br>class Counter:<br>    def __init__(self, max):<br>        self.max = max<br><br>    def __iter__(self):<br>        n = 0<br>        while n < self.max:<br>            yield n<br>            n += 1<br><br>for i in Counter(3):<br>    print(i)  # 0, 1, 2``` |
| **Key Point** | Use generators in `__iter__()` for reusable iterables |

---

## Sequences

| Aspect | Details |
|--------|---------|
| **Purpose** | Ordered collections with indexing |
| **Methods Required** | `__len__()` and `__getitem__(index)` |
| **Use Cases** | Custom list-like objects, indexed access |
| **Code Snippet** | ```python<br>class MySequence:<br>    def __init__(self, data):<br>        self._data = data<br><br>    def __len__(self):<br>        return len(self._data)<br><br>    def __getitem__(self, index):<br>        return self._data[index]<br><br>seq = MySequence([1, 2, 3])<br>print(seq[1])  # 2<br>print(len(seq))  # 3``` |
| **Key Point** | Supports indexing, slicing, and `len()` |

---

## Container Objects (`__contains__`)

| Aspect | Details |
|--------|---------|
| **Purpose** | Enable `in` operator for membership testing |
| **Method** | `__contains__(self, item)` returns `True`/`False` |
| **Use Cases** | Custom collections, domain-specific membership checks |
| **Code Snippet** | ```python<br>class NumberRange:<br>    def __init__(self, start, end):<br>        self.start = start<br>        self.end = end<br><br>    def __contains__(self, num):<br>        return self.start <= num <= self.end<br><br>r = NumberRange(1, 10)<br>print(5 in r)  # True<br>print(15 in r)  # False``` |
| **Key Point** | Makes code more Pythonic with `if item in container:` |

---

## Dynamic Attributes (`__getattr__`)

| Aspect | Details |
|--------|---------|
| **Purpose** | Handle missing attribute access |
| **Method** | `__getattr__(self, name)` called when attribute not found |
| **Use Cases** | Proxies, delegation, fallback values |
| **Code Snippet** | ```python<br>class Dynamic:<br>    def __init__(self):<br>        self.real = "exists"<br><br>    def __getattr__(self, name):<br>        if name.startswith("auto_"):<br>            return f"Generated: {name}"<br>        raise AttributeError(name)<br><br>obj = Dynamic()<br>print(obj.real)  # exists<br>print(obj.auto_test)  # Generated: auto_test``` |
| **Key Point** | Only called when attribute doesn't exist; raise `AttributeError` for invalid names |

---

## Callable Objects (`__call__`)

| Aspect | Details |
|--------|---------|
| **Purpose** | Make objects callable like functions |
| **Method** | `__call__(self, *args, **kwargs)` |
| **Use Cases** | Decorators, stateful functions, memoization |
| **Code Snippet** | ```python<br>class Multiplier:<br>    def __init__(self, factor):<br>        self.factor = factor<br><br>    def __call__(self, x):<br>        return x * self.factor<br><br>times_three = Multiplier(3)<br>print(times_three(5))  # 15<br>print(times_three(10))  # 30``` |
| **Key Point** | Objects with state that can be called like functions |

---

## Magic Methods Quick Reference

| Syntax | Magic Method | Purpose |
|--------|--------------|---------|
| `obj[key]` | `__getitem__(key)` | Indexing and slicing |
| `len(obj)` | `__len__()` | Get length |
| `with obj:` | `__enter__()`, `__exit__()` | Context management |
| `for i in obj:` | `__iter__()`, `__next__()` | Iteration |
| `item in obj` | `__contains__(item)` | Membership test |
| `obj.attr` (missing) | `__getattr__(name)` | Dynamic attributes |
| `obj(args)` | `__call__(*args)` | Callable objects |
| `str(obj)` | `__str__()` | String representation |
| `repr(obj)` | `__repr__()` | Developer representation |

---

## Memory vs Speed Trade-offs

| Approach | Memory | Speed | When to Use |
|----------|--------|-------|-------------|
| **Generator/Iterator** | Low (one item at a time) | Slower for random access | Large datasets, streaming data |
| **Sequence/List** | High (stores all items) | Fast random access O(1) | Need indexing, small datasets |

---

## Best Practices Summary

✅ **Use context managers** for resource management  
✅ **Use `@contextmanager`** for simple cases  
✅ **Use `default_factory`** in dataclasses for mutable defaults  
✅ **Use single underscore `_`** for private attributes  
✅ **Raise `StopIteration`** when iteration complete  
✅ **Raise `AttributeError`** in `__getattr__` for missing attributes  
✅ **Use comprehensions** for simple transformations  
✅ **Use walrus operator** to avoid repeated calculations  
✅ **Prefer generators** for memory efficiency  
✅ **Use properties** for validation and computed attributes
