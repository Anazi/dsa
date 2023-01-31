def bubble_sort(my_list):
    for i in range(len(my_list) - 1, 0, -1):
        for j in range(i):
            if my_list[j] > my_list[j + 1]:
                temp = my_list[j]
                my_list[j] = my_list[j + 1]
                my_list[j + 1] = temp
    return my_list


print(bubble_sort([4, 2, 6, 5, 1, 3]))


for i in range(6, 0, -1):
    print(i)
    for j in range(i):
        print(j)
