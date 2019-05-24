from abc import abstractmethod
from ine5420_computacao_grafica.matrixTransform import MatrixTransform2D
from ine5420_computacao_grafica.base_forms import Point2D, Point3D, Line, Polygon
import numpy as np
import math
import ine5420_computacao_grafica.clip as clip


# classe que define um objeto basico do universo de representacao
class Object:

    # int id;
    # string name_, type_;

    def __init__(self, obj_id, name, obj_type):
        self.id = obj_id
        self.name = name
        self.type = obj_type
        self.visible = True

    # metodo abstrato que define a maneira como o objeto eh desenhado na tela
    @abstractmethod
    def draw(self, transform, da_width, da_height, cairo):
        pass

    @abstractmethod
    def update_scn(self, transform):
        pass

    @abstractmethod
    def translate(self, vec):
        pass

    @abstractmethod
    def rotate(self, vec, center):
        pass

    @abstractmethod
    def scale(self, amount, center):
        pass

    @abstractmethod
    def clip(self):
        pass

# end of class Object

class DrawablePoint2D(Point2D, Object):
    def __init__(self, obj_id, name, x, y):
        # Object constructor
        Object.__init__(self, obj_id, name, "Point")
        # Constructor of Point
        Point2D.__init__(self, x, y)
        self.nx = x
        self.ny = y

    # implementacao do metodo abstrato definido em Object
    def update_scn(self, transform):
        [self.nx, self.ny, _] = np.array(
                ([self.x, self.y, 1]), dtype=float).dot(transform)

    # implementacao do metodo abstrato definido em Object
    def draw(self, transform: np.array, cairo):
        [vx, vy, _] = np.array(
                ([self.nx, self.ny, 1]), dtype=float).dot(transform)
        cairo.arc(vx, vy, 2, 0, 2*math.pi)
        cairo.fill()

    def translate(self, vec):
        self.x += vec.x
        self.y += vec.y

    def rotate(self, angle, center):
        pass

    def scale(self, amount, center):
        pass

    def clip(self):
        pass
# end of class DrawablePoint


class DrawableLine(Line, Object):

    # Point firstP_, lastP_;

    # construtor
    def __init__(self, obj_id, name, start, end):
        # constructor of Object
        Object.__init__(self, obj_id, name, "Line")
        # constructor of Line
        Line.__init__(self, start, end)
        self.scn = Line(Point2D(0, 0), Point2D(0, 0))

    # implementacao do metodo abstrato definido em Object
    def update_scn(self, transform):
        [self.scn.start.x, self.scn.start.y, _] = np.array(
                ([self.start.x, self.start.y, 1]),
                dtype=float).dot(transform)
        [self.scn.end.x, self.scn.end.y, _] = np.array(
                ([self.end.x, self.end.y, 1]),
                dtype=float).dot(transform)

    # implementacao do metodo abstrato definido em Object
    def draw(self, transform: np.array, cairo):
        # print(transform)
        [v_start_x, v_start_y, _] = np.array(
                ([self.scn.start.x, self.scn.start.y, 1]),
                dtype=float).dot(transform)
        [v_end_x, v_end_y, _] = np.array(
                ([self.scn.end.x, self.scn.end.y, 1]),
                dtype=float).dot(transform)
        cairo.save()
        cairo.move_to(v_start_x, v_start_y)
        cairo.line_to(v_end_x, v_end_y)
        cairo.stroke()
        cairo.restore()

    def get_center(self, center):
        cx = (self.start.x + self.end.x) / 2
        cy = (self.start.y + self.end.y) / 2

        if center == 1:
            return Point2D(0, 0)
        elif center == 2:
            return Point2D(cx, cy)
        else:
            return self.start

    def translate(self, vec):
        self.start.x += vec.x
        self.start.y += vec.y
        self.end.x += vec.x
        self.end.y += vec.y

    def rotate(self, angle, ctr):
        center = self.get_center(ctr)

        mtr = MatrixTransform2D()
        mtr.translate(-center.x, -center.y)
        mtr.rotate(angle/2)
        mtr.translate(center.x, center.y)

        [self.start.x, self.start.y, _] = np.array(
            [self.start.x, self.start.y, 1], dtype=float
        ) @ mtr.tr
        [self.end.x, self.end.y, _] = np.array(
            [self.end.x, self.end.y, 1], dtype=float
        ) @ mtr.tr

    def scale(self, amount, ctr):
        center = self.get_center(ctr)

        mtr = MatrixTransform2D()
        mtr.translate(-center.x, -center.y)
        mtr.scale(amount, amount)
        mtr.translate(center.x, center.y)

        [self.start.x, self.start.y, _] = np.array(
            [self.start.x, self.start.y, 1], dtype=float
        ) @ mtr.tr
        [self.end.x, self.end.y, _] = np.array(
            [self.end.x, self.end.y, 1], dtype=float
        ) @ mtr.tr


    def clip(self, algorithm):
        temp = None
        if algorithm == 1:
            temp = clip.cohenSutherlandClip(
                self.scn.start.x, self.scn.start.y, self.scn.end.x, self.scn.end.y
            )
        elif algorithm == 2:
            temp = clip.nichollLeeNichollClip(self, Line(
                Point2D(self.scn.start.x, self.scn.start.y),
                Point2D(self.scn.end.x, self.scn.end.y)))
        else:
            print("Invalid Clipping Algorithm")
        if temp:
            self.scn = temp
            self.visible = True
        else:
            self.visible = False

