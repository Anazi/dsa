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


my_test_list = [4, 6, 1, 7, 3, 2, 5]

print(pivot(my_test_list, 0, 6))

print(my_test_list)


# def swap_t(t_list, index1, index2):
#     temp = t_list[index1]
#     t_list[index1] = t_list[index2]
#     t_list[index1] = temp
#
#
# def pivot_t(t_list, pivot_index, end_index):
#     swap_index = pivot_index
#     for i in range(pivot_index + 1, end_index + 1):
#         if t_list[i] < t_list[pivot_index]:
#             swap_index += 1
#             swap(t_list, swap_index, i)
#     swap(t_list, pivot_index, swap_index)
#     return pivot_index
