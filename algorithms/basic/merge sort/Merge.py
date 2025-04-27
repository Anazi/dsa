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
    # For dealing with list1 and list2 [MUST be sorted]
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


print(merge([1, 2, 7, 8], [3, 4, 5, 6]))

