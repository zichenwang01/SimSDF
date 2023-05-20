from util import * 
from scene import Scene

@ti.data_oriented
class GUI:
    
    def __init__(self, width=1024, height=1024):
        self.width = width
        self.height = height
    
    def start(self):
        """Start the GUI"""
        self.window = ti.ui.Window("SimSDF", (self.width, self.width))
        self.canvas = self.window.get_canvas()
    
    def is_running(self):
        return self.window.running
    
    def draw(self, scene):
        self.canvas.triangles(vertices=scene.vertices, indices=scene.triangles, color=(1,1,1))