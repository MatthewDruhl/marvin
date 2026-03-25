# PP — CodeSignal Assessment Prep Study Guide

Read this guide top to bottom. Each project section builds on the skills from the one before it. Python skills and standard library tools are introduced the first time you need them.

---

# Project 1: findFirstSubstringOccurrence

String searching without built-in shortcuts. You'll build from a basic manual search up to multi-pattern matching.

---

## String Slicing

### What It Is

Python lets you extract a portion of a string with `s[start:end]`. The result includes the character at `start` but NOT at `end`. This is how you'll compare chunks of text against a pattern.

### Syntax

```python
s = "abcdef"
s[1:4]    # "bcd" — characters at index 1, 2, 3
s[0:3]    # "abc"
s[2:2]    # "" — empty when start == end
s[3:100]  # "def" — Python doesn't crash, just stops at the end
```

### Common Mistake

```python
# WRONG — thinking s[1:4] includes index 4
s = "abcdef"
s[1:4]  # "bcd", NOT "bcde"

# RIGHT — end index is exclusive, like range()
s[1:5]  # "bcde"
```

---

## Manual Substring Search (Sliding Window)

### What It Is

When you can't use `str.find()` or `str.index()`, you search for a substring by sliding a window across the string and comparing at each position. This is the naive string search algorithm.

### Syntax

```python
def search(text: str, pattern: str) -> int:
    for i in range(len(text) - len(pattern) + 1):  # stop early — pattern can't fit past here
        if text[i:i + len(pattern)] == pattern:     # string slicing does the comparison
            return i                                  # found it — return the index
    return -1                                         # exhausted all positions, not found
```

**Key detail:** The range is `len(text) - len(pattern) + 1`. If `text` is 10 chars and `pattern` is 3, you only need to check positions 0-7 (8 positions). Starting at position 8 or later, there aren't enough characters left for the pattern to fit.

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

## Case-Insensitive Search with `.lower()`

### What It Is

