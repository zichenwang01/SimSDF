from util import * 
from gui import GUI
from scene import Scene
from collision import CollisionSolver

scene = Scene(dt=1e-1)
scene.add_sphere(o=vec2(0.2,0.5), r=0.05, m=1, v=vec2(0.1,0))
scene.add_sphere(o=vec2(0.8,0.5), r=0.05, m=1, v=vec2(-0.1,0))

# # check spheres
# print(scene.num_sphere[None])
# for i in range(scene.num_sphere[None]):
#     print(scene.spheres[i].o, scene.spheres[i].r, scene.spheres[i].m)

# # check vertices
# scene.update_vertices()
# print(scene.num_v[None])
# for i in range(scene.num_v[None]):
#     print(scene.vertices[i])

# # check triangles
# print(scene.num_tri[None])
# for i in range(scene.num_tri[None]):
#     print(scene.triangles[3*i], scene.triangles[3*i+1], scene.triangles[3*i+2])

gui = GUI()

collision = CollisionSolver(scene,0.5,0,0)

gui.start()
while gui.is_running():
    for i in range(num_step):
        collision.clearContact()
        collision.collision_detection()
        collision.PGS()
        collision.apply_impulses()
        scene.update()
    
    scene.update_vertices()
    gui.draw(scene)
    gui.window.show()