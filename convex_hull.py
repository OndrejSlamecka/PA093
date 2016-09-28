from Dot import *


def gift_wrapping(points):
    if len(points) <= 2:
        return []

    # Find a starting point q called a pivot
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
