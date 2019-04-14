# classe que define uma linha desenhavel dentro do universo de representacao
import numpy as np
from object import Object
from line import Line
from point import Point


class DrawableLine(Line, Object):

    # Point firstP_, lastP_;

    # construtor
    def __init__(self, id, name, start, end):
        # constructor of Object
        Object.__init__(self, id, name, "Line")
        # constructor of Line
        Line.__init__(self, start, end)
        self.scn = Line(Point(0, 0), Point(0, 0))

    # implementacao do metodo abstrato definido em Object
    def update_scn(self, transform):
        [self.scn.start.x, self.scn.start.y, nz] = np.array(
                ([self.start.x, self.start.y, 1]),
                dtype=float).dot(transform)
        [self.scn.end.x, self.scn.end.y, nz] = np.array(
                ([self.end.x, self.end.y, 1]),
                dtype=float).dot(transform)

    # implementacao do metodo abstrato definido em Object
    def draw(self, transform: np.array, cairo):
        print(transform)
        [v_start_x, v_start_y, nz] = np.array(
                ([self.scn.start.x, self.scn.start.y, 1]),
                dtype=float).dot(transform)
        [v_end_x, v_end_y, nz] = np.array(
                ([self.scn.end.x, self.scn.end.y, 1]),
                dtype=float).dot(transform)
        cairo.save()
        cairo.move_to(v_start_x, v_start_y)
        cairo.line_to(v_end_x, v_end_y)
        cairo.stroke()
        cairo.restore()


# end of class DrawableLine
