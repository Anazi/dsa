import heapq


def find_k_smallest(nums, k):
    """
        Max-heap keeps only K smallest. Top is largest of them (negated).
    """
    # Max-heap of size k using negative values
    max_heap = [-num for num in nums[:k]]
    heapq.heapify(max_heap)

    for num in nums[k:]:
        if -num > max_heap[0]:  # Smaller than largest in heap
            heapq.heappushpop(max_heap, -num)

    return sorted([-x for x in max_heap])  # Return sorted smallest k


# Test
t_nums = [3, 1, 5, 12, 2, 11]
print("K smallest:", find_k_smallest(t_nums, 3))  # Output: [1, 2, 3]
