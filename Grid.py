from pygame import display, draw, Color, font
from math import ceil
from Block import Block
from Vector2 import Vector2
from Bar import MovableBar


class Grid(Block):
    def __init__(self, start_x, final_x, start_y, final_y, net_dist=50, net_line_width=1,
                 net_line_color=Color(200, 200, 200),  **kwargs):
        super().__init__(**kwargs)
        self._functions = dict()
        self.x0 = start_x
        self.xn = final_x
        self.net_line_width = net_line_width
        self.net_line_color = net_line_color
        self.start_x = start_x
        self.final_x = final_x
        self.start_y = start_y
        self.final_y = final_y
        self.net_dist = net_dist
        self.font = font.SysFont('calibri', 14)
        self.settings_changed = False

    @property
    def start_x(self):
        return self._start_x

    @property
    def final_x(self):
        return self._final_x

    @property
    def start_y(self):
        return self._start_y

    @property
    def final_y(self):
        return self._final_y

    @property
    def font(self):
        return self._font

    @start_x.setter
    def start_x(self, new_start_x):
        self._start_x = new_start_x
        self.settings_changed = True

    @final_x.setter
    def final_x(self, new_final_x):
        self._final_x = new_final_x
        self.settings_changed = True

    @start_y.setter
    def start_y(self, new_start_y):
        self._start_y = new_start_y
        self.settings_changed = True

    @final_y.setter
    def final_y(self, new_final_y):
        self._final_y = new_final_y
        self.settings_changed = True

    @font.setter
    def font(self, new_font):
        self._font = new_font

    def update_function(self):
        for _, func in self._functions.items():
            func.compute_points(func)

    def add_functions(self, **kwargs):
        for key, val in kwargs.items():
            self._functions[key] = val

    def get_horizontal_nets(self):
        array = list()
        if self.start_x >= self.final_x:
            return array
        zero_pos = (0 - self.start_x) / (self.final_x - self.start_x) * self.width
        dx = self.net_dist / self.width * (self.final_x - self.start_x)

        step = -ceil(abs(min(0, self.final_x) / dx))
        while self.start_x <= step * dx <= self.final_x:
            array.append([step * dx, Vector2(zero_pos + step * self.net_dist, 0),
                          Vector2(zero_pos + step * self.net_dist, self.height)])
            step -= 1

        step = ceil(max(dx, self.start_x) / dx)
        while self.start_x <= step * dx <= self.final_x:
            array.append([step * dx, Vector2(zero_pos + step * self.net_dist, 0),
                          Vector2(zero_pos + step * self.net_dist, self.height)])
            step += 1
        return array

    def get_vertical_nets(self):
        array = list()
        if self.start_y >= self.final_y:
            return array
        zero_pos = (0 - self.start_y) / (self.final_y - self.start_y) * self.height
        dx = self.net_dist / self.height * (self.final_y - self.start_y)

        step = -ceil(abs(min(0, self.final_y) / dx))
        while self.start_y <= step * dx <= self.final_y:
            array.append([step * dx, Vector2(0, self.height - (zero_pos + step * self.net_dist) - 1),
                          Vector2(self.width, self.height - (zero_pos + step * self.net_dist) - 1)])
            step -= 1

        step = ceil(max(dx, self.start_y) / dx)
        while self.start_y <= step * dx <= self.final_y:
            array.append([step * dx, Vector2(0, self.height - (zero_pos + step * self.net_dist) - 1),
                          Vector2(self.width, self.height - (zero_pos + step * self.net_dist) - 1)])
            step += 1
        return array

    def get_net_lines(self):
        return {"horizontal": self.get_horizontal_nets(), "vertical": self.get_vertical_nets()}

    def draw(self):
        screen = display.get_surface()
        if screen:
            if self.settings_changed:
                self.update_function()
                self.settings_changed = False
            self.draw_nets()
            self.plot_graphs()
            screen.blit(self._face, [self.top_left.x, self.top_left.y])
            self.draw_x_rulers()
            self.draw_y_rulers()

    def draw_nets(self):
        self._face.fill(self.color)
        lines = self.get_net_lines()
        for line in lines["horizontal"] + lines["vertical"]:
            draw.line(self._face, self.net_line_color, [line[1].x, line[1].y], [line[2].x, line[2].y],
                      self.net_line_width)

    def plot_graphs(self):
        if self.start_x >= self.final_x:
            return
        colors = [[200, 0, 0], [0, 150, 0], [0, 0, 200], [0, 0, 0]]
        cnt = 0
        for key, func in self._functions.items():
            points = func.get_points()
            for i in range(1, len(points)):
                if points[i-1].y is None or points[i].y is None:
                    pass
                else:
                    x1 = (points[i - 1].x - self.start_x) / (self.final_x - self.start_x) * self.width
                    y1 = self.height - (points[i - 1].y - self.start_y) / (self.final_y - self.start_y) * self.height-1
                    x2 = (points[i].x - self.start_x) / (self.final_x - self.start_x) * self.width
                    y2 = self.height - (points[i].y - self.start_y) / (self.final_y - self.start_y) * self.height - 1
                    draw.aaline(self._face, colors[cnt], [x1, y1], [x2, y2])
            cnt += 1

    def draw_x_rulers(self):
        screen = display.get_surface()
        if screen:
            lines = self.get_horizontal_nets()
            for line in lines:
                surf = self.font.render(str(round(line[0], 3)), True, [0, 0, 0])
                width = surf.get_width()
                pos_y = line[2].y + 15
                pos_x = line[2].x - width / 2
                screen.blit(surf, (pos_x + self.top_left.x, pos_y + self.top_left.y))
                draw.line(screen, self.net_line_color, [line[2].x + self.top_left.x, line[2].y + self.top_left.y],
                          [line[2].x + self.top_left.x, line[2].y + 10 + self.top_left.y], 1)

    def draw_y_rulers(self):
        screen = display.get_surface()
        if screen:
            lines = self.get_vertical_nets()
            for line in lines:
                surf = self.font.render(str(round(line[0], 3)), True, [0, 0, 0])
                height, width = surf.get_height(), surf.get_width()
                pos_y = line[1].y - height / 2
                pos_x = line[1].x - width - 15
                screen.blit(surf, (pos_x + self.top_left.x, pos_y + self.top_left.y))
                draw.line(screen, self.net_line_color, [line[1].x + self.top_left.x, line[1].y + self.top_left.y],
                          [line[1].x - 10 + self.top_left.x, line[1].y + self.top_left.y], 1)


class MovableGrid(MovableBar, Grid):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def draw(self):
        screen = display.get_surface()
        if screen:
            if self.settings_changed:
                self.update_function()
                self.settings_changed = False
            if not self.state and self.top_left == self.closed_rect.top_left:
                return
            if self.state and self.top_left == self.opened_rect.top_left:
                self.draw_nets()
                self.plot_graphs()
                screen.blit(self._face, [self.top_left.x, self.top_left.y])
                self.draw_x_rulers()
                self.draw_y_rulers()
                return
            else:
                self.draw_nets()
                self.plot_graphs()
                screen.blit(self._face, [self.top_left.x, self.top_left.y])
