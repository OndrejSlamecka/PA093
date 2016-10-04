class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __sub__(self, other):
        return PVector(self.x - other.x, self.y - other.y)

    def __repr__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"


# Returns the PVector given by a - b
def v(a, b):
    return PVector(a.x - b.x, a.y - b.y)