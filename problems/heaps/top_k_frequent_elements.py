from collections import Counter
import heapq


def top_k_frequent_elements(nums, k):
    """
        Heap keeps top K frequent elements by frequency count.

    """
    freq = Counter(nums)
    # Min-heap by frequency (store (freq, num))
    heap = []

    for num, count in freq.items():
        heapq.heappush(heap, (count, num))
        if len(heap) > k:
            heapq.heappop(heap)

    return [num for _, num in heap]


# Test
print("Top K frequent:", top_k_frequent_elements([1, 1, 1, 2, 2, 3], 2))  # Output: [1, 2]
