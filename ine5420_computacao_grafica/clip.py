from ine5420_computacao_grafica.object import Point2D, Line


class Region:
    center = 0
    edge = 1
    corner = 2


class NichollLeeNicholl:
    def __init__(self, line: Line):
        self.x1 = line.start.x
        self.y1 = line.start.y
        self.x2 = line.end.x
        self.y2 = line.end.y

        self.m1 = None
        self.m2 = None
        self.m3 = None
        self.m4 = None
        self.mr = None

        if self.x == 1:
            self.m2 = float('inf')
            self.m3 = float('inf')
        else:
            self.m2 = (-1 - self.y1) / (1 - self.x1)
            self.m3 = (1 - self.y1) / (1 - self.x1)

        if self.x1 == -1:
            self.m1 = float('inf')
            self.m2 = float('inf')
        else:
            self.m1 = (-1 - self.y1) / (-1 - self.x1)
            self.m4 = (1 - self.y1) / (-1 - self.x1)

        if self.x1 == self.x2:
            self.mr = float('inf')
        else:
            self.mr = (self.y - self.y1) / (self.x2 - self.x1)

    def clip(self):
        region = self.get_region()
        clipped = None
        if region is Region.center:
            clipped = self.clip_center()
        elif region is Region.edge:
            clipped = self.clip_edge()
        elif region is Region.corner:
            clipped = self.clip_corner()
        else:
            print('NichollLeeNicholl: invalid region')
        return clipped

    def get_region(self):
        if self.x1 >= -1 and self.x1 <= 1 and\
                self.y1 >= -1 and self.y1 <= 1:
            return Region.center
        if self.x1 < -1 and self.y1 >= -1 and self.y1 <= 1:
            return Region.edge
        if self.x1 <= -1 and self.y1 <= -1:
            return Region.corner
        return -1

    def clip_center(self):
        x2 = None
        y2 = None
        # p2 is on top
        if ((abs(self.mr) >= self.m1 and self.x2 < self.x1)
                or (abs(self.mr) > abs(self.m2) and self.x2 > self.x1)) \
                and self.y1 > self.y2:
            # p2 inside clip window
            if self.y2 > -1:
                x2 = self.x2
                y2 = self.y2
            # p2 outside clip window
            else:
                x2 = self.x1 + (-1 - self.y1) / self.mr
                y2 = -1
        # p2 is on right
        elif self.mr > self.m2 and self.mr < self.m3 and self.x2 >= 1:
            # p2 inside clip window
            if self.x2 < 1:
                x2 = self.x2
                y2 = self.y2
            # p2 outside clip window
            else:
                x2 = 1
                y2 = self.y1 + (1 - self.x1) * self.mr
        # p2 is on bottom
        elif (abs(self.mr) >= self.m3 and self.x2 > self.x1) or\
                (abs(self.mr) > abs(self.m4) and self.x2 < self.x1):
            # p2 inside clip window
            if self.y2 < 1:
                x2 = self.x2
                y2 = self.y2
            # p2 outside clip window
            else:
                x2 = self.x1 + (1 - self.y1) / self.mr
                y2 = -1
        # p2 is on left
        elif self.mr > self.m4 and self.mr < self.m1:
            # p2 inside clip window
            if self.x2 > -1:
                x2 = self.x2
                y2 = self.y2
            # p2 outside clip window
            else:
                x2 = -1
                y2 = self.y1 + (-1 - self.x1) * self.mr
        else:
            return None
        return Line(Point(self.x1, self.y1), Point(x2, y2))

    def clip_edge(self):
        x1 = None
        y1 = None
        x2 = None
        y2 = None
        # p2 is on top_left
        if self.mr > self.m1 and self.mr < self.m2:
            # p2 inside clip window
            if self.y2 > -1:
                x1 = -1
                y1 = self.y1 + (-1 - self.x1) * self.mr
                x2 = self.x2
                y2 = self.y2
            # p2 outside clip window
            else:
                x1 = -1
                y1 = self.y1 + (-1 - self.x1) * self.mr
                x2 = self.x1 + (-1 - self.y1) / self.mr
                y2 = -1
        # p2 is on left_center
        elif self.mr > self.m2 and self.mr < self.m3:
            # p2 inside clip window
            if self.x2 < 1:
                x1 = -1
                y1 = self.y1 + (-1 - self.x1) * self.mr
                x2 = self.x2
                y2 = self.y2
            # p2 outside clip window
            else:
                x1 = -1
                y1 = self.y1 + (-1 - self.x1) * self.mr
                x2 = 1
                y2 = self.y1 + (1 - self.x1) * self.mr
        # p2 is on bottom_left
        elif self.mr > self.m3 and self.mr < self.m4:
            # p2 inside clip window
            if self.y2 < 1:
                x1 = -1
                y1 = self.y1 + (-1 - self.x1) * self.mr
                x2 = self.x2
                y2 = self.y2
            # p2 outside clip window
            else:
                x1 = -1
                y1 = self.y1 + (-1 - self.x1) * self.mr
                x2 = self.x1 + (1 - self.y1) / self.mr
                y2 = 1
        else:
            return None
        return Line(Point(x1, y1), Point(x2, y2))

    def clip_corner(self):
        x1 = None
        y1 = None
        x2 = None
        y2 = None
        # slope
        tm = (-1 - self.y1) / (-1 - self.x1)
        vertical = False
        m2 = self.m2
        m3 = self.m3
        # horizontal
        if tm < 1:
            m2, m3 = m3, m2
            vertical = False
        # vertical
        else:
            vertical = True
        # p2 is on top_right
        if self.mr > self.m1 and self.mr < m2:
            # p2 outside clip window
            if self.x2 > 1 and self.y2 > -1:
                x1 = self.x1 + (-1 - self.y1) / self.mr
                y1 = -1
                x2 = 1
                y2 = self.y1 + (1 - self.x1) * self.mr
            # p2 inside clip window
            elif self.y2 > -1 and self.x2 < 1:
                x1 = x1 + (-1 - self.y1) / self.mr
                y1 = -1
                x2 = self.x2
                y2 = self.y2
        # cardeal
        elif self.mr > m2 and self.mr < m3:
            # p2 vertical
            if vertical:
                # p2 outside clip window
                if self.y2 >= 1:
                    x1 = self.x1 + (-1 - self.y1) / self.mr
                    y1 = -1
                    x2 = self.x1 + (1 - self.y1) / self.mr
                    y2 = 1
                # p2 inside clip window
                elif self.y2 >= -1:
                    x1 = self.x1 + (-1 - self.y1) / self.mr
                    y1 = -1
                    x2 = self.x2
                    y2 = self.y2
            # horizontal
            else:
                # p2 outside clip window
                if self.x2 >= 1:
                    x1 = -1
                    y1 = self.y1 + (-1 - self.x1) * self.mr
                    x2 = 1
                    y2 = self.y1 + (1 - self.x1) * self.mr
                # p2 inside clip window
                elif self.x2 >= -1:
                    x1 = -1
                    y1 = self.y1 + (-1 - self.x1) * self.mr
                    x2 = self.x2
                    y2 = self.y2
        # p2 is on bottom_left
        elif self.mr > m3 and self.mr < self.m4:
            # p2 outside clip window
            if self.y2 >= 1:
                x1 = -1
                y1 = self.y1 + (-1 - self.x1) * self.mr
                x2 = self.x1 + (1 - self.y1) / self.mr
                y2 = 1
            # p2 inside clip window
            elif self.y2 >= -1:
                x1 = -1
                y1 = self.y1 + (-1 - self.x1) * self.mr
                x2 = self.x2
                y2 = self.y2
        else:
            return None
        return Line(Point(x1, y1), Point(x2, y2))
