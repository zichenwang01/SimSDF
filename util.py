import numpy as np 
import taichi as ti 
import taichi.math as tm 

ti.init(arch=ti.cpu)

vec2 = tm.vec2 
vec3 = tm.vec3

# substep
num_step = 100

# time step for each substep
dt = 1e-6

@ti.func
def rot(q, X)->vec2:
    """Rotate point X by rotation q"""
    """Code from https://github.coecis.cornell.edu/cs5643/assignments"""
    return vec2(q.x * X.x - q.y * X.y, q.y * X.x + q.x * X.y)

@ti.func
def roti(q, X)->vec2:
    """Rotate point X by the inverse of rotation q"""
    """Code from https://github.coecis.cornell.edu/cs5643/assignments"""
    return vec2(q.x * X.x + q.y * X.y, -q.y * X.x + q.x * X.y)
