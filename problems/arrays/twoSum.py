"""
Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.
Assume that each input would have exactly one solution.

Eg:
# Example Usage
nums = [2, 7, 11, 15]
target = 9
solver = TwoSumSolver(nums, target)
"""


class TwoSum:
    def __init__(self, nums, target):
        self.nums = nums
        self.target = target
        self.address_cache = {}

    def get_res_brute(self):
        for i in range(len(self.nums)):
            for j in range(i + 1, len(self.nums)):
                if self.nums[i] + self.nums[j] == self.target:
                    return [i, j]
        return [-1, -1]

    def get_res(self):
        """
        Since we are going to look for the complement in the address_cache, it is better to store the address_cache as num -> idx
        And, the cache must be created on the fly just like timestamp check in micro-batching data pipeline.
        """
        for idx, num in enumerate(self.nums):
            complement = self.target - num
            if complement in self.address_cache:
                return [self.address_cache[complement], idx]
            self.address_cache[num] = idx


t_nums = [11, 2, 15, 7]
t_target = 9
solver = TwoSum(t_nums, t_target)
print(f"Brute: {solver.get_res_brute()}")
print(f"Optimised: {solver.get_res()}")
