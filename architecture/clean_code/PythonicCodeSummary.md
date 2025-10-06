# Python Quick Reference 🐍

*Fast lookup for Python concepts while coding*

---

## 📦 Context Managers
**What:** Automatically runs setup code before a block, and cleanup code after (even if errors happen)

**Why use it:** Never forget to close files, release locks, or cleanup resources

```python
# Using @contextmanager (simplest way)
from contextlib import contextmanager

@contextmanager
def my_cm():
    print("Setup - runs before 'with' block")
    yield "resource"  # This value goes to 'as x'
    print("Cleanup - ALWAYS runs, even if error in block")

with my_cm() as x:
    print(f"Using {x}")
    # Cleanup happens automatically here
```

**Real example:**
```python
# Without context manager - BAD (might forget to close)
f = open('file.txt')
data = f.read()
f.close()  # What if error happens before this?

# With context manager - GOOD (always closes)
with open('file.txt') as f:
    data = f.read()
# File is closed here automatically
```

---

## 🔄 Comprehensions
**What:** A shorter way to create lists/dicts/sets using a loop in one line

**Why use it:** More readable than 4-line loops for simple transformations

```python
# Traditional way (verbose)
squares = []
for n in range(5):
    if n % 2 == 0:
        squares.append(n**2)

# Comprehension way (concise)
squares = [n**2 for n in range(5) if n % 2 == 0]
# Format: [WHAT_TO_ADD for ITEM in COLLECTION if CONDITION]

# Dict comprehension
square_dict = {n: n**2 for n in range(5)}
# Result: {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# Set comprehension (removes duplicates)
unique = {x for x in [1, 2, 2, 3]}
# Result: {1, 2, 3}
```

---

## 🎯 Walrus Operator `:=`
**What:** Assigns a value to a variable AND uses it in the same line

**Why use it:** Avoid calling the same function twice or repeating code

```python
# Problem: calling the same function twice
if len(my_list) > 0:
    print(f"Length is {len(my_list)}")  # Called len() again!

# Solution with walrus
if (length := len(my_list)) > 0:
    print(f"Length is {length}")  # Reuse the value!

# Real example: regex
if (match := re.search(r'\d+', text)):
    print(match.group())  # match is available here
else:
    print("No match")
```

**When to use:** When you need a value both for a condition AND inside the block

---

## 🔒 Attributes & Privacy

**What:** Ways to signal which attributes are "internal" vs "public"

| Name | Meaning | Access |
|------|---------|--------|
| `self.name` | Public - anyone can use | Everyone can access |
| `self._name` | Internal - "don't use me" | Convention only (not enforced) |
| `self.__name` | Private - really hidden | Python mangles the name |

```python
class BankAccount:
    def __init__(self):
        self.owner = "Alice"        # Public: anyone can read/write
        self._balance = 1000        # Internal: saying "please don't touch"
        self.__pin = 1234           # Private: actually hidden

account = BankAccount()
print(account.owner)        # ✅ Fine - public
print(account._balance)     # ⚠️ Works but you shouldn't - internal
print(account.__pin)        # ❌ Error - really private
```

**When to use:**
- `public`: Normal attributes everyone can use
- `_internal`: For code organization, not meant for users
- `__private`: Rare - only when you really need to prevent conflicts

---

## 🎛️ Properties
**What:** Makes a method look like an attribute, but with validation/logic

**Why use it:** Control what happens when someone reads or writes an attribute

```python
class Person:
    def __init__(self, age):
        self._age = age  # Store in _age
    
    @property
    def age(self):
        """Called when someone reads .age"""
        return self._age
    
    @age.setter
    def age(self, value):
        """Called when someone writes .age"""
        if value < 0:
            raise ValueError("Age can't be negative!")
        self._age = value

# Usage - looks like normal attribute
person = Person(25)
print(person.age)      # Calls the @property method
person.age = 30        # Calls the @age.setter method
person.age = -5        # Error! Validation runs
```

**When to use:**
- Validation (age must be positive)
- Computed values (full_name from first + last)
- Read-only attributes (no setter)

---

