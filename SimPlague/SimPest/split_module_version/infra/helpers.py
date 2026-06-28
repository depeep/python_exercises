import math

def distance(a, b):
    return math.dist(a, b)

def clamp(value, minv, maxv):
    return max(minv, min(value, maxv))