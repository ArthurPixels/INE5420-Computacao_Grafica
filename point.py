# classe que define um ponto no universo de representacao

from object import Object


class Point(Object):

	# double x_, y_;

	# construtor
	def __init__(self, id, name, x, y):
		super(Point, self).__init__(id, name, "Point")
		self.x_ = x
		self.y_ = y


# end of class Point
