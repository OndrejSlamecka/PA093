from operator import itemgetter

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __hash__(self):
        return hash((self.x, self.y))


# Returns the PVector given by a - b
def v(a, b):
    return PVector(a.x - b.x, a.y - b.y)


def ccw(p1, p2, p3):
    #   0 if the points are colinear
    # > 0 if                ccw
    # < 0 if                cw
    return (p2.x - p1.x)*(p3.y - p1.y) - (p2.y - p1.y)*(p3.x - p1.x)


def closestDot(dots, p):
    """
    Returns the dot closest to given coordinates and the squared distance.
    """
    if len(dots) == 0:
        return None, None

    if not isinstance(p, Dot):
        p = Dot(p[0], p[1])

    dots_and_distances = [(dot, (dot.x - p.x)**2 + (dot.y - p.y)**2)
                          for dot in dots if dot != p]

    return min(dots_and_distances, key=itemgetter(1))
