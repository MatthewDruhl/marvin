# Teach-Back Key Concepts Checklists

Checklists for evaluating teach-back explanations. Each item represents a key concept the user should cover or demonstrate understanding of during teach-back.

---

## DSA Topics

### Recursion
- [ ] Base case and recursive case (two essential parts)
- [ ] How the call stack works during recursion
- [ ] Stack overflow: what causes it (missing/incorrect base case)
- [ ] Head vs tail recursion difference
- [ ] Can write a basic recursive function (e.g., factorial, fibonacci)
- [ ] Python does NOT optimize tail recursion

### Linear Search
- [ ] Time complexity: O(1) best, O(n) average/worst
- [ ] When to choose over binary search (unsorted data, small datasets, linked lists)
- [ ] Can implement with enumerate()

### Binary Search
- [ ] Prerequisite: sorted array
- [ ] Time complexity: O(log n)
- [ ] Iterative vs recursive space complexity (O(1) vs O(log n))
- [ ] Integer overflow concern with (low + high) and the safer alternative
- [ ] Can implement iteratively with low/high/mid pointers

### Bubble Sort
- [ ] Adjacent element comparison and swapping
- [ ] Largest elements "bubble up" to the end
- [ ] Time: O(n^2) avg/worst, O(n) best with optimization
- [ ] Early termination optimization (no swaps = sorted)
- [ ] Space: O(1), in-place

### Selection Sort
- [ ] Find minimum from unsorted portion, swap to front
- [ ] Time: O(n^2) in ALL cases
- [ ] NOT stable (swapping can change relative order)
- [ ] Fewer swaps than bubble sort — O(n) vs O(n^2)

### Insertion Sort
- [ ] Builds sorted portion one element at a time
- [ ] Time: O(n) best (nearly sorted), O(n^2) avg/worst
- [ ] Stable sort (only shifts strictly greater elements)
- [ ] Best for: small datasets, nearly sorted data, online sorting
- [ ] Advantage over bubble/selection for nearly-sorted data

### Quick Sort
- [ ] Pivot selection and partitioning
- [ ] Time: O(n log n) avg, O(n^2) worst
- [ ] Worst case cause: pivot always min/max (e.g., sorted array + first-element pivot)
- [ ] Mitigations: random pivot, median-of-three, introsort
- [ ] Space: O(log n) avg (call stack)
- [ ] Vs merge sort: in-place, better cache, but not stable/not guaranteed O(n log n)

### Merge Sort
- [ ] Divide in half recursively, merge back in sorted order
- [ ] Time: O(n log n) in ALL cases
- [ ] Space: O(n) for temporary arrays
- [ ] Stable (equal elements: take from left first with <=)
- [ ] Preferred for linked lists (sequential access only needed)
- [ ] Can implement the merge function

### Tree Traversals
- [ ] DFS three orders: in-order (L,Root,R), pre-order (Root,L,R), post-order (L,R,Root)
- [ ] In-order on BST gives sorted sequence
- [ ] BFS: level by level using a queue
- [ ] DFS vs BFS: space complexity (O(h) vs O(w))
- [ ] Can implement in-order traversal recursively
- [ ] Can implement BFS with deque

---

*Checklists derived from question-bank.md answers. Update when new topics or questions are added.*
