# classe que define uma Window do universo de representacao

import point

class Window:

	# Point win_min_, win_max_, lower_, upper_;

	# construtor
	def __init__(self, xmin, xmax, ymin, ymax):
		self.win_min_ = Point(xmin, ymin)
		self.win_max_ = Point(xmax, ymax)
		self.lower_ = Point(xmax, ymin)
		self.upper_ = Point(xmin, ymax)


	# METODOS PARA MOVIMENTACAO DA WINDOW
	# Move a window para cima
	def moveUp(self, amount):
		self.lower_ = Point(self.lower_.get_x(), self.lower_.get_y() - amount)
		self.upper_ = Point(self.upper_.get_x(), self.upper_.get_y() - amount)

	# Move a window para a direita
	def moveRight(self, amount):
		self.lower_ = Point(self.lower_.get_x() - amount, self.lower_.get_y())
		self.upper_ = Point(self.upper_.get_x() - amount, self.upper_.get_y())

	# Move a window para baixo
	def moveDown(self, amount):
		self.lower_ = Point(self.lower_.get_x(), self.lower_.get_y() + amount)
		self.upper_ = Point(self.upper_.get_x(), self.upper_.get_y() + amount)

	# Move a window para a esquerda
	def moveLeft(self, amount):
		self.lower_ = Point(self.lower_.get_x() + amount, self.lower_.get_y())
		self.upper_ = Point(self.upper_.get_x() + amount, self.upper_.get_y())


	# ZoomIn
	def zoomIn(self, amount):
		self.lower_ = Point(self.lower_.get_x() + amount, self.lower_.get_y() + amount)
		self.upper_ = Point(self.upper_.get_x() - amount, self.upper_.get_y() - amount)

	# ZoomOut
	def zoomOut(self, amount):
		self.lower_ = Point(self.lower_.get_x() - amount, self.lower_.get_y() - amount)
		self.upper_ = Point(self.upper_.get_x() + amount, self.upper_.get_y() + amount)


# end of class Window
