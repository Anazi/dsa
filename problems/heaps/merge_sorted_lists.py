"""
    📋 Problem Statement (Again)
        You are given k sorted iterators.
        Merge them into a single sorted iterator, such that:
            -> .next() gives the next smallest element.
            -> .has_next() tells if more elements exist.
            -> Every operation should be efficient (not naive rebuilding).

    🔥 Key Points
        - Multiple sorted streams → You need a way to always pull the smallest next.
        - Min-Heap allows you to get the minimum efficiently.
        - Lazy fetching → Only load next element when needed, not upfront.
        - Every .next() must do:
            - Pop the smallest from heap.
            - Push the next from that iterator if available.
"""


import heapq
from typing import Iterator, List


class MergeSortedIterator:
    def __init__(self, sorted_iterables: List[List[int]]):
        self.sorted_iterables = sorted_iterables
        self.min_heap = []
        self.iterators = []

    def build_ds(self):
        """
            Build initial heap by inserting the first element of each iterator.
                LAZY LOADING, ONLY FIRST ELEMENTS IN HEAP
        """
        for idx, iterable in enumerate(self.sorted_iterables):
            it = iter(iterable)
            self.iterators.append(it)

            first_value = next(it, None)
            if first_value is not None:
                # Store tuple: (value, source iterator index)
                heapq.heappush(self.min_heap, (first_value, idx))

    def has_next(self) -> bool:
        """
            Returns True if there are still elements to process.
        """
        return len(self.min_heap) > 0

    def next(self) -> int:
        """
            Returns the next smallest element across all iterators.
        """
        if not self.has_next():
            raise StopIteration("No more elements.")

        # Pop the smallest element for heap
        value, idx = heapq.heappop(self.min_heap)

        # Get the NEXT VALUE from "iterator" based on "idx" and push it to "min_heap"
        next_value = next(self.iterators[idx], None)
        if next_value is not None:
            heapq.heappush(self.min_heap, (next_value, idx))

        return value

    def merge_sorted_iterators(self) -> List[int]:
        """
            Service method to merge all iterators into one sorted list.
        """
        self.build_ds()

        # Get the merged list and return list
        result = []
        while self.has_next():
            result.append(self.next())
        return result


lists = [
        [1, 4, 7],
        [2, 5, 8],
        [3, 6, 9]
    ]

merger = MergeSortedIterator(lists)
merged_output = merger.merge_sorted_iterators()
print("Merged Sorted Output:", merged_output)  # Output: [1, 2, 3, 4, 5, 6, 7, 8, 9]
