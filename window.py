# classe que define uma Window do universo de representacao

from point import Point
import numpy as np


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
        translation = np.array((
            [1, 0, 0],
            [0, 1, 0],
            [self.wc.x, self.wc.y, 1]
        ), dtype=float)

        [cos_theta] = np.cos([self.theta])
        [sin_theta] = np.sin([self.theta])
        rotation = np.array((
            [cos_theta, -sin_theta, 0],
            [sin_theta, cos_theta, 0],
            [0, 0, 1]
        ), dtype=float)

        normalization = np.array((
            [2/self.width, 0, 0],
            [0, 2/self.height, 0],
            [0, 0, 1]
        ), dtype=float)
        transform = translation.dot(rotation).dot(normalization)
        return transform

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
