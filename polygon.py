# classe que representa um poligono generico

from object import Object

class Polygon(Object):

	# list points_;

	# construtor
	def __init__(self, id, name, points):
		super(Polygon, self).__init__(id, name, "Polygon")
		self.points_ = points


# end of class Polygon
