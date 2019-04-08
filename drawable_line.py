# classe que define uma linha desenhavel dentro do universo de representacao

from object import Object
from line import Line


class DrawableLine(Line, Object):

    # Point firstP_, lastP_;

    # construtor
    def __init__(self, id, name, firstP, lastP):
        # constructor of Object
        Object.__init__(self, id, name, "Line")
        # constructor of Line
        Line.__init__(self, firstP, lastP)


    # implementacao do metodo abstrato definido em Object
    def draw(self, transform_x, transform_y, cairo):
        cairo.move_to(transform_x(self.firstP_.x_), transform_y(self.firstP_.y_))
        cairo.line_to(transform_x(self.lastP_.x_), transform_y(self.lastP_.y_))
        cairo.stroke()


# end of class DrawableLine
