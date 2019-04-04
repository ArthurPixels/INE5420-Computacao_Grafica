# classe que define uma linha dentro do universo de representacao

from object import Object


class Line(Object):

    # Point firstP_, lastP_;

    # construtor
    def __init__(self, id, name, firstP, lastP):
        super(Line, self).__init__(id, name, "Line")
        self.firstP_ = firstP
        self.lastP_ = lastP


    # implementacao do metodo abstrato definido em Object
    def draw(self, transform_x, transform_y, cairo):
        cairo.move_to(transform_x(self.firstP_.x_), transform_y(self.firstP_.y_))
        cairo.line_to(transform_x(self.lastP_.x_), transform_y(self.lastP_.y_))
        cairo.stroke()


# end of class Line
