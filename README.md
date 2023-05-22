# SimSDF: Physically-Based Simulation with Signed Distance Field

![Example Figure](./figures/max_sdf.png)

This repository contains an implementation for the CS5643 final project, coded by Zichen Wang, Xilai Dai, and Barry Lyu.

## Environment
The environment setup for this repository is fairly simple. Run  
```conda create sim-sdf ```  
```conda activate sim-sdf```  
```pip install numpy taichi matplot```

## Code Structure
Here is a breakdown of the repository to facilitate better comprehension of our codes. The repository contains many folders, and each folder presents a scene using a certain approach--  

Folders starting with `sphere` denote head-on collision experiment of two spheres;  
Folders starting with `many_spheres` denote a scene of many spheres.  
Folders ending with `gt` denote the ground truth using particle simulation;  
Folders ending with `mesh` denote the baseline using mesh to approximate the sphere;  
Folders ending with `sdf`denote our method using SDF.

Inside each folder, we have the following files--  
`main.py` is the primary entry pooint. It is also where the initial scene is delcared.  
`util.py` combines configures with common functions.  
`scene.py` contains the `Scene` class.  
`shape.py` contains the supported object classes. Refer to the `Object` class as an interface for all objects.  
 `gui.py` implements the GUI.  
 `maxsdf.py` generates the illustrative figure shown above.
