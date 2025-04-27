import json
import math
from typing import List


def power_func(val: float, p: float):
    if p == 0:
        return 1
    return val * power_func(val=val, p=p - 1)


t_val, t_p = 15, 3
print(f'power_func for val {t_val} with power {t_p}:- {power_func(val=t_val, p=t_p)}')


def arr_max(arr: List, length: int):
    if length == 0:
        return 0
    sub_res = arr_max(arr=arr, length=length - 1)
    return max(sub_res, arr[length - 1])


t_arr, t_len = [1, 8, 2, 10, 13], 4
print(f'arr_max for {t_arr} with test_length {t_len}:- {arr_max(arr=t_arr, length=t_len)}')


def arr_sum(arr: List, length: int):
    if length == 0:
        return 0
    sub_res = arr_sum(arr=arr, length=length - 1)
    return sub_res + arr[length - 1]


t_arr, t_len = [1, 8, 2, 10], 3
print(f'arr_sum for {t_arr} with test_length {t_len}:- {arr_sum(arr=t_arr, length=t_len)}')


def arr_avg(arr: List, length: int):
    if length == 0:
        return 0
    sub_res = arr_avg(arr=arr, length=length - 1)
    return (sub_res + arr[length - 1])/length


t_arr, t_len = [1, 8, 2, 10], 4
print(f'arr_avg for {t_arr} with test_length {t_len}:- {arr_avg(arr=t_arr, length=t_len)}')
