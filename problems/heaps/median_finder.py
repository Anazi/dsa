import heapq


class MedianFinder:
    """
        - Maintain two balanced heaps: left half (max-heap), right half (min-heap).
        - Median = root(s) of heaps.
    """
    def __init__(self):
        self.small = []  # Max-heap (inverted)
        self.large = []  # Min-heap

    def add_num(self, num):
        heapq.heappush(self.small, -num)
        heapq.heappush(self.large, -heapq.heappop(self.small))  # Balance towards large

        if len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))

    def find_median(self):
        if len(self.small) > len(self.large):
            return -self.small[0]
        return (-self.small[0] + self.large[0]) / 2


# Test
mf = MedianFinder()
for n in [5, 15, 1, 3]:
    mf.add_num(n)
print("Median:", mf.find_median())  # Output: 4.0
