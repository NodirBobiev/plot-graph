from Block import Block
from Rectangle import Rectangle
from Vector2 import Vector2


class Bar(Block):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._children = []

    def add_child(self, new_child):
        self._children.append(new_child)

    def add_children(self, *args):
        for arg in args:
            self._children.append(arg)

    def get_children(self):
        return self._children

    def mouse_click(self, mouse_pos, *args, **kwargs):
        for child in self._children:
            child.mouse_click(mouse_pos, *args, **kwargs)
        return self.check_point(mouse_pos)

    def key_pressed(self, *args, **kwargs):
        for child in self._children:
            child.key_pressed(*args, **kwargs)

    def update(self, *args, **kwargs):
        if not self.active:
            return
        self.draw()
        for child in self._children:
            child.update(*args, **kwargs)


class MovableBar(Bar):
    def __init__(self, opened_rect: Rectangle, closed_rect: Rectangle, speed: float, **kwargs):
        super().__init__(**kwargs)
        self._opened_rect = opened_rect.copy()
        self._closed_rect = closed_rect
        self._speed = speed
        self._state = True

    @property
    def state(self):
        return self._state

    @property
    def is_open(self):
        return self._state

    @property
    def speed(self):
        return self._speed

    @property
    def opened_rect(self):
        return self._opened_rect

    @property
    def closed_rect(self):
        return self._closed_rect

    def open(self):
        self._state = True

    def close(self):
        self._state = False

    def update(self, time_passed, *args, **kwargs):
        if not self.active:
            return
        vector = None
        if self.state and self.top_left != self.opened_rect.top_left:
            vector = self.opened_rect.top_left - self.top_left
        if not self.state and self.top_left != self.closed_rect.top_left:
            vector = self.closed_rect.top_left - self.top_left
        if vector and vector != Vector2.zero():
            length = vector.get_magnitude()
            vector = vector.get_normalized() * min(self.speed * time_passed, length)
            self.move(vector)
            for child in self._children:
                child.move(vector)
        self.draw()
        for child in self._children:
            child.update(time_passed, *args, **kwargs)
