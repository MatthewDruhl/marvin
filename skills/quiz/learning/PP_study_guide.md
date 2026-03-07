# PP — CodeSignal Assessment Prep Study Guide

This guide covers the core skills you'll need for the 4 practice problems. Each section teaches a concept in isolation so you can apply it yourself when coding the solutions.

---

## 1. String Searching (Manual Substring Matching)

### What It Is

When you can't use `str.find()` or `str.index()`, you need to search for a substring by sliding a window across the string and comparing character by character. This is the naive string search algorithm — it checks every possible starting position in the main string and compares the substring at that position.

### Syntax

```python
# The sliding window pattern for substring search
def search(text: str, pattern: str) -> int:
    # Outer loop: every valid starting position
    for i in range(len(text) - len(pattern) + 1):  # stop early — pattern can't fit past here
        # Inner check: does the slice at position i match the pattern?
        if text[i:i + len(pattern)] == pattern:     # string slicing does the comparison
            return i                                  # found it — return the index
    return -1                                         # exhausted all positions, not found
```

**Key detail:** The range is `len(text) - len(pattern) + 1`. If `text` is 10 chars and `pattern` is 3, you only need to check positions 0–7 (8 positions). Starting at position 8 or later, there aren't enough characters left for the pattern to fit.

### Mini Example

```python
text = "abcdef"
pattern = "cde"

# i=0: "abc" != "cde"
# i=1: "bcd" != "cde"
# i=2: "cde" == "cde" → return 2
# i=3: never reached
```

### Common Mistake

```python
# WRONG — range goes too far, causes index errors or misses the +1
for i in range(len(text)):
    if text[i:i + len(pattern)] == pattern:
        return i

# RIGHT — stop when pattern can't fit anymore
for i in range(len(text) - len(pattern) + 1):
    if text[i:i + len(pattern)] == pattern:
        return i
```

