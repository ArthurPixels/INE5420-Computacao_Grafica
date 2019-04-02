# classe que representa um poligono generico

from object import Object

class Polygon(Object):

	# list points_;

	# construtor
	def __init__(self, name, points):
		super(Polygon, self).__init__(name, "Polygon")
		self.points_ = points

	# retorna a lista de pontos do poligono
	def getListaPontos(self):
		return self.points_

	# altera a lista de pontos do poligono
	def setListaPontos(self, newPoints):
		self.points_ = newPoints


# end of class Polygon
