def number_of_paths(m, n):
    """
    Count all possible paths from top left to bottom right of a mXn matrix
    :param m: int
    :param n: int
    :return: int
    """
    if m == 0 or n == 0:
        return 1
    return number_of_paths(m - 1, n) + number_of_paths(m, n - 1)


m1 = 2
n1 = 3


# print(number_of_paths(m1, n1))  # 10


def product_except_self(nums):
    """
    :type nums: List[int]
    :rtype: List[int]
    eg:
    nums: [1, 2, 3, 4]
    res: [24, 12, 8, 6]
    """
    res = [1] * len(nums)

    pre_val = 1
    for i in range(len(nums)):
        # Pre prod from left to right - [1, 1, 2, 6]
        res[i] = pre_val
        pre_val = pre_val * nums[i]

    post_val = 1
    for i in range(len(nums) - 1, -1, -1):
        res[i] = res[i] * post_val
        post_val = post_val * nums[i]
    return res  # [24, 12, 8, 6]


print(product_except_self(nums=[1, 2, 3, 4]))
