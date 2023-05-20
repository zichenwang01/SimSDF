from util import *

@ti.dataclass
class Object:
    """ Base class for all objects in the scene.
        This class serves as an interface for all objects in the scene.
        It is not meant to be instantiated."""
    
    o : vec2  # origin (center of mass)
    R : vec2  # rotation (cosine/sine pair)
    v : vec2  # linear velocity
    ω : float # angular velocity
    m : float # mass
    I : float # moment of inertia
    size : float # collision detection radius
    color : vec3 
    
    def __init__(self, o, R=vec2(1,0), v=vec2(0,0), ω=0, m=1, I=None, size=None):
        pass
    
    @ti.func 
    def sdf(self, x):
        """Get the signed distance from a point to the object"""
        pass
    
    @ti.func 
    def collision_detection(self, sphere):
        """Get the intersection point between two objects.
           If there is no intersection, return (-1,-1)"""
        pass
    
    @ti.func
    def triangles(self, num_v, num_tri, triangles):
        """ Render the object as a set of triangles in local coordinates.
            For rigid bodies, this function should only be called once"""
        pass
    
    @ti.func 
    def update(self):
        """Numerical integration"""
        pass

@ti.dataclass
class Sphere:
    o : vec2  # origin (center of mass)
    r : float # radius
    m : float # mass
    v : vec2  # linear velocity
    ω : float # angular velocity
    R : vec2  # rotation (cosine/sine pair)
    I : float # moment of inertia
    size: float # collision detection radius
    color : vec3
    
    @ti.func
    def init(self, o, r, m=1, v=vec2(0,0), ω=0):
        self.o = o
        self.r = r
        self.m = m
        self.v = v
        self.ω = ω
        self.R = vec2(1,0)
        self.I = 0.25 * m * r * r
        self.size = r
        self.color = vec3(1,1,1)
    
    @ti.func
    def sdf(self, x):
        return (x - self.o).norm() - self.r
    
    # @ti.func 
    # def collision_detection(self, sphere):
    #     """Ground truth. Only used for debugging."""
    #     itx = vec2(-1,-1)
    #     if (self.o - sphere.o).norm() < self.r + sphere.r:
    #         itx = 0.5 * (self.o + sphere.o)
    #     return itx
    
    @ti.func 
    def sdf_grad(self, x):
        return (x - self.o).normalized()
    
    @ti.func 
    def collide_sdf(self, sphere, x):
        return tm.max(self.sdf(x), sphere.sdf(x))
    
    @ti.func 
    def collide_grad(self, sphere, x):
        left = self.collide_sdf(sphere, x - vec2(1e-4,0))
        right = self.collide_sdf(sphere, x + vec2(1e-4,0))
        up = self.collide_sdf(sphere, x - vec2(0,1e-4))
        down = self.collide_sdf(sphere, x + vec2(0,1e-4))
        
        dx = (right - left) / 2e-4
        dy = (down - up) / 2e-4
        
        return vec2(dx, dy).normalized()
    
    @ti.func
    def collision_detection(self, sphere):
        itx = 0.5 * (self.o + sphere.o)
        for i in range(5):
            grad = self.collide_grad(sphere, itx)
            itx -= self.collide_sdf(sphere, itx) * grad
        return itx
    
    @ti.func 
    def triangles(self, num_v, num_tri, triangles):
        for i in range(res):
            triangles[3 * num_tri[None]] = num_v[None]
            triangles[3 * num_tri[None] + 1] = num_v[None] + i + 1
            triangles[3 * num_tri[None] + 2] = num_v[None] + (i + 1) % res + 1
            ti.atomic_add(num_tri[None], 1)
        ti.atomic_add(num_v[None], res + 1)
        
    
    @ti.func
    def update(self):
        self.o += self.v * dt
        self.R += self.ω * dt
        self.R = self.R.normalized()
