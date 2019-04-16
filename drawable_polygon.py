import numpy as np
from object import Object
from line import Line
from point import Point


class DrawablePolygon(Polygon, Object):
    def __init__(self, id, name, points):
        Object.__init__(self, id, name, "Polygon")
        Polygon.__init__(self, points)

    # implementacao do metodo abstrato definido em Object
    def update_scn(self, transform):
        [self.scn.start.x, self.scn.start.y, nz] = np.array(
                ([self.start.x, self.start.y, 1]),
                dtype=float).dot(transform)

    # implementacao do metodo abstrato definido em Object
    def draw(self, transform_x, transform_y, cairo):
        cairo.save()
        cairo.move_to(
            transform_x(self.points_[0].x_),
            transform_y(self.points_[0].y_)
        )
        for i in range(1, len(self.points_)):
            cairo.line_to(
                transform_x(self.points_[i].x_),
                transform_y(self.points_[i].y_)
            )

        cairo.line_to(
            transform_x(self.points_[0].x_),
            transform_y(self.points_[0].y_)
        )
        cairo.stroke_preserve()
        # cairo.restore()
