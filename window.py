# classe que define uma Window do universo de representacao
from matrixTransform import MatrixTransform
from object import Point
import numpy as np


class Window:
    # Point win_min_, win_max_, lower_, upper_;

    # construtor
    def __init__(self, wc: Point, theta, width, height):
        self.wc = wc
        self.theta = theta
        self.width = width
        self.height = height
        self.transform = self.update()

    def translate(self, x, y):
        self.transform = self.update()
        try:
            inverse = np.linalg.inv(self.transform)
        except np.linalg.LinAlgError:
            print('Error: (MatrixTransform) not invertible')
        else:
            [self.wc.x, self.wc.y, z] = np.array(
                    ([x/10, y/10, 1]), dtype=float).dot(inverse)
            self.transform = self.update()

    def rotate(self, rotation):
        self.theta += rotation
        self.transform = self.update()

    def update(self):
        mtr = MatrixTransform()
        mtr.translate(self.wc.x, self.wc.y)
        mtr.rotate(self.theta)
        mtr.scale(2/self.width, 2/self.height)
        return mtr.tr

    # Zoom
    def zoom(self, amount):
        self.width += amount
        self.height += amount
        self.transform = self.update()


# end of class Window