# end of class DrawableLine


class DrawablePolygon(Polygon, Object):
    def __init__(self, obj_id, name, points, filled):
        Object.__init__(self, obj_id, name, "Polygon")
        Polygon.__init__(self, points)
        self.scn = []
        self.filled = filled

    # implementacao do metodo abstrato definido em Object
    def update_scn(self, transform):
        for index, point in enumerate(self.scn):
            [point.start.x, point.start.y, _] = np.array(
                    ([self.points[index].start.x, self.points[index].start.y, 1]),
                    dtype=float).dot(transform)

    # implementacao do metodo abstrato definido em Object
    def draw(self, transform_x, transform_y, cairo):
        cairo.save()
        cairo.move_to(
            transform_x(self.points[0].x),
            transform_y(self.points[0].y)
        )
        for i in range(1, len(self.points)):
            cairo.line_to(
                transform_x(self.points[i].x),
                transform_y(self.points[i].y)
            )

        cairo.line_to(
            transform_x(self.points[0].x),
            transform_y(self.points[0].y)
        )
        cairo.stroke_preserve()

        if filled:
            pass   # PREENCHER O POLIGONO
        # cairo.restore()

    def get_center(self, center):
        cx = 0
        cy = 0
        for point in self.points:
            cx += point.x
            cy += point.y
        cx /= len(self.points)
        cy /= len(self.points)

        if center == 1:
            return Point2D(0, 0)
        elif center == 2:
            return Point2D(cx, cy)
        else:
            return self.start

    def translate(self, vec):
        for i in range(self.points):
            self.points[i].x += vec.x
            self.points[i].y += vec.y

    def rotate(self, angle, ctr):
        center = self.get_center(ctr)
        mtr = MatrixTransform2D()
        mtr.translate(-center.x, -center.y)
        mtr.rotate(angle)
        mtr.translate(center.x, center.y)

        for point in self.points:
            [point.x, point.y, _] = np.array(
                [point.x, point.y, 1], dtype=float
            ) @ mtr.tr

    def scale(self, amount, ctr):
        center = self.get_center(ctr)

        mtr = MatrixTransform2D()
        mtr.translate(-center.x, -center.y)
        mtr.scale(amount, amount)
        mtr.translate(center.x, center.y)

        for point in self.points:
            [point.x, point.y, _] = np.array(
                [point.x, point.y, 1], dtype=float
            ) @ mtr.tr
