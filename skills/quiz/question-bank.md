# Question Bank

Last updated: 2026-03-24

---

## DSA Topics

### Recursion

**Q1 - Conceptual:** What are the two essential parts of every recursive function?
**A:** A base case (stopping condition) and a recursive case (the function calling itself with a smaller/simpler input).

**Q2 - Code Output:** What does this function return when called with `factorial(5)`?
```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```
**A:** 120 (5 * 4 * 3 * 2 * 1)

**Q3 - Conceptual:** What is a stack overflow in the context of recursion, and what causes it?
**A:** A stack overflow occurs when the call stack exceeds its size limit, typically caused by a missing or incorrect base case leading to infinite recursion.

**Q4 - Code Writing:** Write a recursive function to calculate the nth Fibonacci number.
**A:**
```python
def fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

**Q5 - Conceptual:** What's the difference between head recursion and tail recursion?
**A:** In head recursion, the recursive call happens before processing (the work is done after the call returns). In tail recursion, all processing happens before the recursive call — the recursive call is the last operation. Tail recursion can be optimized by compilers into iteration (though Python doesn't do this).

---

### Linear Search

**Q1 - Conceptual:** What is the time complexity of linear search in the best, average, and worst cases?
**A:** Best: O(1) — element is first. Average: O(n). Worst: O(n) — element is last or not present.

**Q2 - Code Writing:** Write a linear search function that returns the index of a target value, or -1 if not found.
**A:**
```python
def linear_search(arr: list, target) -> int:
    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1
```

**Q3 - Compare/Contrast:** When would you choose linear search over binary search?
**A:** When the data is unsorted (binary search requires sorted data), when the dataset is very small (overhead of sorting isn't worth it), or when you're searching a linked list (no random access for binary search).

**Q4 - Code Output:** What does this return? `linear_search([3, 7, 1, 9, 4], 9)`
**A:** 3 (the index of 9 in the list)

---

### Binary Search

**Q1 - Conceptual:** What is the key prerequisite for binary search, and what is its time complexity?
**A:** The array must be sorted. Time complexity is O(log n).

**Q2 - Code Writing:** Implement binary search iteratively.
**A:**
```python
def binary_search(arr: list, target) -> int:
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1
```

**Q3 - Conceptual:** Why do we use `(low + high) // 2` instead of just dividing the array length? What's a potential issue?
**A:** In some languages, `low + high` can cause integer overflow when both are large. A safer alternative is `low + (high - low) // 2`. In Python this isn't an issue due to arbitrary precision integers, but it's good practice.

**Q4 - Compare/Contrast:** Compare the space complexity of iterative vs recursive binary search.
**A:** Iterative: O(1) space. Recursive: O(log n) space due to the call stack frames.

**Q5 - Code Output:** How many comparisons does binary search need (maximum) for a sorted array of 1000 elements?
**A:** ceil(log2(1000)) = 10 comparisons.

---

### Bubble Sort

**Q1 - Conceptual:** Explain how bubble sort works in one or two sentences.
**A:** Bubble sort repeatedly steps through the list, compares adjacent elements, and swaps them if they're in the wrong order. Larger elements "bubble up" to the end with each pass. It repeats until no swaps are needed.

**Q2 - Conceptual:** What are bubble sort's time and space complexities?
**A:** Time: O(n²) average and worst case, O(n) best case (already sorted, with optimization). Space: O(1) — it sorts in place.

**Q3 - Code Output:** After ONE complete pass of bubble sort on `[5, 3, 8, 1, 2]`, what does the array look like?
**A:** `[3, 5, 1, 2, 8]` — the largest element (8) has bubbled to the end.

**Q4 - Code Writing:** Implement bubble sort with the early termination optimization.
**A:**
```python
def bubble_sort(arr: list) -> list:
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr
```

**Q5 - Conceptual:** What does the early termination optimization do, and what case does it improve?
**A:** If no swaps occur during a pass, the array is already sorted and we can stop early. This improves the best case to O(n) for already-sorted arrays.

---

### Selection Sort

**Q1 - Conceptual:** Explain how selection sort works.
**A:** Selection sort divides the array into sorted (left) and unsorted (right) portions. It repeatedly finds the minimum element from the unsorted portion and swaps it with the first unsorted element.

**Q2 - Conceptual:** What are selection sort's time and space complexities? Is it stable?
**A:** Time: O(n²) in all cases (best, average, worst). Space: O(1). It is NOT stable — equal elements may change relative order due to swapping.

**Q3 - Compare/Contrast:** What advantage does selection sort have over bubble sort?
**A:** Selection sort makes fewer swaps — at most O(n) swaps vs O(n²) for bubble sort. This matters when write operations are expensive.

**Q4 - Code Writing:** Implement selection sort.
**A:**
```python
def selection_sort(arr: list) -> list:
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr
```

---

### Insertion Sort

**Q1 - Conceptual:** Explain how insertion sort works.
**A:** Insertion sort builds the sorted array one element at a time. It takes each element and inserts it into its correct position within the already-sorted portion by shifting larger elements to the right.

**Q2 - Conceptual:** What are insertion sort's complexities, and when is it a good choice?
**A:** Time: O(n) best (nearly sorted), O(n²) average and worst. Space: O(1). Good for small datasets, nearly sorted data, or online sorting (data arriving one element at a time).

**Q3 - Compare/Contrast:** Why is insertion sort preferred over bubble and selection sort for nearly-sorted data?
**A:** For nearly-sorted data, insertion sort approaches O(n) because each element only needs to shift a small number of positions. Bubble sort (without optimization) and selection sort still do O(n²) comparisons regardless.

**Q4 - Code Writing:** Implement insertion sort.
**A:**
```python
def insertion_sort(arr: list) -> list:
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr
```

**Q5 - Conceptual:** Is insertion sort stable? Why or why not?
**A:** Yes, insertion sort is stable. Equal elements are never swapped past each other because we only shift elements that are strictly greater than the key.

---

### Quick Sort

**Q1 - Conceptual:** Explain the quick sort algorithm. What is the role of the pivot?
**A:** Quick sort picks a pivot element, then partitions the array so all elements less than the pivot go left and all greater go right. It then recursively sorts the left and right sub-arrays. The pivot ends up in its final sorted position after partitioning.

**Q2 - Conceptual:** What are quick sort's time and space complexities?
**A:** Time: O(n log n) average, O(n²) worst case (when pivot is always the smallest or largest element). Space: O(log n) average (call stack), O(n) worst case.

**Q3 - Conceptual:** What causes quick sort's worst-case performance, and how can you mitigate it?
**A:** Worst case occurs when the pivot is always the min or max (e.g., already sorted array with first element as pivot). Mitigations: random pivot selection, median-of-three pivot, or using introsort (switch to heapsort when recursion is too deep).

**Q4 - Code Writing:** Implement quick sort.
**A:**
```python
def quick_sort(arr: list) -> list:
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)
```

**Q5 - Compare/Contrast:** Compare quick sort vs merge sort. When would you choose one over the other?
**A:** Quick sort: O(1) extra space (in-place version), better cache performance, faster in practice. Merge sort: guaranteed O(n log n), stable, better for linked lists and external sorting. Choose merge sort when stability or guaranteed performance matters; quick sort for general-purpose in-memory sorting.

---

### Merge Sort

**Q1 - Conceptual:** Explain how merge sort works.
**A:** Merge sort divides the array in half recursively until each sub-array has one element, then merges the sub-arrays back together in sorted order. The merge step compares elements from both halves and builds the sorted result.

**Q2 - Conceptual:** What are merge sort's time and space complexities?
**A:** Time: O(n log n) in ALL cases (best, average, worst). Space: O(n) for the temporary arrays used during merging.

