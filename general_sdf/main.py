from util import * 
from gui import GUI
from scene import Scene
from collision import CollisionSolver

Cr = 0.5
β = 0.5
μ = 0

scene = Scene(dt=1e-1)
scene.add_sphere(o=vec2(0.2,0.5), r=0.05, m=1, v=vec2(0.1,0))
scene.add_sphere(o=vec2(0.8,0.5), r=0.05, m=1, v=vec2(-0.1,0))

solver = CollisionSolver(scene, Cr, β, μ)

gui = GUI()

gui.start()
while gui.is_running():
    for i in range(num_step):
        scene.collision_detection()
        scene.update()
    
    scene.update_vertices()
    gui.draw(scene, solver)
    gui.window.show()