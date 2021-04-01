import numpy as np


class BSpline:
    def __init__(self, degree, knot_vector, weights, control_points):
        if len(knot_vector) != len(weights) + degree + 1:
            raise Exception('m != n + p + 1')
        if len(control_points) != len(weights):
            raise Exception('Length of weights must be equal to length of control points vector!')
        self._degree = degree
        self._knot_vector = np.array(knot_vector)
        self._weights = np.array(weights)
        self._control_points = np.array([np.array(list(point)) for point in control_points])
        self._cache = {}

    def _b_spline_basis_function(self, i, p, u):
        if (i, p, u) in self._cache:
            return self._cache.get((i, p, u))
        res = 0
        if p == 0:
            return 1 if self._knot_vector[i] <= u < self._knot_vector[i + 1] else 0
        if self._knot_vector[i + p] - self._knot_vector[i] != 0:
            res += (u - self._knot_vector[i]) / (
                    self._knot_vector[i + p] - self._knot_vector[i]) * self._b_spline_basis_function(i, p - 1, u)
        if self._knot_vector[i + p + 1] - self._knot_vector[i + 1] != 0:
            res += (self._knot_vector[i + p + 1] - u) / (
                    self._knot_vector[i + p + 1] - self._knot_vector[i + 1]) * self._b_spline_basis_function(i + 1,
                                                                                                             p - 1, u)
        self._cache[(i, p, u)] = res
        return res


class NURBSpline3deg6points(BSpline):
    def __init__(self, points):
        assert len(points) == 6
        super().__init__(3, [i / 9 for i in range(10)], [point.get_weight() for point in points],
                         [point.get_coordinates().values() for point in points])

    def _nurbs_basis_function(self, i, u):
        denominator = sum([self._b_spline_basis_function(j, self._degree, u) * self._weights[j] for j in
                           range(len(self._weights))])
        if denominator == 0.:
            denominator = 1e-3
        return (self._b_spline_basis_function(i, self._degree, u) * self._weights[i]) / denominator

    def _nurbs_curve(self, u):
        return np.sum([self._nurbs_basis_function(i, u) * self._control_points[i] for i in range(len(self._weights))],
                      axis=0)

    def get_nurbs_curve_points(self):
        x = np.arange(0, 1, step=0.01)
        return [self._nurbs_curve(i) for i in x][1:]

    def set_points(self, points):
        self._control_points = np.array([np.array(list(point.get_coordinates().values())) for point in points])
        self._weights = np.array([point.get_weight() for point in points])