## 🛠️ Method Types

**The BIG confusion:** Do I need to create an object first, or can I call directly on the class?

```python
class Pizza:
    def __init__(self, size, toppings):
        self.size = size
        self.toppings = toppings
    
    # 1️⃣ INSTANCE METHOD (normal method)
    # ⚠️ MUST create object first! Cannot call on class directly.
    def describe(self):
        return f"{self.size} inch pizza with {self.toppings}"
    
    # 2️⃣ CLASS METHOD
    # ✅ Call DIRECTLY on class (no object needed)
    # Often used to create objects in different ways
    @classmethod
    def margherita(cls, size):
        """Creates and returns a new Pizza object"""
        return cls(size, ['mozzarella', 'tomato', 'basil'])
    
    # 3️⃣ STATIC METHOD
    # ✅ Call DIRECTLY on class (no object needed)
    # Just a utility function, doesn't create objects
    @staticmethod
    def is_valid_size(size):
        """Checks if size is valid - just returns True/False"""
        return size in [8, 10, 12, 14, 16]


# HOW TO USE EACH TYPE:

# ❌ CANNOT do this with instance method:
# Pizza.describe()  # ERROR! No pizza object exists yet

# ✅ Instance method - MUST create object first:
pizza = Pizza(12, ['pepperoni'])  # Step 1: Create object
print(pizza.describe())            # Step 2: Call method on that object
# Output: "12 inch pizza with ['pepperoni']"

# ✅ Class method - call DIRECTLY, no object needed:
marg = Pizza.margherita(14)       # Creates object for you!
print(marg.describe())             # Now you have object, can use instance methods
# Output: "14 inch pizza with ['mozzarella', 'tomato', 'basil']"

# ✅ Static method - call DIRECTLY, no object needed:
print(Pizza.is_valid_size(10))    # Just call it! Returns True
print(Pizza.is_valid_size(99))    # Returns False
# No object created, just a utility function
```

**Visual guide:**

```python
# Instance method flow:
pizza = Pizza(12, ['cheese'])     # 1. Create object first
pizza.describe()                   # 2. Then call method
        ↑
    needs object!

# Class method flow:
Pizza.margherita(14)              # Call directly, returns new object
  ↑                     ↓
class name          returns object

# Static method flow:
Pizza.is_valid_size(10)           # Call directly, returns result
  ↑                     ↓
class name          returns True/False
```

**Quick decision tree:**
1. Does the method need specific object data (like `self.size`)? → **Instance method**
2. Does it create a new object? → **@classmethod**
3. Is it just a helper function? → **@staticmethod**

---

## 📋 Dataclasses
**What:** Automatically generates `__init__`, `__repr__`, and other methods for data-holding classes

**Why use it:** Less typing, fewer bugs from forgotten code

```python
# Without dataclass (manual work)
class PersonOld:
    def __init__(self, name, age, hobbies):
        self.name = name
        self.age = age
        self.hobbies = hobbies
    
    def __repr__(self):
        return f"PersonOld(name={self.name}, age={self.age}, hobbies={self.hobbies})"
    
    def __eq__(self, other):
        return self.name == other.name and self.age == other.age

# With dataclass (automatic!)
from dataclasses import dataclass, field

@dataclass
class Person:
    name: str
    age: int
    hobbies: list = field(default_factory=list)  # ⚠️ IMPORTANT for lists/dicts
    
    def __post_init__(self):
        """Runs after __init__ for validation"""
        if self.age < 0:
            raise ValueError("Age can't be negative")

# Usage
p = Person("Alice", 30, ["reading"])
print(p)  # Automatic nice printing!
```

**Important:** Always use `field(default_factory=list)` for mutable defaults (lists, dicts)

---

## 🔁 Iterables
**What:** Objects that can be used in a `for` loop

**Why use it:** Create custom objects that work with `for`, `list()`, etc.

