from point import Point
import numpy as np


# classe que define a viewport do universo de representacao
class Viewport:

    # construtor
    def __init__(self, x_min, y_min, x_max, y_max, da_width, da_height):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max
        self.vc = Point((x_max - x_min) / 2, (y_max - y_min) / 2)
        self.transform = self.update(da_width, da_height)

    def update(self, da_width, da_height):
        self.vc = Point(
            da_width / 2,
            da_height / 2
        )

        translation = np.array((
            [1, 0, 0],
            [0, 1, 0],
            [self.vc.x, self.vc.y, 1]
        ), dtype=float)

        normalization = np.array((
            [(self.x_max - self.x_min)/2, 0, 0],
            [0, -(self.y_max - self.y_min)/2, 0],
            [0, 0, 1]
        ), dtype=float)
        transform = normalization.dot(translation)
        return transform

# end of class Viewport
