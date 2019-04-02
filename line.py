# classe que define uma linha dentro do universo de representacao

import point
from object import Object

class Line(Object):

    # Point firstP_, lastP_;
    # construtor
    def __init__(self, name, firstP, lastP):
        super(Line, self).__init__(name, "Line")
        self.firstP_ = firstP
        self.lastP_ = lastP

    # retorna o primeiro ponto da linha
    def getFirstPoint(self):
        return self.firstP_

    # retorna o ultimo ponto da linha
    def getLastPoint(self):
        return self.lastP_

    # altera o primeiro ponto da linha
    def setFirstPoint(self, newPoint):
        self.firstP_ = newPoint

    # altera o ultimo ponto da linha
    def setLastPoint(self, newPoint):
        self.lastP_ = newPoint


# end of class Line
