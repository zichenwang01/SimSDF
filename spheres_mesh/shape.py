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
    
    @ti.func 
    def collision_detection(self, sphere):
        """Baseline by mesh representation"""
        # v1 = ti.Vector.field(3, shape=(res), dtype=ti.f32)
        # for i in range(res):
        #     v1[i] = self.to_world(
        #         self.o, self.R,
        #         tm.rotation2d(i * 2 * tm.pi / res) @ vec2(self.r,0)
        #     )
    
        # v2 = ti.Vector.field(3, shape=(res), dtype=ti.f32)
        # for i in range(res):
        #     v2[i] = sphere.to_world(
        #         sphere.o, sphere.R,
        #         tm.rotation2d(i * 2 * tm.pi / res) @ vec2(sphere.r,0)
        #     )
        
        max_itx = vec2(-1, -1)
        max_sep = -tm.inf
        for i in range(res):
            itx = vec2(-1, -1)
            sep = tm.inf 
            v1 = to_world(
                self.o, self.R,
                tm.rotation2d(i * 2 * tm.pi / res) @ vec2(self.r,0)
            )
            v2 = to_world(
                self.o, self.R,
                tm.rotation2d((i+1) * 2 * tm.pi / res) @ vec2(self.r,0)
            )
            n = normal(v1, v2)
            # print(v1, v2, n)
            for j in range(res):
                v3 = to_world(
                    sphere.o, sphere.R,
                    tm.rotation2d(j * 2 * tm.pi / res) @ vec2(sphere.r,0)
                )
                d = n.dot(v3 - v1)
                if d < sep:
                    sep = d
                    itx = v3
            if sep > max_sep:
                max_sep = sep
                max_itx = itx
            # print(sep)
            
        for i in range(res):
            itx = vec2(-1, -1)
            sep = tm.inf 
            v1 = to_world(
                sphere.o, sphere.R,
                tm.rotation2d(i * 2 * tm.pi / res) @ vec2(sphere.r,0)
            )
            v2 = to_world(
                sphere.o, sphere.R,
                tm.rotation2d((i+1) * 2 * tm.pi / res) @ vec2(sphere.r,0)
            )
            n = normal(v1, v2)
            for j in range(res):
                v3 = to_world(
                    self.o, self.R,
                    tm.rotation2d(j * 2 * tm.pi / res) @ vec2(self.r,0)
                )
                d = n.dot(v3 - v1)
                if d < sep:
                    sep = d
                    itx = v3
            if sep > max_sep:
                max_sep = sep
                max_itx = itx
        
        if max_sep > 0:
            max_itx = vec2(-1, -1)
            
        # print(max_sep)
        return max_itx
            
    
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
