import useful_functions as use_func
from task4.parallelogram import Parallelogram


def input_function_for_task4():

    string = input("Enter the first parallelogram's diagonal: ")

    while True:
        if use_func.check_is_number(string):
            d1 = float(string)
            break
        print("Error.")
        string = input("Enter the first parallelogram's diagonal: ")

    string = input("Enter the second parallelogram's diagonal: ")

    while True:
        if use_func.check_is_number(string):
            d2 = float(string)
            break
        print("Error.")
        string = input("Enter the second parallelogram's diagonal: ")

    string = input("Enter diagonals' angle: ")

    while True:
        if use_func.check_is_number(string):
            angle = float(string)
            break
        print("Error.")
        string = input("Enter diagonals' angle: ")

    color = input("Enter parallelogram's color: ")

    parallelogram = Parallelogram(d1, d2, angle, color)

    parallelogram.draw_parallelogram()

