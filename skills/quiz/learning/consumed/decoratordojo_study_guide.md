# DecoratorDojo Study Guide

A tutorial covering every skill needed for the DecoratorDojo exercises. Read through each section, try the mini examples in a Python REPL, then start the exercises when you feel comfortable.

---

## Decorator Basics

### What is a Decorator?

A decorator is a function that takes another function as input, adds some behavior around it, and returns a new function. When you write `@my_decorator` above a function definition, Python automatically passes that function through the decorator. It's shorthand — `@my_decorator` on `def greet()` is the same as writing `greet = my_decorator(greet)` after the definition.

### Syntax — The Basic Decorator Pattern

```python
def my_decorator(func):          # receives the original function
    def wrapper(*args, **kwargs): # replacement function that gets called instead
        # --- do something BEFORE the original runs ---
        result = func(*args, **kwargs)  # call the original
        # --- do something AFTER the original runs ---
        return result             # MUST return the result!
    return wrapper                # return the wrapper (not wrapper() — no parens!)
```

### Mini Example

```python
def shout(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result.upper()
    return wrapper

@shout
def greet(name):
    return f"hello {name}"

print(greet("Matt"))  # "HELLO MATT"
```

Without `@shout`, `greet("Matt")` returns `"hello Matt"`. The decorator intercepts the return value and uppercases it.

### Common Mistake — Forgetting to Return the Wrapper

```python
# WRONG — returns None, so the decorated function becomes None
def bad(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result
    # missing: return wrapper

@bad
def add(a, b):
    return a + b

add(2, 3)  # TypeError: 'NoneType' object is not callable
```

---

## `*args` and `**kwargs`

### What They Are

`*args` collects any number of positional arguments into a tuple. `**kwargs` collects any number of keyword arguments into a dictionary. Together, they let a function accept **anything** — which is essential for decorators, since the wrapper needs to pass through whatever arguments the original function expects.

### Syntax

```python
def wrapper(*args, **kwargs):
    # args is a tuple: (1, 2, 3)
    # kwargs is a dict: {"name": "Matt", "age": 30}
    func(*args, **kwargs)  # unpack and forward them all
```

### Mini Example

```python
def log_call(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        return func(*args, **kwargs)
    return wrapper

@log_call
def multiply(a, b, verbose=False):
    return a * b

multiply(3, 4, verbose=True)
# prints: Calling multiply with args=(3, 4), kwargs={'verbose': True}
# returns: 12
```

### Common Mistake — Hardcoding Arguments

```python
# WRONG — only works for functions with exactly 2 args
def bad_decorator(func):
    def wrapper(a, b):
        return func(a, b)
    return wrapper

# RIGHT — works for ANY function signature
def good_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

---

## Preserving Return Values

### What It Is

The most common decorator bug: calling the original function but forgetting to capture and return its result. The wrapper ends up returning `None` instead of the actual value.

### Syntax

```python
def wrapper(*args, **kwargs):
    result = func(*args, **kwargs)  # capture the return value
    return result                    # pass it back to the caller
