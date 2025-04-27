def swap(my_list, index1, index2):
    """
    Method to swap the items
    :param my_list:
    :param index1:
    :param index2:
    :return:
    """
    temp = my_list[index1]
    my_list[index1] = my_list[index2]
    my_list[index2] = temp


def pivot(my_list, pivot_index, end_index):
    """
    This method
    1. readjusts the list in the format:
        [items smaller than pivot] | pivot | [items bigger than pivot], using pivot idx
    2. returns the pivot index
    :param my_list:
    :param pivot_index:
    :param end_index:
    :return: pivot index (not the pivot value)
    """
    # Setting the swap index at pivot index -> In the beginning, the swap and pivot both
    #   points to the same item(in the list)
    swap_index = pivot_index
    # Start a for loop such that the range:
    #   - starts post the pivot (on the next item in the list)
    #   - stops at one more than the end_index, because the last value will not be considered by the for loop
    for i in range(pivot_index + 1, end_index + 1):
        # Condition for swapping values within the list till the
        #   last value -> pivot | [items smaller than pivot] | [items bigger than pivot]
        if my_list[i] < my_list[pivot_index]:
            swap_index += 1
            swap(my_list, swap_index, i)
    # Rearranging the items to ->  [items smaller than pivot] | pivot | [items bigger than pivot]
    swap(my_list, pivot_index, swap_index)
    # Return the Pivot INDEX, needed for the actual quick sort
    return swap_index


def quick_sort_helper(my_list, left, right):
    """
    This method quick sorts the list based on index using pivot format.
    Approach -> Divide and conquer
    :param my_list: list to be sorted
    :param left: index of the left most value
    :param right: index of the right most value
    :return: quick sorted list
    """
    # Sort only if the left index is smaller that the right index
    if left < right:
        # Initial sorting and rearrangement to the format:
        #   [items smaller than pivot] | pivot | [items bigger than pivot], get the index of the pivot item
        pivot_index = pivot(my_list, left, right)
        # Recursively sort the left side of the list w.r.t Pivot
        quick_sort_helper(my_list, left, pivot_index - 1)
        # Recursively sort the right side of the list w.r.t Pivot
        quick_sort_helper(my_list, pivot_index + 1, right)
    return my_list


def quick_sort(my_list):
    # Create the left and the right of the list:
    #   left -> start with 0 (first index of the list)
    #   right -> since starting from 0th index, right should be 1 less than the len of list - "len(my_list) - 1"
    return quick_sort_helper(my_list, 0, len(my_list) - 1)


print(quick_sort([4, 6, 1, 7, 3, 2, 5, 13, 88888, 2342, 453, 111, 34343]))


"""
# BIG O (*** Never use on SORTED DATA. For Sorted data, use Insertion Sort(or almost sorted data))
1. Time  Complexity - 
        Case 1 (When Data is not sorted):
            for Pivot, n no. of steps to get the pivot -> O(n)
            for recursion, post pivot the list is recursively sorted -> O(log n)
                      --> "O(n log n)"
        Case 2 (When data is sorted) [Actual WORST CASE]:
            Each item is checked on pivot function only since quick sort will not get triggered.
            Thus, Pivot(n times) -->  "O(n^2)"
"""