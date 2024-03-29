import math
import numpy as np
from random import randint


class MathArray:

    def __init__(self, n):
        self.array = np.array(list(map(lambda x: randint(-n, 3), range(n))))

    def __getattr__(self, item):
        print("Access allowed")
        return object.__getattribute__(self, item)

    def count_sum_of_odd_numbers(self):
        odd_array = self.get_odd_array()

        sum_of_odd_elements = sum(odd_array)

        return int(math.fabs(sum_of_odd_elements))

    def get_odd_array(self):
        odd_array = list()

        for i in range(0, len(self.array), 2):
            if self.array[i] < 0:
                odd_array.append(self.array[i])

        return odd_array

    def get_standard_deviation_numpy(self):
        odd_array = self.get_odd_array()

        return round(float(np.std(odd_array)), 2)

    def get_standard_deviation_formula(self):
        odd_array = self.get_odd_array()
        return round(math.sqrt(np.var(odd_array)), 2)


    # def get_standard_deviation_formula(self):
    #     odd_array = self.get_odd_array()
    #     # mean_value = np.mean(odd_array)
    #     #
    #     # odd_array = list(map(lambda i: pow(i - mean_value, 2), odd_array))
    #     #
    #     # sum_of_odd_array = sum(odd_array)
    #
    #     # return round(sum_of_odd_array / len(odd_array), 2)
