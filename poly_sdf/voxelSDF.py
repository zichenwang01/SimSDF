from mesh_to_sdf import mesh_to_voxels, sample_sdf_near_surface,scale_to_unit_cube

import trimesh
import skimage
import sklearn
import numpy as np
import pyrender
import matplotlib.pyplot as plt
import mesh_to_sdf

mesh = trimesh.load('data/woody-full.obj')

mesh = scale_to_unit_cube(mesh)

res = 128

# create an uniform array of query points between -2 and +2
query_points_x = np.linspace(-2.0, 2.0, res)
query_points_y = np.linspace(-2.0, 2.0, res)

query_points = np.meshgrid(query_points_x, query_points_y)

print(query_points)

# stack into 3d points and append 0 for z dimension
query_points = np.stack(query_points, axis=2)
print(query_points)

query_points = np.append(query_points, np.zeros_like(query_points[:, :, :1]), axis=2)

# reshape to a list of 3d coordinates
query_points = query_points.reshape(-1, 3)

print(query_points)


# evaluate the signed distance function at the query points

voxel = mesh_to_sdf.mesh_to_sdf(mesh, query_points, surface_point_method='scan', sign_method='depth', bounding_radius=None, scan_count=100, scan_resolution=400, sample_point_count=10000000, normal_sample_count=11)

# reshape to image
voxel = voxel.reshape(res, res)

print(voxel)

# visualize but flip y axis since image origin is in the top left corner
plt.imshow(np.flip(voxel, axis=0))

plt.show()



# vertices, faces, normals, _ = skimage.measure.marching_cubes(voxels, level=0)
# mesh = trimesh.Trimesh(vertices=vertices, faces=faces, vertex_normals=normals)
# mesh.show()