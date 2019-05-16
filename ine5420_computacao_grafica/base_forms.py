# classe que define um ponto basico no universo de representacao
class Point2D:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
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