**Q3 - Code Writing:** Implement the merge function that combines two sorted arrays.
**A:**
```python
def merge(left: list, right: list) -> list:
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

**Q4 - Conceptual:** Why is merge sort considered stable?
**A:** Because when two elements are equal, the merge step takes from the left sub-array first (`<=`), preserving the original relative order of equal elements.

**Q5 - Conceptual:** Why is merge sort preferred for sorting linked lists over quick sort?
**A:** Linked lists don't support random access, which makes quick sort's partitioning inefficient. Merge sort works well because it only needs sequential access and the merge step can be done in-place for linked lists (no extra O(n) space needed).

---

### Tree Traversals

**Q1 - Conceptual:** Name the three depth-first tree traversal orders and describe the visit sequence for each.
**A:** In-order: left, root, right. Pre-order: root, left, right. Post-order: left, right, root.

**Q2 - Conceptual:** What traversal order gives you a sorted sequence from a binary search tree?
**A:** In-order traversal.

**Q3 - Conceptual:** What is the difference between depth-first search (DFS) and breadth-first search (BFS) for trees?
**A:** DFS explores as deep as possible along each branch before backtracking (uses stack/recursion). BFS explores all nodes at the current depth before moving deeper (uses a queue). DFS uses O(h) space where h is height; BFS uses O(w) space where w is the max width.

**Q4 - Code Writing:** Implement in-order traversal for a binary tree (given a node with `.val`, `.left`, `.right`).
**A:**
```python
def inorder(node) -> list:
    if node is None:
        return []
    return inorder(node.left) + [node.val] + inorder(node.right)
```

**Q5 - Code Writing:** Implement BFS (level-order traversal) for a binary tree.
**A:**
```python
from collections import deque

def level_order(root) -> list:
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        result.append(node.val)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    return result
```

---

## Python Coding Skills

### Writing Clean Functions

**Q1 - Spot the Bug:** What's wrong with this function?
```python
def get_user_data(user_id, db_connection, format_output=True, include_history=True):
    data = db_connection.query(f"SELECT * FROM users WHERE id = {user_id}")
    if include_history:
        history = db_connection.query(f"SELECT * FROM history WHERE user_id = {user_id}")
        data['history'] = history
    if format_output:
        return json.dumps(data)
    return data
```
**A:** SQL injection vulnerability — using f-string interpolation to build SQL queries. Should use parameterized queries: `db_connection.query("SELECT * FROM users WHERE id = %s", (user_id,))`.

**Q2 - Multiple Choice:** Which of these is the best function signature?
- A) `def process(d, f=True, x=None)`
- B) `def process_data(data: dict, flatten: bool = True, exclude: list[str] | None = None) -> dict`
- C) `def process_data(data, flatten, exclude)`
- D) `def processData(data: dict, flatten: bool, exclude: list)`
**A:** B — uses descriptive names, type hints, sensible defaults, and follows snake_case convention.

**Q3 - Code Writing:** Rewrite this function to follow the single responsibility principle:
```python
def handle_order(order):
    total = sum(item['price'] * item['qty'] for item in order['items'])
    tax = total * 0.08
    total_with_tax = total + tax
    with open('orders.log', 'a') as f:
        f.write(f"Order {order['id']}: ${total_with_tax}\n")
    send_email(order['email'], f"Your total is ${total_with_tax}")
    return total_with_tax
```
**A:**
```python
def calculate_order_total(items: list[dict], tax_rate: float = 0.08) -> float:
    subtotal = sum(item['price'] * item['qty'] for item in items)
    return subtotal * (1 + tax_rate)
```
The logging and email should be handled by separate functions. `calculate_order_total` should only calculate.

**Q4 - Spot the Bug:** What's wrong with this default argument?
```python
def add_item(item, items=[]):
    items.append(item)
    return items
```
**A:** Mutable default argument. The list `[]` is created once at function definition time, so all calls share the same list. Fix: use `items=None` and create a new list inside the function:
```python
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

**Q5 - Conceptual:** What does "EAFP" mean in Python, and how does it differ from "LBYL"?
**A:** EAFP = "Easier to Ask Forgiveness than Permission" — use try/except to handle errors. LBYL = "Look Before You Leap" — check conditions before acting. Python favors EAFP:
```python
# LBYL
if key in my_dict:
    value = my_dict[key]

# EAFP (Pythonic)
try:
    value = my_dict[key]
except KeyError:
    handle_missing()
```

---

### Error Handling

**Q1 - Multiple Choice:** What does this code print?
```python
try:
    x = int("abc")
except ValueError:
    print("A")
except Exception:
    print("B")
else:
    print("C")
finally:
    print("D")
```
- A) A then D
- B) B then D
- C) A then C then D
- D) B then C then D
**A:** A — `int("abc")` raises `ValueError`, caught by the first except. `else` only runs if no exception. `finally` always runs. Output: A then D.

**Q2 - Spot the Bug:** What's wrong with this error handling?
```python
def read_config(path):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        pass
```
**A:** Bare `except Exception` with `pass` silently swallows ALL errors — file not found, permission denied, invalid JSON, etc. The caller has no idea anything went wrong. Should catch specific exceptions and either log/raise or return a meaningful default.

**Q3 - Code Writing:** Write a function that reads a JSON file and returns the data, with proper error handling for file-not-found and invalid JSON.
**A:**
```python
def read_json(path: str) -> dict | None:
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File not found: {path}")
        return None
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in {path}: {e}")
        return None
```

---

### Decorators

**Q1 - Conceptual:** What does a decorator do in Python? Describe it without using the `@` syntax.
**A:** A decorator is a function that takes another function as input, wraps it with additional behavior, and returns the modified function. `@my_dec` above `def foo()` is equivalent to writing `foo = my_dec(foo)`.

**Q2 - Spot the Bug:** What's wrong with this decorator?
```python
def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"Took {time.time() - start}s")
```
**A:** The decorator never returns `wrapper`, so applying `@timer` makes the decorated function `None`. Missing `return wrapper` at the end of `timer`, and missing `return result` inside `wrapper`.

**Q3 - Predict the Output:** What does this print?
```python
def double_result(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs) * 2
    return wrapper

@double_result
def add(a, b):
    return a + b

print(add(3, 5))
```
**A:** `16` — `add(3, 5)` returns `8`, then the decorator doubles it to `16`.

**Q4 - Code Writing:** Write a decorator called `lowercase` that converts the return value of a function to lowercase.
**A:**
```python
def lowercase(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result.lower()
    return wrapper
```

**Q5 - Fill in the Blank:** Complete the decorator so the original function runs:
```python
def logger(func):
    def wrapper(*args, **kwargs):
        print("Before call")
        ____________________
        print("After call")
        return result
    return wrapper
```
**A:** `result = func(*args, **kwargs)`

---

### *args and **kwargs

**Q1 - Conceptual:** What types are `*args` and `**kwargs` collected into inside a function?
**A:** `*args` is a **tuple** of positional arguments. `**kwargs` is a **dictionary** of keyword arguments.

**Q2 - Predict the Output:** What does this print?
```python
def show(*args, **kwargs):
    print(len(args), len(kwargs))

show(1, 2, 3, x=10, y=20)
```
**A:** `3 2` — three positional args in the tuple, two keyword args in the dict.

**Q3 - Spot the Bug:** Why will this decorator fail for `greet("Alice", greeting="Hi")`?
```python
def log(func):
    def wrapper(name):
        print("Logging")
        return func(name)
    return wrapper

@log
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}"
```
**A:** The wrapper hardcodes a single parameter `name`, so it can't accept the `greeting` keyword argument. It should use `*args, **kwargs` instead.

**Q4 - Code Writing:** Write a function `combine` that accepts any number of strings and joins them with a separator keyword argument (default `" "`).
**A:**
```python
def combine(*args, separator=" "):
    return separator.join(args)
```

---

### functools.wraps

**Q1 - Conceptual:** What problem does `@functools.wraps(func)` solve?
**A:** Without it, the wrapper function replaces the original function's `__name__`, `__doc__`, and other metadata. `@wraps(func)` copies the original function's metadata onto the wrapper so introspection, `help()`, and debugging show the correct information.

**Q2 - Predict the Output:** What does this print?
```python
from functools import wraps

def bold(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return f"**{func(*args, **kwargs)}**"
    return wrapper

@bold
def title():
    """Return the page title."""
    return "Home"

print(title.__name__)
print(title.__doc__)
```
**A:** `title` and `Return the page title.` — `@wraps` preserved the original function's name and docstring.

**Q3 - Predict the Output:** What changes if `@wraps(func)` is removed from the decorator above?
**A:** `title.__name__` would print `wrapper` and `title.__doc__` would print `None` — the wrapper's metadata replaces the original.

---

### Decorator Factories