```

### Mini Example

```python
def do_nothing(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result  # value passes through unchanged
    return wrapper

@do_nothing
def add(a, b):
    return a + b

print(add(2, 3))  # 5 — not None
```

### Common Mistake — Eating the Return Value

```python
# WRONG — calls func but doesn't return the result
def bad_decorator(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)   # result is thrown away!
    return wrapper

@bad_decorator
def add(a, b):
    return a + b

print(add(2, 3))  # None — the 5 was lost
```

---

## `functools.wraps`

### What It Is

When you wrap a function, the wrapper replaces the original. Without `functools.wraps`, the wrapper's `__name__` and `__doc__` attributes show the wrapper's name, not the original's. `@wraps(func)` copies the original function's metadata onto the wrapper so tools like debuggers, `help()`, and introspection still see the right name and docstring.

### Syntax

```python
from functools import wraps

def my_decorator(func):
    @wraps(func)                     # copies func's __name__, __doc__, etc. onto wrapper
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

### Mini Example

```python
from functools import wraps

def loud(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs).upper()
    return wrapper

@loud
def greet(name):
    """Say hello."""
    return f"hello {name}"

print(greet.__name__)  # "greet" (not "wrapper")
print(greet.__doc__)   # "Say hello."
```

### Common Mistake — Without `@wraps`

```python
def loud(func):
    def wrapper(*args, **kwargs):  # no @wraps
        return func(*args, **kwargs).upper()
    return wrapper

@loud
def greet(name):
    """Say hello."""
    return f"hello {name}"

print(greet.__name__)  # "wrapper" — wrong!
print(greet.__doc__)   # None — lost!
```

---

## Decorator Factories (Decorators with Arguments)

### What It Is

A regular decorator takes a function. But what if you want to pass configuration to the decorator, like `@repeat(3)`? You need a **decorator factory** — a function that takes the argument, and returns a decorator. This creates three levels of nesting: the factory takes the config, the decorator takes the function, the wrapper takes the call arguments.

### Syntax

```python
from functools import wraps

def my_factory(config_value):            # Level 1: takes the argument
    def decorator(func):                  # Level 2: takes the function
        @wraps(func)
        def wrapper(*args, **kwargs):     # Level 3: takes the call args
            # use config_value here
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

### Mini Example

```python
from functools import wraps

def prefix(text):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return f"{text}: {result}"
        return wrapper
    return decorator

@prefix("INFO")
def status():
    return "all systems go"

print(status())  # "INFO: all systems go"
```

### Common Mistake — Missing a Level of Nesting

```python
# WRONG — only two levels, but @prefix("INFO") expects three
def prefix(text):
    def wrapper(*args, **kwargs):
        # where does func come from? Nowhere!
        return f"{text}: {func(*args, **kwargs)}"
    return wrapper

# RIGHT — three levels: factory -> decorator -> wrapper
def prefix(text):
    def decorator(func):
        def wrapper(*args, **kwargs):
            return f"{text}: {func(*args, **kwargs)}"
        return wrapper
    return decorator
```

---

## Decorators Inside a Class

### What It Is

A decorator can be defined as a method inside a class. The key difference: it doesn't take `self` as its first parameter because it runs at **class definition time**, before any instances exist. It's used with `@ClassName._decorator` or just `@_decorator` inside the same class body.

### Syntax

```python
from functools import wraps

class Base:
    def _my_decorator(func):          # no 'self' — this isn't a regular method
        @wraps(func)
        def wrapped(obj, *args, **kwargs):  # 'obj' receives the instance (IS self)
            # do something before
            return func(obj, *args, **kwargs)
        return wrapped

    @_my_decorator
    def some_method(self, value):
        self.value = value
        return self
```

### Mini Example

```python
from functools import wraps

class Greeter:
    greeting = None

    def _log(func):
        @wraps(func)
        def wrapped(obj, *args, **kwargs):
            print(f"Calling {func.__name__} on {obj}")
            return func(obj, *args, **kwargs)
        return wrapped

    @_log
    def set_greeting(self, text):
        self.greeting = text
        return self

g = Greeter()
g.set_greeting("hi")  # prints: Calling set_greeting on <...Greeter...>
print(g.greeting)       # "hi"
```

### Common Mistake — Adding `self` to the Decorator

```python
# WRONG — _my_decorator runs at class definition time, there's no instance yet
class Base:
    def _my_decorator(self, func):  # self doesn't make sense here
        ...

# RIGHT — no self, func is the only parameter
class Base:
    def _my_decorator(func):
        ...
```

---

## `getattr()` for Dynamic Method Dispatch

### What It Is

`getattr(obj, "method_name")` is equivalent to `obj.method_name`, but the method name is a **string** you can build dynamically. This is powerful in the validation pattern: given `set_name`, you construct `"_validate_set_name"` and look it up at runtime without hardcoding it.

### Syntax

```python
method_name = "_validate_" + func.__name__   # build the string
validator = getattr(obj, method_name)          # look up the method
validator(*args)                               # call it
```

### Mini Example

```python
class Calculator:
    def add(self, a, b):
        return a + b

    def multiply(self, a, b):
        return a * b

c = Calculator()
operation = "add"
result = getattr(c, operation)(3, 4)  # same as c.add(3, 4)
print(result)  # 7

operation = "multiply"
result = getattr(c, operation)(3, 4)  # same as c.multiply(3, 4)
print(result)  # 12
```

### Common Mistake — Passing the Function Instead of a String

```python
# WRONG — getattr expects a string, not a function object
getattr(obj, func)

# RIGHT — use func.__name__ to get the string
getattr(obj, "_validate_" + func.__name__)
```

---

## Mutable Default Arguments

### What It Is

Python evaluates default argument values **once**, at function **definition** time (when the `def` line runs), not each time the function is called. If the default is a mutable object like a list, dict, or set, that same object is shared across every call. This means changes in one call leak into the next.

### Syntax — The Problem

```python
def broken(items=[]):     # this [] is created ONCE
    items.append("x")     # mutates the SAME list every call
    return items
```

### Mini Example

```python
def collect(item, bag=[]):
    bag.append(item)
    return bag

print(collect("a"))  # ["a"]
print(collect("b"))  # ["a", "b"] — bag was NOT reset!
print(collect("c"))  # ["a", "b", "c"] — keeps growing
```

### Common Mistake — Expecting a Fresh Default Each Call

```python
# WRONG — shared list across calls
def collect(item, bag=[]):
    bag.append(item)
    return bag

# RIGHT — None sentinel pattern
def collect(item, bag=None):
    if bag is None:
        bag = []          # fresh list every call
    bag.append(item)
    return bag

print(collect("a"))  # ["a"]
print(collect("b"))  # ["b"] — fresh list each time
```

---

## The None Sentinel Pattern

### What It Is

The standard fix for mutable default arguments. Instead of using `[]` or `{}` as a default, use `None`. Then inside the function body, check `if arg is None` and create a fresh mutable. This guarantees each call gets its own independent object.

### Syntax

```python
def my_func(data=None):
    if data is None:
        data = []        # new list created at CALL time, not definition time
    # now use data safely
```

### Mini Example

```python
def register(name, registry=None):
    if registry is None:
        registry = {}
    registry[name] = True
    return registry

print(register("Alice"))  # {"Alice": True}
print(register("Bob"))    # {"Bob": True} — fresh dict, no leak
```

### Common Mistake — Using `==` Instead of `is`

```python
# WRONG — == checks value equality, an empty list [] == None is False anyway,
# but the real issue is: someone could pass an actual empty list and you'd
# accidentally replace it
def my_func(data=None):
    if data == []:    # wrong check
        data = []

# RIGHT — 'is' checks identity, only matches the actual None singleton
def my_func(data=None):
    if data is None:
        data = []
```

---

## `inspect.signature` — Reading Function Signatures

### What It Is

`inspect.signature(func)` returns a `Signature` object that describes a function's parameters — their names, defaults, and kinds. This is useful when you need to programmatically examine what defaults a function has, such as finding which parameters have mutable defaults.

### Syntax

```python
import inspect

sig = inspect.signature(func)
for name, param in sig.parameters.items():
    print(name, param.default)
    # param.default is inspect.Parameter.empty if no default exists
```

### Mini Example

```python
import inspect

def greet(name, greeting="hello", tags=[]):
    pass

sig = inspect.signature(greet)
for name, param in sig.parameters.items():
    if param.default is not inspect.Parameter.empty:
        print(f"{name} has default: {param.default} (type: {type(param.default).__name__})")

# Output:
# greeting has default: hello (type: str)
# tags has default: [] (type: list)
```

### Common Mistake — Forgetting to Check for `Parameter.empty`

```python
# WRONG — parameters without defaults have a special sentinel, not None
if param.default is not None:  # this will miss params with no default
    ...

# RIGHT — use the proper sentinel
if param.default is not inspect.Parameter.empty:
    ...
```

---

## `copy.deepcopy` — Creating Independent Copies

### What It Is

`copy.deepcopy(obj)` creates a completely independent copy of an object and all objects nested inside it. Unlike `copy.copy()` (shallow copy), `deepcopy` recursively copies everything. This is useful when you need to guarantee that modifying the copy never affects the original.

### Syntax

```python
import copy

original = [[1, 2], [3, 4]]
deep = copy.deepcopy(original)
deep[0].append(99)
print(original)  # [[1, 2], [3, 4]] — untouched
```

### Mini Example

```python
import copy

config = {"users": ["Alice"], "settings": {"debug": True}}

backup = copy.deepcopy(config)
backup["users"].append("Bob")
backup["settings"]["debug"] = False

print(config)   # {"users": ["Alice"], "settings": {"debug": True}} — unchanged
print(backup)   # {"users": ["Alice", "Bob"], "settings": {"debug": False}}
```

### Common Mistake — Using Assignment Instead of Copy

```python
# WRONG — both variables point to the SAME object
original = [1, 2, 3]
backup = original
backup.append(4)
print(original)  # [1, 2, 3, 4] — oops!

# RIGHT — deepcopy creates an independent copy
import copy
backup = copy.deepcopy(original)
backup.append(4)
print(original)  # [1, 2, 3] — safe
```
