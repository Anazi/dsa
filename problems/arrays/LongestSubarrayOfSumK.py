"""
Given nums and an integer k, find longest subarray with sum <= k.

Use sliding window:
- Expand right
- Shrink from left if window sum > k
"""


def longest_subarray_sum_leq_k(nums, k):
    left = 0
    window_sum = 0
    max_len = 0

    print(f"range(len(nums)): {range(len(nums))}")
    for right in range(len(nums)):
        window_sum += nums[right]

        # Shrink window when sum exceeds k
        while window_sum > k:
            window_sum -= nums[left]
            left += 1

        max_len = max(max_len, right - left + 1)

    return max_len


# Test
print("Longest sum<=k:", longest_subarray_sum_leq_k([1, 2, 3, 4, 5], 7))  # 3 (subarray: [1,2,3])

# ================ xxx ================

"""
Return both the max length AND the actual subarray with sum <= k.

Sliding window:
- Expand right
- Shrink from left if the window sum exceeds k
- Track best window boundaries (best_left, best_right)
"""


def longest_subarray_sum_leq_k(nums, k):
    left = 0
    window_sum = 0
    max_len = 0
    best_left, best_right = 0, -1  # Default if no subarray found

    for right in range(len(nums)):
        window_sum += nums[right]

        # Shrink window when sum exceeds k
        while window_sum > k:
            window_sum -= nums[left]
            left += 1

        # Check if current window is the best so far
        if (right - left + 1) > max_len:
            max_len = right - left + 1
            best_left, best_right = left, right

    # Extract subarray
    best_subarray = nums[best_left: best_right + 1] if max_len > 0 else []

    return max_len, best_subarray


# Test
nums = [1, 2, 3, 4, 5]
k = 7
length, subarray = longest_subarray_sum_leq_k(nums, k)
print("Max length:", length)  # 3
print("Subarray:", subarray)  # [1, 2, 3]
