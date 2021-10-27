from Block import Block
from Vector2 import Vector2
from pygame import display


class Button(Block):
    def __init__(self, on_click, **kwargs):
        super().__init__(**kwargs)
        self.on_click = on_click
        self._connections = dict()

    def add_connections(self, **kwargs):
        for key, value in kwargs.items():
            self._connections[key] = value

    def remove_connection(self, *args):
        for arg in args:
            del self._connections[arg]

    def get_connection(self, key):
        return self._connections[key]

    def mouse_click(self, mouse_pos: Vector2, *args, **kwargs):
        if self.check_point(mouse_pos):
            self.on_click(self)

    def on_click(self):
        pass


class ButtonWithLabel(Button):
    def __init__(self, label, **kwargs):
        super().__init__(**kwargs)
        self.label = label

    def move(self, ds: Vector2):
        self.top_left = Vector2(self.top_left.x + ds.x, self.top_left.y + ds.y)
        self.label.top_left = Vector2(self.label.top_left.x + ds.x, self.label.top_left.y + ds.y)

    def draw(self):
        screen = display.get_surface()
        if screen:
            screen.blit(self._face, (self.top_left.x, self.top_left.y))
            self.label.draw()


class CheckBox(Button):
    def __init__(self, mark: Block = None, **kwargs):
        super().__init__(**kwargs)
        self.mark = mark
        self.state = True

    def move(self, ds: Vector2):
        self.top_left = Vector2(self.top_left.x + ds.x, self.top_left.y + ds.y)
        self.mark.top_left = Vector2(self.mark.top_left.x + ds.x, self.mark.top_left.y + ds.y)

    def draw(self):
        screen = display.get_surface()
        if screen:
            screen.blit(self._face, (self.top_left.x, self.top_left.y))
            if self.state:
                self.mark.draw()
