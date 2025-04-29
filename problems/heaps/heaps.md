
# 🔥 What is a Heap?

- A **heap** is a **special tree-based data structure**.
- It satisfies the **heap property**:
  - **Min-Heap**: Parent node is always **less than or equal** to its children.
  - **Max-Heap**: Parent node is always **greater than or equal** to its children.
- **Shape**: Always a **complete binary tree** (completely filled except possibly the last level).

---
  
# 🧠 Heap Property

| Type | Property |
|:---|:---|
| **Min-Heap** | Every parent ≤ its children (smallest value at root). |
| **Max-Heap** | Every parent ≥ its children (largest value at root). |

---

# 🏡 Visual Example

## Min-Heap Example:

```
       2
     /   \
    8     3
   / \   /
  10 12 5
```
- 2 ≤ 8 and 2 ≤ 3
- 8 ≤ 10 and 8 ≤ 12
- 3 ≤ 5

✅ Min-heap property satisfied.

---

## Max-Heap Example:

```
       12
     /    \
    10     9
   / \    /
  5  8   3
```
- 12 ≥ 10 and 12 ≥ 9
- 10 ≥ 5 and 10 ≥ 8
- 9 ≥ 3

✅ Max-heap property satisfied.

---

# ⚡ Where is Heap Used?

- Priority Queues (give me min/max element quickly).
- Scheduling systems (CPU schedulers).
- Graph algorithms (Dijkstra, Prim).
- Stream processing (find median dynamically).
- Sort algorithms (Heap Sort).

---

# 🚀 Operations on Heap

| Operation | Time Complexity | Notes |
|:---|:---|:---|
| Insert element | O(log n) | Bubble up |
| Get min/max | O(1) | Just look at root |
| Remove min/max | O(log n) | Remove root, then heapify down |
| Build heap from array | O(n) | Bottom-up building faster than inserting |

---

# 🛠 How Heap is Represented

**Heap is usually stored as an array** (no need to store tree nodes manually).

- For a node at index `i`:
  - **Left Child**: `2i + 1`
  - **Right Child**: `2i + 2`
  - **Parent**: `(i - 1) // 2`

Example:
```python
arr = [2, 8, 3, 10, 12, 5]
```
Represents:

```
       2
     /   \
    8     3
   / \   /
 10 12 5
```

✅ Array and tree perfectly aligned!

---

# 🧹 Heap Summary Table

| Concept | Min-Heap | Max-Heap |
|:---|:---|:---|
| Root | Minimum element | Maximum element |
| Insert | Bubble up to maintain heap property | Same |
| Remove Root | Pop root, push last element, bubble down | Same |
| Representation | Array (with parent/child index formulas) | Same |

---

# 🛠 Python's `heapq` Module

- Python’s `heapq` **only implements a min-heap** by default.
- If you want a **max-heap**, you must **insert negative values**.

---
  
## Examples:

✅ **Min-Heap**

```python
import heapq

heap = []
heapq.heappush(heap, 3)
heapq.heappush(heap, 1)
heapq.heappush(heap, 5)

print(heapq.heappop(heap))  # 1 (smallest)
```

✅ **Max-Heap**

```python
import heapq

heap = []
heapq.heappush(heap, -3)
heapq.heappush(heap, -1)
heapq.heappush(heap, -5)

print(-heapq.heappop(heap))  # 5 (largest)
```

---

# 📈 Priority Queue

A **priority queue** is **basically a heap**.

- Items are processed based on their priority (not insertion order).
- Heaps are **natural way** to implement priority queues:
  - Priority = Value for normal heaps.
  - Priority = Weight/custom key for complex cases.

---

# 🌟 Real World Use Cases

| Example | Heap Type | Why |
|:---|:---|:---|
| Get top-k scores | Min-Heap | Maintain top elements |
| Scheduling jobs | Min-Heap / Max-Heap | Process fastest or most important first |
| Find shortest paths | Min-Heap | Always expand cheapest path |
| Real-time median | Two Heaps (Max + Min) | Balance lower/upper halves |
| Data streams | Min-Heap / Max-Heap | Maintain order dynamically |

---

# 🛠 Important heapq methods

| Function | Description |
|:---|:---|
| `heapq.heappush(heap, item)` | Insert item into heap |
| `heapq.heappop(heap)` | Remove and return smallest item |
| `heapq.heapify(list)` | Convert list into a heap |
| `heapq.heappushpop(heap, item)` | Push then pop atomically (faster) |
| `heapq.nlargest(k, iterable)` | Return k largest elements |
| `heapq.nsmallest(k, iterable)` | Return k smallest elements |

---

# ✨ Quick Diagram

``` 
Heap (Tree Shape) → Stored as Array → Supports O(log n) push/pop → Always get min/max in O(1) 
```

---

# ✅ Final Review

| Property | Heap |
|:---|:---|
| Shape | Complete Binary Tree |
| Types | Min-Heap, Max-Heap |
| Operations | Insert, Remove-Min/Max, Peek-Min/Max |
| Data Structure | Array |
| Complexity | Insert/Pop: O(log n), Peek: O(1) |
| Library | `heapq` (Python) |

---

# 🎯 Now you know:
- Heap = Tree + Array magic.
- Min/Max heap = Just flip the comparison.
- Priority Queue = Heap with smart priorities.
- **Heap is NOT fully sorted** — only partial ordering.
