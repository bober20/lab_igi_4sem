# Created by Soroka Darya.
# LR 3.
# 23.03.24


import useful_functions


def split_string(string):
    """This function splits a string."""

    string_array = string.replace(',', '').split()

    return string_array


def count_words_in_string(string):
    """This function counts words in a string."""

    string_array = split_string(string)

    return len(string_array)


def find_the_longest_word(string):
    """This function finds the longest word in a string."""

    string_array = split_string(string)

    if string_array is None:
        return ""

    longest_word = max(string_array, key=len)
    word_index = string_array.index(longest_word)

    return word_index, longest_word


def print_odd_words(string):
    """This function prints odd words from string."""

    string_array = split_string(string)
    odd_words_list = list()

    if string_array is None:
        return ""

    for i in range(0, len(string_array), 2):
        odd_words_list.append(string_array[i])

    return odd_words_list
