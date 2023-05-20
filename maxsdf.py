import numpy as np 
import matplotlib.pyplot as plt

def sdf1(x):
    return np.linalg.norm(x - np.array([0.35, 0.5]), axis=1) - 0.2 

def sdf2(x):
    return np.linalg.norm(x - np.array([0.65, 0.5]), axis=1) - 0.2 

def sdf_min(x):
    return np.minimum(sdf1(x), sdf2(x))

def sdf_max(x):
    return np.maximum(sdf1(x), sdf2(x))

def gradient(x):
    eps = 1e-4
    dx = (sdf_max(x + np.array([eps, 0])) - sdf_max(x - np.array([eps, 0]))) / (2 * eps)
    dy = (sdf_max(x + np.array([0, eps])) - sdf_max(x - np.array([0, eps]))) / (2 * eps)
    return np.stack([dx, dy], axis=1)

x_range = np.linspace(0, 1, 100)
y_range = np.linspace(0, 1, 100)
x, y = np.meshgrid(x_range, y_range)

x = x.flatten()
y = y.flatten()
xy = np.stack([x, y], axis=1)
sdf = sdf_max(xy)

plt.title('Max SDF')
plt.xlabel('x')
plt.ylabel('y')
plt.xlim(0, 1)
plt.ylim(0, 1)

# plot the zero level curve
contours = plt.contour(x_range, y_range, sdf.reshape(100, 100), levels=[0])
plt.clabel(contours, inline=True, fontsize=8)

# plot the level curves
plt.contourf(x_range, y_range, sdf.reshape(100, 100))
plt.colorbar()

# plot the sdf
# plt.scatter(x, y, c=sdf)
# plt.colorbar()
# plt.show()

# gradient descent to the zero level curve
# p = np.array([[0.499, 0.,]])
# grad = gradient(p)
# step = 0.01
# while sdf_max(p) > 0:
#     p -= step * grad
#     grad = gradient(p)
#     print(p)
#     plt.scatter(p[0, 0], p[0, 1], c='r', s=2)

p = np.array([[0.499, 0.1,]])
plt.scatter(p[0, 0], p[0, 1], c='r', s=2)
grad = gradient(p)
p -= sdf_max(p) * grad
plt.scatter(p[0, 0], p[0, 1], c='r', s=2)
grad = gradient(p)
p -= sdf_max(p) * grad
plt.scatter(p[0, 0], p[0, 1], c='r', s=2)

plt.show()