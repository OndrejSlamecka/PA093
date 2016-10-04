# Python libraries
import random
import math
from operator import itemgetter

# Parts of this project
from Dot import Dot
import convex_hull

## Constants
pointSize = 14
textSize = 12

canvas = {'width': 640, 'height': 640}


## Global state
class State:
    def __init__(self):
        self.mode = 'add'  # also possible: edit, delete
        self.help = False
        self.dots = []
        self.lines = []
        self.dragged = None


state = State()


## UI
def render_text_information():
    background(255)
    text(state.mode, 10, canvas['height'] - 10)
    text('h -- toggle help', 10, 20)
    if state.help:
        help()


# Text information
def help():
    text("""
c -- clear scene
a -- switch to `add` mode
e -- switch to `edit` mode
d -- switch to `delete` mode
r -- add 10 random points
j -- convex hull by gift wrapping
g -- convex hull by Graham scan
""", 10, 20)


# Setup the canvas
def setup():
    size(canvas['width'], canvas['height'])

    # Black objects on white background
    fill(0)
    background(255)

    # Font
    monospaced = createFont("Monospaced", textSize)
    textFont(monospaced)

    render_text_information()


# Re-drawing
def draw():
    background(255)
    render_text_information()

    for dot in state.dots:
        ellipse(dot.x, dot.y, pointSize, pointSize)

    for a, b in state.lines:
        line(a.x, a.y, b.x, b.y)


# Mouse events
def mouseClicked():
    if state.mode == 'add':
        state.dots.append(Dot(mouseX, mouseY))

    if state.mode == 'delete':
        dot = getClickedDot()
        if dot:
            state.dots.remove(dot)


def mousePressed():
    if state.mode == 'edit':
        state.dragged = getClickedDot()


def mouseDragged():
    if state.dragged and state.dragged:
        state.dragged.x = mouseX
        state.dragged.y = mouseY


def mouseReleased():
    if state.mode == 'edit':
        state.dragged = None


# Key events
def keyReleased():
    if key == 'c':
        del state.dots[:]
        del state.lines[:]

    if key == 'a':
        state.mode = 'add'

    if key == 'e':
        state.mode = 'edit'

    if key == 'd':
        state.mode = 'delete'

    if key == 'h':
        state.help = not state.help

    if key == 'r':
        addRandomDots()

    if key == 'j':
        if len(state.dots) > 3:
            points = convex_hull.gift_wrapping(state.dots)
            state.lines.extend(zip(points, points[1:]))
            state.lines.append((points[-1], points[0]))
    
    if key == 'g':
        if len(state.dots) > 3:
            points = convex_hull.graham_scan(state.dots)
            state.lines.extend(zip(points, points[1:]))
            state.lines.append((points[-1], points[0]))        


## Utility functions
def closestDot(x, y):
    """
    Returns the dot closest to given coordinates and the squared distance.
    """
    if len(state.dots) == 0:
        return None, None

    dots_and_distances = [(dot, (dot.x - x)**2 + (dot.y - y)**2)
                          for dot in state.dots]
    return min(dots_and_distances, key=itemgetter(1))


def getClickedDot():
    """
    Returns the clicked dot.
    If there are more such dots it returns the closest one.
    If there are none such dots it returns None.
    """
    if len(state.dots) == 0:
        return None

    dot, distanceSquared = closestDot(mouseX, mouseY)
    if distanceSquared <= (pointSize / 2)**2:
        return dot
    else:
        return None


def addRandomDots():
    """
    Avoids placing the dots over other dots.
    """
    padding = 10 + textSize + pointSize

    dotsAdded = 0
    attempts = 0
    while dotsAdded < 10 and attempts < 500:
        x = random.randint(padding, canvas['width'] - padding)
        y = random.randint(padding, canvas['height'] - padding)

        overlaps = False
        if len(state.dots) > 0:
            _, distance = closestDot(x, y)
            overlaps = distance <= pointSize**2

        if not overlaps:
            state.dots.append(Dot(x, y))
            dotsAdded += 1

        attempts += 1