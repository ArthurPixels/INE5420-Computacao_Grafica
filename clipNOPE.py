from point import Point
import math


class NichollLeeNicholl:
    def __init__(self):
        self.display = False

    def clip(start: Point, end: Point):
        if start.x < -1:
            display = left_column(start, end)
        elif start.x > 1:
            start = rotate(start, 2 * math.pi)
            end = rotate(end, 2 * math.pi)
            display = left_column(start, end)
        else:
            display = center_column(start, end)
        if display:
            # r/restofthefuckingowl

    def left_column(start: Point, end: Point):
        if end.x < -1:
            display = False
        elif start.y > 1:
            display = top_left_corner(start, end)
        elif start.y < -1:
            start.x = -start.x
            end.x = -end.x
            display = top_left_corner(start, end)
            start.x = -start.x
            end.x = -end.x
        else:
            display = left

    def top_left_corner(start: Point, end: Point):
        pass

    def left_bottom_region(start: Point, end: Point):
        pass

    def center_column(start: Point, end: Point):
        pass

    def inside(start: Point, end: Point):
        if end.x < -1:
            start = rotate(start, 2 * math.pi)
            end = rotate(end, 2 * math.pi)
            end_left(start, end)
            start = rotate(start, 2 * math.pi)
            end = rotate(end, 2 * math.pi)
        elif end.y > 1:
            # top intersection
            pass
        elif end.y < -1:
            # bottom intersection
            pass
        return True
