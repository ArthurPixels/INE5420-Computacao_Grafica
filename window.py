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

    def scn_to_world(self, pt: Point):
        self.transform = self.update()
        try:
            inverse = np.linalg.inv(self.transform)
        except np.linalg.LinAlgError:
            print('Error: (Window) not invertible')
        else:
            [x, y, z] = inverse @ np.array(
                    ([pt.x, pt.y, 1]), dtype=float)
            print(f'd_world_x:{x} d_world_y:{y}')
            print(f'wc_x:{self.wc.x} wc_y:{self.wc.y}')
            return Point(x, y)

    def translate(self, pt: Point):
        delta = self.scn_to_world(pt)
        self.wc.x += delta.x
        self.wc.y += delta.y
        self.transform = self.update()

    def rotate(self, rotation):
        self.theta += rotation
        self.transform = self.update()

    def zoom(self, amount):
        self.width += amount
        self.height += amount
        self.transform = self.update()

    def update(self):
        mtr = MatrixTransform()
        mtr.translate(self.wc.x, self.wc.y)
        mtr.rotate(self.theta)
        mtr.scale(2/self.width, 2/self.height)
        return mtr.tr
# end of class Window
