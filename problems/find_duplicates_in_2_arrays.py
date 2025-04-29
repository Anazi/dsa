"""
    📋 Problem Statement
        Given two arrays of integers:

        Find duplicates (common elements) efficiently.

        Also:
            If numbers are very large (huge integers), and you need to store them efficiently in a database,
            how would you design it?

        How to achieve O(log N) search and insertion?

    📄 Example
        Input:
            arr1 = [1, 2, 3, 5, 7]
            arr2 = [3, 5, 6, 7, 8]

        Output:
        [3, 5, 7]
"""


def find_duplicates(arr1, arr2):
    # HashSet allows O(1) lookup per element.
    hashset = set(arr1)

    duplicates = []
    for num in arr2:
        if num in hashset:
            duplicates.append(num)
    return duplicates


t_arr1 = [1, 2, 3, 5, 7]
t_arr2 = [3, 5, 6, 7, 8]
print(f"Find duplicates between {t_arr1} and {t_arr2}: {find_duplicates(t_arr1, t_arr2)}")
