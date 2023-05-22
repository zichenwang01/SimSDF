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
    
    def draw(self, scene, solver):
        self.canvas.triangles(vertices=scene.vertices, 
                              indices=scene.triangles, 
                              per_vertex_color=scene.colors)
        if solver.num_collide[None] > 0:
            self.canvas.circles(centers=solver.collisions.p1,
                                radius=0.005,
                                color=(1, 0, 0))
        
        