When comparing strings case-insensitively, convert both strings to the same case before comparing. The key insight: convert once upfront for comparison, but return indices from the *original* string (the indices are the same since `.lower()` doesn't change string length).

### Syntax

```python
s_lower = s.lower()          # convert entire string to lowercase
sub_lower = substring.lower()

# Now search in the lowered versions — same sliding window as before
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

## First Occurrence of Any Pattern from a List

### What It Is

Given a list of patterns, find the earliest index where any pattern matches. If multiple patterns match at the same index, the longer pattern wins. This combines everything above — you're running the basic search for each pattern and tracking the best result.

### Syntax

```python
def find_first_any(s: str, patterns: list[str]) -> tuple[int, str]:
    n = len(s)
    best_idx, best_pat = float('inf'), None
    for pat in patterns:
        m = len(pat)
        for i in range(n - m + 1):
            if i >= best_idx:
                break                    # no point checking further right
            if s[i:i + m] == pat:
                if i < best_idx or (i == best_idx and m > len(best_pat)):
                    best_idx, best_pat = i, pat
                break                    # first occurrence of this pattern found
    if best_pat is None:
        return (-1, "")
    return (best_idx, best_pat)
```

**New Python skill — `float('inf')`:** A special value that's larger than any number. Useful as an initial "best so far" when searching for a minimum — any real index will be smaller, so the first match always wins.

### Mini Example

```python
>>> find_first_any("abcdef", ["cd", "cde", "xy"])
(2, 'cde')                              # both "cd" and "cde" match at 2, longer wins
```

### Common Mistake

```python
# WRONG — returns first pattern that matches anywhere, not earliest index
for pat in patterns:
    idx = find_first(s, pat)
    if idx != -1:
        return (idx, pat)                # biased toward pattern list order

# RIGHT — track best index across ALL patterns, then return winner
```

---

# Project 2: wordCount

Text processing: splitting, cleaning, counting, and ranking words. Builds on the string skills from Project 1 and introduces dictionaries and sorting.

---

## Whitespace Splitting and Word Counting

### What It Is

Python's `str.split()` (with no arguments) splits on any whitespace and ignores leading/trailing/multiple spaces. Some problems ask you to demonstrate understanding of *how* this works. The concept: iterate through characters, track whether you're inside a word, and count transitions from whitespace to non-whitespace.

**New Python skill — `.isspace()`:** Returns `True` for whitespace characters: `' '`, `'\t'`, `'\n'`, `'\r'`.

### Syntax

```python
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

## Stripping Punctuation with `.strip()`

### What It Is

When processing text for word frequency, you need to remove punctuation so `"hello,"` and `"hello"` are treated as the same word. Python's `str.strip()` method removes characters from the start and end of a string — but leaves the middle untouched.

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

## Frequency Counting with Dictionaries

### What It Is

A frequency map (also called a histogram or counter) tracks how many times each element appears. Python offers several approaches: manual `dict`, `dict.get()`, `collections.defaultdict`, and `collections.Counter`. You'll use these constantly — for word frequency here, and for pair counting in Project 4.

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

## Sorting with Custom Keys (Top-K Problems)

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

# Project 3: hostAllocation

Resource allocation using greedy algorithms. Each variation adds a constraint. Builds on list manipulation and introduces mutable state tracking.

---

## Copying Lists to Protect Input

### What It Is

When your function modifies a list (like reducing host capacities), always work on a copy. Modifying the input list corrupts the caller's data — a common source of bugs that's hard to trace.

### Syntax

```python
original = [5, 3, 8]

# Three equivalent ways to copy
remaining = list(original)    # most readable
remaining = original.copy()   # explicit method
remaining = original[:]       # slice copy
```

### Common Mistake

```python
# WRONG — modifying the original list
def first_fit(hosts, requests):
    for req in requests:
        for h in range(len(hosts)):
            if hosts[h] >= req:     # modifying the INPUT list
                hosts[h] -= req     # caller's data is now corrupted
                break

# RIGHT — work on a copy
remaining = list(hosts)  # now hosts stays untouched
```

---

## Greedy Allocation (First-Fit Algorithm)

### What It Is

First-fit allocation is a greedy strategy: for each request, scan the hosts in order and assign the request to the first host that has enough remaining capacity. After assignment, reduce that host's capacity.

**Python skill — `enumerate()`:** Gives you both the index and value in a loop. Cleaner than `range(len(...))` when you need both.

```python
for h, cap in enumerate(remaining):  # h is the index, cap is the value
```

### Syntax

```python
def first_fit(capacities: list[int], requests: list[int]) -> list[int]:
    remaining = list(capacities)   # copy — don't modify the original
    result = []

    for req in requests:
        assigned = -1              # default: no host found
        for h, cap in enumerate(remaining):
            if cap >= req:         # this host can handle it
                remaining[h] -= req   # reduce capacity
                assigned = h
                break              # FIRST fit — stop at the first match
        result.append(assigned)

    return result
```

### Mini Example

```python
hosts = [5, 3, 8]
requests = [3, 5, 2, 1]

# Request 3: Host 0 (cap 5 >= 3) → assign, cap becomes [2, 3, 8]
# Request 5: Host 0 (cap 2 < 5), Host 1 (cap 3 < 5), Host 2 (cap 8 >= 5) → cap becomes [2, 3, 3]
# Request 2: Host 0 (cap 2 >= 2) → assign, cap becomes [0, 3, 3]
# Request 1: Host 0 (cap 0 < 1), Host 1 (cap 3 >= 1) → cap becomes [0, 2, 3]
# Result: [0, 2, 0, 1]
```

---

## Best-Fit Allocation

### What It Is

Instead of taking the *first* host that fits, take the host with the *smallest remaining capacity* that still fits the request. This minimizes wasted space. When multiple hosts have the same smallest-sufficient capacity, pick the lowest index.

This builds directly on first-fit — the only change is replacing `break` (stop at first match) with tracking the best match across all hosts.

### Syntax

```python
def best_fit(capacities: list[int], requests: list[int]) -> list[int]:
    remaining = list(capacities)
    result = []

    for req in requests:
        best_idx = -1
        best_remaining = float('inf')  # track the smallest sufficient capacity

        for h, cap in enumerate(remaining):
            if cap >= req and cap < best_remaining:  # fits AND is tighter than previous best
                best_idx = h
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
# WRONG — keeping the break from first-fit (finds first fit, not best fit)
for h, cap in enumerate(remaining):
    if cap >= req:
        remaining[h] -= req
        assigned = h
        break              # stops at first match — never checks if a tighter fit exists

# RIGHT — remove break, track best across ALL hosts, deduct AFTER the loop
best_idx, best_cap = -1, float('inf')
for h, cap in enumerate(remaining):
    if cap >= req and cap < best_cap:
        best_idx = h
        best_cap = cap
if best_idx != -1:
    remaining[best_idx] -= req
```

---

## Pattern Comparison: `float('inf')` in find_first_of_any vs best_fit

### Why These Feel Similar

Both patterns use `float('inf')` to initialize a "best so far" variable, then scan candidates looking for a smaller value. But they solve fundamentally different problems, and the difference shows up in one line: **whether the inner loop has a `break`**.

### Side-by-Side Comparison

| | find_first_of_any | best_fit |
|---|---|---|
| **Minimizing** | index (earliest position) | capacity (tightest fit) |
| **Inner loop** | `break` on first match per pattern | scans ALL hosts, no `break` |
| **Why** | first occurrence is the only one that matters | must compare every host to find the smallest |
| **Result tracking** | `best_idx` + `best_pat` (two things) | `best_idx` + `best_cap` (two things) |

### The Key Mental Distinction

- **find_first_of_any** — "find earliest, stop looking for this pattern once found" → inner `break`
- **best_fit** — "find smallest that fits, must check them all to be sure" → no `break`, full scan

**One-line rule: first-fit breaks, best-fit doesn't.**

### Conversion Trick

If you blank on best_fit, write first_fit first (the simpler pattern), then modify it:

1. Remove the `break`
2. Add `best_idx, best_cap = -1, float('inf')` before the inner loop
3. Change `cap >= req` to `cap >= req and cap < best_cap`
4. Move the `remaining[h] -= req` to after the inner loop using `best_idx`

```python
# FIRST-FIT (the pattern you know cold)
for req in requests:
    assigned = -1
    for h, cap in enumerate(remaining):
        if cap >= req:
            remaining[h] -= req
            assigned = h
            break                          # ← stop at first match
    result.append(assigned)

# BEST-FIT (modify first-fit with 4 changes)
for req in requests:
    best_idx = -1
    best_cap = float('inf')                # ← change 1: track best capacity
    for h, cap in enumerate(remaining):
        if cap >= req and cap < best_cap:  # ← change 2: tighter condition
            best_idx = h
            best_cap = cap
                                           # ← change 3: no break
    if best_idx != -1:
        remaining[best_idx] -= req         # ← change 4: deduct AFTER the loop
    result.append(best_idx)
```

---

## Mutable State Tracking (Multiple Constraints)

### What It Is

Some allocation problems have multiple constraints — a host must have enough capacity AND not exceed a maximum number of requests. Track both pieces of state simultaneously using parallel lists.

### Syntax

```python
def allocate_balanced(hosts: list[int], requests: list[int], max_per_host: int) -> list[int]:
    remaining = list(hosts)           # track remaining capacity
    counts = [0] * len(hosts)         # track number of requests per host
    result = []

    for req in requests:
        assigned = -1
        for h in range(len(remaining)):
            if remaining[h] >= req and counts[h] < max_per_host:  # BOTH constraints
                remaining[h] -= req
                counts[h] += 1
                assigned = h
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

## Time-Aware Resource Management

### What It Is

When resources are allocated with a time dimension (start time + duration), you need to track what's active *at a given moment* and free resources when their duration expires. This is the most complex allocation variant — it combines first-fit with an active-allocations list that gets filtered on each request.

**Python skill — tuple unpacking:** When your data has multiple fields, tuples keep them together. Unpack in a `for` loop for readability.

```python
requests = [(0, 3, 5), (1, 2, 3)]  # each is (start_time, duration, load)
for start, duration, load in requests:
    end_time = start + duration
```

### Syntax

```python
def time_aware_allocation(capacities: list[int], requests: list[tuple[int, int, int]]) -> list[int]:
    remaining = list(capacities)
    active = []                          # list of (end_time, host_index, load)
    assignments = []

    for start, duration, load in requests:
        # free expired assignments
        still_active = []
        for end_t, h, ld in active:
            if end_t <= start:
                remaining[h] += ld       # capacity returns
            else:
                still_active.append((end_t, h, ld))
        active = still_active

        # first-fit allocation
        assigned = -1
        for h in range(len(remaining)):
            if remaining[h] >= load:
                remaining[h] -= load
                active.append((start + duration, h, load))
                assigned = h
                break
        assignments.append(assigned)
    return assignments
```

### Key Concept

The "frees at `start_time + duration`" means: if an allocation starts at t=0 with duration=3, it occupies the host during t=0, 1, 2 and is free again at t=3. So a new request at t=3 *can* use that host.

---

# Project 4: countPairsWithDifference

Counting and finding pairs in arrays. Uses the frequency counting skills from Project 2 and introduces optimization with binary search.

---

## Value Pairs vs. Index Pairs

### What It Is

A critical distinction in pair-counting problems. **Read the problem statement carefully** — the type of pair completely changes your approach.

### Decision Rule

| Clue in problem | Pair type | Approach |
|---|---|---|
| "unique pairs", "distinct pairs" | **Value pairs** | `Counter` — duplicates collapse |
| "(i, j) where i < j", "index pairs" | **Index pairs** | Manual dict (build as you go) or nested loops |
| `[1,1,1]` with `k=0` → expects `1` | **Value pairs** | Only one unique pair: (1,1) |
| `[1,1,1]` with `k=0` → expects `3` | **Index pairs** | Three pairs: (0,1), (0,2), (1,2) |

**The examples in the problem are your best clue.** If `[1,1,1]` returns 1, it's value pairs. If it returns 3, it's index pairs.

### Syntax Comparison

```python
nums = [1, 1, 1]
k = 0

# VALUE pairs — O(n): how many unique (a, b) pairs where |a - b| == 0?
freq = Counter(nums)  # Counter({1: 3})
# freq[1] > 1? Yes → count = 1 (one unique pair: (1, 1))

# INDEX pairs — O(n²): how many (i, j) where i < j and |nums[i] - nums[j]| == 0?
count = 0
for i in range(len(nums)):
    for j in range(i + 1, len(nums)):
        if abs(nums[i] - nums[j]) == k:
            count += 1
# Three pairs: (0,1), (0,2), (1,2) → count = 3

# INDEX pairs — O(n log n): same result using sorted + bisect
from bisect import bisect_left, bisect_right
nums_srt = sorted(nums)
count = 0
for i, n in enumerate(nums_srt):
    count += bisect_right(nums_srt, n + k, i + 1) - bisect_left(nums_srt, n + k, i + 1)
# count = 3 — same answer, faster on large inputs
# See "Optimizing Index Pair Counting with bisect" section below for full explanation
```

---

## Hash-Based Complement Lookup

### What It Is

Instead of checking every pair with nested loops (O(n^2)), use a hash (set or dict) to check if a "complement" exists in O(1). The complement is the other value that would complete the pair:
- **Difference problems:** complement of `x` is `x + k`
- **Sum problems:** complement of `x` is `target - x`

This is the core idea behind the classic "Two Sum" problem. You already know `Counter` and `dict.get()` from Project 2 — here you're using them to find pairs instead of counting words.

### Counter vs. Manual Dict

Ask yourself: **Does the problem say "index pairs (i, j) where i < j"?**

| Question asks for... | Data structure | Why |
|---|---|---|
| **Unique value pairs** | `Counter` (count everything upfront) | Position doesn't matter — you just need to know what values exist and how many times |
| **Index pairs where i < j** | Manual `dict` (build as you go) | Position matters — you can only pair with elements you've already passed |

**Think of it this way:**
- **Counter** = dump all puzzle pieces on the table first, then look for matches
- **Manual dict** = walk through a line of people, only shaking hands with people you've already passed

### Why Counter Instead of Set?

A `set` loses count information. `set([5])` and `set([5, 5, 5])` both become `{5}`. This breaks when `k == 0`:
- `5 + 0 = 5` — the complement is the number itself
- With a set, it always finds itself → wrong answer
- You need to know: does this value appear **more than once**? Only `Counter` tells you that

`Counter` gives you everything `set` gives you (unique keys, O(1) lookup) **plus** the count.

### Key Rules

1. **Only check one direction** (`x + k`, not also `x - k`) to avoid double-counting
2. **When `k == 0`:** a value must appear more than once to pair with itself — use `freq[x] > 1`
3. **For sum pairs:** add to `seen` AFTER checking — this guarantees `i < j` (you only pair with previous elements)
4. **`seen[complement]` tells you HOW MANY** previous elements can pair with the current one — add that count, not just 1

### Syntax — Counting Difference Pairs (Unique Values)

```python
from collections import Counter

def count_diff_pairs(nums: list[int], k: int) -> int:
    freq = Counter(nums)   # count everything upfront — position doesn't matter
    count = 0

    for x in freq:         # iterate unique values (same as set, but with counts)
        if k == 0 and freq[x] > 1:     # need at least 2 occurrences to pair with itself
            count += 1
        elif k > 0 and x + k in freq:  # does the complement exist? k > 0 prevents double-entry with k == 0
            count += 1

    return count
```

**Why `k > 0` on the `elif`?** Without it, when `k == 0` the first `if` could be False (only 1 occurrence) but the `elif` would still check `x + 0 in freq` — which is always True. Adding `k > 0` makes the two branches mutually exclusive and avoids this bug.

### Syntax — Returning Difference Pairs (Sorted Output)

Some problems ask you to *return* the actual pairs, not just count them. The only changes: use `sorted(freq)` to iterate in order, and build a list of tuples instead of incrementing a counter.

```python
from collections import Counter

def find_pairs(nums: list[int], k: int) -> list[tuple[int, int]]:
    freq = Counter(nums)
    pairs = []

    for x in sorted(freq):      # sorted iteration gives sorted output for free
        if k == 0:
            if freq[x] > 1:     # need 2+ occurrences to pair with itself
                pairs.append((x, x))
        elif x + k in freq:
            pairs.append((x, x + k))  # (smaller, larger) since k > 0

    return pairs
```

### Syntax — Counting Sum Pairs (By Index)

```python
def count_sum_pairs(nums: list[int], target: int) -> int:
    count = 0
    seen = {}  # value → count of how many times we've seen it SO FAR

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
freq = Counter(nums)  # Counter({1:1, 5:1, 3:1, 4:1, 2:1})

# k != 0, so check x + k in freq:
# x=1: 1+2=3 in freq? Yes → count=1
# x=2: 2+2=4 in freq? Yes → count=2
# x=3: 3+2=5 in freq? Yes → count=3
# x=4: 4+2=6 in freq? No
# x=5: 5+2=7 in freq? No
# Result: 3 pairs → (1,3), (2,4), (3,5)

# k == 0 example:
nums2 = [5, 5, 3]
freq2 = Counter(nums2)  # Counter({5:2, 3:1})
# x=5: freq[5] > 1? Yes → count=1
# x=3: freq[3] > 1? No → skip
# Result: 1 (the pair (5,5))
```

### Mini Example — Sum

```python
nums = [1, 1, 1]
target = 2

# Building seen as we go — each step only knows about PREVIOUS elements:
# seen = {}
# num=1: complement=1, not in seen → seen={1:1}
# num=1: complement=1, in seen (count=1) → count=1, seen={1:2}
#   ↑ 1 previous "1" at index 0 can pair with current index 1 → pair (0,1)
# num=1: complement=1, in seen (count=2) → count=3, seen={1:3}
#   ↑ 2 previous "1"s at indices 0,1 can pair with current index 2 → pairs (0,2), (1,2)
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

# WRONG — using set, breaks on k == 0
num_set = set(nums)
for x in num_set:
    if x + k in num_set:  # when k=0, EVERY value matches itself
        count += 1         # [5] returns 1 but should return 0

# RIGHT — use Counter, check one direction, handle k == 0
freq = Counter(nums)
for x in freq:
    if k == 0 and freq[x] > 1:
        count += 1
    elif k > 0 and x + k in freq:
        count += 1
```

---

## Optimizing Index Pair Counting with `bisect`

### What It Is

When counting index pairs `(i, j)` where `i < j` and the difference falls within a *range* (not just an exact value), the hash-based approach from above doesn't apply cleanly. The brute-force nested loop works but is O(n^2). By sorting the array and using binary search, you can drop this to O(n log n).

**New Python skill — `bisect` module:** Finds insertion points in sorted lists in O(log n) time.

```python
from bisect import bisect_left, bisect_right

sorted_list = [1, 3, 5, 7, 9]

bisect_left(sorted_list, 3)   # → 1  (index where 3 starts)
bisect_right(sorted_list, 7)  # → 4  (index just PAST where 7 ends)
```

- `bisect_left(a, x)` — first position where `x` could be inserted (left side of duplicates)
- `bisect_right(a, x)` — position just after the last `x` (right side of duplicates)

**Counting elements in a range** `[low, high]`:

```python
count_in_range = bisect_right(sorted_list, high) - bisect_left(sorted_list, low)
# For [3, 7]: bisect_right(..., 7) - bisect_left(..., 3) = 4 - 1 = 3 elements (3, 5, 7)
```

### The `lo` Parameter — Restricting the Search Window

Both functions accept an optional third argument `lo` that limits where bisect starts searching:

```python
bisect_left(sorted_list, value, lo)  # only search from index 'lo' onward
```

This doesn't change what index is returned — it still returns the global insertion point. It just skips elements before `lo`, which is how you avoid counting an element as its own partner or double-counting pairs.

### Brute-Force Approach (O(n^2))

```python
def count_pairs_in_range(nums: list[int], low: int, high: int) -> int:
    count = 0
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):          # every pair where i < j
            if low <= abs(nums[i] - nums[j]) <= high:
                count += 1
    return count
