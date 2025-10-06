# Python Quick Reference 

---

## 📦 Context Managers

**What it does:** Automatically runs cleanup code (even if errors happen)

**Why:** Never forget to close files or release resources

### Simple way with `@contextmanager`:
```python
from contextlib import contextmanager

@contextmanager
def my_resource():
    print("Opening resource")
    yield "resource"              # Give this to the 'with' block
    print("Closing resource")     # Always runs!

with my_resource() as r:
    print(f"Using {r}")
```

### Real example:
```python
# ❌ BAD - might not close if error
f = open('file.txt')
data = f.read()
f.close()

# ✅ GOOD - always closes
with open('file.txt') as f:
    data = f.read()
```

---

## 🔄 Comprehensions

**What it does:** Create lists/dicts/sets in one line

**Why:** Shorter and clearer than loops

```python
# Old way
squares = []
for n in range(5):
    squares.append(n**2)

# New way
squares = [n**2 for n in range(5)]

# With condition
evens = [n for n in range(10) if n % 2 == 0]

# Dict comprehension
square_dict = {n: n**2 for n in range(5)}

# Set comprehension (removes duplicates)
unique = {x for x in [1, 2, 2, 3]}  # {1, 2, 3}
```

---

## 🎯 Walrus Operator `:=`

**What it does:** Assign and use a value in the same line

**Why:** Avoid calling the same thing twice

```python
# ❌ Calling len() twice
if len(my_list) > 0:
    print(f"Length: {len(my_list)}")

# ✅ Calculate once, use twice
if (n := len(my_list)) > 0:
    print(f"Length: {n}")
```

**Common use with regex:**
```python
if (match := re.search(r'\d+', text)):
    print(match.group())
```

---

## 🔒 Attributes - Public vs Private

**What it does:** Shows which attributes are meant for users vs internal use

```python
class BankAccount:
    def __init__(self):
        self.owner = "Alice"      # Public: anyone can use
        self._balance = 1000      # Internal: "please don't touch"
        self.__pin = 1234         # Private: really hidden
```

| Style | When to use |
|-------|-------------|
| `self.name` | Normal attributes everyone can use |
| `self._name` | Internal use only (convention, not enforced) |
| `self.__name` | Really private (Python hides it) |

---

## 🎛️ Properties

**What it does:** Attributes with validation or logic

**Why:** Control what happens when reading/writing

```python
class Person:
    def __init__(self, age):
        self._age = age
    
    @property
    def age(self):
        """Read the age"""
        return self._age
    
    @age.setter
    def age(self, value):
        """Write the age with validation"""
        if value < 0:
            raise ValueError("Age can't be negative!")
        self._age = value

# Use like normal attribute
person = Person(25)
print(person.age)       # Calls @property
person.age = 30         # Calls @age.setter
person.age = -5         # Error! Validation runs
```

**When to use:**
- Validation (check values before saving)
- Computed values (calculate on-the-fly)
- Read-only attributes (no setter)

---

## 🛠️ Method Types

### The KEY question: Do I create an object first, or call directly?

```python
class Pizza:
    def __init__(self, size, toppings):
        self.size = size
        self.toppings = toppings
    
    # 1️⃣ INSTANCE METHOD
    # ⚠️ MUST create object first
    def describe(self):
        return f"{self.size} inch pizza with {self.toppings}"
    
    # 2️⃣ CLASS METHOD
    # ✅ Call directly on class
    @classmethod
    def margherita(cls, size):
        return cls(size, ['mozzarella', 'tomato', 'basil'])
    
    # 3️⃣ STATIC METHOD
    # ✅ Call directly on class
    @staticmethod
    def is_valid_size(size):
        return size in [8, 10, 12, 14, 16]
```

### How to use:

```python
# ❌ WRONG - No object exists yet!
# Pizza.describe()  # ERROR

# ✅ Instance method - create object FIRST
pizza = Pizza(12, ['pepperoni'])
pizza.describe()

# ✅ Class method - call directly
marg = Pizza.margherita(14)      # Returns new Pizza object

# ✅ Static method - call directly  
Pizza.is_valid_size(10)          # Returns True/False
```

### Quick guide:

| Method Type | Create object first? | Returns what? | Use for |
|-------------|---------------------|---------------|---------|
| Instance | ✅ Yes | Any value | Using object's data |
| @classmethod | ❌ No | Usually new object | Creating objects differently |
| @staticmethod | ❌ No | Any value | Helper functions |

---

## 📋 Dataclasses

**What it does:** Auto-generates `__init__`, `__repr__`, `__eq__` for you

**Why:** Less typing, fewer bugs

