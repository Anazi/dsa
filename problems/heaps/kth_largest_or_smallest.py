import heapq


def kth_largest(nums, k):
    return heapq.nlargest(k, nums)[-1]  # O(N log k)


def kth_smallest(nums, k):
    return heapq.nsmallest(k, nums)[-1]  # O(N log k)


# Test
print("Kth largest:", kth_largest([3, 2, 1, 5, 6, 4], 2))  # Output: 5
print("Kth smallest:", kth_smallest([3, 2, 1, 5, 6, 4], 2))  # Output: 2
