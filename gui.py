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
        # print(scene.positions)
        self.canvas.circles(scene.positions, radius=1.0/self.width, color=(0.5,0.5,0.5))
        # self.canvas.circles(self.grid, radius=1.0/self.width, color=self.color)