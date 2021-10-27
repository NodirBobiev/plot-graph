class Vector2:
    def __init__(self, x: float, y: float):
        self._x = x
        self._y = y

    def __str__(self):
        return f"<class 'Vector2'<->(x={self.x}, y={self.y})>"

    def __eq__(self, vector):
        return self.x == vector.x and self.y == vector.y

    def __sub__(self, vector):
        return Vector2(self.x - vector.x, self.y - vector.y)

    def __add__(self, vector):
        return Vector2(self.x + vector.x, self.y + vector.y)

    def __mul__(self, scalar: float):
        return Vector2(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar: float):
        return Vector2(self.x / scalar, self.y / scalar)

    def __floordiv__(self, scalar: float):
        return Vector2(self.x // scalar, self.y // scalar)

    def copy(self):
        return Vector2(self.x, self.y)

    @classmethod
    def zero(cls):
        return Vector2(0.0, 0.0)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @x.setter
    def x(self, new_x):
        self._x = new_x

    @y.setter
    def y(self, new_y):
        self._y = new_y

    def get_sqr_magnitude(self):
        return self.x ** 2 + self.y ** 2

    def get_magnitude(self):
        return self.get_sqr_magnitude() ** 0.5

    def get_dist_to(self, vct):
        return (self - vct).get_magnitude()

    def get_squared_dist_to(self, vct):
        return (self - vct).get_sqr_magnitude()

    def get_normalized(self):
        return self / self.get_magnitude()
