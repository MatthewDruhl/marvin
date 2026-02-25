# Question Bank

Last updated: 2026-02-24

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

## Adding Questions

To add a new question, use this format:

```
**Q[N] - [Type]:** [Question text]
**A:** [Answer]
```

Types: Conceptual, Code Output, Code Writing, Compare/Contrast

---

*Question bank managed by MARVIN quiz skill*
