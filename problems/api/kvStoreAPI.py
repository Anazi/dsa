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


# Improved version


"""
Improved Key-Value Store with TTL (Singular Cleanup Version)

Key principles:
- ALL expiration deletions happen ONLY inside _cleanup()
- get(), put(), delete() NEVER delete expired keys directly
- Every public API method calls _cleanup() first
"""


class KeyValueStoreImproved:
    def __init__(self):
        # HashMap: key -> (value, expire_time)
        self.store = {}

        # Min-heap sorted by expire_time: [(expire_time, key)]
        self.expire_heap = []

    def _cleanup(self):
        """
        Singular cleanup point for expired keys.

        Removes all expired entries from both:
        - store (hash map)
        - expire_heap (min-heap)

        Only deletes a key if:
        - heap says it's expired, AND
        - store expiration matches the heap timestamp
        """
        now = time.time()

        # Keep removing expired keys in order of earliest expiry
        while self.expire_heap and self.expire_heap[0][0] <= now:
            expire_time, key = heapq.heappop(self.expire_heap)

            # Ensure key still exists AND timestamps match
            if key in self.store:
                _, current_expire = self.store[key]

                # Only delete if heap timestamp matches store timestamp
                if expire_time == current_expire:
                    del self.store[key]

    def put(self, key, value, ttl_seconds):
        """
        Insert/update a key with TTL.
        """
        self._cleanup()  # ensure store is clean first

        expire_time = time.time() + ttl_seconds

        # Save in hashmap
        self.store[key] = (value, expire_time)

        # Push into heap for time-based cleanup
        heapq.heappush(self.expire_heap, (expire_time, key))

    def get(self, key):
        """
        Return value if key exists (and not expired).
        """
        self._cleanup()  # singular cleanup

        if key not in self.store:
            return None

        value, expire_time = self.store[key]

        # Expiration already handled in _cleanup() => ALWAYS safe to return
        return value

    def delete(self, key):
        """
        Delete key immediately.
        """
        self._cleanup()  # always clean before deletion

        if key in self.store:
            del self.store[key]


# ---------------- TESTING ----------------

if __name__ == "__main__":
    kv = KeyValueStoreImproved()

    kv.put("session", "abc123", ttl_seconds=3)
    print("Get session:", kv.get("session"))  # "abc123"

    time.sleep(4)
    print("After expiry:", kv.get("session"))  # None

    kv.put("k1", "v1", ttl_seconds=10)
    kv.put("k2", "v2", ttl_seconds=1)
    time.sleep(2)
    print("k1 still valid:", kv.get("k1"))  # "v1"
    print("k2 expired:", kv.get("k2"))  # None
