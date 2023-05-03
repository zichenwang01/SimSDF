from util import * 
from shape import Sphere 

@ti.data_oriented
class Scene:
    
    def __init__(self, dt):
        self.num_sphere = 1
        self.spheres = Sphere.field(shape=(100,))
        self.particles = ti.Vector.field(2, shape=(10000), dtype=ti.f32) 
        
        self.spheres[0].init(o=vec2(0.5,0.5), r=0.1, m=1, v=vec2(1,0))


    @ti.func
    def sdf(self, x):
        return self.spheres[0].sdf(x)

    @ti.kernel
    def update(self):
        idx = 0 
        for i in range(self.num_sphere):
            self.spheres[i].update()
            self.spheres[i].particles(idx, self.particles)
        
        
