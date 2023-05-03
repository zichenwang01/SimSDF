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
    def to_local(self, x):
        """Get the local coordinates of a point in world coordinates"""
        pass
    
    @ti.func 
    def to_world(self, x):
        """Get the world coordinates of a point in local coordinates"""
        pass
    
    @ti.func 
    def sdf(self, x):
        """Get the signed distance from a point to the object"""
        pass
    
    @ti.func 
    def update(self):
        """Numerical integration"""
        pass

@ti.dataclass
class Sphere:
    o : vec2  # origin (center of mass)
    r : float # radius
    R : vec2  # rotation (cosine/sine pair)
    v : vec2  # linear velocity
    ω : float # angular velocity
    # l : vec2  # dimensions of box
    m : float # mass
    I : float # moment of inertia
    size: float # collision detection radius
    
    def init(self, o, r, R=vec2(1,0), v=vec2(0,0), ω=0, m=1, I=None, size=None):
        self.o = o
        self.r = r
        self.R = R
        self.v = v
        self.ω = ω
        self.m = m
        
        if I is None:
            self.I = 0.25 * m * r * r
        else:
            self.I = I
        
        if size is None:
            self.size = r
        else:
            self.size = size
    
    @ti.func 
    def to_local(self, x):
        return roti(self.R, x - self.o)
    
    @ti.func 
    def to_world(self, x):
        return rot(self.R, x) + self.o
    
    @ti.func
    def sdf(self, x):
        return (x - self.o).norm()
    
    @ti.func
    def update(self):
        self.o += self.v * dt
        self.R += self.ω * dt
        self.R = self.R.normalized()

