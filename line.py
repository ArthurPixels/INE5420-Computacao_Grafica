# classe que define uma linha dentro do universo de representacao

import point
from object import Object

class Line(Object):

    # Point firstP_, lastP_;

    # construtor
    def __init__(self, id, name, firstP, lastP):
        super(Line, self).__init__(id, name, "Line")
        self.firstP_ = firstP
        self.lastP_ = lastP


    # implementacao do metodo abstrato definido em Object
    def draw(self, cairo):
        cairo.move_to(self.firstP_.x_, self.firstP_.y_)
        cairo.line_to(self.lastP_.x_, self.lastP_.y_)
        cairo.stroke()


# end of class Line
