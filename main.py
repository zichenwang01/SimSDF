from util import * 
from gui import GUI
from scene import Scene

scene = Scene(dt=1e-6)

scene.init()

gui = GUI(scene)

gui.start()
while gui.is_running():
    gui.draw(scene)
    gui.window.show()