"""
2️⃣ Two Sum (Return Indices)
Problem

Given array nums and target t, return indices of two numbers such that they add up to t.
nums: [1, 3, 5, 7, 2], t=4 ==> [1,3]

1️⃣ Intuition

For each number x, you want to know:

“Have I already seen t - x?”

This is memory vs speed trade-off.

2️⃣ Why this is an Arrays + Hashing problem

Array gives sequential access

Hash map lets you:

Store previously seen values

Check complement in O(1)

Sorting breaks indices → bad choice unless stated otherwise.

4️⃣ Optimal Approach

Single pass:

    - Store value → index
    - Check complement before inserting
"""


def two_sum(nums, target):
    seen = {}

    for i, num in enumerate(nums):
        complement = target - num

        if complement in seen:
            return [seen[complement], i]

        seen[num] = i

    return []


# Tests
print(two_sum([2, 7, 11, 15], 9))  # [0, 1]
print(two_sum([3, 2, 4], 6))  # [1, 2]
print(two_sum([3, 3], 6))  # [0, 1]
