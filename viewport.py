from matrixTransform import MatrixTransform2D
from object import Point2D
import numpy as np


# classe que define a viewport do universo de representacao
class Viewport:

    # construtor
    def __init__(self, x_min, y_min, x_max, y_max, da_width, da_height):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max
        self.vc = Point2D((x_max - x_min) / 2, (y_max - y_min) / 2)
        self.transform = self.update(da_width, da_height)

    def update(self, da_width, da_height):
        self.vc = Point2D(
            da_width / 2,
            da_height / 2
        )

        mtr = MatrixTransform2D()
        mtr.scale((self.x_max - self.x_min)/2, -(self.y_max - self.y_min)/2)
        mtr.translate(self.vc.x, self.vc.y)
        return mtr.tr

    def viewport_to_scn(self, pt: Point2D):
        try:
            inverse = np.linalg.inv(self.transform)
        except np.linalg.LinAlgError:
            print('Error: (Viewport) not invertible')
        else:
            [x, y, z] = inverse @ np.array(
                    ([pt.x, pt.y, 1]), dtype=float)
            return Point2D(x, y)
# end of class Viewport
