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