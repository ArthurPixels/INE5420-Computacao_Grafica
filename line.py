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


# end of class Line
