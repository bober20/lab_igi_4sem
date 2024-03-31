# Created by Soroka Darya.
# LR 3.
# 26.03.24


import math
import matplotlib.pyplot as plt
import statistics


class LnCalculations:
    x_list = list()
    y_func = list()
    y_math = list()
    median = 0
    mode = 0
    variance = 0
    stdev = 0

    def __init__(self):
        self.xy_preparation_for_plot()

        self.count_median()
        self.count_mode()
        self.count_stdev()
        self.count_variance()

    def count_using_power_series(self, x, eps=0.1):
        """This function finds the result using power series."""

        math_result = math.log((x + 1) / (x - 1))
        func_result = 0.0
        n = 0

        while n <= 500 and math_result - func_result > eps:
            func_result += 2.0 / ((n * 2.0 + 1) * math.pow(x, n * 2.0 + 1))
            n += 1

        return func_result, math_result

    def xy_preparation_for_plot(self):
        """This function finds the result using power series."""

        for i in range(2, 20):
            self.x_list.append(i)

            result = self.count_using_power_series(i)

            self.y_func.append(result[0])
            self.y_math.append(result[1])

    def plot_screen(self):
        # self.xy_preparation_for_plot()
        plt.plot(self.x_list, self.y_math, label="math")
        plt.plot(self.x_list, self.y_func, label="my_func")
        plt.xlabel('Ось х')  # Подпись для оси х
        plt.ylabel('Ось y')  # Подпись для оси y
        plt.grid(True)
        plt.legend(loc='best', fontsize=12)
        plt.title('График для логарифма')  # Название

        self.plot_file()

        plt.show()

    def plot_file(self):
        plt.savefig('lr_files/math_and_func.pdf')

    def count_median(self):
        self.median = statistics.median(self.x_list)

    def count_mode(self):
        self.mode = statistics.mode(self.x_list)

    def count_variance(self):
        self.variance = statistics.variance(self.x_list)

    def count_stdev(self):
        self.stdev = statistics.stdev(self.x_list)


