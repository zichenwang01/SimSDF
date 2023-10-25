import numpy as np 
import matplotlib.pyplot as plt

def sdf1(x):
    return np.linalg.norm(x - np.array([0.35, 0.5]), axis=1) - 0.2 

def sdf2(x):
    return np.linalg.norm(x - np.array([0.65, 0.5]), axis=1) - 0.2 

def sdf3(x):
    # the three vertices of the triangle
    p1 = np.array([0.49, 0.7])
    p2 = np.array([0.55, 0.4])
    p3 = np.array([0.3, 0.4])

    # the three edges of the triangle
    e1 = p2 - p1
    e2 = p3 - p2
    e3 = p1 - p3

    # the three normals of the triangle
    n1 = np.array([e1[1], -e1[0]])
    n2 = np.array([e2[1], -e2[0]])
    n3 = np.array([e3[1], -e3[0]])

    # the three distances to the edges
    d1 = np.dot(x - p1, n1) / np.linalg.norm(n1)
    d2 = np.dot(x - p2, n2) / np.linalg.norm(n2)
    d3 = np.dot(x - p3, n3) / np.linalg.norm(n3)

    # the three distances to the vertices
    d4 = np.linalg.norm(x - p1, axis=1)
    d5 = np.linalg.norm(x - p2, axis=1)
    d6 = np.linalg.norm(x - p3, axis=1)

    # the sdf is the minimum of the three distances
    return -np.minimum(np.minimum(np.minimum(d1, d2), np.minimum(d3, d4)), np.minimum(d5, d6))

def sdf4(x):
    # the three vertices of the triangle
    p1 = np.array([0.51, 0.7])
    p2 = np.array([0.7, 0.4])
    p3 = np.array([0.45, 0.4])

    # the three edges of the triangle
    e1 = p2 - p1
    e2 = p3 - p2
    e3 = p1 - p3

    # the three normals of the triangle
    n1 = np.array([e1[1], -e1[0]])
    n2 = np.array([e2[1], -e2[0]])
    n3 = np.array([e3[1], -e3[0]])

    # the three distances to the edges
    d1 = np.dot(x - p1, n1) / np.linalg.norm(n1)
    d2 = np.dot(x - p2, n2) / np.linalg.norm(n2)
    d3 = np.dot(x - p3, n3) / np.linalg.norm(n3)

    # the three distances to the vertices
    d4 = np.linalg.norm(x - p1, axis=1)
    d5 = np.linalg.norm(x - p2, axis=1)
    d6 = np.linalg.norm(x - p3, axis=1)

    # the sdf is the minimum of the three distances
    return -np.minimum(np.minimum(np.minimum(d1, d2), np.minimum(d3, d4)), np.minimum(d5, d6))

def sdf_min(x):
    return np.minimum(sdf1(x), sdf2(x))

def sdf_max(x):
    return np.maximum(sdf4(x), sdf3(x))

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

fig, ax = plt.subplots()
plt.title('Gradient Descent to the Contact Region')
plt.xlabel('x')
plt.ylabel('y')
plt.xlim(0, 1)
plt.ylim(0, 1)

# plot the zero level curve
contours = plt.contour(x_range, y_range, sdf.reshape(100, 100), levels=[0], colors = 'white')
plt.clabel(contours, inline=True, fontsize=10,)

# plot the level curves
plt.contourf(x_range, y_range, sdf.reshape(100, 100))
plt.colorbar()

# plot the sdf
# plt.scatter(x, y, c=sdf)
# plt.colorbar()
# plt.show()
# exit(0)

# gradient descent to the zero level curve
# p = np.array([[0.499, 0.,]])
# grad = gradient(p)
# step = 0.01
# while sdf_max(p) > 0:
#     p -= step * grad
#     grad = gradient(p)
#     print(p)
#     plt.scatter(p[0, 0], p[0, 1], c='r', s=2)

# plot the circles
# circle1 = plt.Circle((0.35,0.5), 0.2, color='black', fill=False, linestyle='--')
# circle2 = plt.Circle((0.65,0.5), 0.2, color='black', fill=False, linestyle='--')
# ax.add_artist(circle1)
# ax.add_artist(circle2)

# plot the triangles
triangle1 = plt.Polygon(np.array([[0.51, 0.7], [0.7, 0.4], [0.49, 0.4]]), color='black', fill=False, linestyle='--')
triangle2 = plt.Polygon(np.array([[0.49, 0.7], [0.51, 0.4], [0.3, 0.4]]), color='black', fill=False, linestyle='--')
ax.add_artist(triangle1)
ax.add_artist(triangle2)
plt.show()
exit(0)

# plot the gradient descent points
p = np.array([[0.499, 0.1,]])
plt.scatter(p[0, 0], p[0, 1], c='r', s=5)
grad = gradient(p)
plt.arrow(p[0, 0], p[0, 1], -grad[0, 0] * 0.22, -grad[0, 1] * 0.22, length_includes_head=True, head_length=0.02, head_width=0.01, color='r')

p -= sdf_max(p) * grad
plt.scatter(p[0, 0], p[0, 1], c='r', s=5)
grad = gradient(p)
plt.arrow(p[0, 0], p[0, 1], -grad[0, 0] * 0.09, -grad[0, 1] * 0.09, length_includes_head=True, head_length=0.02, head_width=0.01, color='r')

p -= sdf_max(p) * grad
plt.scatter(p[0, 0], p[0, 1], c='r', s=5)

plt.show()