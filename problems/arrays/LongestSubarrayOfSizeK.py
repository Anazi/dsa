"""
Find max sum of any contiguous subarray of size k.

Typical sliding window:
- Expand to size k
- Slide window by removing left and adding right
"""


def max_subarray_sum_k(nums, k):
    window_sum = sum(nums[:k])
    max_sum = window_sum
    print(f"length of nums: {len(nums)}, window_sum:{window_sum} and max_sum: {max_sum}")
    
    for i in range(k, len(nums)):
        print(f"i: {i}, where k:{k} with window_sum: {window_sum}")
        window_sum += nums[i] - nums[i - k]
        print(f"new window_sum: {window_sum} because nums[i]:{nums[i]} and nums[i - k]:{nums[i - k]}, nums[i] - nums[i - k]:{nums[i] - nums[i - k]}")
        max_sum = max(max_sum, window_sum)

    return max_sum


# Test
print("Max subarray sum:", max_subarray_sum_k([2, 1, 5, 1, 3, 2], 3))  # 9
