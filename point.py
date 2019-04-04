# classe que define um ponto no universo de representacao

from object import Object
import math


class Point(Object):

	# double x_, y_;

	# construtor
	def __init__(self, id, name, x, y):
		super(Point, self).__init__(id, name, "Point")
		self.x_ = x
		self.y_ = y


	# implementacao do metodo abstrato definido em Object
	def draw(self, cairo):
		cairo.arc(self.x_, self.y_, 1, 0, 2*math.pi)
		cairo.fill()

# end of class Point
