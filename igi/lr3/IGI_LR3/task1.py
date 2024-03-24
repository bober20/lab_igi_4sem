# Created by Soroka Darya.
# LR 3.
# 23.03.24


import math
import useful_functions


def using_power_series(x, eps):
    """This function finds the result using power series."""

    n = 0.0

    math_result = math.log((x + 1) / (x - 1))
    func_result = 0.0

    while n <= 500 and math_result - func_result > eps:
        func_result += 2.0 / ((n * 2.0 + 1) * math.pow(x, n * 2.0 + 1))
        n += 1

    # print("x\tn\tF(x)\tMath F(x)\teps\n")
    # print(x, "\t", n, "\t", func_result, "\t", math_result, "\t", eps, "\n")

    return func_result, math_result, n
