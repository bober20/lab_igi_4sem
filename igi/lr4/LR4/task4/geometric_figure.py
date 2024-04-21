from abc import abstractmethod


class GeometricFigure:
    """This class defines the superior class for figure."""

    def __init__(self, name):
        self.name_of_figure = name

    @abstractmethod
    def get_squire(self):
        return -1
