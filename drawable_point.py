# classe que define um ponto desenhavel no universo de representacao
import numpy as np
from object import Object
from point import Point

import math


class DrawablePoint(Point, Object):

    # double x_, y_;

    # construtor
    def __init__(self, id, name, x, y):
        # Object constructor
        Object.__init__(self, id, name, "Point")
        # Constructor of Point
        Point.__init__(self, x, y)
        self.nx = x
        self.ny = y
        self.nz = 1

    # implementacao do metodo abstrato definido em Object
    def update_scn(self, transform):
        [self.nx, self.ny, self.nz] = np.array(
                ([self.x, self.y, 1]), dtype=float).dot(transform)

    # implementacao do metodo abstrato definido em Object
    def draw(self, transform: np.array, cairo):
        [vx, vy, vz] = np.array(
                ([self.nx, self.ny, 1]), dtype=float).dot(transform)
        cairo.arc(vx, vy, 2, 0, 2*math.pi)
        cairo.fill()

# end of class DrawablePoint
