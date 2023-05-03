from util import * 
from shape import Sphere 

@ti.data_oriented
class Scene:
    
    def __init__(self, dt):
        self.dt = dt
        self.num_obj = 10
        self.spheres = Sphere.field(shape=(2,))
        self.spheres[0] = Sphere(o=vec2(0,0), r=0.5, m=1)
        self.spheres[1] = Sphere(o=vec2(1,0), r=0.5, m=1)

    def sdf(self, x):
        return self.spheres[0].sdf(x)

# @ti.kernel 
# def test():
#     # scene.spheres[1] = Sphere(o=vec2(1,0), r=0.5, m=1)
#     scene.spheres[0].o = vec2(1,0)
#     print(scene.spheres[0].o)
#     print(scene.spheres.o)

# scene = Scene(dt=1e-6)
# test()
