from typing import Tuple

import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def get_raw_pts(n_in_row: int) -> np.ndarray:
    assert n_in_row > 6
    result = get_pts_in_octant(n_in_row)
    result = np.append(result, result.dot(np.array([[-1, 0, 0], [0, 1, 0], [0, 0, 1]])), 0)
    result = np.append(result, result.dot(np.array([[1, 0, 0], [0, -1, 0], [0, 0, 1]])), 0)
    result = np.append(result, result.dot(np.array([[1, 0, 0], [0, 1, 0], [0, 0, -1]])), 0)
    indices = get_indices(n_in_row)
    result = result[indices]
    return result


def get_pts_in_octant(n_in_row: int) -> np.ndarray:
    a1 = 9e-1
    a2 = 9e-1
    a3 = 9e-1
    u = np.linspace(0, np.pi / 2, n_in_row)
    v = np.linspace(0, np.pi / 2, n_in_row)
    x = a1 * np.outer(np.cos(u), np.sin(v))
    y = a2 * np.outer(np.sin(u), np.sin(v))
    z = a3 * np.outer(np.ones(np.size(u)), np.cos(v))
    x = x.reshape(n_in_row ** 2)
    y = y.reshape(n_in_row ** 2)
    z = z.reshape(n_in_row ** 2)
    res = np.array(list(zip(x, y, z)))
    res = np.unique(res.round(decimals=5), axis=0)
    sort_ind = np.lexsort((res[:, 0], res[:, 1], -res[:, 2]))
    res = res[sort_ind]
    return res


def get_pts(n_in_row: int) -> np.ndarray:
    pts = get_raw_pts(n_in_row)
    pts = pts.reshape((pts.shape[0] * pts.shape[1] // 9, 3, 3))
    pts = add_normals(pts)
    pts = pts[pts[:, 2] < 0.7]
    return pts.reshape(pts.shape[0] * pts.shape[1])


def add_normals(triangles: np.ndarray) -> np.ndarray:
    result = []
    for idx, triangle in enumerate(triangles):
        a = triangle[0]
        b = triangle[1]
        c = triangle[2]
        x = b - a
        y = c - a
        if a[0]*a[1]*a[2] == 0 \
                and b[0]*b[1]*b[2] == 0 \
                and c[0]*c[1]*c[2] == 0:
            for _ in range(3):
                result.append(-np.cross(x, y))
        elif a[0]*a[1]*a[2]>=0 and c[0]*c[1]*c[2] >= 0:
            for _ in range(3):
                result.append(np.cross(x, y))
        else:
            for _ in range(3):
                result.append(-np.cross(x, y))
    result = normalize(np.array(result))
    triangles = triangles.reshape((triangles.shape[0] * triangles.shape[1], triangles.shape[2]))
    return np.append(triangles, result, 1)


def normalize(vectors: np.array) -> np.array:
    eps = 1e-10
    for i, vec in enumerate(vectors):
        vectors[i] = vec/(np.linalg.norm(vec)+eps)
    return vectors


def get_indices(n_in_row: int) -> np.ndarray:
    indices = []
    for i in range(1, n_in_row):
        indices.append(0)
        indices.append(i)
        indices.append(i + 1)
    for i in range(1, n_in_row - 1):
        for j in range(1, n_in_row):
            indices.extend([(i - 1) * n_in_row + j, i * n_in_row + j, i * n_in_row + j + 1])
            indices.extend([(i - 1) * n_in_row + j, i * n_in_row + j + 1, (i - 1) * n_in_row + j + 1])
    indices = np.array(indices)
    octant_increment = indices.max()
    for i in range(3):
        indices = np.append(indices, indices + octant_increment + 1)
        octant_increment = indices.max()
    return indices


if __name__ == '__main__':
    matplotlib.use('Qt5Agg')
    n_in_row = 7

    pts = get_pts(n_in_row)
    print(pts.reshape((pts.shape[0] // 6, 6))[0:20])
    pts = pts.reshape((pts.shape[0] // 6, 6))[:,  0:3]
    pts = pts.reshape((np.prod(pts.shape)))[0:100]
    # print(get_indices(n_in_row).reshape((50688//3,3))[0:150])

    # print(pts.shape)
    # for i in range(0, len(pts), 3):
    #     print(f"{round(pts[i], 2):5} {round(pts[i + 1], 2): 5} {round(pts[i + 2], 2): 5}")
    # fig = plt.figure()
    # ax = plt.axes(projection='3d')
    # stop_ind = len(pts) // 3
    # # ax.scatter(pts[0:stop_ind * 3:3], pts[1:stop_ind * 3:3], pts[2:stop_ind * 3:3], 'b')
    # for i in range(0, stop_ind * 3, 3):  # plot each point + it's index as text above
    #     ax.scatter(pts[i], pts[i + 1], pts[i + 2], color='b')
    #     ax.text(pts[i + 0], pts[i + 1], pts[i + 2], '%s' % (str(i // 3)), size=10, zorder=1,
    #             color='k')
    #     # if i % 2 == 0:
    #     #     ax.plot([pts[i], pts[i+3]], [pts[i + 1], pts[i + 4]], [pts[i + 2], pts[i + 5]])
    # plt.show()
