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
res = 128

@ti.func
def rot(q:vec2, X:vec2)->vec2:
    """Rotate point X by rotation q"""
    return vec2(q.x * X.x - q.y * X.y, q.y * X.x + q.x * X.y)

@ti.func
def roti(q:vec2, X:vec2)->vec2:
    """Rotate point X by the inverse of rotation q"""
    return vec2(q.x * X.x + q.y * X.y, -q.y * X.x + q.x * X.y)

@ti.func
def to_local(o:vec2, q:vec2, X:vec2)->vec2:
    """Get the local coordinates of a point in world coordinates"""
    return roti(q, X - o)

@ti.func
def to_world(o:vec2, q:vec2, X:vec2)->vec2:
    """Get the world coordinates of a point in local coordinates"""
    return rot(q, X) + o

@ti.func
def normal(v1:vec2, v2:vec2)->vec2:
    """Get the normal vector of a line"""
    e = (v2 - v1).normalized()
    return vec2(e.y, -e.x)

@ti.func
def crossZ(p: float, q: vec2) -> vec2:
    """cross product of z-axis vector with xy-plane vector"""
    return vec2(-p * q.y, p * q.x)
