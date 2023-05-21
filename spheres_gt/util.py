import numpy as np
import taichi as ti
import taichi.math as tm

ti.init(arch=ti.cpu)

vec2 = tm.vec2
vec3 = tm.vec3
mat3 = tm.mat3

# substep
num_step = 100

# time step for each substep
dt = 1e-4

# number of vertices for each sphere
res = 32

# simulation parameters
Cr, β, μ = 0.5, 0.5, 0.1

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
def crossXY(u: vec2, v: vec2):
    """cross product of two xy plane vectors"""
    return u.x * v.y - u.y * v.x


@ti.func
def cross(w: float, v: vec2):
    """cross product of z-axis vector with xy-plane vector"""
    return vec2(-w*v.y, w*v.x)


@ti.func
def to2d(v: vec3):
    """convert 3d vector to 2d"""
    return vec2(v.x, v.y)


@ti.func
def b2w(p, q, X):
    """body to world"""
    return p + rot(q, X)


@ti.func
def w2b(p, q, x):
    """world to body"""
    return roti(q, x - p)


@ti.func
def crossZ(p: float, q: vec2) -> vec2:
    """cross product of z-axis vector with xy-plane vector"""
    return vec2(-p * q.y, p * q.x)
