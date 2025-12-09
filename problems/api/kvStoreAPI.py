import heapq
import time

"""
Design a Key-Value Store API with TTL.

Requirements:
- put(key, value, ttl)
- get(key) returns value or None
- delete(key)
- Keys auto-expire after TTL
- Expired keys never returned
- Efficient cleanup using min-heap of expire timestamps
"""


class KeyValueStore:
    def __init__(self):
        # key -> (value, expire_time)
        self.store = {}

        # min-heap of (expire_time, key)
        self.expire_heap = []

    def _cleanup(self):
        """
        Remove expired keys.

        Expiration rule:
        - If heap top has expired timestamp, remove it
        - But only if it matches the current store timestamp
          (handles overwrites properly)
        """
        now = time.time()

        while self.expire_heap and self.expire_heap[0][0] <= now:
            expire_time, key = heapq.heappop(self.expire_heap)

            # Check if key still exists and matches this expire time
            if key in self.store:
                current_value, current_expire = self.store[key]

                # Only delete if the timestamps match
                if current_expire == expire_time:
                    del self.store[key]

    def put(self, key, value, ttl_seconds):
        """
        Insert or update a key with given TTL.
        TTL is absolute expiry from now: expire_time = now + ttl
        """
        expire_time = time.time() + ttl_seconds

        # Write to store hash map
        self.store[key] = (value, expire_time)

        # Push expiry to heap
        heapq.heappush(self.expire_heap, (expire_time, key))

    def get(self, key):
        """
        Return value if key exists and not expired.
        Otherwise return None.
        """
        self._cleanup()

        if key not in self.store:
            return None

        value, expire_time = self.store[key]

        # Check expiration
        if expire_time <= time.time():
            # Expired - remove immediately
            del self.store[key]
            return None

        return value

    def delete(self, key):
        """
        Delete a key immediately, if present.
        """
        if key in self.store:
            del self.store[key]


# ---------------- TESTING ----------------

kv = KeyValueStore()
kv.put("session", "abc123", ttl_seconds=3)
print("Get session:", kv.get("session"))  # "abc123"

time.sleep(4)
print("After expiry:", kv.get("session"))  # None

kv.put("k1", "v1", ttl_seconds=10)
kv.put("k2", "v2", ttl_seconds=1)
time.sleep(2)
print("k1 still valid:", kv.get("k1"))  # v1
print("k2 expired:", kv.get("k2"))  # None
