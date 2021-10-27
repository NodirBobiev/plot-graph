import pygame

from Bar import MovableBar
from Block import Block, Label, InputField
from Button import Button, ButtonWithLabel, CheckBox
from Configuration import *
from Grid import MovableGrid
from NumericMethod import NumericMethod, exact_cp, local_error_cp, nothing_f, compute_points, euler_f, rk_f, imp_f, \
    global_error_cp
from Rectangle import Rectangle
from Vector2 import Vector2

grids = []
bar = None


def open_close_bar_btn(self):
    bar = self.get_connection('bar')
    if bar.is_open:
        bar.close()
    else:
        bar.open()


def checkboxes(self):
    method = self.get_connection('method')
    local = self.get_connection('local')
    gbl = self.get_connection('gbl')
    if self.state:
        self.mark.deactivate()
        self.state = False
        method.hidden = True
        local.hidden = True
        gbl.hidden = True
    else:
        self.mark.activate()
        self.state = True
        method.hidden = False
        local.hidden = False
        gbl.hidden = False


def grid_switch_btn(self):
    global grids, bar
    if bar is not None:
        bar.close()

    for grid in grids:
        grid.close()
    index = self.get_connection('index')
    if len(grids) > index:
        grids[index].open()


def run():
    global bar, grids
    pygame.init()
    pygame.key.set_repeat(500, 50)

    is_x_pressed = False
    is_y_pressed = False
    is_mouse_pressed = False
    # screen initialization
    pygame.display.set_caption("Plot The Graph")
    pygame.display.set_mode(SCREENSIZE)

    bar = MovableBar(color=pygame.Color(255, 240, 190), speed=2000,
                     rect=Rectangle(size=Vector2(BARSIZE[0], BARSIZE[1]), top_left=Vector2(0, 0)),
                     opened_rect=Rectangle(size=Vector2(BARSIZE[0], BARSIZE[1]), top_left=Vector2(0, 0)),
                     closed_rect=Rectangle(size=Vector2(BARSIZE[0], BARSIZE[1]), top_left=Vector2(-BARSIZE[0] +
                                                                                                  BARBTNSIZE[0], 0)))

    bar_btn = Button(on_click=open_close_bar_btn, color=pygame.Color(220, 200, 200),
                     rect=Rectangle(size=Vector2(30, BARSIZE[1]), top_right=bar.top_right))
    bar_btn.add_connections(bar=bar)
    bar.add_child(bar_btn)

    main_grid = MovableGrid(opened_rect=Rectangle(size=Vector2(*GRIDSIZE), top_right=Vector2(SCREENSIZE[0] - 20, 7)),
                            closed_rect=Rectangle(size=Vector2(*GRIDSIZE), top_left=Vector2(*SCREENSIZE)),
                            speed=3000, start_x=0, final_x=6, start_y=0, final_y=400, color=[245, 245, 240],
                            rect=Rectangle(size=Vector2(*GRIDSIZE), top_right=Vector2(SCREENSIZE[0] - 20, 7)))
    exact_method = NumericMethod(cp_f=exact_cp, next_f=nothing_f, grid=main_grid, n=main_grid.width, iv=Vector2(0, 1))
    euler_method = NumericMethod(cp_f=compute_points, next_f=euler_f, grid=main_grid, n=15, iv=Vector2(1, 1))
    imp_euler_method = NumericMethod(cp_f=compute_points, next_f=imp_f, grid=main_grid, n=15, iv=Vector2(1, 1))
    runge_kutta_method = NumericMethod(cp_f=compute_points, next_f=rk_f, grid=main_grid, n=15, iv=Vector2(1, 1))
    main_grid.add_functions(exact_method=exact_method, euler_method=euler_method, imp_euler_method=imp_euler_method,
                            runge_kutta_method=runge_kutta_method)
    local_grid = MovableGrid(opened_rect=Rectangle(size=Vector2(*GRIDSIZE), top_right=Vector2(SCREENSIZE[0] - 20, 7)),
                             closed_rect=Rectangle(size=Vector2(*GRIDSIZE), bottom_right=Vector2(0, 0)),
                             speed=3000, start_x=0, final_x=6, start_y=0, final_y=400, color=[240, 245, 245],
                             rect=Rectangle(size=Vector2(*GRIDSIZE), bottom_right=Vector2(0, 0)))
    euler_local = NumericMethod(cp_f=local_error_cp, next_f=euler_f, grid=local_grid, n=15, iv=Vector2(1, 1))
    imp_euler_local = NumericMethod(cp_f=local_error_cp, next_f=imp_f, grid=local_grid, n=15, iv=Vector2(1, 1))
    runge_kutta_local = NumericMethod(cp_f=local_error_cp, next_f=rk_f, grid=local_grid, n=15, iv=Vector2(1, 1))
    nothing_local = NumericMethod(cp_f=nothing_f, next_f=nothing_f, grid=local_grid)
    local_grid.add_functions(nothing_local=nothing_local, euler_local=euler_local, imp_euler_local=imp_euler_local,
                             runge_kutta_local=runge_kutta_local)

    global_grid = MovableGrid(opened_rect=Rectangle(size=Vector2(*GRIDSIZE), top_right=Vector2(SCREENSIZE[0] - 20, 7)),
                              closed_rect=Rectangle(size=Vector2(*GRIDSIZE), top_right=Vector2(0, SCREENSIZE[1])),
                              speed=3000, start_x=2, final_x=15, start_y=0, final_y=2000, color=[245, 240, 245],
                              rect=Rectangle(size=Vector2(*GRIDSIZE), top_right=Vector2(0, SCREENSIZE[1])))
    global_grid.x0, global_grid.xn = 1, 6
    euler_global = NumericMethod(cp_f=global_error_cp, next_f=euler_f, grid=global_grid, iv=Vector2(1, 1))
    imp_euler_global = NumericMethod(cp_f=global_error_cp, next_f=imp_f, grid=global_grid, iv=Vector2(1, 1))
    runge_kutta_global = NumericMethod(cp_f=global_error_cp, next_f=rk_f, grid=global_grid, iv=Vector2(1, 1))
    nothing_global = NumericMethod(cp_f=nothing_f, next_f=nothing_f, grid=global_grid)
    global_grid.add_functions(nothing_global=nothing_global, euler_global=euler_global,
                              imp_euler_global=imp_euler_global,
                              runge_kutta_global=runge_kutta_global)

    grids.append(main_grid)
    grids.append(local_grid)
    grids.append(global_grid)

    line_size, line_pos, label_size = Vector2(80, 1), Vector2(30, 30), Vector2(100, 30)
    texts = ['Exact Solution', 'Euler Method', 'Improved Euler', 'Runge Kutta']
    line_colors = [(200, 0, 0), (0, 150, 0), (0, 0, 200), (0, 0, 0)]
    methods = [exact_method, euler_method, imp_euler_method, runge_kutta_method]
    lcls = [nothing_local, euler_local, imp_euler_local, runge_kutta_local]
    gbls = [nothing_global, euler_global, imp_euler_global, runge_kutta_global]
    for i in range(4):
        line = Block(color=line_colors[i], rect=Rectangle(size=line_size, top_left=line_pos))
        label = Label(text=texts[i], color=bar.color, rect=Rectangle(size=label_size,
                                                                     center=line.center + Vector2(95, 0)))
        chk_box = CheckBox(on_click=checkboxes, color=pygame.Color(180, 180, 180),
                           rect=Rectangle(size=Vector2(20, 20), center=label.center + Vector2(label.width / 2 + 20, 0)))
        chk_box.mark = Block(color=pygame.Color(0, 0, 0), rect=Rectangle(size=Vector2(10, 10),
                                                                         center=chk_box.center))
        chk_box.add_connections(method=methods[i], local=lcls[i], gbl=gbls[i])
        bar.add_children(line, label, chk_box)
        line_pos.y += label.height

    label_x0 = Label(text="x0: ", color=bar.color, rect=Rectangle(size=Vector2(30, 30), top_left=Vector2(70, 150)))
    input_x0 = InputField(text="1", place_holder="enter number...", color=[255, 255, 255],
                          rect=Rectangle(size=Vector2(100, 30), center=label_x0.center + Vector2(65, 0)))
    label_xn = Label(text="xn: ", color=bar.color,
                     rect=Rectangle(size=label_x0.size, top_left=label_x0.top_left + Vector2(0, label_x0.height + 10)))
    input_xn = InputField(text="6", place_holder="enter number...", color=[255, 255, 255],
                          rect=Rectangle(size=Vector2(100, 30), center=label_xn.center + Vector2(65, 0)))
    label_y0 = Label(text="y0: ", color=bar.color,
                     rect=Rectangle(size=label_xn.size, top_left=label_xn.top_left + Vector2(0, label_xn.height + 10)))
    input_y0 = InputField(text="1", place_holder="enter number...", color=[255, 255, 255],
                          rect=Rectangle(size=Vector2(100, 30), center=label_y0.center + Vector2(65, 0)))
    label_n0 = Label(text="n0: ", color=bar.color,
                     rect=Rectangle(size=label_y0.size, top_left=label_y0.top_left + Vector2(0, label_y0.height + 10)))
    input_n0 = InputField(text="2", place_holder="enter number...", color=[255, 255, 255],
                          rect=Rectangle(size=Vector2(100, 30), center=label_n0.center + Vector2(65, 0)))
    label_N = Label(text="N: ", color=bar.color,
                    rect=Rectangle(size=label_n0.size, top_left=label_n0.top_left + Vector2(0, label_n0.height + 10)))
    input_N = InputField(text="15", max_size=3, place_holder="enter number...", color=[255, 255, 255],
                         rect=Rectangle(size=Vector2(100, 30), center=label_N.center + Vector2(65, 0)))
    bar.add_children(label_x0, input_x0, label_xn, input_xn, label_y0, input_y0, label_n0, input_n0, label_N, input_N)

    main_grid_btn = ButtonWithLabel(on_click=grid_switch_btn, color=pygame.Color(200, 100, 0),
                                    label=Label(text="Graphs", color=[200, 100, 0],
                                                rect=Rectangle(size=Vector2(100, 30), center=Vector2(140, 380))),
                                    rect=Rectangle(size=Vector2(100, 30), center=Vector2(140, 380)))
    local_grid_btn = ButtonWithLabel(on_click=grid_switch_btn, color=pygame.Color(200, 100, 0),
                                     label=Label(text="Local Errors", color=[200, 100, 0],
                                                 rect=Rectangle(size=Vector2(100, 30), center=Vector2(80, 420))),
                                     rect=Rectangle(size=Vector2(100, 30), center=Vector2(80, 420)))
    global_grid_btn = ButtonWithLabel(on_click=grid_switch_btn, color=pygame.Color(200, 100, 0),
                                      label=Label(text="Global Errors", color=[200, 100, 0],
                                                  rect=Rectangle(size=Vector2(100, 30), center=Vector2(200, 420))),
                                      rect=Rectangle(size=Vector2(100, 30), center=Vector2(200, 420)))
    main_grid_btn.add_connections(index=0)
    local_grid_btn.add_connections(index=1)
    global_grid_btn.add_connections(index=2)
    bar.add_children(main_grid_btn, local_grid_btn, global_grid_btn)

    local_grid.close()
    global_grid.close()
    clock = pygame.time.Clock()
    running = True
    methods = [euler_method, imp_euler_method, runge_kutta_method, euler_local, imp_euler_local,
               runge_kutta_local, euler_global, imp_euler_global, runge_kutta_global]
    while running:
        try:
            new_val = float(input_x0.text)
            # print(new_val, main_grid.x0,  main_grid.xn, main_grid.start_x, main_grid.final_x)
            if new_val != main_grid.x0:
                main_grid.x0 = main_grid.start_x = new_val
                local_grid.x0 = local_grid.start_x = new_val
                global_grid.x0 = new_val
                for mt in methods:
                    mt.iv = Vector2(new_val, mt.iv.y)
        except ValueError:
            pass
        try:
            new_val = float(input_xn.text)
            if new_val != main_grid.xn:
                main_grid.xn = main_grid.final_x = new_val
                local_grid.xn = local_grid.final_x = new_val
                global_grid.xn = new_val
        except ValueError:
            pass
        try:
            new_val = float(input_y0.text)
            for mt in methods:
                mt.iv = Vector2(mt.iv.x, new_val)
            main_grid.update_function()
            local_grid.update_function()
            global_grid.update_function()
        except ValueError:
            pass
        try:
            new_val = float(input_n0.text)
            new_val = int(new_val)
            input_n0.text = str(new_val)
            if new_val != global_grid.start_x:
                global_grid.start_x = new_val
        except ValueError:
            pass
        try:
            new_val = float(input_N.text)
            new_val = int(new_val)
            input_N.text = str(new_val)
            if new_val != global_grid.final_x:
                global_grid.final_x = new_val
                for mt in methods:
                    mt.n = new_val
        except ValueError:
            pass

        if main_grid.is_open:
            grid = main_grid
        elif local_grid.is_open:
            grid = local_grid
        else:
            grid = global_grid
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                bar.key_pressed(key=event.key)
                if event.key == pygame.K_x:
                    is_x_pressed = True
                if event.key == pygame.K_y:
                    is_y_pressed = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_x:
                    is_x_pressed = False
                if event.key == pygame.K_y:
                    is_y_pressed = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    is_mouse_pressed = not bar.mouse_click(mouse_pos=Vector2(mouse_pos[0], mouse_pos[1]))
                    if not grid.check_point(point=Vector2(mouse_pos[0], mouse_pos[1])):
                        is_mouse_pressed = False
                elif event.button not in [4, 5] or not grid.active or grid.final_x <= grid.start_x:
                    pass
                elif is_x_pressed:
                    length = grid.final_x - grid.start_x
                    if event.button == 4:
                        newlength = length / XSCALE
                    else:
                        newlength = length * XSCALE
                    if 0.1 <= newlength <= 1000:
                        grid.start_x = grid.start_x + (length - newlength) / 2
                        grid.final_x = grid.final_x - (length - newlength) / 2
                elif is_y_pressed:
                    length = grid.final_y - grid.start_y
                    if event.button == 4:
                        newlength = length / YSCALE
                    else:
                        newlength = length * YSCALE
                    if 0.1 <= newlength <= 2000:
                        grid.start_y = grid.start_y + (length - newlength) / 2
                        grid.final_y = grid.final_y - (length - newlength) / 2

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    is_mouse_pressed = False

        ds = pygame.mouse.get_rel()
        if is_mouse_pressed and grid.start_x <= grid.final_x:
            mv_x = ds[0] * (grid.final_x - grid.start_x) / grid.width
            mv_y = ds[1] * (grid.final_y - grid.start_y) / grid.height
            grid.start_x -= mv_x
            grid.final_x -= mv_x
            grid.start_y += mv_y
            grid.final_y += mv_y

        time_passed = clock.get_time() / 1000
        pygame.display.get_surface().fill(BACKGROUNCOLOR)

        global_grid.update(time_passed)
        local_grid.update(time_passed)
        main_grid.update(time_passed)
        bar.update(time_passed)

        pygame.display.flip()
        # print(f"Game FPS={clock.get_fps()};  time_passed={time_passed}")
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    run()
