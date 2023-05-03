from util import * 

@ti.data_oriented
class GUI:
    
    def __init__(self, scene, width=800, height=800):
        self.width = width
        self.height = height
        self.grid = ti.Vector.field(2, shape=(width, height), dtype=ti.float32)
        # self.sdf = ti.field(dtype=ti.float32)
    
    def start(self):
        """Start the GUI"""
        self.window = ti.ui.Window("SimSDF", (self.width, self.width))
        self.canvas = self.window.get_canvas()
    
    def is_running(self):
        return self.window.running
    
    def draw(self, scene):
        self.canvas.circles(self.grid, radius=0.1, color=(1,0,0))
        # self.canvas.circles(scene.spheres[0].o, radius=scene.spheres[0].r, color=(1,0,1))