**Q1 - Conceptual:** How many levels of nesting does a decorator factory require, and what does each level receive?
**A:** Three levels: (1) the factory receives the configuration argument, (2) the decorator receives the function, (3) the wrapper receives the call arguments.

**Q2 - Spot the Bug:** What's wrong with this decorator factory?
```python
def repeat(n):
    def wrapper(*args, **kwargs):
        for _ in range(n):
            result = func(*args, **kwargs)
        return result
    return wrapper

@repeat(3)
def say_hi():
    print("hi")
```
**A:** Missing the middle nesting level. `repeat(n)` returns `wrapper` directly, but `wrapper` references `func` which is never defined. Needs a `decorator(func)` level between `repeat` and `wrapper`.

**Q3 - Code Writing:** Write a decorator factory `tag(name)` that wraps a function's string return value in an HTML tag. Example: `@tag("b")` on a function returning `"hello"` produces `"<b>hello</b>"`.
**A:**
```python
from functools import wraps

def tag(name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return f"<{name}>{result}</{name}>"
        return wrapper
    return decorator
```

**Q4 - Fill in the Blank:** Complete this decorator factory:
```python
def retry(attempts):
    def ________(func):
        def wrapper(*args, **kwargs):
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if i == attempts - 1:
                        raise
        return wrapper
    return ________
```
**A:** `decorator` for both blanks — the middle level function that receives `func` and the return value of the factory.

---

### Class Decorators

**Q1 - Conceptual:** When you define a decorator as a method inside a class, why doesn't it take `self` as its first parameter?
**A:** The decorator runs at **class definition time**, before any instances exist. There is no instance to bind to `self`. The decorator receives only the function being decorated.

**Q2 - Spot the Bug:** What's wrong here?
```python
class Validator:
    def _check(self, func):
        def wrapped(obj, *args, **kwargs):
            print("Checking...")
            return func(obj, *args, **kwargs)
        return wrapped

    @_check
    def process(self, data):
        return data
```
**A:** `_check` has `self` as its first parameter, but decorators defined in a class body run at class definition time — there's no instance. Remove `self` from `_check`.

**Q3 - Predict the Output:** What does this print?
```python
class Formatter:
    def _upper(func):
        def wrapped(obj, *args, **kwargs):
            return func(obj, *args, **kwargs).upper()
        return wrapped

    @_upper
    def greet(self, name):
        return f"hello {name}"

f = Formatter()
print(f.greet("world"))
```
**A:** `HELLO WORLD` — the `_upper` decorator uppercases the return value. `obj` receives the instance (`self`).

---

### getattr() Dynamic Dispatch

**Q1 - Conceptual:** What does `getattr(obj, "method_name")` return?
**A:** It returns the attribute (method, property, or value) named `"method_name"` from `obj`. It's equivalent to `obj.method_name` but the name is a string, allowing dynamic lookup at runtime.

**Q2 - Code Writing:** Write a function `call_method(obj, name, *args)` that dynamically calls a method on `obj` by string name, passing any extra arguments.
**A:**
```python
def call_method(obj, name, *args):
    method = getattr(obj, name)
    return method(*args)
```

**Q3 - Predict the Output:** What does this print?
```python
class Math:
    def square(self, x):
        return x ** 2
    def cube(self, x):
        return x ** 3

m = Math()
for op in ["square", "cube"]:
    print(getattr(m, op)(4))
```
**A:** `16` then `64` — dynamically calls `m.square(4)` and `m.cube(4)`.

---

### Mutable Default Arguments

**Q1 - Predict the Output:** What does this print?
```python
def track(event, log=[]):
    log.append(event)
    return log

print(track("login"))
print(track("logout"))
print(track("login"))
```
**A:** `['login']`, then `['login', 'logout']`, then `['login', 'logout', 'login']` — the same list is reused across all calls because mutable defaults are created once at definition time.

**Q2 - Conceptual:** *When* does Python evaluate default argument values — at function definition or at each call?
**A:** At **function definition** time (when the `def` line executes). This is why mutable defaults like `[]` or `{}` are shared across calls.

**Q3 - Refactor:** Fix this function so each call gets an independent list:
```python
def add_tag(tag, tags=[]):
    tags.append(tag)
    return tags
```
**A:**
```python
def add_tag(tag, tags=None):
    if tags is None:
        tags = []
    tags.append(tag)
    return tags
```

**Q4 - Spot the Bug:** What's wrong with this cache?
```python
def fetch_data(url, cache={}):
    if url not in cache:
        cache[url] = requests.get(url).json()
    return cache[url]
```
**A:** The `cache={}` is a mutable default — it persists across calls, which here is actually the *intended* behavior (caching). But it's still a bug because: (1) the cache can never be cleared, (2) it survives across test runs causing flaky tests, (3) it's an implicit global. Use `None` sentinel and a class or module-level cache instead.

---

### None Sentinel Pattern

**Q1 - Conceptual:** Why should you use `is None` instead of `== None` when checking for the None sentinel?
**A:** `is` checks identity (is this the exact same object?), while `==` checks equality (do these have the same value?). `None` is a singleton, so `is` is both faster and more correct. An object could override `__eq__` to return `True` when compared to `None`, giving a false positive.

**Q2 - Fill in the Blank:** Complete the function:
```python
def create_user(name, permissions=None):
    if ________________:
        permissions = ["read"]
    return {"name": name, "permissions": permissions}
```
**A:** `permissions is None`

**Q3 - Predict the Output:** What does this print?
```python
def register(name, members=None):
    if members is None:
        members = []
    members.append(name)
    return members

a = register("Alice")
b = register("Bob")
print(a, b)
```
**A:** `['Alice'] ['Bob']` — each call creates a fresh list because of the None sentinel pattern. No leakage between calls.

---

### inspect.signature

**Q1 - Conceptual:** What does `inspect.signature(func)` return, and what can you learn from it?
**A:** It returns a `Signature` object describing the function's parameters — their names, default values, annotations, and kinds (positional, keyword, etc.).

**Q2 - Predict the Output:** What does this print?
```python
import inspect

def connect(host, port=5432, ssl=True):
    pass

sig = inspect.signature(connect)
for name, param in sig.parameters.items():
    if param.default is not inspect.Parameter.empty:
        print(f"{name}={param.default}")
```
**A:** `port=5432` then `ssl=True` — skips `host` because it has no default (its default is `Parameter.empty`).

**Q3 - Spot the Bug:** What's wrong with this check?
```python
import inspect

sig = inspect.signature(func)
for name, param in sig.parameters.items():
    if param.default is not None:
        print(f"{name} has a default")
```
**A:** Using `is not None` instead of `is not inspect.Parameter.empty`. Parameters without defaults don't have `None` as their default — they have the sentinel `inspect.Parameter.empty`. This check would miss parameters with `None` as an actual default and incorrectly flag parameters with no default.

---

### copy.deepcopy

**Q1 - Conceptual:** What's the difference between `copy.copy()` (shallow) and `copy.deepcopy()`?
**A:** Shallow copy creates a new outer object but shares references to nested objects. Deep copy recursively creates new copies of all nested objects. Modifying a nested object in a shallow copy affects the original; in a deep copy it doesn't.

**Q2 - Predict the Output:** What does this print?
```python
import copy

original = {"scores": [90, 85, 92]}
shallow = copy.copy(original)
shallow["scores"].append(100)
print(original["scores"])
```
**A:** `[90, 85, 92, 100]` — shallow copy shares the inner list, so appending to the copy also modifies the original.

**Q3 - Predict the Output:** What if we used `deepcopy` instead?
```python
import copy

original = {"scores": [90, 85, 92]}
deep = copy.deepcopy(original)
deep["scores"].append(100)
print(original["scores"])
```
**A:** `[90, 85, 92]` — deep copy created an independent copy of the nested list, so the original is untouched.

**Q4 - Spot the Bug:** What's wrong here?
```python
defaults = {"tags": ["python"], "active": True}
user_config = defaults
user_config["tags"].append("sql")
```
**A:** `user_config = defaults` doesn't copy anything — both variables point to the same dict. Appending to `user_config["tags"]` also modifies `defaults["tags"]`. Use `copy.deepcopy(defaults)` for an independent copy.

---

### Instance Attributes and self

