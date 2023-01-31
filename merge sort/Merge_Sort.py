def merge(list1, list2):
    """
    This method to be only used when the data is SORTED.
    :param list1:
    :param list2:
    :return:
    """
    combined = []
    i = 0
    j = 0
    # For dealing with list1 and list2
    while i < len(list1) and j < len(list2):
        if list1[i] < list2[j]:
            combined.append(list1[i])
            i += 1
        else:
            combined.append(list2[j])
            j += 1
    #  Case when list1 has a few items remaining
    while i < len(list1):
        combined.append(list1[i])
        i += 1
    #  Case when list2 has a few items remaining
    while j < len(list2):
        combined.append(list2[j])
        j += 1
    return combined


def merge_sort(my_list):
    # Base Case - if list has only 1 element
    if len(my_list) == 1:
        return my_list
    # to make sure that the mid is a whole number and not fraction
    mid = int(len(my_list) / 2)
    # Make a left list excluding mid
    left = my_list[:mid]
    # Make a right list including mid
    right = my_list[mid:]
    # Add recursion on the return to break the list till 1 element in each list,
    #   and then Merge them -> Merge Sort
    return merge(merge_sort(left), merge_sort(right))


print(merge_sort([3, 1, 4, 2, 7, 8, 19, 5]))

'''
# BIG O
1. Space Complexity - 0(n) because the list is being broken (multiple new list)
2. Time  Complexity - O(log n) (list are divided making them smaller) + 
                      O(n) (to combine the broken lists)
                      --> "O(n log n)" 
'''