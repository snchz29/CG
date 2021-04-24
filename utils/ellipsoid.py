import matplotlib.pyplot as plt
import numpy as np


def get_pts(n_pts: int) -> np.ndarray:
    a1 = 5e-1
    a2 = 5e-1
    a3 = 5e-1
    u = np.linspace(0, 2 * np.pi, n_pts)
    v = np.linspace(0, np.pi, n_pts)

    x = a1 * np.outer(np.cos(u), np.sin(v))
    y = a2 * np.outer(np.sin(u), np.sin(v))
    z = a3 * np.outer(np.ones(np.size(u)), np.cos(v))
    x = x.reshape(n_pts ** 2)
    y = y.reshape(n_pts ** 2)
    z = z.reshape(n_pts ** 2)
    res = np.array(list(zip(x, y, z)))
    sort_ind = np.lexsort((res[:, 0], res[:, 1], res[:, 2]))
    res = res[sort_ind]
    shape = res.shape
    return res.reshape(shape[0] * shape[1])


def get_indices(n_pts):
    indices = [0, 1, 2, 1, 2, 3, ]
    cur_z_ind = 4
    while cur_z_ind < n_pts//3:
        indices.append(cur_z_ind - 4)
        indices.append(cur_z_ind - 2)
        indices.append(cur_z_ind - 0)
        cur_z_ind += 1
    return indices


if __name__ == '__main__':
    pts = get_pts(6)
    for i in range(0, len(pts), 3):
        print(f"{round(pts[i], 2):5} {round(pts[i + 1], 2): 5} {round(pts[i + 2], 2): 5}")
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    stop_ind = len(pts) // 3
    ax.scatter(pts[0:stop_ind * 3:3], pts[1:stop_ind * 3:3], pts[2:stop_ind * 3:3], 'b')
    for i in range(99, stop_ind * 3, 3):  # plot each point + it's index as text above
        ax.scatter(pts[i], pts[i + 1], pts[i + 2], color='b')
        ax.text(pts[i + 0], pts[i + 1], pts[i + 2], '%s' % (str(i // 3)), size=10, zorder=1,
                color='k')
    plt.show()

    print(get_indices(len(pts)))
