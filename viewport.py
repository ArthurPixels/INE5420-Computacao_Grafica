from matrixTransform import MatrixTransform
from object import Point
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

        mtr = MatrixTransform()
        mtr.scale((self.x_max - self.x_min)/2, -(self.y_max - self.y_min)/2)
        mtr.translate(self.vc.x, self.vc.y)
        return mtr.tr

    def viewport_to_scn(self, pt: Point):
        try:
            inverse = np.linalg.inv(self.transform)
        except np.linalg.LinAlgError:
            print('Error: (Viewport) not invertible')
        else:
            [x, y, z] = np.array(
                    ([pt.x, pt.y, 1]), dtype=float) @ inverse
            return Point(x, y)
# end of class Viewport
