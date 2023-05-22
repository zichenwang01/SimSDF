from shape import Mesh_shape
from util import *

rect1 = Mesh_shape('data/rect.obj', o=vec2(0, 0), R=vec2(1, 0), v=vec2(0, 0), ω=0, m=1, I=1, scale=1, color=vec3(1, 0, 0))
rect2 = Mesh_shape('data/rect.obj', o=vec2(1.6, 0), R=vec2(0.894427, 0.447214), v=vec2(0, 0), ω=0, m=1, I=1, scale=1, color=vec3(0, 1, 0))
print('loaded all')
col = rect1.collide(rect2)
print(col)