**Q1 - Spot the Bug:** What's wrong with this class?
```python
class Timer:
    def __init__(self, seconds):
        seconds = seconds

    def display(self):
        print(f"{self.seconds} seconds remaining")
```
**A:** `seconds = seconds` assigns the parameter to itself — it doesn't store it on the instance. Should be `self.seconds = seconds`. Calling `display()` will raise `AttributeError`.

**Q2 - Predict the Output:** What does this print?
```python
class Tracker:
    def __init__(self):
        self.count = 0

    def tick(self):
        self.count += 1
        return self.count

t = Tracker()
print(t.tick(), t.tick(), t.tick())
```
**A:** `1 2 3` — each call increments `self.count` and returns the new value.

**Q3 - Conceptual:** Why must you use `self.attribute` to access instance data inside methods, rather than just `attribute`?
**A:** Without `self.`, Python looks for a local or global variable named `attribute`, not the instance's data. `self` explicitly refers to the current instance, so `self.attribute` accesses the value stored on that specific object.

---

### Class vs Instance Attributes

**Q1 - Predict the Output:** What does this print?
```python
class Server:
    MAX_CONNECTIONS = 100

    def __init__(self, name):
        self.name = name

a = Server("alpha")
b = Server("beta")
print(a.MAX_CONNECTIONS, b.MAX_CONNECTIONS)
print(a.name, b.name)
```
**A:** `100 100` then `alpha beta` — `MAX_CONNECTIONS` is shared (class attribute), `name` is unique per instance.

**Q2 - Spot the Bug:** What's wrong with this class?
```python
class ChatRoom:
    messages = []

    def post(self, msg):
        self.messages.append(msg)

room1 = ChatRoom()
room2 = ChatRoom()
room1.post("hello")
print(room2.messages)
```
**A:** `messages = []` is a class attribute, so all instances share the same list. `room2.messages` prints `["hello"]` even though only `room1` posted. Fix: initialize `self.messages = []` in `__init__`.

**Q3 - Conceptual:** Where should you define a constant like `PI = 3.14159` — as a class attribute or an instance attribute? Why?
**A:** As a class attribute. Constants are shared by all instances and never change per-object, so there's no reason to create separate copies. Access via `ClassName.PI` or `self.PI`.

---

### Abstract Base Classes

**Q1 - Predict the Output:** What happens when you run this?
```python
import abc

class Serializer(abc.ABC):
    @abc.abstractmethod
    def serialize(self, data) -> str:
        pass

s = Serializer()
```
**A:** `TypeError: Can't instantiate abstract class Serializer with abstract method serialize` — ABCs with abstract methods cannot be instantiated directly.

**Q2 - Spot the Bug:** Why doesn't this enforce the abstract method?
```python
import abc

class Database:
    @abc.abstractmethod
    def connect(self):
        pass

d = Database()
```
**A:** `Database` doesn't inherit from `abc.ABC`. Without that, `@abstractmethod` has no enforcement mechanism and `Database()` creates an instance without error.

**Q3 - Code Writing:** Define an abstract class `Exporter` with two abstract methods: `export(data)` returning `str` and `file_extension()` returning `str`.
**A:**
```python
import abc

class Exporter(abc.ABC):
    @abc.abstractmethod
    def export(self, data) -> str:
        pass

    @abc.abstractmethod
    def file_extension(self) -> str:
        pass
```

**Q4 - Conceptual:** What happens if a concrete class inherits from an ABC but doesn't implement all abstract methods?
**A:** Python raises `TypeError` when you try to instantiate the concrete class. It lists which abstract methods are still missing.

---

### __str__ Method

**Q1 - Spot the Bug:** Why does `print(p)` show `<__main__.Product object at 0x...>` instead of the expected string?
```python
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def _str_(self):
        return f"{self.name}: ${self.price:.2f}"
```
**A:** Single underscores `_str_` instead of double `__str__`. Python doesn't recognize it as the dunder method, so it falls back to the default object representation.

**Q2 - Code Writing:** Write a `__str__` method for a `Coordinate` class that displays as `"(x, y)"` format.
**A:**
```python
def __str__(self):
    return f"({self.x}, {self.y})"
```

**Q3 - Conceptual:** What's the difference between `__str__` and `__repr__`?
**A:** `__str__` is for human-readable display (used by `print()` and `str()`). `__repr__` is for unambiguous developer representation (used in the REPL and `repr()`). `__repr__` should ideally produce a string that could recreate the object. If only one is defined, `__repr__` is used as a fallback for `__str__`.

---

### Composition Over Inheritance

**Q1 - Conceptual:** What's the difference between composition ("has-a") and inheritance ("is-a")?
**A:** Inheritance means a class extends another — a `Dog` *is an* `Animal`. Composition means a class contains another as an attribute — a `Car` *has an* `Engine`. Composition is more flexible because you can swap components without changing the class hierarchy.

**Q2 - Multiple Choice:** A `Playlist` manages a collection of `Song` objects. Which design is correct?
- A) `class Playlist(Song):`
- B) `class Playlist(list):`
- C) `class Playlist:` with `self.songs = []` in `__init__`
- D) `class Song(Playlist):`
**A:** C — a Playlist *has* songs (composition). It's not a Song, and inheriting from `list` exposes too many internals.

**Q3 - Refactor:** What's wrong with this design?
```python
class Garage(Car):
    def __init__(self):
        super().__init__()
        self.cars = []
```
**A:** A Garage is not a Car — this is incorrect inheritance. A Garage *has* cars. Should be `class Garage:` with `self.cars = []`, no inheritance from `Car`.

---

### isinstance() and Polymorphism

**Q1 - Predict the Output:** What does this print?
```python
class Animal:
    pass

class Dog(Animal):
    pass

d = Dog()
print(isinstance(d, Dog))
print(isinstance(d, Animal))
print(type(d) == Animal)
```
**A:** `True`, `True`, `False` — `isinstance` checks inheritance (Dog is-a Animal), but `type()` checks the exact class only.

**Q2 - Code Writing:** Given a list of mixed objects, write a one-liner that returns only the strings.
```python
items = [42, "hello", 3.14, "world", True, "foo"]
```
**A:**
```python
strings = [x for x in items if isinstance(x, str)]
```

**Q3 - Conceptual:** Why is `isinstance()` preferred over `type()` for type checking?
**A:** `isinstance()` respects inheritance — it returns `True` for instances of subclasses. `type()` only matches the exact class. Using `isinstance()` supports polymorphism and doesn't break when someone subclasses your types.

---

### @property Decorator

**Q1 - Predict the Output:** What does this print?
```python
class Square:
    def __init__(self, side):
        self.side = side

    @property
    def area(self):
        return self.side ** 2

s = Square(5)
print(s.area)
print(type(s.area))
```
**A:** `25` then `<class 'int'>` — `area` is accessed like an attribute (no parentheses) but computed by the method.

**Q2 - Spot the Bug:** What's wrong here?
```python
s = Square(5)
print(s.area())
```
**A:** `area` is a `@property`, so `s.area` already returns the value (an `int`). Adding `()` tries to call `25()`, which raises `TypeError: 'int' object is not callable`.

**Q3 - Conceptual:** When would you use `@property` instead of a regular method?
**A:** When the value is computed from existing attributes and should feel like accessing data rather than performing an action. Properties are good for derived/calculated values like `area`, `full_name`, or `is_valid` — things the caller thinks of as attributes, not operations.

**Q4 - Code Writing:** Add a `@property` called `is_empty` to a class with a `self.items` list that returns `True` when the list has no elements.
**A:**
```python
@property
def is_empty(self):
    return len(self.items) == 0
```

---

## Pythonic Code

### Idiomatic Patterns

**Q1 - Refactor:** Rewrite this in a more Pythonic way:
```python
result = []
for i in range(len(names)):
    if len(names[i]) > 3:
        result.append(names[i].upper())
```
**A:**
```python
result = [name.upper() for name in names if len(name) > 3]
```
Uses list comprehension instead of manual loop with `range(len())` and `.append()`.

**Q2 - Multiple Choice:** Which is the Pythonic way to swap two variables?
- A) `temp = a; a = b; b = temp`
- B) `a, b = b, a`
- C) `a = a ^ b; b = a ^ b; a = a ^ b`
- D) `swap(a, b)`
**A:** B — Python supports tuple unpacking for swaps. No temp variable needed.

