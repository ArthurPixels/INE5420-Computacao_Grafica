# difference to consider two float numbers equal
DELTA = 0.000001

# classe que define um ponto basico no universo de representacao
class Point2D:
    def __init__(self, x: float, y: float, type=0):
        self.x = x
        self.y = y
        self.type = type
        self.visited = False

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __eq__(self, p2):
        return abs(self.x - p2.x) < DELTA and abs(self.y - p2.y) < DELTA

# end of class Point

class Point3D:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

# classe que define uma linha basica dentro do universo de representacao
class Line:
    def __init__(self, start: Point2D, end: Point2D):
        self.start = start
        self.end = end
# end of class Line


# classe que representa um poligono generico
class Polygon:
    def __init__(self, points):
        self.points = points

# end of class Polygon
