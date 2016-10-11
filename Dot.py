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
    # 0  points are colinear
    # >0 cw
    # <0 ccw
    return (p2.x - p1.x)*(p3.y - p1.y) - (p2.y - p1.y)*(p3.x - p1.x)

