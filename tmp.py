import numpy as np
import taichi as ti 
import taichi.math as tm

ti.init(arch=ti.cpu)

lst = ti.field(dtype=ti.f32, shape=(2,))

@ti.func
def func(lst):
    lst[0] = 1.0

@ti.kernel
def kernel():
    for i,j in ti.ndrange(20, 20):
        x = tm.vec2((i-10)/10, (j-10)/10) 
        print(x)
    
    # for i,j in np.arange(-2,2), np.arange(-2,2):
    #     print(i,j)

kernel()