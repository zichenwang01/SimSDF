from util import * 
from shape import Sphere 

@ti.dataclass 
class Particle:
    p : vec2 
    idx : int

@ti.data_oriented
class Scene:
   
    def __init__(self, dt):
        # spheres
        self.num_sphere = ti.field(dtype=ti.i32, shape=())
        self.spheres = Sphere.field(shape=(100,))
        
        # particles in local coordinates
        self.num_pt = ti.field(dtype=ti.i32, shape=())
        self.particles = Particle.field(shape=(10000,))
        self.positions = ti.Vector.field(2, shape=(10000), dtype=ti.f32)
        
        # self.particles = ti.Vector.field(2, shape=(10000), dtype=ti.f32) 
        # self.indecies = ti.field(dtype=ti.i32, shape=(10000))
    
    @ti.kernel
    def add_sphere(self, o:vec2, r:float, m:float):
        """Initialize a sphere"""
        self.spheres[self.num_sphere[None]].init(o=o, r=r, m=m)
        print(self.spheres[self.num_sphere[None]].r)
        self.spheres[self.num_sphere[None]].particles(self.num_sphere, 
                                                      self.num_pt, self.particles)
        self.num_sphere[None] += 1

    @ti.func
    def sdf(self, x):
        return self.spheres[0].sdf(x)

    @ti.kernel
    def update(self):
        for i in range(self.num_sphere[None]):
            self.spheres[i].update()
        
        # print(self.num_pt[None])
        for i in range(self.num_pt[None]):
            idx = self.particles[i].idx
            self.positions[i] = to_world(self.spheres[idx].o, self.spheres[idx].R, self.particles[i].p)
        
        
