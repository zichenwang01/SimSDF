from util import *
from scene import *
from response import *

@ti.dataclass
class Shape:
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

    sdf_map : np.array
    sdf_grad_map : np.array
    normal_map : np.array

    def __init__(self, o, R=vec2(1,0), v=vec2(0,0), ω=0, m=1, I=1, size=1):
        pass

    #convert a point from voxel space to world space
    def to_world(vec2):
        pass
    
    def collide_sdf(self, object, itx):
        pass
    
    def update(self, dt):
        pass

# returns (is_collision, collision_data)
def check_collision(object1, object2):
    pass

