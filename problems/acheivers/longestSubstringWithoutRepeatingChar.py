"""
4️⃣ Longest Substring Without Repeating Characters
Problem

Return length of the longest substring without repeating characters.
aabcdeefghi

1️⃣ Intuition
    You want:
        A window
        That expands
        And shrinks when a duplicate appears
        Classic sliding window.

2️⃣ Why this is Strings + Hashing
    String traversal
    Hash map stores last seen index
    Needed for jumping left pointer

3️⃣ Brute Force
    Check all substrings
    ❌ O(n³)

4️⃣ Optimal Approach
    Sliding window with last seen index.
"""


class LongestSubstringSolver:
    """
    This class demonstrates multiple ways to solve:
    'Longest Substring Without Repeating Characters'

    Each method exists to answer a specific interview follow-up:
    - Why not use a set?
    - How does this work on a stream?
    - What about Unicode?
    - How to return the substring itself?
    """

    # ------------------------------------------------------------
    # 1. Standard Optimal Solution (Length only)
    # ------------------------------------------------------------
    def longest_length(self, s: str) -> int:
        """
        Uses a sliding window + hashmap.

        WHY hashmap and not set?
        - A set can tell us a duplicate EXISTS
        - But a hashmap tells us WHERE it was last seen
        - This allows us to JUMP the left pointer directly

        Time: O(n)
        Space: O(k) where k = unique characters
        """

        last_seen = {}  # char -> last index
        left = 0
        max_len = 0

        for right, ch in enumerate(s):
            # If character repeats inside current window
            if ch in last_seen and last_seen[ch] >= left:
                # Move left pointer past last occurrence
                left = last_seen[ch] + 1

            last_seen[ch] = right
            max_len = max(max_len, right - left + 1)

        return max_len

    # ------------------------------------------------------------
    # 2. Returning the actual substring (not just length)
    # ------------------------------------------------------------
    def longest_substring(self, s: str) -> str:
        """
        Same logic as longest_length, but we track indices
        to return the substring itself.

        Interviewers often ask this as a follow-up.
        """

        last_seen = {}
        left = 0
        max_len = 0
        start_index = 0

        for right, ch in enumerate(s):
            if ch in last_seen and last_seen[ch] >= left:
                left = last_seen[ch] + 1

            last_seen[ch] = right

            if right - left + 1 > max_len:
                max_len = right - left + 1
                start_index = left

        return s[start_index:start_index + max_len]

    # ------------------------------------------------------------
    # 3. WHY NOT a set? (Educational / Interview Explanation)
    # ------------------------------------------------------------
    def longest_length_using_set(self, s: str) -> int:
        """
        This method works, but is SUB-OPTIMAL in clarity.

        WHY interviewers dislike this:
        - When a duplicate appears, we must shrink the window
          ONE CHARACTER AT A TIME.
        - We cannot jump the left pointer.
        - Logic is harder to reason about.

        Still O(n), but less elegant.
        """

        seen = set()
        left = 0
        max_len = 0

        for right in range(len(s)):
            while s[right] in seen:
                seen.remove(s[left])
                left += 1

            seen.add(s[right])
            max_len = max(max_len, right - left + 1)

        return max_len

    # ------------------------------------------------------------
    # 4. Stream-based version (characters arrive one by one)
    # ------------------------------------------------------------
    def longest_length_stream(self, char_stream) -> int:
        """
        This handles a STREAM of characters instead of a full string.

        Key idea:
        - We no longer rely on indices from a string
        - We maintain our own running index counter

        This is how you'd solve it for:
        - Kafka consumer
        - Socket stream
        - File stream
        """

        last_seen = {}
        left = 0
        max_len = 0
        index = 0  # Simulated index for stream

        for ch in char_stream:
            if ch in last_seen and last_seen[ch] >= left:
                left = last_seen[ch] + 1

            last_seen[ch] = index
            max_len = max(max_len, index - left + 1)
            index += 1

        return max_len

    # ------------------------------------------------------------
    # 5. Unicode discussion (No code change needed)
    # ------------------------------------------------------------
    def unicode_note(self):
        """
        Python strings are Unicode by default.

        This means:
        - 'a', 'ä', '你', '🚀' are all valid keys
        - Hashmap solution works without modification

        If this were C++/Java:
        - You must clarify encoding (UTF-8 vs UTF-16)
        - Use code points, not bytes
        """
        pass

    # ------------------------------------------------------------
    # 6. Test runner (what you'd verbally walk through)
    # ------------------------------------------------------------
    def run_tests(self):
        print("=== BASIC LENGTH ===")
        print(self.longest_length("abcabcbb"))  # 3
        print(self.longest_length("bbbbb"))     # 1
        print(self.longest_length("pwwkew"))    # 3

        print("\n=== SUBSTRING ===")
        print(self.longest_substring("abcabcbb"))  # "abc"
        print(self.longest_substring("pwwkew"))    # "wke"

        print("\n=== SET VERSION ===")
        print(self.longest_length_using_set("abcabcbb"))  # 3

        print("\n=== STREAM VERSION ===")
        stream = iter("abcabcbb")
        print(self.longest_length_stream(stream))  # 3

        print("\n=== UNICODE ===")
        print(self.longest_length("你好吗你好"))  # 3


# ------------------------------------------------------------
# Run tests
# ------------------------------------------------------------
solver = LongestSubstringSolver()
solver.run_tests()


