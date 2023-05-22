from mesh_to_sdf import mesh_to_voxels, sample_sdf_near_surface

import trimesh
import numpy as np
import matplotlib.pyplot as plt
import mesh_to_sdf


def scale_to_cube(mesh, scale=1.0):
    if isinstance(mesh, trimesh.Scene):
        mesh = mesh.dump().sum()

    vertices = mesh.vertices - mesh.bounding_box.centroid
    vertices *= scale * 2 / np.max(mesh.bounding_box.extents)

    return trimesh.Trimesh(vertices=vertices, faces=mesh.faces)


def load_mesh(path, scale=1.0, resolution=512, voxel_range=4):
    mesh = trimesh.load(path)
    mesh = scale_to_cube(mesh, scale=scale)

    # define the resolution and size of the voxel grid (the size is total size of the grid in all dimensions)
    res = resolution

    size_range_x = voxel_range
    size_range_y = voxel_range

    lattice_x = size_range_x / (res - 1)
    lattice_y = size_range_y / (res - 1)
    ha_x = size_range_x / 2 + lattice_x
    ha_y = size_range_y / 2 + lattice_y
    # create an uniform array of query points between -2 and +2
    query_points_x = np.linspace(-ha_x, ha_x, res+2)
    query_points_y = np.linspace(-ha_y, ha_y, res+2)

    query_points = np.meshgrid(query_points_x, query_points_y)

    # stack into 3d points and append 0 for z dimension
    query_points = np.stack(query_points, axis=2)
    query_points = np.append(query_points, np.zeros_like(query_points[:, :, :1]), axis=2)

    # reshape to a list of 3d coordinates
    query_points = query_points.reshape(-1, 3)

    # calculate sdf
    voxel = mesh_to_sdf.mesh_to_sdf(mesh, query_points, surface_point_method='scan', sign_method='depth', bounding_radius=None,
                                    scan_count=100, scan_resolution=400, sample_point_count=10000000, normal_sample_count=11)
    # reshape to image
    voxel = voxel.reshape(res+2, res+2)

    voxel_xy = voxel.transpose()
    grad = np.gradient(voxel_xy)

    grad_arr = np.stack(grad, axis=-1)
    grad_arr = grad_arr[1:-1, 1:-1]

    # Compute the magnitude of the gradient
    grad_mag = np.sqrt(np.sum(grad_arr**2, axis=-1))

    # Normalize the gradient by dividing by the magnitude
    norm_grad = grad_arr / grad_mag[..., None]

    # Replace any NaNs that might have resulted from division by zero
    norm_grad = np.nan_to_num(norm_grad)

    position_map = np.zeros([res, res, 2])
    # position_map.shape
    for x in range(0, res):
        for y in range(0, res):
            ref_x = - size_range_x / 2 + x * lattice_x
            ref_y = - size_range_y / 2 + y * lattice_y
            point_to_x = ref_x - norm_grad[x, y, 0] * voxel_xy[x+1, y+1]
            point_to_y = ref_y - norm_grad[x, y, 1] * voxel_xy[x+1, y+1]
            position_map[x, y, 0] = point_to_x
            position_map[x, y, 1] = point_to_y

    # volxe_xy contains the sdf values, index 0 is x, index 1 is y start from small to large
    # position_map contains the position of the point to the surface, index 0 is x, index 1 is y
    return voxel_xy, norm_grad, position_map, mesh


# voxel_xy, position_map = load_mesh('data/rect.obj', scale=1.0, resolution=512, voxel_range=4.0)
# plt.imshow(voxel_xy)
# plt.show()
# plt.imshow(position_map[:, :, 0])
# plt.show()
# plt.imshow(position_map[:, :, 1])
# plt.show()
