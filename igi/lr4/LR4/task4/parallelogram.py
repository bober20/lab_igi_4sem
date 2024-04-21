from task4.geometric_figure import GeometricFigure
from task4.figure_color import FigureColor
import math
import matplotlib.pyplot as plt
import numpy as np


class Parallelogram(GeometricFigure):
    filename = 'lr_files/parallelogram.png'

    def __init__(self, d1, d2, angle, color):
        self.d1 = d1
        self.d2 = d2
        self.angle = angle
        self.color = FigureColor(color)
        super().__init__("Parallelogram")

    def get_squire(self):
        return self.d1 * self.d2 * math.sin(self.angle) / 2

    def draw_parallelogram(self):
        # Calculate the coordinates of the parallelogram vertices
        p1 = np.array([0, 0])
        p2 = np.array([self.d1, 0])
        p3 = np.array([self.d2 * np.cos(np.radians(self.angle)), self.d2 * np.sin(np.radians(self.angle))])
        p4 = p2 + p3
        parallelogram_coords = np.array([p1, p2, p4, p3])

        # Plot the parallelogram
        plt.fill(parallelogram_coords[:, 0], parallelogram_coords[:, 1], color=self.color.get_color)
        plt.plot(parallelogram_coords[:, 0], parallelogram_coords[:, 1], color=self.color.get_color)

        # Set plot limits and labels
        plt.xlim(min(parallelogram_coords[:, 0]) - 1, max(parallelogram_coords[:, 0]) + 1)
        plt.ylim(min(parallelogram_coords[:, 1]) - 1, max(parallelogram_coords[:, 1]) + 1)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Parallelogram')

        # Save the plot to a file
        plt.savefig(self.filename)
        plt.show()
