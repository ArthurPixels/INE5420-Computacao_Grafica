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

	# retorna o ponto que representa win_min (esquerdo inferior)
	def get_win_min(self):
		return self.win_min_

	# retorna o ponto que representa win_max (direito superior)
	def get_win_max(self):
		return self.win_max_

	# retorna o ponto que representa o ponto direito inferior da window
	def get_win_lower(self):
		return self.lower_

	# retorna o ponto que representa o ponto esquerdo superior da window
	def get_win_upper(self):
		return self.upper_

	# altera o ponto que representa o ponto esquerdo superior da window
	def set_win_min(self, x, y):
		self.win_min_ = Point(x, y)

	# altera o ponto que representa o ponto esquerdo superior da window
	def set_win_max(self, x, y):
		self.win_max_ = Point(x, y)

	# altera o ponto que representa o ponto esquerdo superior da window
	def set_win_lower(self, x, y):
		self.lower_ = Point(x, y)

	# altera o ponto que representa o ponto esquerdo superior da window
	def set_win_upper(self, x, y):
		self.upper_ = Point(x, y)


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
