from Vector2 import Vector2
import math
from Configuration import *


class NumericMethod:
    def __init__(self, cp_f, next_f, grid, n=None, iv: Vector2 = None):
        self.grid = grid
        self._n = n
        self._iv = iv
        self.compute_points = cp_f
        self.next_f = next_f
        self._points = []
        self.compute_points(self)
        self.hidden = False

    @property
    def n(self):
        return self._n

    @property
    def iv(self):
        return self._iv

    @n.setter
    def n(self, new_n):
        self._n = new_n
        self.compute_points(self)

    @iv.setter
    def iv(self, new_value: Vector2):
        self._iv = new_value

    def get_points(self):
        if self.hidden:
            return []
        return self._points

    def compute_points(self):
        pass

    def next_f(self):
        pass


def exact_cp(self):
    self._points = []
    h = (self.grid.final_x - self.grid.start_x) / (self.n - 1)
    for i in range(self.n):
        y = exact_f(self.grid.start_x + h * i)
        if self.grid.start_x + h * i < 0 <= self.grid.start_x + h * (i + 1):
            self._points.append(Vector2(self.grid.start_x + h * i, None))
        else:
            self._points.append(Vector2(self.grid.start_x + h * i, y))


def compute_points(self):
    self._points = []
    if self.grid.final_x < self.iv.x or self.grid.xn <= self.grid.x0 or self.n <= 1:
        return
    h = (self.grid.xn - self.grid.x0) / (self.n - 1)
    point = Vector2(self.iv.x, self.iv.y)
    num_points = int((self.grid.final_x - self.iv.x) / h) + 2
    for i in range(num_points):
        if point.x >= self.grid.start_x or point.x < self.grid.start_x <= point.x + h:
            self._points.append(point)
        point = self.next_f(point, h)
        if point is None:
            break


def euler_f(point, h):
    f_val = y_prime(point.x, point.y)
    if f_val is None:
        return None
    return Vector2(point.x + h, point.y + h * f_val)


def imp_f(point, h):
    k_1_i = y_prime(point.x, point.y)
    if k_1_i is None:
        return None
    k_2_i = y_prime(point.x + h, point.y + h * k_1_i)
    if k_2_i is None:
        return None
    return Vector2(point.x + h, point.y + (h / 2) * (k_1_i + k_2_i))


def rk_f(point, h):
    k_1_i = y_prime(point.x, point.y)
    if k_1_i is None:
        return None
    k_2_i = y_prime(point.x + h / 2, point.y + h / 2 * k_1_i)
    if k_2_i is None:
        return None
    k_3_i = y_prime(point.x + h / 2, point.y + h / 2 * k_2_i)
    if k_3_i is None:
        return None
    k_4_i = y_prime(point.x + h, point.y + h * k_3_i)
    if k_4_i is None:
        return None
    return Vector2(point.x + h, point.y + (h / 6) * (k_1_i + 2 * k_2_i + 2 * k_3_i + k_4_i))


def local_error_cp(self):
    self._points = []
    if self.grid.final_x < self.iv.x or self.grid.xn <= self.grid.x0 or self.n <= 1:
        return
    h = (self.grid.xn - self.grid.x0) / (self.n - 1)
    point = Vector2(self.iv.x, self.iv.y)
    num_points = int((self.grid.final_x - self.iv.x) / h) + 2
    for i in range(num_points):
        if point.x >= self.grid.start_x or point.x < self.grid.start_x <= point.x + h:
            exact_val = exact_f(point.x)
            if exact_val is None:
                return
            self._points.append(Vector2(point.x, abs(exact_val - point.y)))
        point = self.next_f(point, h)
        if point is None:
            return


def global_error_cp(self):
    self._points = []
    st_x = max(2, int(self.grid.start_x))
    fl_x = int(self.grid.final_x) + 1
    if st_x >= fl_x or self.grid.xn <= self.grid.x0:
        return
    for n in range(st_x, fl_x + 1):
        h = (self.grid.xn - self.grid.x0) / (n - 1)
        point = Vector2(self.iv.x, self.iv.y)
        num_points = int((self.grid.xn - self.grid.x0) / h) + 2
        max_val = 0
        for i in range(num_points):
            if point.x >= self.grid.x0 or point.x < self.grid.xn <= point.x + h:
                exact_val = exact_f(point.x)
                if exact_val is None:
                    break
                max_val = max(max_val, abs(exact_val - point.y))
            point = self.next_f(point, h)
            if point is None:
                break
        self._points.append(Vector2(n, max_val))


def y_prime(x, y):
    if x == 0.0:
        return None
    return (3 * y + 2 * x * y) / (x ** 2)


def exact_f(x):
    if x == 0.0:
        return None
    return (x ** 2) * NUMBER_E ** min(31, -3 / x + 3)


def nothing_f(*args):
    pass
