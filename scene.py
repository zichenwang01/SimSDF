from util import * 
from shape import Sphere 


@ti.data_oriented
class Scene:
   
    def __init__(self, dt):
        # spheres
        self.num_sphere = ti.field(dtype=ti.i32, shape=())
        self.spheres = Sphere.field(shape=(100,))
        
        # triangles in local coordinates
        self.num_v = ti.field(dtype=ti.i32, shape=())
        self.num_tri = ti.field(dtype=ti.i32, shape=())
        self.vertices = ti.Vector.field(2, shape=(10000), dtype=ti.f32)
        self.triangles = ti.field(dtype=ti.i32, shape=(3*10000))

    
    @ti.kernel
    def add_sphere(self, o:vec2, r:float, m:float):
        """Initialize a sphere"""
        num_sphere = self.num_sphere[None]
        self.spheres[num_sphere].init(o=o, r=r, m=m)
        self.spheres[num_sphere].triangles(self.num_v, 
                                           self.num_tri, 
                                           self.triangles)
        self.num_sphere[None] += 1

    @ti.func
    def sdf(self, x):
        return self.spheres[0].sdf(x)

    @ti.kernel
    def update(self):
        for i in range(self.num_sphere[None]):
            self.spheres[i].update()
        
    @ti.kernel
    def update_vertices(self):
        for i in range(self.num_sphere[None]):
            self.vertices[i * (res + 1)] = self.spheres[i].o
            for j in range(res):
                self.vertices[i * (res + 1) + j + 1] = to_world(
                    self.spheres[i].o,
                    self.spheres[i].R,
                    tm.rotation2d(j * 2 * tm.pi / res) @ vec2(self.spheres[i].r,0)
                )
        
        
