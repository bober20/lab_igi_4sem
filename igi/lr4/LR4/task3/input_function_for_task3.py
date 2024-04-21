from task3.calculations import LnCalculations


def input_function_for_task3():
    calculations = LnCalculations()

    print("Mode: ", calculations.mode)
    print("Stdev: ", calculations.stdev)
    print("Variance: ", calculations.variance)
    print("Median: ", calculations.median)
    print("Average: ", calculations.average)

    calculations.plot_screen()
