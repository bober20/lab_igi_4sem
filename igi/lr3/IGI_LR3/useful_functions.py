def generator(init_array):
    """This function generates a list for odd numbers."""

    values = [4*i for i in init_array if i % 2 != 0]

    return values


def generator_function(init_array):
    for i in init_array:
        yield i*3


def decorator_for_menu(func):
    """This decorator allows to start function multiple times."""

    def wrapper():
        print(func.__doc__)
        while True:
            print("To exit this function type 'exit' and anything to stay in the function.")
            n = input()
            if (n == "exit"):
                break

            print("Result: ", func())

    return wrapper


def decorator_for_menu_without_print(func):
    """This decorator allows to start function multiple times."""

    def wrapper():
        print(func.__doc__)
        while True:
            print("To exit this function type 'exit' and anything to stay in the function.")
            n = input()
            if (n == "exit"):
                break

            func()
    return wrapper


def check_is_number(x):
    try:
        float(x)

    except:
        print("Enter a number not a string.")
        return False

    return True


def check_is_integer(x):
    try:
        int(x)

    except:
        print("Enter an integer not a string.")
        return False

    return True

