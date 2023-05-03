from util import * 
from scene import Scene

@ti.data_oriented
class GUI:
    
    def __init__(self, scene, width=1024, height=1024):
        self.scene = scene
        self.width = width
        self.height = height
        
        # self.partciles = ti.Vector.field(2, shape=(width * height,), dtype=ti.f32)
        # for i, j in ti.ndrange(width, height):
        #     self.partciles[i * width + j] = vec2(i/width, j/height)
        # self.sdf = ti.field(dtype=ti.f32, shape=(width * height,))
        # self.color = ti.Vector.field(3, shape=(width * height,), dtype=ti.f32)
        
        # self.grid = ti.Vector.field(2, shape=(width  * height,), dtype=ti.f32)
        # for i, j in ti.ndrange(width, height):
        #     self.grid[i * width + j] = [i/width, j/height]
    
    def start(self):
        """Start the GUI"""
        self.window = ti.ui.Window("SimSDF", (self.width, self.width))
        self.canvas = self.window.get_canvas()
    
    def is_running(self):
        return self.window.running
    
    def draw(self, scene):
        self.canvas.circles(scene.sphere_pt, radius=1.0/self.width, color=(0.5,0.5,0.5))
        # self.canvas.circles(self.grid, radius=1.0/self.width, color=self.color)