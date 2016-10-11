from Dot import *
from collections import deque


# For now we assume the polygon is convex
def triangulate(lines):
    if len(lines) == 0:
        return []

    # TODO: comparing xs
    
    min_y = 9999
    min_y_i = -1
    for i in range(len(lines)):
        if lines[i][0].y < min_y:
            min_y = lines[i][0].y
            min_y_i = i
            
        if lines[i][1].y < min_y:
            min_y = lines[i][1].y
            min_y_i = i
        

    min_edge = min(enumerate(lines), key=lambda i_e: (i_e[1].y, i_e[1].x))
    max_edge = max(enumerate(lines), key=lambda i_e: (i_e[1].y, i_e[1].x))
    
    left = []
    right = []
    for i in range(len(lines)):
        line = lines[(min_edge[0] + i) % len(lines)]
        if line == max_edge:
            break
        
        left.append(line)

    polygon = list(set([u for u,v in lines]))

    D = []

    dots = sorted(polygon, key=lambda p: (p.y, p.x))
    S = [dots[0], dots[1]]

    # Compute sides
    top = dots[0]
    bottom = dots[-1]

    right = [p for p in dots if ccw(bottom, top, p) >= 0]
    left = [p for p in dots if ccw(bottom, top, p) < 0]

    print(left)
    print(right)

    # shouldn't dots[0] and dots[1] lie on one chain?
    right = right[1:]
    if left and dots[1] == left[0]:
        S_top_side = 'left'
        left = left[1:]
    else:
        S_top_side = 'right'
        right = right[1:]

    for j in range(2, len(dots) - 1):
        print(S, S_top_side, dots[j])
        # if dots[j], S[-1] lie on different top-bottom paths
        if (left and dots[j] == left[0] and S_top_side == 'right') \
            or (right and dots[j] == right[0] and S_top_side == 'left'):
            # Pop all vertices from S and insert a diagonal from dots[j]
            # to popped vertices except the last one

            for i in range(len(S) - 1):
                D.append((dots[j], S[-1]))
                S.pop()

            # pop the last one
            S.pop()

            S.append(dots[j-1])
        else:
            S.pop()

            last_popped = None
            for i in range(len(S)):
                # TODO: if dots[j] S[-1] is outside the polygon, break
                #if right and dots[j] == right[0] and len(S) > 1 and ccw(S[-2], S[-1], dots[j]) > 0:
                #    break
                # if S_side == 'left' and len(S) > 1 and ccw(S[-2], S[-1], dots[j]) > 0:
                    # break
                D.append((dots[j], S[-1]))
                last_popped = S.pop()

            # Push the last vertex that has been popped back onto S
            if last_popped:
                S.append(last_popped)

        S.append(dots[j])        

        if left and dots[j] == left[0]:
            S_top_side = 'left'
            left = left[1:]
        else:
            S_top_side = 'right'
            right = right[1:]            

    for i in range(1, len(S) - 1):
        D.append((dots[-1], S[i]))

    return D