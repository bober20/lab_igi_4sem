from task5.math_array import MathArray
import useful_functions as use_func


def input_function_for_task5():
    while True:
        exit_string = input("Exit? y/n: ")
        if exit_string == "y":
            break

        n = input("Enter array size: ")

        while True:
            if use_func.check_is_integer(n):
                n = int(n)
                break
            print("Error.")
            n = input("Enter array size: ")

        math_array = MathArray(n)

        print("Generated array: ", math_array.array)
        print("Odd array: ", math_array.get_odd_array())
        print("Odd array sum: ", math_array.count_sum_of_odd_numbers())
        print("Standard deviation using formula: ", math_array.get_standard_deviation_formula())
        print("Standard deviation using numpy: ", math_array.get_standard_deviation_numpy())
