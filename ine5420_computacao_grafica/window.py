# classe que define uma Window do universo de representacao
from ine5420_computacao_grafica.matrixTransform import MatrixTransform2D
from ine5420_computacao_grafica.object import Point2D
import numpy as np


class Window:
    # Point win_min_, win_max_, lower_, upper_;

    # construtor
    def __init__(self, wc: Point2D, theta, width, height):
        self.wc = wc
        self.theta = theta
        self.width = width
        self.height = height
        self.transform = self.update()

    def scn_to_world(self, pt: Point2D):
        self.transform = self.update()
        try:
            inverse = np.linalg.inv(self.transform)
        except np.linalg.LinAlgError:
            print('Error: (Window) not invertible')
        else:
            [x, y, _] = inverse @ np.array(
                ([pt.x, pt.y, 1]), dtype=float)
            # print(f'd_world_x:{x} d_world_y:{y}')
            # print(f'wc_x:{self.wc.x} wc_y:{self.wc.y}')
            return Point2D(x, y)

    def translate(self, pt: Point2D):
        self.wc.x += pt.x
        self.wc.y += pt.y
        self.transform = self.update()

    def rotate(self, rotation):
        self.theta += rotation
        self.transform = self.update()

    def zoom(self, amount):
        self.width += amount
        self.height += amount
        self.transform = self.update()

    def update(self):
        mtr = MatrixTransform2D()
        mtr.translate(self.wc.x, self.wc.y)
        mtr.rotate(self.theta)
        mtr.scale(2/self.width, 2/self.height)
        return mtr.tr
# end of class Window
