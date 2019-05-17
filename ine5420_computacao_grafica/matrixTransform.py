import numpy as np


class MatrixTransform2D:
    def __init__(self):
        self.tr = np.array((
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ), dtype=float)

    def translate(self, x, y):
        translation = np.array((
            [1, 0, 0],
            [0, 1, 0],
            [x, y, 1]
        ), dtype=float)
        self.tr = self.tr @ translation

    def rotate(self, theta):
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)
        rotation = np.array((
            [cos_theta, -sin_theta, 0],
            [sin_theta, cos_theta, 0],
            [0, 0, 1]
        ), dtype=float)
        self.tr = self.tr @ rotation

    def scale(self, width, height):
        sc = np.array((
            [width, 0, 0],
            [0, height, 0],
            [0, 0, 1]
        ), dtype=float)
        self.tr = self.tr @ sc

class MatrixTransform3D:
    def __init__(self):
        self.tr = np.array((
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ), dtype=float)

    def translate(self, x, y, z):
        translation = np.array((
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [x, y, z, 0]
        ), dtype=float)
        self.tr = self.tr @ translation

    def rotate_x(self, theta):
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)
        rotation = np.array((
            [1, 0, 0, 0],
            [0, cos_theta, sin_theta, 0],
            [0, -sin_theta, cos_theta, 0],
            [0, 0, 0, 1]
        ), dtype=float)
        self.tr = self.tr @ rotation

    def rotate_y(self, theta):
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)
        rotation = np.array((
            [cos_theta, 0, -sin_theta, 0],
            [0, 1, 0, 0],
            [sin_theta, 0, cos_theta, 0],
            [0, 0, 0, 1]
        ), dtype=float)
        self.tr = self.tr @ rotation

    def rotate_z(self, theta):
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)
        rotation = np.array((
            [cos_theta, sin_theta, 0, 0],
            [-sin_theta, cos_theta, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ), dtype=float)
        self.tr = self.tr @ rotation

    def scale(self, sx, sy, sz):
        sc = np.array((
            [sx, 0, 0, 0],
            [0, sy, 0, 0],
            [0, 0, sz, 0],
            [0, 0, 0, 1]
        ), dtype=float)
        self.tr = self.tr @ sc
