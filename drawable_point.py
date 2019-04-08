# classe que define um ponto desenhavel no universo de representacao

from object import Object
from point import Point

import math


class DrawablePoint(Point, Object):

	# double x_, y_;

	# construtor
	def __init__(self, id, name, x, y):
		# Object constructor
		Object.__init__(self, id, name, "Point")
		# Constructor of Point
		Point.__init__(self, x, y)


	# implementacao do metodo abstrato definido em Object
	def draw(self, transform_x, transform_y, cairo):
		cairo.arc(transform_x(self.x_), transform_y(self.y_), 1, 0, 2*math.pi)
		cairo.fill()

# end of class DrawablePoint
