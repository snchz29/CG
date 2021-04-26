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
    pts = pts[pts[:, 2] < 0.5]
    return pts.reshape(pts.shape[0] * pts.shape[1])


def add_normals(triangles: np.ndarray) -> np.ndarray:
    result = []
    for idx, triangle in enumerate(triangles):
        a = triangle[0]
        b = triangle[1]
        c = triangle[2]
        x = b - a
        y = c - a
        for _ in range(3):
            result.append(np.cross(x, y))
    result = normalize(np.array(result))
    triangles = triangles.reshape((triangles.shape[0] * triangles.shape[1], triangles.shape[2]))
    return np.append(triangles, result, 1)


def normalize(vectors: np.array) -> np.array:
    for i, vec in enumerate(vectors):
        vectors[i] = vec / abs(np.linalg.norm(vec))
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
        indices = np.append(indices, np.flip(indices, 0) + octant_increment + 1)
        octant_increment = indices.max()
    return indices
