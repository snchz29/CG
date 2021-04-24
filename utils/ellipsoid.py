from typing import List, Tuple

import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def get_pts(n_in_row: int) -> np.ndarray:
    assert n_in_row > 6
    result = get_pts_in_octant((1, 1, 1), n_in_row)
    result = np.append(result, get_pts_in_octant((1, 1, -1), n_in_row), 0)
    result = np.append(result, get_pts_in_octant((1, -1, 1), n_in_row), 0)
    result = np.append(result, get_pts_in_octant((1, -1, -1), n_in_row), 0)
    result = np.append(result, get_pts_in_octant((-1, 1, 1), n_in_row), 0)
    result = np.append(result, get_pts_in_octant((-1, 1, -1), n_in_row), 0)
    result = np.append(result, get_pts_in_octant((-1, -1, 1), n_in_row), 0)
    result = np.append(result, get_pts_in_octant((-1, -1, -1), n_in_row), 0)
    return result


def get_pts_in_octant(octant: Tuple[int], n_in_row: int) -> np.ndarray:
    a1 = 5e-1
    a2 = 5e-1
    a3 = 5e-1
    u = np.linspace(0, np.pi / 2, n_in_row)
    v = np.linspace(0, np.pi / 2, n_in_row)
    x = a1 * np.outer(np.cos(u), np.sin(v))
    y = a2 * np.outer(np.sin(u), np.sin(v))
    z = a3 * np.outer(np.ones(np.size(u)), np.cos(v))
    x = x.reshape(n_in_row ** 2)
    y = y.reshape(n_in_row ** 2)
    z = z.reshape(n_in_row ** 2)
    res = np.array(list(zip(x, y, z)))
    res = np.unique(res.round(decimals=2), axis=0)
    sort_ind = np.lexsort((res[:, 0], res[:, 1], -res[:, 2]))
    res = res[sort_ind]
    res[:, 0] = res[:, 0] * octant[0]
    res[:, 1] = res[:, 1] * octant[1]
    res[:, 2] = res[:, 2] * octant[2]
    shape = res.shape
    return res.reshape(shape[0] * shape[1])


def get_indices(n_in_row: int) -> np.ndarray:
    indices = []
    for i in range(1, n_in_row):
        indices.append(0)
        indices.append(i)
        indices.append(i + 1)
    for i in range(1, n_in_row - 1):
        indices.extend([(i - 1) * n_in_row + 1, i * n_in_row + 1, i * n_in_row + 2])
        for j in range(2, n_in_row):
            indices.extend([(i - 1) * n_in_row + j, i * n_in_row + j - 1, i * n_in_row + j])
            if j > 1:
                indices.extend([(i - 1) * n_in_row + j, i * n_in_row + j, i * n_in_row + j + 1])
        indices.extend([(i - 1) * n_in_row + n_in_row, i * n_in_row + n_in_row - 1, i * n_in_row + n_in_row])
    indices = np.array(indices)
    octant_increment = indices.max()
    for i in range(8):
        indices = np.append(indices, indices + octant_increment+1)
        octant_increment = indices.max()
    return indices


if __name__ == '__main__':
    matplotlib.use('Qt5Agg')
    n_in_row = 7
    pts = get_pts(n_in_row)
    print(get_indices(n_in_row)[0:400])

    # print(pts)
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
