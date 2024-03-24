import useful_functions
import math


from task1 import using_power_series
from task2 import integer_sum
from task3 import count_letters, count_integers
from task4 import print_odd_words, find_the_longest_word, count_words_in_string
from task5 import get_index_and_sum


@useful_functions.decorator_for_menu
def input_function_for_task1():
    """This function is an input function for task1"""
    print("Enter x: ")
    x = input()

    while not useful_functions.check_is_number(x) or math.fabs(float(x)) <= 1:
        print("Error. Enter x: ")
        x = input()

    x = float(x)

    print("Enter eps: ")
    eps = input()

    while not useful_functions.check_is_number(eps):
        eps = input()

    eps = float(eps)

    print("Calculations has started")
    print(using_power_series.__doc__)
    print("x\tn\tF(x)\tMath F(x)\teps\n")

    func_result, math_result, n = using_power_series(x, eps)
    result_list = [x, n, func_result, math_result, eps]
    result_string = ""
    for item in result_list:
        result_string += str(item)
        result_string += '\t'

    return result_string


@useful_functions.decorator_for_menu
def input_function_for_task2():
    """This function is an input function for task2"""

    values = []

    while True:
        print("Input negative integers, to exit input positive integer.")
        n = input()

        if not useful_functions.check_is_integer(n):
            continue

        n = int(n)

        if n > 0:
            break

        values.append(n)

    return integer_sum(values)


@useful_functions.decorator_for_menu
def input_function_for_task3():
    """This function is an input function for task3"""

    string = input("Input string: ")

    return f"integers: {count_integers(string)}, uppercase letters: {count_letters(string)}"


@useful_functions.decorator_for_menu
def input_function_for_task4():
    """This function is an input function for task4"""

    string = input("Enter a string: ")

    return f"odd_words: {print_odd_words(string)}, \nthe longest word: {find_the_longest_word(string)},\n" \
           f"number of words in string: {count_words_in_string(string)}"


@useful_functions.decorator_for_menu_without_print
def input_function_for_task5():
    """This function executes the task number five from lab."""

    values = []
    n = input("Enter size of array:")

    while not useful_functions.check_is_integer(n):
        print("Error. Enter size of array: ")
        n = input()

    for i in range(int(n)):
        x = input("Enter a number: ")
        while not useful_functions.check_is_number(x):
            print("Error. Enter a number: ")
            x = input()

        values.append(float(x))

    print("Using only input")
    print("Array: ")

    for i in values:
        print(f'{i:.3f}')
    print(f"Result: {get_index_and_sum(values)}")

    print("Using generator")

    values = useful_functions.generator(values)

    print("Array: ")
    for i in values:
        print(f'{i:.3f}')
    print(f"Result: {get_index_and_sum(values)}")
