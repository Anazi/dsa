"""
3️⃣ Group Anagrams (a word, phrase, or name formed by rearranging the letters of another, such as cinema, formed from iceman.)
Problem
    Group words that are anagrams.

1️⃣ Intuition
    Anagrams:
        - Same characters
        - Same frequency
        - Order doesn’t matter
            So you need a canonical representation.

2️⃣ Why this is Strings + Hashing
    You need:
        A way to normalize words
        A map from normalized form → list of words
        Hash maps naturally group values.

4️⃣ Optimal Approach
    Two valid keys:
        - Sorted string ("eat" → "aet")
        - Frequency tuple (26-length array)
    Sorting is acceptable unless constraints are huge.
"""

from collections import defaultdict


def group_anagrams(words):
    groups = defaultdict(list)

    for word in words:
        key = ''.join(sorted(word))
        groups[key].append(word)

    return list(groups.values())


# Tests
print(group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))



"""
5️⃣ Optimal Approach (What we actually do)
    For each word:
        Create an array of size 26
        Count characters
        Convert array to tuple
        Use tuple as dictionary key
        Append word to its group
"""


def group_anagrams_tup(words):
    groups = {}  # key: frequency tuple, value: list of words

    for word in words:
        # Step 1: create frequency array
        freq = [0] * 26

        for ch in word:
            freq[ord(ch) - ord('a')] += 1
        print(f"freq: {freq}")

        # Step 2: convert to tuple (hashable)
        key = tuple(freq)

        # Step 3: group words
        if key not in groups:
            groups[key] = []

        groups[key].append(word)

    # Step 4: return grouped values
    return list(groups.values())


# Tests
print(group_anagrams_tup(["eat", "tea", "tan", "ate", "nat", "bat"]))


