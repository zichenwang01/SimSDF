from util import * 
from shape import Sphere 

@ti.data_oriented
class Scene:
   
    def __init__(self, dt):
        # spheres
        self.num_sphere = ti.field(dtype=ti.i32, shape=())
        self.spheres = Sphere.field(shape=(100,))
        self.objs = self.spheres
        
        # triangles in local coordinates
        self.num_v = ti.field(dtype=ti.i32, shape=())
        self.num_tri = ti.field(dtype=ti.i32, shape=())
        self.vertices = ti.Vector.field(2, shape=(10000), dtype=ti.f32)
        self.triangles = ti.field(dtype=ti.i32, shape=(3*10000))
        self.colors = ti.Vector.field(3, shape=(10000), dtype=ti.f32)

        # colliding points
        self.num_collide = ti.field(dtype=ti.i32, shape=())
        self.collide = ti.Vector.field(2, shape=(10000), dtype=ti.f32)

    @ti.func
    def clear_collision(self):
        self.num_collide[None] = 0
        self.collide.fill(0)

    @ti.func
    def add_collision(self, p:vec2):
        self.collide[self.num_collide[None]] = p
        ti.atomic_add(self.num_collide[None],1)
    
    @ti.kernel
    def add_sphere(self, o:vec2, x:float,y:float, m:float, v:vec2):
        """Initialize a sphere"""
        num_sphere = self.num_sphere[None]
        self.spheres[num_sphere].init(o=o, x=x,y=y, m=m, v=v)
        self.spheres[num_sphere].triangles(self.num_v, 
                                           self.num_tri, 
                                           self.triangles)
        self.num_sphere[None] += 1

    @ti.func
    def sdf(self, x):
        dist = tm.inf
        for i in range(self.num_sphere[None]):
            dist = min(dist, self.spheres[i].sdf(x))
        return dist

    @ti.func
    def sdf_grad(self, x):
        dx = (self.sdf(x + vec2(1e-4, 0)) - self.sdf(x - vec2(1e-4, 0))) / 2e-4
        dy = (self.sdf(x + vec2(0, 1e-4)) - self.sdf(x - vec2(0, 1e-4))) / 2e-4
        return vec2(dx, dy)

    @ti.kernel
    def update(self):
        for i in range(self.num_sphere[None]):
            self.spheres[i].update()
        
    @ti.kernel
    def update_vertices(self):
        """Update vertices of all spheres"""
        for i in range(self.num_sphere[None]):
            self.vertices[i*4] = to_world(self.spheres[i].o, self.spheres[i].R, vec2(-self.spheres[i].x,-self.spheres[i].y))
            self.vertices[i*4+1] = to_world(self.spheres[i].o, self.spheres[i].R, vec2(self.spheres[i].x,-self.spheres[i].y))
            self.vertices[i*4+2] = to_world(self.spheres[i].o, self.spheres[i].R, vec2(self.spheres[i].x,self.spheres[i].y))
            self.vertices[i*4+3] = to_world(self.spheres[i].o, self.spheres[i].R, vec2(-self.spheres[i].x,self.spheres[i].y))
            self.colors[i*4] = self.spheres[i].color
            self.colors[i*4+1] = self.spheres[i].color
            self.colors[i*4+2] = self.spheres[i].color
            self.colors[i*4+3] = self.spheres[i].color
        
