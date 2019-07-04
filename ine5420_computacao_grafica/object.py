from abc import abstractmethod
from ine5420_computacao_grafica.matrixTransform import MatrixTransform2D
from ine5420_computacao_grafica.base_forms import (
        Point2D,
        Line,
        Polygon,
        CurveType
    )
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
    def clip(self, algorithm=None):
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

    def clip(self, algorithm=None):
        if clip.pointClip(Point2D(self.nx, self.ny)):
            self.visible = True
        else:
            self.visible = False

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
            temp = clip.cohenSutherlandClip(Line(self.scn.start, self.scn.end))
        elif algorithm == 2:
            temp = clip.nichollLeeNichollClip(Line(self.scn.start, self.scn.end))
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
        self.scn = []
        self.scn.append([])
        for index, point in enumerate(self.points):
            [vx, vy, _] = np.array(
                    ([self.points[index].x, self.points[index].y, 1]),
                    dtype=float).dot(transform)
            self.scn[0].append(Point2D(vx, vy))

    # implementacao do metodo abstrato definido em Object
    def draw(self, transform: np.array, cairo):
        for polygon in range(len(self.scn)):
            cairo.save()
            [vx, vy, _] = np.array(
                ([self.scn[polygon][0].x, self.scn[polygon][0].y, 1]),
                dtype=float).dot(transform)
            cairo.move_to(vx, vy)

            for i in range(1, len(self.scn[polygon])):
                [vx, vy, _] = np.array(
                    ([self.scn[polygon][i].x, self.scn[polygon][i].y, 1]),
                    dtype=float).dot(transform)
                cairo.line_to(vx, vy)

            [vx, vy, _] = np.array(
                ([self.scn[polygon][0].x, self.scn[polygon][0].y, 1]),
                dtype=float).dot(transform)
            cairo.line_to(vx, vy)

            if self.filled:
                cairo.fill()
            else:
                cairo.stroke()

            cairo.restore()


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
            return self.points[0]

    def translate(self, vec):
        for point in self.points:
            point.x += vec.x
            point.y += vec.y

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

    def clip(self, algorithm):
        temp = clip.weilerAthertonPolygonClip(Polygon(self.scn[0]))

        if temp:
            self.scn = temp
            self.visible = True
        else:
            self.visible = False


class DrawableCurve(Polygon, Object):
    def __init__(self, obj_id, name, points, curve_type: CurveType):
        Object.__init__(self, obj_id, name, curve_type)
        Polygon.__init__(self, points)
        self.scn = []
        self.curve_type = curve_type
        self.bezier_matrix = np.array((
            [-1, 3, -3, 1],
            [3, -6, 3, 0],
            [-3, 3, 0, 0],
            [1, 0, 0, 0]
        ), dtype=float)
        self.bspline_matrix = np.array((
            [-1, 3, -3, 1],
            [3, -6, 3, 0],
            [-3, 0, 3, 0],
            [1, 4, 1, 0]
        ), dtype=float) / 6

    # implementacao do metodo abstrato definido em Object
    def update_scn(self, transform):
        self.scn = []
        for index, point in enumerate(self.points):
            [vx, vy, _] = np.array(
                    ([self.points[index].x, self.points[index].y, 1]),
                    dtype=float).dot(transform)
            self.scn.append(Point2D(vx, vy))

    def calc_bspline_foward(self, delta):
        return np.array((
                [0, 0, 0, 1],
                [delta**3, delta**2, delta, 0],
                [6 * (delta**3), 2 * (delta**2), 0, 0],
                [6 * (delta**3), 0, 0, 0],
            ), dtype=float)

    # implementacao do metodo abstrato definido em Object
    def draw(self, transform: np.array, cairo):
        resolution = 50
        points = []

        array_x = np.array(
            [pt.x for pt in self.scn],
            dtype=float)

        array_y = np.array(
            [pt.y for pt in self.scn],
            dtype=float)

        if self.curve_type == CurveType.bezier:
            for section in range(0, len(self.scn) - 1, 3):
                for delta in np.linspace(0, 1, resolution):
                    T = np.array(
                        [delta**3, delta**2, delta, 1], dtype=float)
                    TM = T @ self.bezier_matrix
                    x = TM @ array_x[section:section + 4]
                    y = TM @ array_y[section:section + 4]
                    points.append(Point2D(x, y))

        elif self.curve_type == CurveType.b_spline:
            for i in range(0, len(self.scn) - 3):
                Gx = array_x[i:i + 4]
                Gy = array_y[i:i + 4]
                Cx = self.bspline_matrix @ Gx
                Cy = self.bspline_matrix @ Gy

                E = self.calc_bspline_foward(1.0 / resolution)
                Dx = E @ Cx
                Dy = E @ Cy

                for _ in range(resolution + 1):
                    x = Dx[0]
                    y = Dy[0]

                    Dx = Dx + np.append(Dx[1:], 0)
                    Dy = Dy + np.append(Dy[1:], 0)

                    points.append(Point2D(x, y))

        cairo.save()
        [vx, vy, _] = np.array(
            ([points[0].x, points[0].y, 1]),
            dtype=float).dot(transform)
        cairo.move_to(vx, vy)
        for i in range(1, len(points) - 1):
            x = points[i].x
            y = points[i].y
            [vx, vy, _] = np.array(
                ([x, y, 1]),
                dtype=float).dot(transform)
            if -1 <= x and x <= 1 and -1 <= y and y <= 1:
                cairo.line_to(vx, vy)
                cairo.stroke()
            cairo.move_to(vx, vy)
