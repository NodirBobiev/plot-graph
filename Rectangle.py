"""
  ,_____ (x, y)
 V
 .____________
 |           |   |
 | Rectangle |  height
 |___________|   |
  -- width --

"""
from Vector2 import Vector2


class Rectangle:
    def __init__(self, size: Vector2, top_left: Vector2 = None, top_right: Vector2 = None,
                 bottom_left: Vector2 = None, bottom_right: Vector2 = None, center: Vector2 = None):
        self.size = size
        if top_left:
            self.top_left = top_left
        elif top_right:
            self.top_right = top_right
        elif bottom_left:
            self.bottom_left = bottom_left
        elif bottom_right:
            self.bottom_right = bottom_right
        elif center:
            self.center = center
        else:
            raise ValueError("At least one of the positions must be given!")

    def __eq__(self, rect):
        return self.size == rect.size and self.top_left == rect.top_left

    def __str__(self):
        return f"<Class 'Rectangle'<->(size={self.size}, top_left={self.top_left})>"

    @property
    def size(self):
        return self._size.copy()

    @property
    def width(self):
        return self.size.x

    @property
    def height(self):
        return self.size.y

    @property
    def top_left(self):
        return self._top_left.copy()

    @property
    def top_right(self):
        return Vector2(self.top_left.x + self.width - 1, self.top_left.y)

    @property
    def bottom_left(self):
        return Vector2(self.top_left.x, self.top_left.y + self.height - 1)

    @property
    def bottom_right(self):
        return Vector2(self.top_left.x + self.width - 1, self.top_left.y + self.height - 1)

    @property
    def center(self):
        return Vector2(self.top_left.x + self.width // 2, self.top_left.y + self.height // 2)

    @size.setter
    def size(self, new_size: Vector2):
        self._size = new_size.copy()

    @width.setter
    def width(self, new_width: int):
        self._size.x = new_width

    @height.setter
    def height(self, new_height: int):
        self._size.y = new_height

    @top_left.setter
    def top_left(self, new_top_left: Vector2):
        self._top_left = new_top_left.copy()

    @top_right.setter
    def top_right(self, new_top_right: Vector2):
        self.top_left = Vector2(new_top_right.x - self.size.x + 1, new_top_right.y)

    @bottom_left.setter
    def bottom_left(self, new_bottom_left: Vector2):
        self.top_left = Vector2(new_bottom_left.x, new_bottom_left.y - self.size.y + 1)

    @bottom_right.setter
    def bottom_right(self, new_bottom_right: Vector2):
        self.top_left = Vector2(new_bottom_right.x - self.size.x + 1, new_bottom_right.y - self.size.y + 1)

    @center.setter
    def center(self, new_center):
        self.top_left = Vector2(new_center.x - self.size.x // 2, new_center.y - self.size.y // 2)

    def check_point(self, point: Vector2):
        if self.top_left.x <= point.x <= self.top_right.x and self.top_left.y <= point.y <= self.bottom_left.y:
            return True
        return False

    def move(self, ds: Vector2):
        self.top_left = Vector2(self.top_left.x + ds.x, self.top_left.y + ds.y)

    def copy(self):
        return Rectangle(size=self.size, top_left=self.top_left)
