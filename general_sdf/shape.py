# from __future__ import annotations

from util import *
from collision import collideInfo
import trimesh
from voxelSDF import load_mesh


TOTAL_RESOLUTION = 512
DETECT_DENSITY = 20
DETECT_THRESHOLD = 2e-2


# @ti.dataclass
class Shape:
    """ Base class for all objects in the scene.
        This class serves as an interface for all objects in the scene.
        It is not meant to be instantiated."""

    o: vec2  # origin (center of mass)
    R: vec2  # rotation (cosine/sine pair)
    v: vec2  # linear velocity
    ω: float  # angular velocity
    m: float  # mass
    I: float  # moment of inertia
    size: float  # collision detection radius
    color: vec3

    sdf_map: np.ndarray
    position_map: np.ndarray
    grad_map: np.ndarray
    map_size: float
    lattice_size: float

    def __init__(self, o, R=vec2(1, 0), v=vec2(0, 0), ω=0, m=1, I=1, size=1):
        pass

    # convert a point from voxel space to world space
    def to_world(vec2):
        pass

    def collide_sdf(self, object, itx):
        pass

    def update(self, dt):
        pass

# returns (is_collision, collision_data)


# @ti.dataclass
class Mesh_shape():
    o: vec2  # origin (center of mass)
    R: vec2  # rotation (cosine/sine pair)
    v: vec2  # linear velocity
    ω: float  # angular velocity
    m: float  # mass
    I: float  # moment of inertia
    size: float  # collision detection radius
    color: vec3

    sdf_map: np.ndarray
    position_map: np.ndarray
    grad_map: np.ndarray
    map_size: float
    lattice_size: float

    mesh: trimesh.base.Trimesh
    mesh_path: str

    def __init__(self, mesh_path, o=vec2(0, 0), R=vec2(1, 0), v=vec2(0, 0), ω=0, m=1, I=1, scale=1, color=vec3(1, 1, 1)):
        self.mesh_path = mesh_path

        self.o = o
        self.R = R
        self.v = v
        self.ω = ω
        self.m = m
        self.I = I
        self.size = scale
        self.color = color

        self.mesh = None
        self.sdf_map = None
        self.position_map = None
        self.grad_map = None
        self.map_size = None
        self.lattice_size = None
        self.initialize_mesh()

    def initialize_mesh(self):
        self.map_size = self.size * 4
        self.lattice_size = self.map_size / (TOTAL_RESOLUTION - 1)
        self.sdf_map, self.grad_map, self.position_map, self.mesh = load_mesh(self.mesh_path, scale=self.size, resolution=TOTAL_RESOLUTION, voxel_range=self.map_size)

    @ti.func
    def to_world(self, vec2):
        return to_world(self.o, self.ω, vec2)

    @ti.func
    def to_local(self, vec2):
        return to_local(self.o, self.ω, vec2)

    @ti.func
    def collide(self, other):

        # initialize query points
        num = 20
        larger_size = max(self.size, other.size)
        query_points = generate_points_on_bisector(self.o, other.o, larger_size, num)
        # initialize possible point array
        isCollide = np.ones(num)

        # transform query points to self local space
        query_points_local_self = vec2.field(shape=(num,))
        for i in range(0, num):
            query_points_local_self[i] = self.to_local(query_points[i])

        # construct self boundary in both self local and global space
        self_boundary_local = vec2.field(shape=(num,))
        self_boundary_global = vec2.field(shape=(num,))
        self_resolution = self.sdf_map.shape[0]
        for i in range(0, num):
            # self_boundary_local[i] = self.sdf_map.sample(query_points_local_self[i])
            idx_x = int((query_points_local_self[i][0]-self.map_size/2)/self.lattice_size)
            idx_y = int((query_points_local_self[i][1]-self.map_size/2)/self.lattice_size)
            if idx_x < 0 or idx_x >= self_resolution or idx_y < 0 or idx_y >= self_resolution:
                self_boundary_local[i][0] = 0
                self_boundary_local[i][1] = 0
                isCollide[i] = 0
            else:
                self_boundary_local[i][0] = self.position_map[idx_x, idx_y, 0]
                self_boundary_local[i][1] = self.position_map[idx_x, idx_y, 1]
            self_boundary_global[i] = self.to_world(self_boundary_local[i])

        # test each bpundary point in other local space
        self_boundary_in_other_local = vec2.field(shape=(num,))
        other_resolution = other.sdf_map.shape[0]
        count = 0
        indices = np.zeros([num, 2])
        for i in range(0, num):
            if isCollide[i] == 0:
                continue
            self_boundary_in_other_local[i] = other.to_local(self_boundary_global[i])
            idx_x = int((self_boundary_in_other_local[i][0]-other.map_size/2)/other.lattice_size)
            idx_y = int((self_boundary_in_other_local[i][1]-other.map_size/2)/other.lattice_size)
            if idx_x < 0 or idx_x >= other_resolution or idx_y < 0 or idx_y >= other_resolution:
                isCollide[i] = 0
            else:
                if other.sdf_map[idx_x, idx_y] > DETECT_THRESHOLD:
                    isCollide[i] = 0
                else:
                    indices[i, 0] = idx_x
                    indices[i, 1] = idx_y
                    isCollide[i] = 1
                    count += 1
        cols = collideInfo.field(shape=(count,))
        for i in range(0, num):
            if isCollide[i] == 1:
                p1 = self_boundary_local[i]
                r1 = self_boundary_global[i] - self.o
                r2 = self_boundary_global[i] - other.o
                n1 = other.grad_map[indices[i, 0], indices[i, 1]]
                sep = - other.sdf_map[indices[i, 0], indices[i, 1]]
                cols[count-1] = collideInfo(p1, r1, r2, n1, sep)
                count -= 1
        return cols
        # raise NotImplementedError
