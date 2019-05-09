from ine5420_computacao_grafica.base_forms import Point2D, Line


# Type OutCode
# INSIDE = 0  // 0000
# LEFT   = 1  // 0001
# RIGHT  = 2  // 0010
# BOTTOM = 4  // 0100
# TOP    = 8  // 1000

# compute the OutCode of a point
def computeOutCode(x, y, xmin, ymin, xmax, ymax):
    code = 0;
    if x < xmin:
        code |= 1
    elif x > xmax:
        code |= 2
    if y < ymin:
        code |= 4
    elif y > ymax:
        code |= 8

    return code


# clips a line using Cohen-Sutherland
def cohenSutherlandClip(x0, y0, x1, y1):

    codeP0 = computeOutCode(x0, y0, -1, -1, 1, 1)
    codeP1 = computeOutCode(x1, y1, -1, -1, 1, 1)

    if not(codeP0 | codeP1):
        # TOTALMENTE CONTIDA
        return Line(Point2D(x0, y0), Point2D(x1, y1))
    elif (codeP0 & codeP1):
        # TOTALMENTE FORA DA JANELA
        return None
    else:
        # PARCIALMENTE CONTIDA (CALCULAR CLIP PARA OS DOIS PONTOS)
        p0 = Point2D(x0, y0)
        p1 = Point2D(x1, y1)

        m = (y1-y0)/(x1-x0)

        if codeP0:
            p0 = calculateCSInterception(x0, y0, codeP0, m, -1, 1, -1, 1)

        if p0 and codeP1:
            p1 = calculateCSInterception(x1, y1, codeP1, m, -1, 1, -1, 1)

        if not(p0) or not(p1):
            return None
        else:
            return Line(p0, p1)


# calculates a new point over the window based on the coordinates and region code
def calculateCSInterception(x, y, regionCode, m, xe, xd, yf, yt):
    new_y = None
    new_x = None
    if regionCode & 1: # LEFT
        new_y = m * (xe - x) + y
    if regionCode & 2: # RIGHT
        new_y = m * (xd - x) + y
    if regionCode & 4: # BOTTOM
        new_x = x + 1/m * (yf - y)
    if regionCode & 8: # TOP
        new_x = x + 1/m * (yt - y)


    if new_x and new_y:
        if new_x >= xe and new_x <= xd and new_y >= yf and new_y <= yt:
            return Point2D(new_x, new_y)

    elif new_x:
        if new_x >= xe and new_x <= xd:
            return Point2D(new_x, y)

    elif new_y:
        if new_y >= yf and new_y <= yt:
            return Point2D(x, new_y)

    return None



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
        return Line(Point2D(self.x1, self.y1), Point2D(x2, y2))

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
        return Line(Point2D(x1, y1), Point2D(x2, y2))

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
        return Line(Point2D(x1, y1), Point2D(x2, y2))