```python
# Without dataclass
class PersonOld:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __repr__(self):
        return f"Person(name={self.name}, age={self.age})"

# With dataclass
from dataclasses import dataclass, field

@dataclass
class Person:
    name: str
    age: int
    hobbies: list = field(default_factory=list)  # ⚠️ Must use for lists!
    
    def __post_init__(self):
        if self.age < 0:
            raise ValueError("Age can't be negative")

p = Person("Alice", 30)
print(p)  # Nice automatic printing
```

**⚠️ Important:** Always use `field(default_factory=list)` for mutable defaults

---

## 🔁 Iterables

**What it does:** Makes your object work in `for` loops

```python
class Countdown:
    def __init__(self, start):
        self.start = start
    
    def __iter__(self):
        n = self.start
        while n > 0:
            yield n
            n -= 1

# Usage
for num in Countdown(5):
    print(num)  # 5, 4, 3, 2, 1

numbers = list(Countdown(3))  # [3, 2, 1]
```

**When to use:** Custom collections, lazy data loading

---

## 📚 Sequences

**What it does:** Makes your object work like a list (indexing, `len()`)

```python
class Playlist:
    def __init__(self, songs):
        self._songs = songs
    
    def __len__(self):
        return len(self._songs)
    
    def __getitem__(self, index):
        return self._songs[index]

# Usage
playlist = Playlist(["Song A", "Song B", "Song C"])
print(len(playlist))      # 3
print(playlist[0])        # "Song A"
print(playlist[1:3])      # ["Song B", "Song C"]
```

---

## 🎯 Useful Magic Methods

### `__contains__` - Makes `in` work

```python
class AgeRange:
    def __init__(self, min_age, max_age):
        self.min = min_age
        self.max = max_age
    
    def __contains__(self, age):
        return self.min <= age <= self.max

teens = AgeRange(13, 19)
print(15 in teens)  # True
print(25 in teens)  # False
```

### `__getattr__` - Handle missing attributes

```python
class Config:
    def __init__(self):
        self.debug = True
    
    def __getattr__(self, name):
        if name.startswith("enable_"):
            return False  # Default for all 'enable_' settings
        raise AttributeError(f"No config: {name}")

config = Config()
print(config.debug)            # True
print(config.enable_logging)   # False (auto-generated)
```

### `__call__` - Make objects callable

```python
class Multiplier:
    def __init__(self, factor):
        self.factor = factor
    
    def __call__(self, x):
        return x * self.factor

times_3 = Multiplier(3)
print(times_3(5))   # 15
print(times_3(10))  # 30
```

---

## ⚡ Generator vs List

**Question:** When do I use each?

```python
# Generator - memory efficient
def big_numbers():
    for i in range(1000000):
        yield i * 2
# Creates one number at a time

# List - fast access
nums = [i * 2 for i in range(1000000)]
# Creates all numbers immediately
```

| Use | When |
|-----|------|
| **Generator** | Large data, streaming, iterate once |
| **List** | Small data, need indexing, iterate many times |

---

## 🎓 Magic Methods Cheat Sheet

| You write | Python calls | What it does |
|-----------|--------------|--------------|
| `obj[key]` | `__getitem__(key)` | Get item by index |
| `len(obj)` | `__len__()` | Get length |
| `with obj:` | `__enter__()`, `__exit__()` | Context manager |
| `for x in obj:` | `__iter__()` | Make iterable |
| `item in obj` | `__contains__(item)` | Check membership |
| `obj.missing` | `__getattr__(name)` | Handle missing attrs |
| `obj(args)` | `__call__(*args)` | Call like function |
| `str(obj)` | `__str__()` | String for users |
| `repr(obj)` | `__repr__()` | String for developers |

---

## ✅ Common Mistakes

### ❌ Mutable default in dataclass
```python
@dataclass
class Person:
    hobbies: list = []  # BAD! Shared between all objects

# ✅ Fix
@dataclass  
class Person:
    hobbies: list = field(default_factory=list)
```

### ❌ Calling function twice
```python
if len(my_list) > 10:
    print(f"Length: {len(my_list)}")  # Calculated twice

# ✅ Fix with walrus
if (n := len(my_list)) > 10:
    print(f"Length: {n}")
```

### ❌ Forgetting to close files
```python
f = open('file.txt')
data = f.read()
f.close()  # Might not run if error

# ✅ Fix with context manager
with open('file.txt') as f:
    data = f.read()
```

---

## 🚀 Common Patterns

**Factory method:**
```python
@classmethod
def from_string(cls, s):
    name, age = s.split(',')
    return cls(name, int(age))
```

**Read-only property:**
```python
@property
def full_name(self):
    return f"{self.first} {self.last}"
# No setter = read-only
```

**Stateful callable:**
```python
class Counter:
    def __init__(self):
        self.count = 0
    
    def __call__(self):
        self.count += 1
        return self.count

counter = Counter()
print(counter())  # 1
print(counter())  # 2
```
