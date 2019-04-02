# classe que define a viewport do universo de representacao

class Viewport:

	# float x_min_, y_min_, x_max_, y_max_;

	# construtor
	def __init__(self, x_min, y_min, x_max, y_max):
		self.x_min_ = x_min
		self.y_min_ = y_min
		self.x_max_ = x_max
		self.y_max_ = y_max

	# retorna x_min
	def get_xmin(self):
		return self.x_min_

	# retorna y_min
	def get_ymin(self):
		return self.y_min_

	# retorna x_max
	def get_xmax(self):
		return self.x_max_

	# retorna y_max
	def get_ymax(self):
		return self.y_max_


# end of class Viewport