```

Simple and correct, but checks every possible pair. For an array of 10,000 elements that's ~50 million comparisons.

### Bisect Approach (O(n log n))

```python
from bisect import bisect_left, bisect_right

def count_pairs_in_range(nums: list[int], low: int, high: int) -> int:
    nums_srt = sorted(nums)                         # O(n log n) — pay this cost once
    count = 0

    for i, n in enumerate(nums_srt):                # for each element...
        low_limit = n + low                         # smallest valid partner
        high_limit = n + high                       # largest valid partner
        # count elements in [low_limit, high_limit], searching only AFTER index i
        count += bisect_right(nums_srt, high_limit, i + 1) - bisect_left(nums_srt, low_limit, i + 1)

    return count
```

**Why this works:**
1. **Sort once** — puts values in order so bisect can binary-search
2. **For each element `n`** — valid partners have values between `n + low` and `n + high`
3. **`i + 1` as `lo`** — only search elements after the current index, ensuring each pair is counted once and an element doesn't pair with itself
4. **`bisect_right - bisect_left`** — gives the count of elements in that range in O(log n)

### Mini Example

```python
nums = [1, 5, 3, 4, 2]
low, high = 1, 2

nums_srt = [1, 2, 3, 4, 5]

# i=0, n=1: partners in [2, 3], search from index 1
#   bisect_right([...], 3, 1) = 3, bisect_left([...], 2, 1) = 1 → 3 - 1 = 2 pairs
# i=1, n=2: partners in [3, 4], search from index 2
#   bisect_right([...], 4, 2) = 4, bisect_left([...], 3, 2) = 2 → 4 - 2 = 2 pairs
# i=2, n=3: partners in [4, 5], search from index 3
#   bisect_right([...], 5, 3) = 5, bisect_left([...], 4, 3) = 3 → 5 - 3 = 2 pairs
# i=3, n=4: partners in [5, 6], search from index 4
#   bisect_right([...], 6, 4) = 5, bisect_left([...], 5, 4) = 4 → 5 - 4 = 1 pair
# i=4, n=5: partners in [6, 7], search from index 5
#   bisect_right([...], 7, 5) = 5, bisect_left([...], 6, 5) = 5 → 5 - 5 = 0 pairs
# Total: 2 + 2 + 2 + 1 + 0 = 7 ✓
```

### When to Use Each

| Approach | Time | Best for |
|---|---|---|
| Nested `i, j` loop | O(n^2) | Small arrays, simplicity, when you need it to "just work" |
| Sorted + bisect | O(n log n) | Large arrays, performance-sensitive problems |

**Assessment tip:** Start with the brute-force loop — it's fast to write and easy to verify. If the problem has large inputs or you have time left, optimize with bisect.

### Common Mistake

```python
# WRONG — searching the unsorted list (bisect requires sorted input!)
nums_srt = sorted(nums)
for i, n in enumerate(nums_srt):
    count += bisect_right(nums, n + high, i + 1)  # searching 'nums' not 'nums_srt'!

# WRONG — not passing lo, counts pairs in both directions (double-counting)
for i, n in enumerate(nums_srt):
    count += bisect_right(nums_srt, n + high) - bisect_left(nums_srt, n + low)

# RIGHT — search the sorted list, pass i + 1 as lo
for i, n in enumerate(nums_srt):
    count += bisect_right(nums_srt, n + high, i + 1) - bisect_left(nums_srt, n + low, i + 1)
```

---

# Quick Reference

| Task | Tool | Example |
|------|------|---------|
| String slice | `s[start:end]` | `"abcdef"[1:4]` → `"bcd"` |
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
| Enumerate a list | `enumerate(items)` | Index + value in one loop |
| Unpack tuples in loop | `for a, b in items` | Readable multi-field iteration |
| Binary search (left) | `bisect_left(a, x, lo)` | First insertion point for `x` from `lo` onward |
| Binary search (right) | `bisect_right(a, x, lo)` | Position just past last `x` from `lo` onward |
| Count in sorted range | `bisect_right(a, hi) - bisect_left(a, lo)` | Elements in `[lo, hi]` in sorted list |

---

Good luck with the assessment! Work through each project in order, run the tests, and make sure you understand *why* each solution works — not just *that* it works.
