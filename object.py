from abc import abstractmethod
import numpy as np
import math


# classe que define um objeto basico do universo de representacao
class Object:

    # int id;
    # string name_, type_;

    # construtor
    def __init__(self, id, name, type):
        self.id_ = id
        self.name_ = name
        self.type_ = type

    # metodo abstrato que define a maneira como o objeto eh desenhado na tela
    @abstractmethod
    def draw(self, transform, da_width, da_height, cairo):
        pass

    @abstractmethod
    def update_scn(self, transform):
        pass

# end of class Object


# classe que define um ponto basico no universo de representacao
class Point():
    # double x_, y_;
    # construtor
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
# end of class Point


# classe que define uma linha basica dentro do universo de representacao
class Line():
    # construtor
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end
# end of class Line


# classe que representa um poligono generico
class Polygon():

    # list points_;

    # construtor
    def __init__(self, points):
        self.points_ = points
# end of class Polygon


class DrawablePoint(Point, Object):
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
        # print(transform)
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
