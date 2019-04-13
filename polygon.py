# classe que representa um poligono generico

from object import Object

class Polygon(Object):

	# list points_;

	# construtor
	def __init__(self, id, name, points):
		super(Polygon, self).__init__(id, name, "Polygon")
		self.points_ = points


	# implementacao do metodo abstrato definido em Object
	def draw(self, transform_x, transform_y, cairo):
		cairo.move_to(transform_x(self.points_[0].x_), transform_y(self.points_[0].y_))
		for i in range(1, len(self.points_)):
			cairo.line_to(transform_x(self.points_[i].x_), transform_y(self.points_[i].y_))

		cairo.line_to(transform_x(self.points_[0].x_), transform_y(self.points_[0].y_))
		cairo.stroke_preserve()

# end of class Polygon
