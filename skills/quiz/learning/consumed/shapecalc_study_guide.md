# ShapeCalc Study Guide

A tutorial covering every skill used in the ShapeCalc project. Review each section and try the mini examples in a Python REPL to reinforce the concepts.

---

## Instance Attributes and `self`

### What It Is

In Python, `self` refers to the specific instance of a class. When you create an attribute inside `__init__`, you must attach it to `self` — otherwise it's just a local variable that disappears when `__init__` finishes. Every time you want to read or write an instance's data inside a method, you go through `self`.

### Syntax

```python
class Dog:
    def __init__(self, name, age):
        self.name = name    # stored on the instance — persists
        self.age = age      # stored on the instance — persists

    def speak(self):
        return f"{self.name} says woof!"  # access via self
```

### Mini Example

```python
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1
        return self.count

c = Counter()
print(c.increment())  # 1
print(c.increment())  # 2
print(c.count)         # 2
```

### Common Mistake — Forgetting `self.`

```python
# WRONG — radius is a local variable, gone after __init__ exits
class Circle:
    def __init__(self, radius):
        radius = radius  # assigns parameter to itself — does nothing useful

    def area(self):
        return 3.14 * self.radius ** 2  # AttributeError: no self.radius!

# RIGHT
class Circle:
    def __init__(self, radius):
        self.radius = radius  # stored on the instance
```

---

## Class Attributes vs Instance Attributes

### What It Is

A **class attribute** is defined directly in the class body (not inside a method). It's shared across all instances — there's one copy. An **instance attribute** is created with `self.something` inside `__init__` (or another method). Each instance gets its own copy. Use class attributes for constants or shared data, instance attributes for per-object data.

### Syntax

```python
class MyClass:
    SHARED_VALUE = 42           # class attribute — one copy for all instances

    def __init__(self, unique):
        self.unique = unique    # instance attribute — one per instance
```

### Mini Example

```python
class Car:
    WHEELS = 4  # class attribute — all cars have 4 wheels

    def __init__(self, color):
        self.color = color  # instance attribute — each car has its own color

red = Car("red")
blue = Car("blue")

print(red.WHEELS)    # 4 — accessed through instance
print(blue.WHEELS)   # 4 — same value, shared
print(Car.WHEELS)    # 4 — accessed through class

print(red.color)     # "red" — unique to this instance
print(blue.color)    # "blue" — unique to this instance
```

### Common Mistake — Using a Class Attribute When You Need an Instance Attribute

```python
# WRONG — all instances share the same list!
class Team:
    members = []  # class attribute

    def add(self, name):
        self.members.append(name)

a = Team()
b = Team()
a.add("Alice")
print(b.members)  # ["Alice"] — oops, shared!

# RIGHT — each instance gets its own list
class Team:
    def __init__(self):
        self.members = []  # instance attribute

    def add(self, name):
        self.members.append(name)
```

---

## Abstract Base Classes with `abc`

### What It Is

An abstract base class (ABC) defines a blueprint that subclasses must follow. You mark methods with `@abc.abstractmethod` to say "any subclass MUST implement this method." You cannot create an instance of the ABC directly — Python raises `TypeError` if you try. This enforces a contract: every concrete shape must have `area()` and `perimeter()`.

### Syntax

```python
import abc

class Animal(abc.ABC):
    @abc.abstractmethod
    def speak(self) -> str:
        pass                  # no implementation — subclasses provide it

    @abc.abstractmethod
    def legs(self) -> int:
        pass
```

### Mini Example

```python
import abc

class Vehicle(abc.ABC):
    @abc.abstractmethod
    def fuel_type(self) -> str:
        pass

class ElectricCar(Vehicle):
    def fuel_type(self) -> str:
        return "electricity"

# This works:
car = ElectricCar()
print(car.fuel_type())  # "electricity"

# This fails:
v = Vehicle()  # TypeError: Can't instantiate abstract class Vehicle
```

### Common Mistake — Forgetting to Inherit from `abc.ABC`

```python
# WRONG — without abc.ABC, abstractmethod doesn't enforce anything
import abc

class Shape:
    @abc.abstractmethod
    def area(self):
        pass

s = Shape()  # no error! The "abstract" method didn't protect anything

# RIGHT — inherit from abc.ABC
class Shape(abc.ABC):
    @abc.abstractmethod
    def area(self):
        pass

s = Shape()  # TypeError — properly enforced
```

---

## The `__str__` Method

### What It Is

`__str__` is a special (dunder) method that Python calls when you use `str()` on an object or `print()` it. It should return a human-readable string representation. Without it, printing an object gives something unhelpful like `<__main__.Circle object at 0x...>`.

### Syntax

```python
class MyClass:
    def __str__(self) -> str:
        return "a friendly description"
```

### Mini Example

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Point({self.x}, {self.y})"

p = Point(3, 7)
print(p)        # Point(3, 7)
print(str(p))   # Point(3, 7)
```

### Common Mistake — Misspelling the Dunder

```python
# WRONG — single underscores, Python won't recognize it
class Point:
    def _str_(self):
        return "Point"