**Q3 - Refactor:** Make this more Pythonic:
```python
found = False
for item in inventory:
    if item['status'] == 'available':
        found = True
        break
if found:
    print("Item available")
```
**A:**
```python
if any(item['status'] == 'available' for item in inventory):
    print("Item available")
```
Uses `any()` with a generator expression instead of a flag variable.

**Q4 - Predict the Output:** What does this print?
```python
names = ['alice', 'bob', 'charlie']
greeting = ', '.join(name.title() for name in names)
print(greeting)
```
**A:** `Alice, Bob, Charlie` — `.join()` with a generator expression, `.title()` capitalizes first letter of each word.

**Q5 - Spot the Bug:** What's wrong here?
```python
data = {'a': 1, 'b': 2, 'c': 3}
for key in data:
    if data[key] < 2:
        del data[key]
```
**A:** Modifying a dictionary while iterating over it — raises `RuntimeError: dictionary changed size during iteration`. Fix:
```python
data = {k: v for k, v in data.items() if v >= 2}
```

---

### PEP 8 and Style

**Q1 - Multiple Choice:** Which follows PEP 8 naming conventions?
- A) `class user_account:` / `def GetBalance():`
- B) `class UserAccount:` / `def get_balance():`
- C) `class User_Account:` / `def getBalance():`
- D) `class useraccount:` / `def get_balance():`
**A:** B — PEP 8 uses `CamelCase` for classes and `snake_case` for functions/methods.

**Q2 - Refactor:** Fix the PEP 8 issues:
```python
import os,sys
from collections import *
x=  10
y =20
if(x==10):
    print ( "yes" )
```
**A:**
```python
import os
import sys

x = 10
y = 20
if x == 10:
    print("yes")
```
Issues: imports on one line, wildcard import, inconsistent spacing around `=`, unnecessary parentheses in `if`, spaces inside `print()` parens.

**Q3 - Conceptual:** What is the maximum recommended line length in PEP 8, and what are your options when a line is too long?
**A:** 79 characters (72 for docstrings/comments). Options: implicit line continuation inside brackets/parens, backslash continuation (less preferred), or break the expression into smaller parts with intermediate variables.

**Q4 - Multiple Choice:** What's the correct import order per PEP 8?
- A) Third-party, standard library, local
- B) Local, standard library, third-party
- C) Standard library, third-party, local
- D) Alphabetical regardless of source
**A:** C — Standard library first, then third-party, then local/project imports. Each group separated by a blank line.

---

### lambda with Built-in Functions

**Q1 - Code Writing:** Given a list of tuples `students = [("Alice", 88), ("Bob", 95), ("Carol", 72)]`, use `max()` with a `lambda` to find the student with the highest score.
**A:**
```python
top = max(students, key=lambda s: s[1])
```

**Q2 - Predict the Output:** What does this print?
```python
words = ["fig", "banana", "apple", "kiwi"]
result = sorted(words, key=lambda w: len(w))
print(result)
```
**A:** `['fig', 'kiwi', 'apple', 'banana']` — sorted by string length, shortest first.

**Q3 - Spot the Bug:** Why does this raise an error?
```python
class Task:
    def __init__(self, name, priority):
        self.name = name
        self.priority = priority

tasks = [Task("a", 3), Task("b", 1), Task("c", 2)]
urgent = max(tasks)
```
**A:** Python doesn't know how to compare `Task` objects. `max()` needs a `key` parameter: `max(tasks, key=lambda t: t.priority)`.

**Q4 - Code Writing:** Use `sum()` with a generator expression to calculate the total price from a list of dicts: `items = [{"name": "A", "price": 10}, {"name": "B", "price": 25}, {"name": "C", "price": 8}]`.
**A:**
```python
total = sum(item["price"] for item in items)
```

---

### List Comprehension Filtering

**Q1 - Refactor:** Rewrite this using a list comprehension:
```python
result = []
for word in words:
    if len(word) >= 4:
        result.append(word.upper())
```
**A:**
```python
result = [word.upper() for word in words if len(word) >= 4]
```

**Q2 - Spot the Bug:** What's wrong with this approach?
```python
names = ["Alice", "Bob", "Charlie", "Dave"]
for name in names:
    if len(name) < 4:
        names.remove(name)
print(names)
```
**A:** Modifying a list while iterating over it. `remove()` shifts elements, causing items to be skipped. Result is unpredictable. Fix: `names = [n for n in names if len(n) >= 4]`.

**Q3 - Predict the Output:** What does this print?
```python
nums = range(1, 11)
result = [n ** 2 for n in nums if n % 3 == 0]
print(result)
```
**A:** `[9, 36, 81]` — squares of 3, 6, and 9 (the multiples of 3 from 1-10).

---

## Docker

### Container Basics

**Q1 - Conceptual:** What is the difference between a Docker image and a Docker container?
**A:** An image is a read-only template with instructions for creating a container (like a class). A container is a running instance of an image (like an object). You can run multiple containers from the same image.

**Q2 - Multiple Choice:** Which command runs a container from the `python:3.12` image, maps port 8000 on the host to port 5000 in the container, and removes it when it stops?
- A) `docker run -p 8000:5000 --rm python:3.12`
- B) `docker run -p 5000:8000 --rm python:3.12`
- C) `docker start -p 8000:5000 --rm python:3.12`
- D) `docker run --port 8000:5000 --remove python:3.12`
**A:** A — `-p host:container`, `--rm` auto-removes on stop. `-p` format is `host_port:container_port`.

**Q3 - Conceptual:** What is the difference between `CMD` and `ENTRYPOINT` in a Dockerfile?
**A:** `CMD` provides default arguments that can be overridden at run time. `ENTRYPOINT` sets the main executable and is harder to override. They're often used together: `ENTRYPOINT` defines the command, `CMD` provides default arguments.

**Q4 - Spot the Bug:** What's wrong with this Dockerfile?
```dockerfile
FROM python:3.12
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app
CMD ["python", "app.py"]
```
**A:** `COPY . /app` appears twice. The first copy happens before `pip install`, so any code change invalidates the dependency cache. Better approach: copy `requirements.txt` first, install deps, then copy the rest:
```dockerfile
FROM python:3.12
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

**Q5 - Conceptual:** What does `docker exec -it <container> /bin/bash` do?
**A:** Opens an interactive bash shell inside a running container. `-i` keeps STDIN open (interactive), `-t` allocates a pseudo-TTY (terminal). Useful for debugging.

---

### Docker Compose

**Q1 - Conceptual:** What problem does Docker Compose solve?
**A:** Docker Compose lets you define and run multi-container applications with a single YAML file (`docker-compose.yml`). Instead of running multiple `docker run` commands with all their flags, you define services, networks, and volumes declaratively.

**Q2 - Code Writing:** Write a basic `docker-compose.yml` that runs a Python web app and a PostgreSQL database.
**A:**
```yaml
services:
  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
  db:
    image: postgres:16
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

**Q3 - Multiple Choice:** What does `docker compose up -d` do?
- A) Builds images and starts containers in debug mode
- B) Builds images and starts containers in detached (background) mode
- C) Downloads images only
- D) Starts containers and deletes them when stopped
**A:** B — `-d` means detached mode, containers run in the background.

**Q4 - Conceptual:** What is a Docker volume and why would you use one?
**A:** A volume is a persistent storage mechanism managed by Docker. Container filesystems are ephemeral — data is lost when the container is removed. Volumes persist data beyond the container lifecycle. Used for databases, config files, and any data you need to keep.

---

## PMP Topics

*Source: TIA Education Group PDFs (PM+Terms, PM+Principles, PM+Domains, PM+Processes)*

### Core Definitions (PM+Terms)

**Q1 - Multiple Choice:** What are the three characteristics of a project?
- A) Funded, Staffed, Scheduled
- B) Unique, Temporary, Progressively Elaborated
- C) Planned, Executed, Closed
- D) Scoped, Budgeted, Delivered
**A:** B — A project is a temporary endeavor that produces a unique product, service, or result. It is temporary (definite beginning and ending) and progressively elaborated.

**Q2 - Multiple Choice:** What is the difference between a project, a program, and a portfolio?
- A) They are different names for the same thing
- B) A project is temporary work; a program is related projects managed together; a portfolio is programs and projects achieving strategic objectives
- C) A project is small; a program is medium; a portfolio is large
- D) A project has one PM; a program has two; a portfolio has three
**A:** B — A project may or may not be part of a program, but a program will always have projects. A portfolio is a collection of projects, programs, and subsidiary portfolios managed to achieve strategic (long-term) objectives.

