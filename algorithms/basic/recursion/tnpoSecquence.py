from typing import List


def three_n_plus_one_seq(val: float):
    print(f'{val}')

    if val == 1:
        return

    if val % 2 == 0:
        new_val = val/2
        three_n_plus_one_seq(val=new_val)
    else:
        new_val = 3*val+1
        three_n_plus_one_seq(val=new_val)


print(three_n_plus_one_seq(val=3))


def len_three_n_plus_one_seq(val: float):
    if val == 1:
        return 1

    if val % 2 == 0:
        new_val = val/2
        return 1 + len_three_n_plus_one_seq(val=new_val)
    else:
        new_val = 3*val+1
        return 1 + len_three_n_plus_one_seq(val=new_val)


print(len_three_n_plus_one_seq(val=4))
