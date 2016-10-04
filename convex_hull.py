from Dot import *


## Gift wrapping

def gift_wrapping(points):
    if len(points) <= 2:
        return []

    # Find a starting point q
    q = min(points, key=lambda p: p.y)

    # And an auxiliary point which forms a line l with q,
    # such that l is parallel with the x axis
    # (This first line will provide a starting direction for the algorithm)
    aux = Dot(-1, q.y)

    # In each step of the loop below we will find a point of the hull
    hull_point = None

    # In each step hull_point (so far not in H!) will be added to H
    # maintaing the invariant that H \ {aux} is a subset of the convex
    # hull of points

    # q has to be in H by its choice above
    H = [aux, q]

    while hull_point != q:
        # l and stl are the last and the second to last points in H
        l, stl = H[-1], H[-2]

        # The new hull_point will be chosen from points \ {l, stl}
        points_prime = filter(lambda p: p != l and p != stl, points)

        # The new hull_point is a point p
        hull_point = min(points_prime, # in points_prime, minimizing
            key = lambda p:
                PVector.angleBetween( # the angle between
                    v(stl, l), # the stl-l vector
                    v(l,   p) # and the l-p vector
                )
        )

        H.append(hull_point)

    # Remove the auxiliary point and one occurence of q
    del H[0], H[0]

    # Now H is a convex hull of the given points
    return H


## Graham scan

from collections import deque


def ccw(p1, p2, p3):
    # 0  points are colinear
    # >0 cw
    # <0 ccw
    return (p2.x - p1.x)*(p3.y - p1.y) - (p2.y - p1.y)*(p3.x - p1.x)
    

def graham_scan(points):
    if len(points) <= 2:
        return []

    # Find a starting point q
    q = min(points, key=lambda p: (p.y, p.x))
    
    # Sort by angle
    x_axis = v(Dot(1,0), Dot(0,0))    
    s_points = sorted(points, key=lambda p: PVector.angleBetween(v(p, q), x_axis))
    
    # Initialize the queue
    Q = deque()
    Q.append(q)
    Q.append(s_points[1])
    
    # Find new points
    j = 2
    while j < len(s_points):
        if ccw(Q[-2], Q[-1], s_points[j]) >= 0:
            Q.append(s_points[j])
            j = j + 1
        else:
            Q.pop()            
    
    return list(Q)