**Q3 - Multiple Choice:** What is the difference between operations management and project management?
- A) There is no difference
- B) Operations deals with ongoing production of goods/services; projects are temporary endeavors
- C) Operations are temporary; projects are permanent
- D) Operations only happen in manufacturing
**A:** B — Operations management deals with the ongoing production of goods and/or services. Projects are temporary and produce unique results.

**Q4 - Multiple Choice:** A project takes a company from a current state to a desired state. What is this concept called?
- A) Progressive elaboration
- B) Projects enable changes
- C) Operations management
- D) Portfolio alignment
**A:** B — Projects can be a vehicle for change in an organization, taking a company from its current state to a desired state.

**Q5 - Multiple Choice:** What is a deliverable?
- A) A project management plan
- B) Any unique and verifiable product, service, or result that must be accepted by the customer or sponsor
- C) The final project report
- D) A status update sent to stakeholders
**A:** B — A deliverable is any unique and verifiable product, service, or result. It may be tangible or intangible and must be accepted by the customer or sponsor for the phase.

**Q6 - Multiple Choice:** What is a phase in project management?
- A) A single task
- B) A collection of logically related project activities that culminates in the completion of one or more deliverables
- C) A project management methodology
- D) A meeting with stakeholders
**A:** B — The number of phases depends on the industry type and size/complexity of the project.

**Q7 - Multiple Choice:** What are the three pillars of Project Governance?
- A) Scope, Schedule, Cost
- B) Structure, People, Information
- C) Planning, Execution, Closing
- D) Risk, Quality, Resources
**A:** B — Project Governance is the framework within which project decisions are made, based on Structure, People, and Information.

**Q8 - Multiple Choice:** What is a milestone?
- A) A task that takes exactly one day
- B) A significant event or achievement that marks a key point or completion of a major deliverable
- C) A meeting with the sponsor
- D) A budget checkpoint
**A:** B — A milestone marks a key point or completion of a major deliverable. Task duration refers to the amount of time to complete a specific task or activity.

---

### Project Roles and Stakeholders (PM+Terms)

**Q1 - Multiple Choice:** What is the primary responsibility of a project sponsor?
- A) Managing the day-to-day project tasks
- B) Funding the project and making key decisions
- C) Writing the project schedule
- D) Managing the project team's performance reviews
**A:** B — The sponsor is the project champion who funds the project and makes decisions. They can be internal or external to the organization.

**Q2 - Multiple Choice:** Which role is senior to the project manager and may be responsible for several projects at the same time?
- A) Sponsor
- B) Functional Manager
- C) Program Manager
- D) Product Manager
**A:** C — The Program Manager is senior to the project manager, may oversee several projects simultaneously, and helps resolve conflicts in the project.

**Q3 - Multiple Choice:** What is the hierarchy of project roles from strongest to weakest authority?
- A) Expeditor → Coordinator → Manager
- B) Manager → Coordinator → Expeditor
- C) Coordinator → Manager → Expeditor
- D) Manager → Expeditor → Coordinator
**A:** B — Project Manager (empowered to lead, authorized to make decisions, responsible for success/failure) → Project Coordinator (weaker, may be authorized to make decisions) → Project Expeditor (weakest role, very limited decision ability).

**Q4 - Multiple Choice:** Which of the following is NOT one of the 6 roles of a Project Manager?
- A) Initiator
- B) Negotiator
- C) Budget Analyst
- D) Facilitator
**A:** C — The 6 PM roles are: Initiator, Negotiator, Listener, Coach, Working Member, and Facilitator.

**Q5 - Multiple Choice:** What is a stakeholder?
- A) Only the project team members
- B) An individual, group, or organization that may affect, be affected, or perceive to be affected by the project
- C) Only the project sponsor
- D) Only the customer
**A:** B — Key stakeholders include: Project Manager, Customer, Project Team, Project Sponsor, and Functional Manager (who generally controls resources).

**Q6 - True/False:** Project management and product management are the same thing.
**A:** False. Project management focuses on delivering specific projects within scope, timeline, and budget. Product management is the broader discipline. Project management is one component of product development.

---

### PMO and Organizational Structures (PM+Terms)

**Q1 - Multiple Choice:** What are the three types of Project Management Office (PMO)?
- A) Small, Medium, Large
- B) Supportive, Controlling, Directive
- C) Functional, Matrix, Projectized
- D) Strategic, Tactical, Operational
**A:** B — Supportive (provides templates, training, lessons learned), Controlling (determines framework/methodology and specific forms), Directive (controls the project; PM is assigned and reports to the PMO).

**Q2 - Multiple Choice:** In which organizational structure does the project manager have "little to no" authority?
- A) Strong Matrix
- B) Projectized
- C) Functional
- D) Balanced Matrix
**A:** C — In a Functional organization, the PM has little/no authority and budget is controlled by the functional manager. Team members report directly to the functional manager.

**Q3 - Multiple Choice:** In which organizational structure does the PM have the greatest amount of authority?
- A) Functional
- B) Weak Matrix
- C) Balanced Matrix
- D) Projectized
**A:** D — In a Projectized organization, the PM has the greatest authority (High/Total). The team is assigned full-time and moves to other assignments when the project is complete.

**Q4 - Multiple Choice:** What are the three types of matrix organizations?
- A) Small, Medium, Large
- B) Weak, Balanced, Strong
- C) Simple, Complex, Hybrid
- D) Functional, Operational, Strategic
**A:** B — Weak, Balanced, and Strong. They differ in the PM's authority relative to the functional manager's authority.

**Q5 - Multiple Choice:** In a Functional organization, who controls the budget?
- A) The Project Manager
- B) The Functional Manager
- C) The Sponsor
- D) The budget is shared equally
**A:** B — In a Functional organization, budget controls rest with the Functional Manager.

---

### Project Life Cycle and Approaches (PM+Terms)

**Q1 - Multiple Choice:** What are the three main types of project life cycle approaches?
- A) Fast, Medium, Slow
- B) Plan-Driven/Predictive, Change-Driven/Adaptive, Hybrid
- C) Waterfall, Scrum, Kanban
- D) Simple, Complex, Critical
**A:** B — The Project Life Cycle can be Plan-Driven/Predictive/Traditional, Change-Driven (Iterative, Incremental, Adaptive), or Hybrid.

**Q2 - Multiple Choice:** Which project management approach emphasizes "extensive upfront planning" and "limited changes with a well-defined change control process"?
- A) Adaptive
- B) Agile
- C) Predictive
- D) Kanban
**A:** C — The Predictive approach follows a linear and sequential process with emphasis on control, documentation, and limited flexibility.

**Q3 - Multiple Choice:** Which of the following is NOT a characteristic of the Adaptive approach?
- A) Self-organizing teams
- B) Sequential execution
- C) Customer collaboration
- D) Iterative and incremental development
**A:** B — Sequential execution is Predictive. Adaptive uses iterative/incremental development with self-organizing teams and customer collaboration.

---

### Issues, Risks, Assumptions, and Constraints (PM+Terms)

**Q1 - Multiple Choice:** A team member says "We assume the vendor will deliver materials by March 15th." What is this classified as?
- A) A Risk
- B) An Issue
- C) An Assumption
- D) A Constraint
**A:** C — An Assumption is a statement or belief considered to be true for planning purposes but hasn't been proven.

**Q2 - Multiple Choice:** What is the key difference between a Risk and an Issue?
- A) Risks are positive; issues are negative
- B) Risks may occur in the future; issues have already arisen
- C) Risks affect scope; issues affect schedule
- D) There is no difference
**A:** B — Risks are potential future events. Issues are problems that have already arisen during the project.

**Q3 - Multiple Choice:** Which of the following is NOT one of the 6 project constraints?
- A) Scope
- B) Schedule
- C) Stakeholders
- D) Quality
**A:** C — The 6 constraints are Scope, Schedule, Cost, Risk, Quality, and Resources. They are interrelated — changing one affects the others.

