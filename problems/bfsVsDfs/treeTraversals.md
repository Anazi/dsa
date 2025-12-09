# 🌳 Base Tree Definition (for all problems)

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

We will reuse this in every question.

---

# ==========================================

# ✅ PART 1 — DFS Traversals

# ==========================================

DFS traversals use **recursion** (implicit stack) or a manual stack.

Three types:

1. **Preorder**   → Root, Left, Right
2. **Inorder**    → Left, Root, Right
3. **Postorder**  → Left, Right, Root

---

# 🌟 DFS-Q1: Preorder Traversal (Root → Left → Right)

### Problem

Return the preorder traversal of a binary tree.

### Why it’s asked

* Easiest DFS form
* Used in serialization questions
* Tests comfort with recursion

### Code (with comments)

```python
def preorder_traversal(root):
    """
    Preorder DFS: Visit Root → Left → Right
    """
    result = []

    def dfs(node):
        if not node:
            return

        # 1. Visit the root
        result.append(node.val)

        # 2. Traverse left subtree
        dfs(node.left)

        # 3. Traverse right subtree
        dfs(node.right)

    dfs(root)
    return result
```

---

# 🌟 DFS-Q2: Inorder Traversal (Left → Root → Right)

### Problem

Return the inorder traversal of a binary tree.

### Why it’s asked

* For **Binary Search Trees**, inorder = sorted list
* Interviewers want to see if you know the "middle" step before root

### Code

```python
def inorder_traversal(root):
    """
    Inorder DFS: Visit Left → Root → Right
    Gives sorted output for BSTs.
    """
    result = []

    def dfs(node):
        if not node:
            return

        # 1. Left subtree
        dfs(node.left)

        # 2. Visit the root
        result.append(node.val)

        # 3. Right subtree
        dfs(node.right)

    dfs(root)
    return result
```

---

# 🌟 DFS-Q3: Postorder Traversal (Left → Right → Root)

### Problem

Return the postorder traversal of a binary tree.

### Why it’s asked

* Often used for evaluating expressions
* Tests patience and correct order because root is visited last

### Code

```python
def postorder_traversal(root):
    """
    Postorder DFS: Visit Left → Right → Root
    Useful in deleting trees or evaluating expression trees.
    """
    result = []

    def dfs(node):
        if not node:
            return

        # 1. Left subtree
        dfs(node.left)

        # 2. Right subtree
        dfs(node.right)

        # 3. Visit the root last
        result.append(node.val)

    dfs(root)
    return result
```

---

# 🌳 Example Tree (used for all outputs)

```
        1
       / \
      2   3
     / \
    4   5
```

Let’s test:

```python
root = TreeNode(1,
         TreeNode(2, TreeNode(4), TreeNode(5)),
         TreeNode(3))

print("Preorder:", preorder_traversal(root))   # [1, 2, 4, 5, 3]
print("Inorder:", inorder_traversal(root))     # [4, 2, 5, 1, 3]
print("Postorder:", postorder_traversal(root)) # [4, 5, 2, 3, 1]
```

---

# ==========================================

# ✅ PART 2 — BFS Traversal

# ==========================================

Only one BFS traversal exists:

### **Level Order Traversal**

This visits nodes **level by level**, using a **queue**.

---

# 🌟 BFS-Q1: Level Order Traversal (Breadth-first)

### Problem

Return the list of levels of the tree.

### Why it’s asked

* Proves understanding of BFS + queues
* Used in shortest path, graph traversal, topological reasoning
* SAP / Amazon / Meta ask this frequently

### Code

```python
from collections import deque

def level_order(root):
    """
    BFS traversal: level by level.
    Uses a queue (FIFO) to process nodes in layers.
    """
    if not root:
        return []

    result = []
    queue = deque([root])  # start with root in queue

    while queue:
        level_size = len(queue)  # number of nodes in this level
        level_nodes = []         # values for this level

        # Process all nodes of the current level
        for _ in range(level_size):
            node = queue.popleft()    # remove from front
            level_nodes.append(node.val)

            # Push children for next level
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        # Add the collected level values
        result.append(level_nodes)

    return result
```

Test:

```python
print("Level Order:", level_order(root))
# [[1], [2, 3], [4, 5]]
```

---

# ==========================================

# 🚀 BONUS: Combined Traversal Problem Interviewers Ask

# ==========================================

### 🧩 Q: Print all DFS traversals AND BFS traversal

(in one interview question)

You already have the answers:

| Traversal         | Order                           |
| ----------------- | ------------------------------- |
| Preorder          | Root, Left, Right               |
| Inorder           | Left, Root, Right               |
| Postorder         | Left, Right, Root               |
| BFS (Level Order) | Level 0 → Level 1 → Level 2 → … |


