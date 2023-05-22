import numpy as np
import taichi as ti
import taichi.math as tm

ti.init(arch=ti.cpu)

vec2 = tm.vec2
vec3 = tm.vec3

# substep
num_step = 100

# time step for each substep
dt = 1e-3

# number of vertices for each sphere
res = 3


@ti.func
def rot(q: vec2, X: vec2) -> vec2:
    """Rotate point X by rotation q"""
    return vec2(q.x * X.x - q.y * X.y, q.y * X.x + q.x * X.y)


@ti.func
def roti(q: vec2, X: vec2) -> vec2:
    """Rotate point X by the inverse of rotation q"""
    return vec2(q.x * X.x + q.y * X.y, -q.y * X.x + q.x * X.y)


@ti.func
def to_local(o: vec2, q: vec2, X: vec2) -> vec2:
    """Get the local coordinates of a point in world coordinates"""
    return roti(q, X - o)


@ti.func
def to_world(o: vec2, q: vec2, X: vec2) -> vec2:
    """Get the world coordinates of a point in local coordinates"""
    return rot(q, X) + o


@ti.func
def crossZ(p: float, q: vec2) -> vec2:
    """cross product of z-axis vector with xy-plane vector"""
    return vec2(-p * q.y, p * q.x)


@ti.func
def normal(v1: vec2, v2: vec2) -> vec2:
    """Get the normal vector of a line"""
    e = (v2 - v1).normalized()
    return vec2(e.y, -e.x)


@ti.func
def calculate_perpendicular_bisector(dot1: vec2, dot2: vec2):
    midpoint = (dot1 + dot2) / 2  # Calculate the midpoint between the two dots
    vector = dot2 - dot1  # Calculate the vector between the two dots
    perpendicular = vec2([-vector[1], vector[0]])  # Calculate the perpendicular vector
    return midpoint, perpendicular


@ti.func
def generate_points_on_bisector(dot1: vec2, dot2: vec2, length: float, num: int):
    midpoint, perpendicular = calculate_perpendicular_bisector(dot1, dot2)
    direction = perpendicular / tm.length(perpendicular)  # Normalize the perpendicular vector
    half_length = length / 2
    step = length / (num - 1)  # Calculate the step size
    start_point = midpoint - half_length * direction
    # points = [midpoint + i * step * direction for i in range(num)]  # Generate evenly distributed points
    points = vec2.field(shape=(num,))
    for i in range(num):
        points[i] = start_point + i * step * direction
    return points