```python
class Countdown:
    """Counts down from a number"""
    def __init__(self, start):
        self.start = start
    
    def __iter__(self):
        """Returns an iterator - use yield for simplicity"""
        n = self.start
        while n > 0:
            yield n  # Pause here and return n, resume next time
            n -= 1

# Usage
for num in Countdown(5):
    print(num)  # Prints: 5, 4, 3, 2, 1

# Works with list() too
numbers = list(Countdown(3))  # [3, 2, 1]
```

**When to use:** Custom collections, lazy loading data, sequences that don't fit in memory

---

## 📚 Sequences
**What:** Objects that support indexing with `[0]`, `[1]`, etc. and `len()`

**Why use it:** Make your object act like a list (indexing, slicing, length)

```python
class Playlist:
    """A music playlist that acts like a list"""
    def __init__(self, songs):
        self._songs = songs
    
    def __len__(self):
        """len(playlist) returns number of songs"""
        return len(self._songs)
    
    def __getitem__(self, index):
        """playlist[0] returns first song"""
        return self._songs[index]

# Usage
playlist = Playlist(["Song A", "Song B", "Song C"])
print(len(playlist))        # 3
print(playlist[0])          # "Song A"
print(playlist[1:3])        # ["Song B", "Song C"] - slicing works!
```

**When to use:** When you want your object to act like a list/tuple

---

## 🎯 More Magic Methods

### `__contains__` - Make `in` work
**What:** Let users check if something is "in" your object

```python
class AgeRange:
    def __init__(self, min_age, max_age):
        self.min = min_age
        self.max = max_age
    
    def __contains__(self, age):
        """Checks if age is in range"""
        return self.min <= age <= self.max

# Usage
teens = AgeRange(13, 19)
print(15 in teens)      # True
print(25 in teens)      # False
```

### `__getattr__` - Handle missing attributes
**What:** Called when someone accesses an attribute that doesn't exist

```python
class Config:
    def __init__(self):
        self.debug = True
    
    def __getattr__(self, name):
        """Return default for missing config values"""
        if name.startswith("enable_"):
            return False  # Default all 'enable_' settings to False
        raise AttributeError(f"No config: {name}")

config = Config()
print(config.debug)              # True (exists)
print(config.enable_logging)     # False (doesn't exist, default)
print(config.unknown)            # Error
```

### `__call__` - Make objects callable like functions
**What:** Let you call an object like `obj()`

```python
class Greeter:
    def __init__(self, greeting):
        self.greeting = greeting
    
    def __call__(self, name):
        """Called when you do greeter(name)"""
        return f"{self.greeting}, {name}!"

# Usage
say_hi = Greeter("Hello")
say_hey = Greeter("Hey")

print(say_hi("Alice"))   # "Hello, Alice!"
print(say_hey("Bob"))    # "Hey, Bob!"
```

**When to use:** Objects that act like functions but need to remember state

---

## ⚡ Generator vs List

**The question:** Should I use a generator or a list?

```python
# Generator (memory efficient)
def big_numbers():
    for i in range(1000000):
        yield i * 2
# Only creates one number at a time

gen = big_numbers()
print(next(gen))  # 0
print(next(gen))  # 2

# List (fast access but uses memory)
nums = [i * 2 for i in range(1000000)]
# Creates all million numbers immediately
print(nums[500000])  # Fast random access
```

**Use generator when:** Large data, streaming, don't need all at once
**Use list when:** Small data, need indexing, need to iterate multiple times

---

## ✅ Common Mistakes

```python
# ❌ DON'T: Mutable default in dataclass
@dataclass
class Person:
    hobbies: list = []  # BAD! All persons share same list

# ✅ DO: Use default_factory
@dataclass
class Person:
    hobbies: list = field(default_factory=list)  # Each person gets own list

# ❌ DON'T: Call function twice
if len(my_list) > 10:
    print(f"Big list: {len(my_list)} items")  # Calculated twice!

# ✅ DO: Use walrus
if (size := len(my_list)) > 10:
    print(f"Big list: {size} items")  # Calculated once!

# ❌ DON'T: Forget to close resources
f = open('file.txt')
data = f.read()
f.close()  # Might not run if error

# ✅ DO: Use context manager
with open('file.txt') as f:
    data = f.read()
# Always closes
```
