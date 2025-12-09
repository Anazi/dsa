import heapq


def find_k_largest(nums, k):
    """
        Only store top K largest seen so far. Heap top always gives smallest of those K.
    """
    # Min-heap of size k: smallest of the largest k is at top
    min_heap = nums[:k]
    heapq.heapify(min_heap)
    print(f"minheap after heapify of size {k} --> {min_heap}")

    for num in nums[k:]:
        if num > min_heap[0]:  # If current number is larger than smallest in heap
            heapq.heappushpop(min_heap, num)  # Push and pop(smallest item) in one step
            print(f"for num {num}'s changes, minheap becomes: {min_heap}")

    return sorted(min_heap, reverse=True)  # Largest to smallest


# Test
t_nums = [3, 1, 5, 12, 2, 11, 6, 1, 3, 7]
t_k = 3
print(f"For nums:{t_nums} and K:{t_k}, the k largest elements are:", find_k_largest(t_nums, t_k))  # Output: [12, 11, 5]