print(Point())  # <__main__.Point object at 0x...> — _str_ was ignored

# RIGHT — double underscores on both sides
class Point:
    def __str__(self):
        return "Point"
```

---

## Composition Over Inheritance

### What It Is

Composition means a class **has** other objects as attributes, rather than **extending** them through inheritance. A `ShapeCollection` isn't a shape itself — it *contains* shapes. This keeps the design flexible: the collection doesn't need to implement `area()` or `perimeter()`, it just works with objects that do.

### Syntax

```python
class Collection:
    def __init__(self, items):
        self.items = items   # "has" items, doesn't inherit from item

    def total(self):
        return sum(item.value for item in self.items)
```

### Mini Example

```python
class Engine:
    def __init__(self, horsepower):
        self.horsepower = horsepower

class Car:
    def __init__(self, engine):
        self.engine = engine  # Car HAS an engine

    def describe(self):
        return f"Car with {self.engine.horsepower}hp engine"

e = Engine(200)
c = Car(e)
print(c.describe())  # "Car with 200hp engine"
```

### Common Mistake — Inheriting When You Should Compose

```python
# WRONG — a Library is not a Book
class Library(Book):
    pass

# RIGHT — a Library HAS books
class Library:
    def __init__(self, books):
        self.books = books
```

---

## `isinstance()` and Polymorphism

### What It Is

`isinstance(obj, SomeClass)` returns `True` if `obj` is an instance of `SomeClass` or any of its subclasses. It's useful for filtering objects by type. Polymorphism means you can call the same method (`area()`) on different types (Circle, Rectangle) and get the right behavior — each class defines its own version.

### Syntax

```python
isinstance(obj, ClassName)         # True/False
isinstance(obj, (ClassA, ClassB))  # True if either match
```

### Mini Example

```python
class Animal:
    pass

class Dog(Animal):
    pass

class Cat(Animal):
    pass

pets = [Dog(), Cat(), Dog(), Cat(), Dog()]

dogs = [p for p in pets if isinstance(p, Dog)]
print(len(dogs))  # 3
```

### Common Mistake — Using `type()` Instead of `isinstance()`

```python
# WRONG — type() doesn't account for inheritance
class Shape:
    pass

class Circle(Shape):
    pass

c = Circle()
print(type(c) == Shape)       # False — c is a Circle, not exactly Shape
print(isinstance(c, Shape))   # True — Circle IS a Shape (inheritance)
```

---

## The `@property` Decorator

### What It Is

`@property` lets you define a method that behaves like an attribute — you access it without parentheses. It's useful for computed values that should look like simple attributes to the outside world. Instead of calling `collection.count()`, you just write `collection.count`.

### Syntax

```python
class MyClass:
    @property
    def value(self):
        return self._computed_thing
```

### Mini Example

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    @property
    def area(self):
        return self.width * self.height

r = Rectangle(3, 4)
print(r.area)    # 12 — no parentheses needed
# print(r.area())  # TypeError — it's a property, not a method call
```

### Common Mistake — Calling a Property Like a Method

```python
r = Rectangle(3, 4)

# WRONG — property is already "called" by accessing it
print(r.area())  # TypeError: 'int' object is not callable

# RIGHT — access like an attribute
print(r.area)    # 12
```

---

## `lambda` with `max()` and `sum()`

### What It Is

`max()` and `sum()` are built-in functions that work with iterables. `max()` accepts a `key` parameter — a function that extracts the comparison value from each element. `lambda` creates a small anonymous function inline, perfect for these one-off keys.

### Syntax

```python
max(iterable, key=lambda item: item.some_attribute)
sum(item.value for item in iterable)  # generator expression
```

### Mini Example

```python
class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

students = [Student("Alice", 92), Student("Bob", 88), Student("Carol", 95)]

top = max(students, key=lambda s: s.grade)
print(top.name)  # "Carol"

total = sum(s.grade for s in students)
print(total)  # 275
```

### Common Mistake — Forgetting the `key` Parameter

```python
# WRONG — Python doesn't know how to compare Student objects
top = max(students)  # TypeError: '>' not supported between instances of 'Student'

# RIGHT — tell max() what to compare
top = max(students, key=lambda s: s.grade)
```

---

## List Comprehensions for Filtering

### What It Is

A list comprehension with an `if` clause creates a new list containing only elements that pass a condition. It's a concise, Pythonic alternative to a `for` loop with `append`. Used heavily in ShapeCalc for methods like `of_type()`.

### Syntax

```python
[item for item in iterable if condition]
```

### Mini Example

```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

evens = [n for n in numbers if n % 2 == 0]
print(evens)  # [2, 4, 6, 8, 10]

big = [n for n in numbers if n > 5]
print(big)  # [6, 7, 8, 9, 10]
```

### Common Mistake — Mutating Instead of Filtering

```python
# WRONG — modifying a list while iterating over it
numbers = [1, 2, 3, 4, 5]
for n in numbers:
    if n % 2 != 0:
        numbers.remove(n)  # skips elements, unpredictable results

# RIGHT — create a new filtered list
evens = [n for n in numbers if n % 2 == 0]
```
