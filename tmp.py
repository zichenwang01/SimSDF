import numpy as np 
import taichi as ti

ti.init(arch=ti.cpu)

v = ti.field(dtype=ti.f32, shape=(3))
v += 1

print(v)