**Q4 - Multiple Choice:** The vendor notifies the team they will be 2 weeks late. This was previously an assumption that they'd deliver on time. What has it become?
- A) A constraint
- B) A risk
- C) An issue
- D) It's still an assumption
**A:** C — An Issue. The assumption (believed true) had a risk (might not deliver). Now that late delivery has occurred, it's an issue.

---

### Areas of a Project (PM+Terms)

**Q1 - Multiple Choice:** Which project area is concerned with "acquiring resources from outside the project team"?
- A) Resources
- B) Communications
- C) Procurements
- D) Stakeholders' Engagement
**A:** C — Procurements deals with acquiring resources from outside the project team.

**Q2 - Multiple Choice:** Which project area ensures "all stakeholders get the correct information at the right time"?
- A) Stakeholders' Engagement
- B) Quality
- C) Communications
- D) Risk
**A:** C — Communications ensures all stakeholders get the correct information at the right time.

**Q3 - True/False:** The 9 knowledge areas include Scope, Schedule, Cost, Quality, Resources, Communications, Risk, Procurements, and Stakeholders' Engagement.
**A:** True. These are the 9 key knowledge areas of a project.

---

### Emotional Intelligence (PM+Terms)

**Q1 - Multiple Choice:** What does Emotional Intelligence (EQ) refer to in project management?
- A) The ability to calculate project metrics accurately
- B) The ability to recognize, understand, and manage emotions in oneself and others
- C) The ability to create detailed project schedules
- D) The ability to negotiate contracts effectively
**A:** B — EQ involves self-awareness, empathy, and using emotions to guide thinking and behavior.

**Q2 - Multiple Choice:** Which of the following is NOT one of the 5 areas where EQ plays a significant role?
- A) Relationship Building
- B) Budget Forecasting
- C) Communication and Conflict Management
- D) Motivation and Influence
**A:** B — The 5 areas are: Relationship Building, Communication and Conflict Management, Motivation and Influence, Leadership and Decision Making, and Stakeholders Management.

---

### Leadership vs. Management (PM+Terms)

**Q1 - Multiple Choice:** According to PMI, Management "directs using positional power." What does Leadership use instead?
- A) Contractual authority
- B) Relational power (guide, influence, collaborate)
- C) Financial incentives
- D) Organizational hierarchy
**A:** B — Leadership uses relational power. Management directs using positional power.

**Q2 - Multiple Choice:** Which phrase is associated with Management (not Leadership)?
- A) "Do the right things"
- B) "Focus on long-range vision"
- C) "Do things right"
- D) "Challenge status quo"
**A:** C — "Do things right" is Management. Leadership "does the right things."

**Q3 - True/False:** Leadership should not be confused with authority.
**A:** True. Authority is the right to exercise power and control. Leadership is about inspiring and motivating toward a common goal.

---

### PMI Code of Ethics and Professional Conduct (PM+Principles)

**Q1 - Multiple Choice:** PMI's Code of Ethics is based on which four values?
- A) Integrity, Transparency, Quality, Efficiency
- B) Responsibility, Respect, Fairness, Honesty
- C) Trust, Accountability, Communication, Leadership
- D) Courage, Commitment, Focus, Openness
**A:** B — Responsibility, Respect, Fairness, and Honesty.

**Q2 - True/False:** Principles and morals are the same thing according to PMI.
**A:** False. Principles can, but do not necessarily, reflect morals. A code of ethics is related to morals.

---

### The 12 Principles of Project Management (PM+Principles)

**Q1 - Multiple Choice:** Which PM principle includes Integrity, Care, Trustworthiness, and Compliance?
- A) Demonstrate leadership behaviors
- B) Be a diligent, respectful, and caring steward
- C) Create a collaborative project team environment
- D) Focus on value
**A:** B — Stewardship includes Integrity (behave honestly), Care (fiduciaries of organizational matters), Trustworthiness (represent authority accurately), and Compliance (comply with laws/rules/regulations).

**Q2 - True/False:** Accountability can be shared among team members.
**A:** False. Accountability is NOT shared — one person is answerable for the outcome. Responsibility CAN be shared.

**Q3 - Multiple Choice:** What is the difference between Authority, Accountability, and Responsibility?
- A) They all mean the same thing
- B) Authority is the right to make decisions; Accountability is being answerable for an outcome (not shared); Responsibility is being obligated to do something (can be shared)
- C) Authority is for managers; Accountability is for teams; Responsibility is for sponsors
- D) Authority and Accountability are the same; Responsibility is different
**A:** B — Authority is the right to make decisions, establish procedures, apply resources, expend funds, or give approvals. Accountability is not shared. Responsibility can be shared.

**Q4 - Multiple Choice:** According to "Focus on Value," when can value be realized?
- A) Only at the end of the project
- B) Only after the project is complete
- C) Throughout the project, at the end, or after completion
- D) Only at predefined milestones
**A:** C — Value is the ultimate indicator of project success. A business case contains: business need, project justification, and business strategy.

**Q5 - Multiple Choice:** What does "Focus on Value" say about deliverables vs. outcomes?
- A) Deliverables are more important than outcomes
- B) Project teams should shift focus from deliverables to the intended outcomes to support value realization
- C) Outcomes don't matter if deliverables are completed
- D) Deliverables and outcomes are the same thing
**A:** B — To support value realization, project teams shift focus from deliverables to intended outcomes, delivering on the vision rather than simply creating a specific deliverable.

**Q6 - Multiple Choice:** Systems Thinking in project management means:
- A) Using the latest project management software tools
- B) Taking a holistic view of the project as a system with its own working parts
- C) Breaking the project into the smallest possible tasks
- D) Focusing only on internal processes
**A:** B — A project is a system of interdependent and interacting domains. Internal and external conditions continuously change, and a single change can create several impacts.

**Q7 - Multiple Choice:** What are the four common sources of complexity in projects?
- A) Scope, Schedule, Cost, Quality
- B) Human behavior, System behavior, Uncertainty and ambiguity, Technological innovation
- C) Stakeholders, Budget, Timeline, Resources
- D) Planning, Execution, Monitoring, Closing
**A:** B — Human behavior, System behavior, Uncertainty and ambiguity, and Technological innovation.

**Q8 - Multiple Choice:** What is the difference between Adaptability and Resiliency?
- A) They mean the same thing
- B) Adaptability is responding to change; Resiliency is recovering from setbacks
- C) Adaptability is for agile only; Resiliency is for predictive only
- D) Adaptability is a team skill; Resiliency is organizational
**A:** B — Adaptability is responding to changing conditions. Resiliency is absorbing impacts and recovering quickly from setbacks.

**Q9 - Multiple Choice:** Which principle states each project is unique and should use "just enough" process?
- A) Navigate complexity
- B) Optimize risk responses
- C) Tailor based on context
- D) Build quality into processes and deliverables
**A:** C — Design methods based on project needs. Use "just enough" process to maximize value, manage cost, and enhance speed.

**Q10 - True/False:** Risks can only be negative (threats).
**A:** False. Risks can be positive (opportunities) or negative (threats). Teams maximize positive risks and decrease exposure to negative risks.

**Q11 - Multiple Choice:** What three factors influence how an organization addresses risk?
- A) Budget, Schedule, Scope
- B) Risk attitude, Risk appetite, Risk threshold
- C) Sponsor preference, Team experience, Project size
- D) Industry standards, Legal requirements, Stakeholder demands
**A:** B — Risk attitude, risk appetite, and risk threshold.

**Q12 - Multiple Choice:** Who can demonstrate leadership on a project?
- A) Only the project manager
- B) Only senior management
- C) Any project team member
- D) Only the sponsor
**A:** C — Any project team member can demonstrate leadership behaviors. Effective leaders adapt their style to the situation.

**Q13 - True/False:** Effective change management uses a motivational strategy rather than a forceful one.
**A:** True. Too much change too fast leads to change fatigue and/or resistance.

**Q14 - Multiple Choice:** Quality in project management is primarily about:
- A) Using the most expensive materials
- B) Meeting the acceptance criteria for deliverables
- C) Completing the project as fast as possible
- D) Having zero defects
**A:** B — Meeting acceptance criteria, satisfying stakeholders' expectations, and fulfilling project and product requirements.

