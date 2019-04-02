# classe que define um ponto no universo de representacao

from object import Object


class Point(Object):

	# double x_, y_;

	# construtor
	def __init__(self, name, x, y):
		super(Point, self).__init__(name, "Point")
		self.x_ = x
		self.y_ = y

	# retorna o valor de x
	def get_x(self):
		return self.x_

	# retorna o valor de y
	def get_y(self):
		return self.y_

	# altera o valor de x
	def set_x(self, x):
		self.x_ = x

	# altera o valor de y
	def set_y(self, y):
		self.y_ = y


# end of class Point
