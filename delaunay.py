from Dot import *
from math import sqrt

class AEL:
    def __init__(self, dt):
        self.edges = []
        self.dt = dt

    def add(self, e):
        a, b = e
        if (b, a) in self.edges:
            self.edges.remove(e)
        else:
            self.edges.append(e)

        self.dt.append(e)

    def empty(self):
        return not self.edges

    def remove(self, e):
        self.edges.remove(e)

    def first(self):
        return self.edges[0]


def dd(c, e):
    """
    The delaunay distance of point c from edge e = (a, b)
    """
    a, b = e

    # Compute the center s
    # https://en.wikipedia.org/wiki/Circumscribed_circle#Cartesian_coordinates_2
    d = 2*(a.x*(b.y - c.y) + b.x*(c.y - a.y) + c.x*(a.y - b.y))
    sx = ((a.x**2 + a.y**2)*(b.y - c.y) + (b.x**2 + b.y**2)*(c.y - a.y) + (c.x**2 + c.y**2)*(a.y - b.y)) / d
    sy = ((a.x**2 + a.y**2)*(c.x - b.x) + (b.x**2 + b.y**2)*(a.x - c.x) + (c.x**2 + c.y**2)*(b.x - a.x)) / d
    s = Dot(sx, sy)

    # Compute the radius r
    r = sqrt((s.x - c.x)**2 + (s.y - c.y)**2)

    if (ccw(c, a, b) < 0 and ccw(s, a, b) > 0) or (ccw(c, a, b) > 0 and ccw(s, a, b) < 0):
        return -r
    else:
        return r


# Prerequisite: No three points should be colinear
def triangulate(points):
    if not points:
        return []

    dt = [] # list of edges in the triangulation
    ael = AEL(dt)

    p1 = points[0]
    p2 = closestDot(points, p1)[0] # closestDot returns dot and distance

    points_left_of_e = [p for p in points if ccw(p, p1, p2) < 0]

    if points_left_of_e:
        e = (p1, p2)
        p = min(points_left_of_e, key=lambda p: dd(p, e))
        e2, e3 = (p2, p), (p, p1)
    else:
        e = (p2, p1)
        points_left_of_e = [p for p in points if ccw(p, p2, p1) < 0]
        p = min(points_left_of_e, key=lambda p: dd(p, e))
        e2, e3 = (p, p2), (p1, p)

    ael.add(e)
    ael.add(e2)
    ael.add(e3)

    while not ael.empty():
        e = ael.first()
        p1, p2 = e
        oe = (p2, p1)

        points_left_of_oe = [p for p in points if ccw(p, p2, p1) < 0]
        if points_left_of_oe:
            p = min(points_left_of_oe, key=lambda p: dd(p, oe))
            e2, e3 = (p, oe[0]), (oe[1], p)

            conds = [[ek not in ael.edges, not (ek[1], ek[0]) in ael.edges,
                      ek not in dt, (ek[1], ek[0]) not in dt] for ek in [e2, e3]]

            if all(conds[0]):
                ael.add(e2)

            if all(conds[1]):
                ael.add(e3)

        # dt.append(oe)
        ael.remove(e)

    return dt