The wrong version technically works in Python because slicing past the end just returns a shorter string (so it won't crash), but it's wasteful and shows a misunderstanding of the bounds. More importantly, when you switch to character-by-character comparison instead of slicing, incorrect bounds *will* cause bugs.

### Edge Cases to Watch

- **Empty substring:** What should `search("hello", "")` return? Think about this before coding.
- **Empty string:** `search("", "abc")` should return -1.
- **Overlapping matches:** `"aaa"` contains `"aa"` starting at index 0 AND index 1. When finding all occurrences, advance by 1 (not by `len(pattern)`).

---

## 2. String Case Conversion for Comparison

### What It Is

When comparing strings case-insensitively, convert both strings to the same case (typically lowercase) before comparing. The key insight: convert for comparison, but return indices from the *original* string.

### Syntax

```python
s_lower = s.lower()          # convert entire string to lowercase
sub_lower = substring.lower()

# Now search in the lowered versions
for i in range(len(s_lower) - len(sub_lower) + 1):
    if s_lower[i:i + len(sub_lower)] == sub_lower:
        return i  # return index — it's the same in both original and lowered string
```

### Mini Example

```python
s = "Hello World"
sub = "LO WO"

s_lower = "hello world"
sub_lower = "lo wo"

# Search "lo wo" in "hello world" → found at index 3
# Return 3 (valid in both original and lowered string)
```

### Common Mistake

```python
# WRONG — converting character by character inside the loop (inefficient)
for i in range(len(s)):
    if s[i].lower() == substring[0].lower():
        # then check rest...

# RIGHT — convert once, search in the converted strings
s_lower = s.lower()
sub_lower = substring.lower()
# then use the same search pattern as before
```

---

## 3. Whitespace Splitting and Word Counting

### What It Is

Python's `str.split()` (with no arguments) splits on any whitespace and ignores leading/trailing/multiple spaces. This is incredibly useful, but some problems ask you to demonstrate understanding of *how* this works. The concept: iterate through characters, track whether you're inside a word, and count transitions from whitespace to non-whitespace.

### Syntax

```python
# The state-tracking approach
def count_words(s: str) -> int:
    count = 0
    in_word = False              # track state: are we currently inside a word?

    for char in s:
        if char.isspace():       # whitespace characters: ' ', '\t', '\n', '\r'
            in_word = False      # we've left the word
        elif not in_word:        # non-space AND we weren't in a word
            count += 1           # we just entered a new word
            in_word = True       # now we're in a word

    return count
```

### Mini Example

```python
s = "  hello   world  "
# Char-by-char:
#   ' ' ' ' → whitespace, in_word stays False
#   'h'     → not space, not in_word → count=1, in_word=True
#   'e' 'l' 'l' 'o' → not space, in_word=True → skip
#   ' ' ' ' ' ' → whitespace → in_word=False
#   'w'     → not space, not in_word → count=2, in_word=True
#   'o' 'r' 'l' 'd' → skip
#   ' ' ' ' → whitespace → in_word=False
# Result: 2
```

### Common Mistake

```python
# WRONG — counting spaces instead of words
count = s.count(" ") + 1  # fails for "  hello   world  " → gives 7

# WRONG — splitting and counting empties
count = len(s.split(" "))  # split on single space, gets empty strings

# RIGHT — use .split() with no args (handles all whitespace)
count = len(s.split())  # but the problem may restrict this!
```

**Note:** `s.split(" ")` and `s.split()` are different. The former splits only on single spaces and keeps empty strings. The latter splits on any whitespace and discards empties.

---

## 4. Stripping Punctuation from Words

### What It Is

When processing text for word frequency, you often need to remove punctuation so `"hello,"` and `"hello"` are treated as the same word. Python's `str.strip()` method removes characters from the start and end of a string.

### Syntax

```python
punctuation = ".,!?;:"

word = "hello!"
clean = word.strip(punctuation)  # "hello" — removes matching chars from both ends

word2 = "...yes..."
clean2 = word2.strip(punctuation)  # "yes"

word3 = "don't"
clean3 = word3.strip(punctuation)  # "don't" — apostrophe not in our set, stays
```

### Mini Example

```python
sentence = "Hello, world! Hello."
words = sentence.split()          # ["Hello,", "world!", "Hello."]
punctuation = ".,!?;:"

cleaned = []
for w in words:
    clean = w.strip(punctuation).lower()  # strip punct, then lowercase
    if clean:                              # skip if stripping left an empty string
        cleaned.append(clean)

# cleaned = ["hello", "world", "hello"]
```

### Common Mistake

```python
# WRONG — using replace() removes punctuation from INSIDE words too
word = "can't!"
word.replace("!", "").replace("'", "")  # "cant" — destroyed the apostrophe

# RIGHT — strip() only removes from the edges
word.strip(".,!?;:")  # "can't" — apostrophe in the middle is preserved
```

---

## 5. Frequency Counting with Dictionaries

### What It Is

A frequency map (also called a histogram or counter) tracks how many times each element appears. Python offers several approaches: manual `dict`, `dict.get()`, `collections.defaultdict`, and `collections.Counter`.

### Syntax

```python
from collections import Counter, defaultdict

items = ["apple", "banana", "apple", "cherry", "banana", "apple"]

# Approach 1: Manual dictionary with .get()
freq = {}
for item in items:
    freq[item] = freq.get(item, 0) + 1   # .get(key, default) avoids KeyError
# freq = {"apple": 3, "banana": 2, "cherry": 1}

# Approach 2: defaultdict — automatically initializes missing keys
freq = defaultdict(int)                    # int() returns 0
for item in items:
    freq[item] += 1                        # no need for .get(), key auto-created

# Approach 3: Counter — does it all in one line
freq = Counter(items)                      # Counter({"apple": 3, "banana": 2, "cherry": 1})
freq.most_common(2)                        # [("apple", 3), ("banana", 2)] — top k!
```

### Mini Example

```python
text = "the cat sat on the mat the"
words = text.lower().split()
freq = {}
for w in words:
    freq[w] = freq.get(w, 0) + 1
# freq = {"the": 3, "cat": 1, "sat": 1, "on": 1, "mat": 1}
```

### Common Mistake

```python
# WRONG — KeyError on first occurrence
freq = {}
for w in words:
    freq[w] += 1  # KeyError: 'the' doesn't exist yet!

# RIGHT — use .get() with a default
freq = {}
for w in words:
    freq[w] = freq.get(w, 0) + 1
```

---

## 6. Sorting with Custom Keys (Top-K Problems)

### What It Is

Python's `sorted()` accepts a `key` function that determines the sort order, and a `reverse` flag. For top-K frequency problems, you sort by frequency (descending) and break ties alphabetically (ascending). You can combine multiple sort criteria using tuples as keys.

### Syntax

```python
freq = {"apple": 3, "banana": 2, "cherry": 2, "date": 1}

# Sort by frequency descending, then alphabetically ascending on ties
sorted_words = sorted(
    freq.keys(),
    key=lambda w: (-freq[w], w)  # negative frequency for descending; word for alpha ascending
)
# sorted_words = ["apple", "banana", "cherry", "date"]
# banana and cherry both have freq 2, "banana" < "cherry" alphabetically
```

**How tuple sorting works:** Python compares tuples element by element. `(-3, "apple")` comes before `(-2, "banana")` because `-3 < -2`. When the first elements are equal (both `-2`), it compares the second elements: `"banana" < "cherry"`.

### Mini Example

```python
freq = {"cat": 2, "bat": 2, "ant": 3}
k = 2

sorted_words = sorted(freq.keys(), key=lambda w: (-freq[w], w))
top_k = sorted_words[:k]  # ["ant", "bat"] — ant has highest freq, bat wins tie with cat
```

### Common Mistake

```python
# WRONG — sorting by frequency ascending (default)
sorted(freq.keys(), key=lambda w: freq[w])  # lowest frequency first

# WRONG — forgetting tie-breaking
sorted(freq.keys(), key=lambda w: -freq[w])  # ties are in arbitrary order

# RIGHT — negate frequency AND include alphabetical tie-breaker
sorted(freq.keys(), key=lambda w: (-freq[w], w))
```

---

## 7. Greedy Allocation (First-Fit Algorithm)

### What It Is

First-fit allocation is a greedy strategy: for each request, scan the hosts in order and assign the request to the first host that has enough remaining capacity. After assignment, reduce that host's capacity. This models real-world resource allocation (servers, memory blocks, bin packing).

### Syntax

```python
def first_fit(capacities: list[int], requests: list[int]) -> list[int]:
    remaining = list(capacities)   # copy — don't modify the original
    result = []

    for req in requests:
        assigned = -1              # default: no host found
        for i, cap in enumerate(remaining):
            if cap >= req:         # this host can handle it
                remaining[i] -= req   # reduce capacity
                assigned = i
                break              # FIRST fit — stop at the first match
        result.append(assigned)

    return result
```

### Mini Example

```python
hosts = [5, 3, 8]
requests = [3, 5, 2, 1]

# Request 3: Host 0 (cap 5 >= 3) → assign, cap becomes [2, 3, 8]
# Request 5: Host 0 (cap 2 < 5), Host 1 (cap 3 < 5), Host 2 (cap 8 >= 5) → assign, cap becomes [2, 3, 3]
# Request 2: Host 0 (cap 2 >= 2) → assign, cap becomes [0, 3, 3]
# Request 1: Host 0 (cap 0 < 1), Host 1 (cap 3 >= 1) → assign, cap becomes [0, 2, 3]
# Result: [0, 2, 0, 1]
```

### Common Mistake

```python
# WRONG — modifying the original list
def first_fit(hosts, requests):
    for req in requests:
        for i in range(len(hosts)):
            if hosts[i] >= req:     # modifying the INPUT list
                hosts[i] -= req     # caller's data is now corrupted
                break

# RIGHT — work on a copy
remaining = list(hosts)  # or hosts.copy() or hosts[:]
```

---

## 8. Best-Fit Allocation

### What It Is

Best-fit is a variation of first-fit where instead of taking the *first* host that fits, you take the host with the *smallest remaining capacity* that still fits the request. This minimizes wasted space. When multiple hosts have the same smallest-sufficient capacity, pick the one with the lowest index.

### Syntax

```python
def best_fit(capacities: list[int], requests: list[int]) -> list[int]:
    remaining = list(capacities)
    result = []

    for req in requests:
        best_idx = -1
        best_remaining = float('inf')  # track the smallest sufficient capacity

        for i, cap in enumerate(remaining):
            if cap >= req and cap < best_remaining:  # fits AND is tighter than previous best
                best_idx = i
                best_remaining = cap

        if best_idx != -1:
            remaining[best_idx] -= req
        result.append(best_idx)

    return result
```

### Mini Example

```python
hosts = [5, 3, 8]
requests = [3]

# Host 0: cap 5 >= 3, remaining=5 → best so far (idx=0)
# Host 1: cap 3 >= 3, remaining=3 < 5 → new best (idx=1, tighter fit)
# Host 2: cap 8 >= 3, remaining=8 > 3 → skip
# Result: [1] — Host 1 is the best fit (exact match)
```

### Common Mistake

```python
# WRONG — using min() without considering the capacity constraint
best = min(range(len(remaining)), key=lambda i: remaining[i])
# This picks the host with LEAST capacity, even if it can't handle the request!

# RIGHT — filter first, then find minimum
candidates = [(remaining[i], i) for i in range(len(remaining)) if remaining[i] >= req]
if candidates:
    _, best_idx = min(candidates)  # min by (capacity, index) — tuple comparison handles tie-breaking
```

---

## 9. Mutable State Tracking (Capacity + Count Constraints)

### What It Is

Some allocation problems have multiple constraints — a host must have enough capacity AND not exceed a maximum number of requests. Track both pieces of state simultaneously using parallel lists or a list of objects/tuples.

### Syntax

```python
def allocate_balanced(hosts: list[int], requests: list[int], max_per_host: int) -> list[int]:
    remaining = list(hosts)           # track remaining capacity
    counts = [0] * len(hosts)         # track number of requests per host
    result = []

    for req in requests:
        assigned = -1
        for i in range(len(remaining)):
            if remaining[i] >= req and counts[i] < max_per_host:  # BOTH constraints
                remaining[i] -= req
                counts[i] += 1
                assigned = i
                break
        result.append(assigned)

    return result
```

### Mini Example

```python
hosts = [10, 10]
requests = [1, 1, 1, 1, 1]
max_per_host = 2

# Req 1: Host 0 (cap=10, count=0<2) → cap=[9,10], count=[1,0]
# Req 1: Host 0 (cap=9, count=1<2)  → cap=[8,10], count=[2,0]
# Req 1: Host 0 (count=2, NOT <2!) → skip. Host 1 (cap=10, count=0<2) → cap=[8,9], count=[2,1]
# Req 1: Host 1 (cap=9, count=1<2)  → cap=[8,8], count=[2,2]
# Req 1: Host 0 (count=2) → skip. Host 1 (count=2) → skip. assigned=-1
# Result: [0, 0, 1, 1, -1]
```

---

## 10. Hash-Based Pair Counting (Complement Lookup)

### What It Is

Instead of checking every pair with nested loops (O(n^2)), use a set or dict to check if a "complement" exists. For difference problems: given a number `x`, you need `x + k` or `x - k` to exist. For sum problems: given `x`, you need `target - x` to exist. This is the core idea behind the classic "Two Sum" problem.

### Syntax — Difference Pairs (Unique Values)

```python
def count_diff_pairs(nums: list[int], k: int) -> int:
    num_set = set(nums)    # O(1) lookup
    count = 0

    for x in num_set:      # iterate unique values only
        if x + k in num_set:   # does the complement exist?
            count += 1

    # If k == 0, each number pairs with itself — we already count it once
    # If k > 0, we only check x + k (not x - k) to avoid double-counting
    return count
```

### Syntax — Sum Pairs (By Index)

```python
def count_sum_pairs(nums: list[int], target: int) -> int:
    count = 0
    seen = {}  # value → count of how many times we've seen it

    for num in nums:
        complement = target - num
        if complement in seen:
            count += seen[complement]  # each previous occurrence forms a valid pair
        seen[num] = seen.get(num, 0) + 1  # add AFTER checking, so i < j is guaranteed

    return count
```

### Mini Example — Difference

```python
nums = [1, 5, 3, 4, 2]
k = 2
num_set = {1, 2, 3, 4, 5}

# x=1: 1+2=3 in set? Yes → count=1
# x=2: 2+2=4 in set? Yes → count=2
# x=3: 3+2=5 in set? Yes → count=3
# x=4: 4+2=6 in set? No
# x=5: 5+2=7 in set? No
# Result: 3 pairs → (1,3), (2,4), (3,5)
```

### Mini Example — Sum

```python
nums = [1, 1, 1]
target = 2
# seen = {}
# num=1: complement=1, not in seen → seen={1:1}
# num=1: complement=1, in seen (count=1) → count=1, seen={1:2}
# num=1: complement=1, in seen (count=2) → count=3, seen={1:3}
# Result: 3 (index pairs: (0,1), (0,2), (1,2))
```

### Common Mistake

```python
# WRONG — O(n^2) brute force with nested loops
for i in range(len(nums)):
    for j in range(i + 1, len(nums)):
        if abs(nums[i] - nums[j]) == k:
            count += 1
# This works but is too slow for large inputs

# WRONG — double-counting difference pairs
for x in num_set:
    if x + k in num_set:
        count += 1
    if x - k in num_set:  # this counts each pair twice!
        count += 1

# RIGHT — only check one direction
for x in num_set:
    if x + k in num_set:
        count += 1
```

---

## 11. Returning Pairs vs. Counting Pairs

### What It Is

Some problems ask you to *return* the actual pairs, not just count them. This changes the data structure you use and how you handle duplicates. When returning pairs sorted by first element, build a list and sort it.

### Syntax

```python
def find_pairs(nums: list[int], k: int) -> list[tuple[int, int]]:
    num_set = set(nums)
    pairs = []

    for x in sorted(num_set):    # sorted iteration gives sorted output for free
        if x + k in num_set:
            pairs.append((x, x + k))  # (smaller, larger) since k >= 0

    return pairs
```

### Mini Example

```python
nums = [1, 5, 3, 4, 2]
k = 2
num_set = {1, 2, 3, 4, 5}

# Iterate sorted: 1, 2, 3, 4, 5
# x=1: 3 in set → (1, 3)
# x=2: 4 in set → (2, 4)
# x=3: 5 in set → (3, 5)
# x=4: 6 not in set
# x=5: 7 not in set
# Result: [(1, 3), (2, 4), (3, 5)] — already sorted!
```

---

## 12. Index Pairs vs. Value Pairs

### What It Is

A critical distinction in pair-counting problems: are you counting *unique value pairs* or *unique index pairs*? The answer completely changes your approach.

- **Value pairs:** Use a `set` — duplicates in the input collapse into one value.
- **Index pairs:** Every position matters — `[1, 1, 1]` has 3 index pairs `(0,1), (0,2), (1,2)`.

### Syntax Comparison

```python
nums = [1, 1, 1]
k = 0

# VALUE pairs: how many unique (a, b) pairs where |a - b| == 0?
num_set = set(nums)  # {1}
# Only one unique pair: (1, 1) → count = 1

# INDEX pairs: how many (i, j) where i < j and |nums[i] - nums[j]| == 0?
count = 0
for i in range(len(nums)):
    for j in range(i + 1, len(nums)):
        if abs(nums[i] - nums[j]) == k:
            count += 1
# Three pairs: (0,1), (0,2), (1,2) → count = 3
```

**Read the problem statement carefully** to determine which type is being asked for.

---

## 13. Time-Aware Resource Management

### What It Is

When resources are allocated with a time dimension (start time + duration), you need to track what's allocated *at a given moment* and free resources when their duration expires. One approach: maintain a list of active allocations per host and filter by time.

### Syntax

```python
from collections import defaultdict

def allocate_with_time(hosts: list[int], requests: list[tuple[int, int, int]]) -> list[int]:
    capacities = list(hosts)
    # Track active allocations: host_index → list of (end_time, load)
    active = defaultdict(list)
    result = []

    for start, duration, load in requests:
        end_time = start + duration

        # Free expired allocations for all hosts
        for i in range(len(capacities)):
            still_active = []
            for alloc_end, alloc_load in active[i]:
                if alloc_end > start:          # still running at this start_time
                    still_active.append((alloc_end, alloc_load))
                else:
                    capacities[i] += alloc_load  # free the capacity
            active[i] = still_active

        # First-fit among available hosts
        assigned = -1
        for i in range(len(capacities)):
            if capacities[i] >= load:
                capacities[i] -= load
                active[i].append((end_time, load))
                assigned = i
                break
        result.append(assigned)

    return result
```

### Key Concept

The "frees at `start_time + duration`" means: if an allocation starts at t=0 with duration=3, it occupies the host during t=0, 1, 2 and is free again at t=3. So a new request at t=3 *can* use that host.

---

## Quick Reference: Python Tools for Assessment

| Task | Tool | Example |
|------|------|---------|
| Check if char is whitespace | `char.isspace()` | `' '.isspace()` → `True` |
| Lowercase a string | `s.lower()` | `"Hello".lower()` → `"hello"` |
| Strip specific chars | `s.strip(chars)` | `"hi!".strip("!.")` → `"hi"` |
| Split on whitespace | `s.split()` | `"a  b".split()` → `["a", "b"]` |
| Get with default | `d.get(k, 0)` | Avoid `KeyError` |
| Count elements | `Counter(items)` | `Counter(["a","a","b"])` → `{"a":2,"b":1}` |
| Top-K from Counter | `.most_common(k)` | Returns `[(elem, count), ...]` |
| Sort with key | `sorted(x, key=fn)` | `sorted(d, key=lambda w: -d[w])` |
| Copy a list | `list(original)` | Avoids mutating the input |
| Infinity sentinel | `float('inf')` | For "find minimum" patterns |

---

Good luck with the assessment! Work through each sub-project, run the tests, and make sure you understand *why* each solution works — not just *that* it works.
