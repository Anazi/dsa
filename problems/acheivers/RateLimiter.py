"""
2️⃣ Rate Limiter (Backend / SaaS-Oriented)

🧠 Intuition

“A rate limiter answers one question:
Should I allow this request right now?”

So you need:
    Time awareness
    Per-user or per-key tracking
    Efficient cleanup of old requests

❓ Which strategy?
    We’ll implement Sliding Window using timestamps because:
    More accurate than fixed window
    Easy to explain
    Clean logic

⏱ Complexity
    Per request: O(1) amortized
    Space: O(N) where N = requests in window
"""


import time
from collections import deque
from threading import Lock


class RateLimiter:
    """
    Sliding Window Rate Limiter.

    This class contains:
    1. A naive (NOT thread-safe) implementation
    2. A correct thread-safe implementation using per-key locks
    """

    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds

        # --------------------------------------------------------
        # DATA STRUCTURES (IMPORTANT TO VISUALIZE)
        # --------------------------------------------------------

        # key -> deque of timestamps
        # Example:
        # {
        #   "user1": deque([1000.0, 1001.2, 1002.5]),
        #   "user2": deque([1003.1])
        # }
        self.requests = {}

        # key -> lock (used ONLY in thread-safe version)
        # Example:
        # {
        #   "user1": <Lock object at 0xABC>,
        #   "user2": <Lock object at 0xDEF>
        # }
        self.locks = {}

        # Protects creation of per-key deque + lock
        self.global_lock = Lock()

    # ============================================================
    # 1️⃣ NAIVE VERSION (NOT THREAD SAFE)
    # ============================================================
    def allow_request_naive(self, key: str, current_time: float = None) -> bool:
        """
        ❌ NOT SAFE under parallel requests.

        Problem:
        - len() check and append() are NOT atomic together
        - Two threads can both pass the check and exceed the limit
        """

        if current_time is None:
            current_time = time.time()

        if key not in self.requests:
            self.requests[key] = deque()

        timestamps = self.requests[key]

        # Cleanup old timestamps
        while timestamps and current_time - timestamps[0] > self.window_seconds:
            timestamps.popleft()

        # ❌ Race condition here under parallel access
        if len(timestamps) < self.max_requests:
            timestamps.append(current_time)
            return True
        else:
            return False

    # ============================================================
    # 2️⃣ THREAD-SAFE VERSION (PER-KEY LOCKING)
    # ============================================================
    def _get_key_structs(self, key):
        """
        Lazily initializes per-key deque and lock.

        This must be protected by a global lock to avoid:
        - Two threads creating two different deques for same key
        """

        with self.global_lock:
            if key not in self.requests:
                self.requests[key] = deque()
                self.locks[key] = Lock()

            return self.requests[key], self.locks[key]

    def allow_request(self, key: str, current_time: float = None) -> bool:
        """
        ✅ Thread-safe version.

        Guarantees that for a given key:
        - cleanup
        - count check
        - append

        all happen atomically.
        """

        if current_time is None:
            current_time = time.time()

        timestamps, lock = self._get_key_structs(key)

        # Per-key critical section
        with lock:
            # Cleanup old timestamps
            while timestamps and current_time - timestamps[0] > self.window_seconds:
                timestamps.popleft()

            if len(timestamps) < self.max_requests:
                timestamps.append(current_time)
                return True
            else:
                return False

    # ============================================================
    # TESTS
    # ============================================================
    @staticmethod
    def run_tests():
        print("=== RATE LIMITER TESTS ===")

        limiter = RateLimiter(max_requests=3, window_seconds=10)
        base_time = 1000.0

        print("\n-- Naive version (logic only, not concurrency-safe) --")
        print(limiter.allow_request_naive("user1", base_time))       # True
        print(limiter.allow_request_naive("user1", base_time + 1))   # True
        print(limiter.allow_request_naive("user1", base_time + 2))   # True
        print(limiter.allow_request_naive("user1", base_time + 3))   # False

        print("\n-- Thread-safe version --")
        limiter = RateLimiter(max_requests=3, window_seconds=10)

        print(limiter.allow_request("user1", base_time))       # True
        print(limiter.allow_request("user1", base_time + 1))   # True
        print(limiter.allow_request("user1", base_time + 2))   # True
        print(limiter.allow_request("user1", base_time + 3))   # False

        print("\n-- Window slides --")
        print(limiter.allow_request("user1", base_time + 11))  # True

        print("\n-- Different users (no contention) --")
        print(limiter.allow_request("user2", base_time))       # True
        print(limiter.allow_request("user2", base_time + 1))   # True


# Run tests
RateLimiter.run_tests()
