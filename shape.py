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
    # l : vec2  # dimensions of box
    m : float # mass
    I : float # moment of inertia
    size: float # collision detection radius
    
    def __init__(self, o, R=vec2(1,0), v=vec2(0,0), ω=0, m=1, I=None, size=None):
        pass
    
    @ti.func 
    def sdf(self, x):
        """Get the signed distance from a point to the object"""
        pass
    
    @ti.func
    def particles(self):
        """ Render the object as a set of particles in local coordinates.
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
    
    @ti.func
    def sdf(self, x):
        return (x - self.o).norm() - self.r
    
    @ti.func
    def particles(self, idx, num_pt, particles):
        for i,j in ti.ndrange(20, 20):
            
            local = vec2(float((i-10.0)/10.0), (j-10.0)/10.0) * self.size
            # print(local)
            world = to_world(self.o, self.R, local)
            
            if self.sdf(world) < 0:
                # print(local)
                particles[num_pt[None]].p = local
                particles[num_pt[None]].idx = idx[None]
                ti.atomic_add(num_pt[None], 1)
    
    @ti.func
    def update(self):
        self.o += self.v * dt
        self.R += self.ω * dt
        self.R = self.R.normalized()
