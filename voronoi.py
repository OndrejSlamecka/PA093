# Computes the Voronoi diagram from Delaunay triangulation
from Dot import *

class Triangle:
    def __init__(self, edges):
        self.edges = edges

        # Compute the points
        pts = []
        for e in edges:
            pts.extend([e[0], e[1]])
        pts = list(set(pts))

        self.center = center(*pts)

    def borders(self, t):
        for edge in self.edges:
            e_prime = (edge[1], edge[0])
            if edge in t.edges or e_prime in t.edges:
                return True

        return False


def diagram(triangles):
    # Each input triangle is formed by three line segments
    triangles = map(Triangle, triangles)
    lines = []

    n = len(triangles)
    for i in range(n):
        for j in range(i + 1, n):
            if triangles[i].borders(triangles[j]):
                lines.append((triangles[i].center, triangles[j].center))

    # Filter out duplicates
    # TODO: Figure out how to not put them in in the first place
    filtered_lines = []
    for l in lines:
        if l not in filtered_lines and (l[1], l[0]) not in filtered_lines:
            filtered_lines.append(l)

    return filtered_lines
