import matplotlib.pyplot as plt
import numpy as np


class BSpline:
    def __init__(self, degree, knot_vector, weights, control_points):
        if len(knot_vector) != len(weights) + degree + 1:
            raise Exception('m != n + p + 1')
        if len(control_points) != len(weights):
            raise Exception('Length of weights must be equal to length of control points vector!')
        self.degree = degree
        self.knot_vector = np.array(knot_vector)
        self.weights = np.array(weights)
        self.control_points = np.array(control_points)
        for p in self.control_points:
            p = np.array(p)

    def b_spline_basis_function(self, i, p, u):
        res = 0
        if p == 0:
            return 1 if self.knot_vector[i] <= u < self.knot_vector[i + 1] else 0
        if self.knot_vector[i + p] - self.knot_vector[i] != 0:
            res += (u - self.knot_vector[i]) / (
                    self.knot_vector[i + p] - self.knot_vector[i]) * self.b_spline_basis_function(i, p - 1, u)
        if self.knot_vector[i + p + 1] - self.knot_vector[i + 1] != 0:
            res += (self.knot_vector[i + p + 1] - u) / (
                    self.knot_vector[i + p + 1] - self.knot_vector[i + 1]) * self.b_spline_basis_function(i + 1,
                                                                                                          p - 1, u)
        return res

    def nurbs_basis_function(self, i, u):
        return (self.b_spline_basis_function(i, self.degree, u) * self.weights[i]) / \
               sum([self.b_spline_basis_function(j, self.degree, u) * self.weights[j] for j in
                    range(len(self.weights))])

    def nurbs_curve(self, u):
        return np.sum([self.nurbs_basis_function(i, u) * self.control_points[i] for i in range(len(self.weights))],axis=0)

    def plot(self):
        x = np.arange(0, 1, step=0.01)
        y = [[self.nurbs_basis_function(i, x_) for x_ in x] for i in range(len(self.weights))]
        for y_ in y:
            plt.plot(x, y_)
        plt.show()
        points = [self.nurbs_curve(x_) for x_ in x]
        x = []
        y = []
        for point in points:
            x.append(point[0])
            y.append(point[1])
        plt.plot(x, y)
        plt.axis('equal')
        plt.show()


if __name__ == '__main__':
    points = [
        [0, 0],
        [1, 1],
        [2, 10],
        [3, -10],
        [4, 3],
        [5, 7],
        [6, 7],
    ]
    spline = BSpline(3, [0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1], [1, 1, 1, 1, 1, 1, 1], points)
    spline.plot()
