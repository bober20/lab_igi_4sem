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

    max_length = len(string_array[0])
    word_index = 0
    word = string_array[0]

    for i in range(len(string_array)):
        word_lenght = len(string_array[i])

        if max_length < word_lenght:
            max_length = word_lenght
            word_index = i
            word = string_array[i]

    return word_index, word


def print_odd_words(string):
    """This function prints odd words from string."""

    string_array = split_string(string)
    odd_words_list = list()

    if string_array is None:
        return ""

    for i in range(len(string_array)):
        odd_words_list.append(string_array[i])

    return odd_words_list
