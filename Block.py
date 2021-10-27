import pygame
from pygame import Surface, display, Color, font, draw
from Rectangle import Rectangle
from ObjectBehaviour import ObjectBehaviour


class Block(Rectangle, ObjectBehaviour):
    def __init__(self, color, rect: Rectangle):
        super().__init__(size=rect.size, top_left=rect.top_left)
        self._face = Surface([self.width, self.height])
        self._face.fill(color)
        self._active = True
        self._color = color

    @property
    def face(self):
        return self._face.copy()

    @property
    def color(self):
        return self._color

    @property
    def active(self):
        return self._active

    @face.setter
    def face(self, new_face: Surface):
        self._face = new_face.copy()

    @color.setter
    def color(self, new_color: Color):
        self._color = new_color

    def activate(self):
        self._active = True

    def deactivate(self):
        self._active = False

    def update(self, *args, **kwargs):
        if self.active:
            self.draw()

    def draw(self):
        screen = display.get_surface()
        if screen:
            screen.blit(self._face, [self.top_left.x, self.top_left.y])


class Label(Block):
    def __init__(self, text='', font_family='calibri', font_size=16, font_color=[0, 0, 0], **kwargs):
        super().__init__(**kwargs)
        self._text = text
        self._font_family = font_family
        self._font_size = font_size
        self._font_color = font_color
        self.blit_text()

    @property
    def font_familiy(self):
        return self._font_family

    @property
    def font_size(self):
        return self._font_size

    @property
    def font_color(self):
        return self._font_color

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, new_val):
        self._text = new_val

    def blit_text(self):
        fnt = font.SysFont(self.font_familiy, self.font_size)
        fnt_surf = fnt.render(self.text, True, self.font_color)
        x = (self.width - fnt_surf.get_width()) / 2
        y = (self.height - fnt_surf.get_height()) / 2
        self._face.blit(fnt_surf, [x, y])


class InputField(Label):
    def __init__(self, place_holder="", max_size=5, place_holder_color=[100, 100, 100], **kwargs):
        self.place_holder = place_holder
        self.place_holder_color = place_holder_color
        self.max_size = max_size
        self.input_state = False
        super().__init__(**kwargs)

    def mouse_click(self, mouse_pos, *args, **kwargs):
        if self.check_point(mouse_pos):
            self.input_state = True
        else:
            self.input_state = False

    def key_pressed(self, key):
        chars = [(str(i), str(i)) for i in range(10)] + [('-', '-'), ('.', '.')]
        for char in chars:
            if pygame.key.key_code(char[0]) == key:
                self.add_char(char[1])
                return
        if key == pygame.K_BACKSPACE:
            self.remove_last_char()

    def add_char(self, char):
        if len(self.text) >= self.max_size:
            return
        if self.input_state:
            if char == '-':
                if self._text == "":
                    self._text += char
            elif char == '.':
                if self._text != "" and self._text[-1] != '-' and '.' not in self._text:
                    self._text += char
            else:
                self._text += char
            self.blit_text()

    def remove_last_char(self):
        if self.input_state:
            self._text = self._text[:-1]
            self.blit_text()

    def blit_text(self):
        self._face.fill(self.color)
        fnt = font.SysFont(self.font_familiy, self.font_size)
        if self.text != "":
            fnt_surf = fnt.render(self.text, True, self.font_color)
        else:
            fnt_surf = fnt.render(self.place_holder, True, self.place_holder_color)
        y = (self.height - fnt_surf.get_height()) / 2
        self._face.blit(fnt_surf, (5, y))

    def draw(self):
        screen = display.get_surface()
        if screen:
            screen.blit(self._face, [self.top_left.x, self.top_left.y])
            if self.input_state:
                draw.rect(screen, [0, 0, 200], [(self.top_left.x, self.top_left.y), (self.width, self.height)], width=2)
