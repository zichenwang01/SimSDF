from util import * 
from gui import GUI
from scene import Scene

scene = Scene(dt=1e-1)

gui = GUI()

gui.start()
while gui.is_running():
    for i in range(num_step):
        scene.update()
    
    gui.draw(scene)
    gui.window.show()