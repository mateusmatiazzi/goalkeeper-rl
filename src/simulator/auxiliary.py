"""
@author  Mateus Paiva Matiazzi
"""

import numpy as np
import numpy.linalg as la
import math
import random

def unitVector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angleBetween(v1, v2, ccw=True):
    """ Returns the angle in radians between vectors 'v1' and 'v2' """
    cosang = np.dot(v1, v2)
    sinang = np.cross(v1, v2)
    if ccw:
        sinang = la.norm(np.cross(v1, v2))
    return np.arctan2(sinang, cosang)  # atan2(y, x) or atan2(sin, cos)

def rotateVector(x, angle):
    """Rotate vector x anticlockwise around the origin by angle degrees, return angle in format [x, y]"""
    y1 = math.cos(angle)*x[0] - math.sin(angle)*x[1]
    y2 = math.sin(angle)*x[0] + math.cos(angle)*x[1]
    return [y1, y2]

def rotatePoint(origin, point, angle):
    """Rotate a point counterclockwise by a given angle around a given origin.
    The angle should be given in radians."""
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return (int(qx),int(qy))

def distancePoints(a, b):
    """Distance between two points"""
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2)**0.5

def maxAbs(x, y):
    """Return the maximum absolute value"""
    return max(abs(x), abs(y))

def throwInGoal(top, bottom, ball):
    """Return a vector to throw the ball"""
    final = [120, random.randint(bottom, top)]
    return [final[0] - ball[0], final[1] - ball[1]]
