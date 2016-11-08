from Dot import *


class KDTreeNode:
    def __init__(self, point, depth):
        self.point = point
        self.depth = depth
        self.left = None
        self.right = None
    
    def __repr__(self):
        return str(self.point) + " at " + str(self.depth) + " [" + str(self.left) + " | " + str(self.right) + "]"


def build(P, depth):    
    if len(P) == 0:
        return None
    
    if len(P) == 1:
        return KDTreeNode(P[0], depth)
    else:                                
        if depth % 2 == 0:
            Px = sorted(P, key=lambda p: p.x)
            mi = len(Px) / 2
            median = Px[mi]
            P1, P2 = Px[:mi], Px[mi + 1:]
        else:
            Py = sorted(P, key=lambda p: p.y)
            mi = len(Py) / 2
            median = Py[mi]
            P1, P2 = Py[:mi], Py[mi + 1:]
                
            
        v = KDTreeNode(median, depth)
        v.left = build(P1, depth + 1)
        v.right = build(P2, depth + 1)            
        return v
    
    
def lines(root, top, right, bottom, left):
    if not root or (not root.left and not root.right):
        return []
    
    if root.depth % 2 == 0:
        x = root.point.x
        line = (Dot(x, top), Dot(x, bottom))        
        return [line] + lines(root.left, top, x, bottom, left) + lines(root.right, top, right, bottom, x)
    else:
        y = root.point.y
        line = (Dot(left, y), Dot(right, y))
        return [line] + lines(root.left, top, right, y, left) + lines(root.right, y, right, bottom, left)