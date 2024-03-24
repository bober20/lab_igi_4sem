# Created by Soroka Darya.
# LR 3.
# 23.03.24


import math


def find_smallest_integer(values):
    """This function returns the smallest in modulus element."""

    return sorted(values, key=lambda x: math.fabs(x))[0]


def sum_of_list(values, index):
    """This function returns sum of elements starting with determined element."""

    return sum(values[index:])


def find_positive_integer_in_list(values):
    """This function returns the first positive number in the list."""

    return next(i for i, x in enumerate(values) if x > 0)


def get_index_and_sum(values):
    """This function returns index of the first positive number in the list and list's sum."""

    index = find_positive_integer_in_list(values)
    result_sum = sum_of_list(values, index)

    index = find_positive_integer_in_list(values)

    return index, result_sum
