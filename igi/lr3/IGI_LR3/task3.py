# Created by Soroka Darya.
# LR 3.
# 23.03.24


import useful_functions


# def decorator_timer(func):
#     """This is a decorator that counts amount of time spent on processing."""
#
#     def wrapper(string):
#         start_time = time.time()
#         print(func(string))
#         end_time = time.time()
#         return "Time spent: " + str(end_time - start_time)
#
#     return wrapper


def decorator_docstring(func):
    """Decorator for function's docstring."""

    def wrapper(string):
        print(func.__doc__)
        return func(string)

    return wrapper


@decorator_docstring
def count_letters(string):
    """This function counts amount of uppercase letters in a string."""

    counter = 0
    for character in string:
        if character.isupper():
            counter += 1

    return counter


@decorator_docstring
def count_integers(string):
    """This function counts amount of integers in a string."""

    counter = 0
    for character in string:
        if character.isdigit():
            counter += 1

    return counter
