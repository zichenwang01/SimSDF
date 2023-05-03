from util import * 
from shape import Sphere 

@ti.data_oriented
class Scene:
    
    def __init__(self, dt):
        self.dt = dt
        
        self.num_sphere = 2
        self.spheres = Sphere.field(shape=(100,))
        self.sphere_pt = ti.Vector.field(2, shape=(10000), dtype=ti.f32) 
        self.spheres[0].init(o=vec2(0.5,0.5), r=0.1, m=1)


    @ti.func
    def sdf(self, x):
        return self.spheres[0].sdf(x)

    @ti.kernel 
    def init(self):
        print(self.sphere_pt[0])
        self.spheres[0].particles(0, self.sphere_pt)
        print(self.sphere_pt[0])

