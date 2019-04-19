# classe que define uma Window do universo de representacao
from matrixTransform import MatrixTransform
from point import Point


class Window:
    # Point win_min_, win_max_, lower_, upper_;

    # construtor
    def __init__(self, wc: Point, theta, width, height):
        self.wc = wc
        self.theta = theta
        self.width = width
        self.height = height
        self.transform = self.update()

    def translate(self, translation):
        self.wc += translation
        self.transform = self.update()

    def rotate(self, rotation):
        self.theta += rotation
        self.transform = self.update()

    def update(self):
        mtr = MatrixTransform()

        mtr.translate(self.wc.x, self.wc.y)
        mtr.rotate(self.theta)
        mtr.scale(2/self.width, 2/self.height)

        return mtr.tr

    # METODOS PARA MOVIMENTACAO DA WINDOW (ver essas funcoes)
    # Move a window para cima
    def moveUp(self, amount):
        self.win_min_ = Point(self.win_min_.x_, self.win_min_.y_ + amount)
        self.win_max_ = Point(self.win_max_.x_, self.win_max_.y_ + amount)

    # Move a window para a direita
    def moveRight(self, amount):
        self.win_min_ = Point(self.win_min_.x_ + amount, self.win_min_.y_)
        self.win_max_ = Point(self.win_max_.x_ + amount, self.win_max_.y_)

    # Move a window para baixo
    def moveDown(self, amount):
        self.win_min_ = Point(self.win_min_.x_, self.win_min_.y_ - amount)
        self.win_max_ = Point(self.win_max_.x_, self.win_max_.y_ - amount)

    # Move a window para a esquerda
    def moveLeft(self, amount):
        self.win_min_ = Point(self.win_min_.x_ - amount, self.win_min_.y_)
        self.win_max_ = Point(self.win_max_.x_ - amount, self.win_max_.y_)

    # ZoomIn
    def zoomIn(self, amount):
        self.win_min_ = Point(self.win_min_.x_ + amount, self.win_min_.y_ + amount)
        self.win_max_ = Point(self.win_max_.x_ - amount, self.win_max_.y_ - amount)

    # ZoomOut
    def zoomOut(self, amount):
        self.win_min_ = Point(self.win_min_.x_ - amount, self.win_min_.y_ - amount)
        self.win_max_ = Point(self.win_max_.x_ + amount, self.win_max_.y_ + amount)


# end of class Window
