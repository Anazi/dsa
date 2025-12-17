"""
1️⃣ LRU Cache (Object-Oriented, Interview-Grade)
🧠 Intuition (how to explain it live)
“LRU means we evict the item that hasn’t been used for the longest time.
So I need:
    Fast access by key
    Fast reordering by recent usage”

    --> That immediately gives:
            HashMap → O(1) lookup
            Doubly Linked List → O(1) move-to-front + eviction

❓ Why not just a list?
    Removing from the middle is O(n)
    Interviewers expect O(1) operations

⏱ Complexity
    get / put: O(1)
    Space: O(capacity)
"""


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev: Node = None
        self.next: Node = None


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity

        self.cache = {}

        # Dummy head and tail to avoid null-checks
        self.head = Node(0, 0)
        self.tail = Node(0, 0)

        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node):
        # HEAD <-> A <-> B(dropped) <-> C <-> TAIL
        prev_node = node.prev
        next_node = node.next

        prev_node.next = next_node
        next_node.prev = prev_node

    def _add_to_front(self, node: Node):
        # HEAD <-> A <-> B(moving) <-> C <-> TAIL

        left = self.head
        right = self.head.next

        # B points to neighbors
        node.prev = left
        node.next = right

        # Neighbors pointing back
        left.next = node
        right.prev = node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1

        node: Node = self.cache[key]
        self._remove(node)
        self._add_to_front(node)
        return node.value

    def put(self, key: int, value: int):
        if key in self.cache:
            node: Node = self.cache[key]
            self._remove(node)
            self._add_to_front(node)
        else:
            node: Node = Node(key=key, value=value)
            self.cache[key] = node
            self._add_to_front(node)

            # special case --> if capacity exceeded
            if len(self.cache) > self.capacity:
                node_to_remove = self.tail.prev
                self._remove(node=node_to_remove)
                del self.cache[node_to_remove.key]

    @staticmethod
    def run_tests():
        print("=== LRU CACHE TESTS ===")

        lru = LRUCache(2)
        lru.put(1, 1)
        lru.put(2, 2)

        print(lru.get(1))  # 1
        lru.put(3, 3)  # evicts 2
        print(lru.get(2))  # -1

        lru.put(4, 4)  # evicts 1
        print(lru.get(1))  # -1
        print(lru.get(3))  # 3
        print(lru.get(4))  # 4


LRUCache.run_tests()