**Q15 - Multiple Choice:** What are the 12 Principles in order? (Select the correct first 6)
- A) Stewardship, Team, Stakeholders, Value, Systems, Leadership
- B) Planning, Executing, Monitoring, Controlling, Closing, Initiating
- C) Scope, Schedule, Cost, Quality, Risk, Resources
- D) Charter, Plan, Execute, Monitor, Close, Lessons Learned
**A:** A — (1) Be a diligent, respectful, and caring steward, (2) Create a collaborative project team environment, (3) Effectively engage with stakeholders, (4) Focus on value, (5) Recognize, evaluate, and respond to system interactions, (6) Demonstrate leadership behaviors. The remaining 6 are: (7) Tailor based on context, (8) Build quality into processes and deliverables, (9) Navigate complexity, (10) Optimize risk responses, (11) Embrace adaptability and resiliency, (12) Enable change to achieve the envisioned future state.

---

### Performance Domains (PM+Domains)

**Q1 - Multiple Choice:** How many Performance Domains are there in PMBOK 7th Edition?
- A) 5
- B) 8
- C) 10
- D) 12
**A:** B — The 8 Performance Domains are: Stakeholders, Team, Development Approach and Life Cycle, Planning, Project Work, Delivery, Measurement, and Uncertainty.

**Q2 - Multiple Choice:** What are the 5 steps of Effective Stakeholder Engagement (in order)?
- A) Plan, Execute, Monitor, Control, Close
- B) Identify, Understand, Analyze, Prioritize, Engage, Monitor
- C) Identify, Understand and Analyze, Prioritize, Engage, Monitor
- D) Define, Measure, Analyze, Improve, Control
**A:** C — Identify → Understand and Analyze → Prioritize → Engage → Monitor (continuous cycle).

**Q3 - Multiple Choice:** In the Stakeholder Performance Domain, what indicates stakeholders may NOT be engaged or aligned with project objectives?
- A) On-time deliverables
- B) A significant number of changes or modifications to scope and product requirements
- C) Positive stakeholder feedback
- D) Budget under-run
**A:** B — A significant number of scope/requirement changes may indicate stakeholders are not engaged or aligned.

**Q4 - Multiple Choice:** What are the three outcomes of the Team Performance Domain?
- A) On-time, On-budget, On-scope
- B) Shared ownership, A high-performing team, Appropriate leadership and interpersonal skills
- C) Hired staff, Trained staff, Retained staff
- D) Communication plan, RACI chart, Org chart
**A:** B — Shared ownership (all members know vision/objectives), high-performing team (trusts, collaborates, adapts), and appropriate leadership/interpersonal skills demonstrated by all.

**Q5 - Multiple Choice:** What is servant leadership?
- A) A leadership style where the PM makes all decisions
- B) A method based on understanding and addressing the needs and development of project team members
- C) A management approach focused on efficiency
- D) A style where team members serve the PM
**A:** B — Servant leaders focus on: Are team members growing? Are they becoming healthier, wiser, freer, and more autonomous? Behaviors include obstacle removal, diversion shield, and encouragement/development opportunities.

**Q6 - Multiple Choice:** Leadership can be centralized or distributed. What does "centralized" mean?
- A) All team members share accountability equally
- B) Accountability is assigned to one individual
- C) The team votes on decisions
- D) The sponsor makes all decisions
**A:** B — Centralized: accountability is assigned to one individual. Distributed: shared among a project management team and project team members.

**Q7 - Multiple Choice:** What does "delivery cadence" refer to in the Development Approach and Life Cycle Performance Domain?
- A) The project management methodology
- B) The timing and frequency of project deliverables
- C) The meeting schedule
- D) The sprint duration
**A:** B — Delivery cadence refers to the timing and frequency of project deliverables. Projects can have single, multiple, or periodic deliveries.

**Q8 - Multiple Choice:** Which three categories of factors influence the selection of a development approach?
- A) Cost, Time, Quality
- B) Product/service/result factors, Project factors, Organization factors
- C) Team size, Budget, Deadline
- D) Sponsor preference, Industry standard, Legal requirement
**A:** B — Product/service/result (innovation, requirements certainty, scope stability, risk, regulations), Project (stakeholders, schedule constraints, funding), Organization (structure, culture, capability, team size/location).

---

### Process Groups and Processes (PM+Processes)

**Q1 - Multiple Choice:** What are the 5 Process Groups?
- A) Define, Plan, Build, Test, Deploy
- B) Initiating, Planning, Executing, Monitoring & Controlling, Closing
- C) Scope, Schedule, Cost, Quality, Risk
- D) Start, Middle, End, Review, Archive
**A:** B — Initiating (2 processes), Planning (24 processes), Executing (10 processes), Monitoring & Controlling (12 processes), Closing (1 process).

**Q2 - Multiple Choice:** What are the two processes in the Initiating process group?
- A) Plan Scope Management and Collect Requirements
- B) Develop Project Charter and Identify Stakeholders
- C) Direct and Manage Project Work and Monitor and Control Project Work
- D) Develop Project Management Plan and Close Project or Phase
**A:** B — Develop Project Charter and Identify Stakeholders.

**Q3 - Multiple Choice:** What does the Project Charter formally do?
- A) Assigns team members to tasks
- B) Formally authorizes the existence of the project and assigns the PM and their authority level
- C) Defines the project schedule
- D) Establishes the project budget
**A:** B — The Project Charter is signed by senior management, contains high-level requirements and risks, preliminary budget and schedule, and project purpose/justification. The approved charter formally initiates the project.

**Q4 - Multiple Choice:** What are the two outputs of the "Develop Project Charter" process?
- A) Project Management Plan and Schedule
- B) Project Charter and Assumption Log
- C) Stakeholder Register and Risk Register
- D) WBS and Budget
**A:** B — The Project Charter and the Assumption Log (a list of things perceived to be true and things that might constrain the project).

**Q5 - Multiple Choice:** What is the Project Management Plan?
- A) Just a schedule
- B) A comprehensive document that outlines how the project is executed, monitored and controlled, and closed
- C) A list of team members
- D) The project budget
**A:** B — It contains 4 baselines (Scope, Schedule, Cost, Performance Measurement), 14 subsidiary plans, and is only changed when a change request is generated and approved by the change control board.

**Q6 - Multiple Choice:** What is the difference between Product Scope and Project Scope?
- A) They are the same thing
- B) Product Scope is features/functions of the product; Project Scope is the work needed to deliver it
- C) Product Scope is bigger; Project Scope is smaller
- D) Product Scope is for the customer; Project Scope is for the team
**A:** B — Product Scope = features and functions that characterize a product, service, or result. Project Scope = the work needed to deliver a product, service, or result with specified features.

**Q7 - Multiple Choice:** What is "Gold Plating" in project management?
- A) Using expensive materials
- B) Doing extra work not in the scope
- C) Adding a gold standard quality check
- D) Exceeding the budget
**A:** B — Gold Plating is doing extra work not in the scope. Scope Creep is unauthorized work added to the scope. Both should be prevented.

**Q8 - Multiple Choice:** The Salience Model categorizes stakeholders using which three dimensions?
- A) Cost, Schedule, Scope
- B) Power, Urgency, Legitimacy
- C) Interest, Influence, Impact
- D) Internal, External, Neutral
**A:** B — Power (level of authority), Urgency (immediate attention), Legitimacy (how appropriate is their involvement).

**Q9 - Multiple Choice:** What are the four Directions of Influence for stakeholders?
- A) North, South, East, West
- B) Upward, Downward, Outward, Sideward
- C) Internal, External, Positive, Negative
- D) High, Medium, Low, None
**A:** B — Upward (senior management), Downward (team members), Outward (vendors, government, public, end-users), Sideward (peers such as other project managers).

**Q10 - Multiple Choice:** What information should a Stakeholder Register contain?
- A) Only names and phone numbers
- B) Contact info, role, communication requirements, expectations, how affected, and power/influence level
- C) Only their approval authority
- D) Only their department
**A:** B — The Stakeholder Register contains contact information, role (team member, sponsor, functional manager), communication requirements, expectations, how affected by project, and power/influence level.

---

## Adding Questions

To add a new question, use this format:

```
**Q[N] - [Type]:** [Question text]
**A:** [Answer]
```

Types: Conceptual, Code Output, Code Writing, Compare/Contrast, Multiple Choice, True/False

---

*Question bank managed by MARVIN quiz skill*
