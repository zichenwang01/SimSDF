from util import * 
from response import *
from shape import Shape, check_collision

@ti.data_oriented
class Scene:  
    def __init__(self, dt):
      self.num_shapes = ti.field(dtype=ti.i32, shape=())
      self.shapes = Shape.field(shape=(100,))
      self.response = CollisionResponse(self, Cr, β, μ)
      self.dt = dt
      self.collisions = ti.field(2, shape=(10000), dtype=ti.f32)
      self.num_collide = ti.field(dtype=ti.i32, shape=())
      
      # TODO add Shape class

    @ti.kernel
    def add_shape(self,shape):
      num_shapes = self.num_shapes[None]
      self.shapes[num_shapes] = shape
      ti.atomic_add(self.num_shapes[None],1)

    @ti.kernel
    def collision_detection(self):

      self.response.init_contact()

      for i in range(self.num_shapes[None]):
        for j in range(i + 1, self.num_shapes[None]):
            is_collision, collision_data = check_collision(self.shapes[i], self.shapes[j])
            if is_collision: 
              self.response.addContact(collision_data)
              #TODO add the point of collision
              self.collisions[self.num_collide[None]] = points
              ti.atomic_add(self.num_collide[None], 1)
      
      self.response.PGS()
      self.response.apply_impulses()

    @ti.kernel
    def update(self):
      for i in range(self.num_shapes[None]):
        self.shapes[i].update(dt)

    
              
            