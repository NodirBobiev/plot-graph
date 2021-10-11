"""
  _____ (x, y)
 V
 .____________
 |           |   |
 | Rectangle |  height
 |___________|   |
  -- width --

"""

class Rectangle:
    def __init__(self, x, y, width, height):
        self._x, self._y, self._width, self._height = x, y, width, height

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_center_x(self):
        return self._x + self._width / 2

    def get_center_y(self):
        return self._y + self._height / 2

    def get_center(self):
        return [self.get_center_x(), self.get_center_y()]

    def set_width(self, new_width):
        self._width = new_width

    def set_height(self, new_height):
        self._height = new_height

    def set_x(self, new_x):
        self._x = new_x

    def set_y(self, new_y):
        self._y = new_y

    def set_pos(self, new_pos):
        self.set_x(new_pos[0])
        self.set_y(new_pos[1])

    def set_center_x(self, new_x):
        self._x = new_x - self._width / 2

    def set_center_y(self, new_y):
        self._y = new_y - self._height / 2

    def set_center(self, new_pos):
        self.set_center_x(new_pos[0])
        self.set_center_y(new_pos[1])
