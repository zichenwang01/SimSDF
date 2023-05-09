import numpy as np
import taichi as ti
import taichi.math as tm

ti.init(arch=ti.cpu)

vec2 = tm.vec2

@ti.dataclass
class Particle:
    a : vec2
    
@ti.kernel 
def func(x:vec2, y:vec2=vec2(1,0)):
    p = Particle()
    p.a = vec2(1,2)

func(x=vec2(1,2))