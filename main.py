from util import * 
from gui import GUI
from scene import Scene

scene = Scene(dt=1e-1)
scene.add_sphere(o=vec2(0.5,0.5), r=0.02, m=1)

print(scene.spheres[0].r)

gui = GUI()

gui.start()
while gui.is_running():
    for i in range(num_step):
        scene.update()
    
    gui.draw(scene)
    gui.window.show()