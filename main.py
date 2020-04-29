import pygame, random, numpy
import sys
import config
import tkinter
from game_window_class import *
from button_class import *
from collections import Counter

WIDTH, HEIGHT = config.WIDTH, config.HEIGHT
BACKGROUND = (199, 199, 199)
FPS = 30
colors = []
dx = config.dx
dy = config.dy
global entry
# ----------------------------SETTING---------------------------------#
def get_events():
    global running
    global window_width
    global window_height
    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
            window_width = event.w
            window_height = event.h
            window = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
            window.fill(background)
            reset_game_resize(window_width, window_height)
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if mouse_on_grid(mouse_pos, window_width, window_height):
                click_cell(mouse_pos)
            else:
                for button in buttons:
                    button.click()

def update():
    nbh = ''
    per = ''
    if nh == 0:
        nbh = 'Moore'
    if nh == 1:
        nbh = 'Neumann'
    if nh == 2:
        nbh = 'Pent'
    if nh == 3:
        nbh = 'Hex'
    if nh == 4:
        nbh = 'Radius'

    if periodic:
        per = 'On'
    else:
        per = 'Off'
    for button in buttons:
        button.update(mouse_pos)
    game_window.update()
    t = font.render('Ilość Z.: {}'.format(iterations), True, font_color, font_background)
    t_rect = t.get_rect()
    t_rect.centerx, t_rect.centery = WIDTH // 5 - 100, 474
    window.blit(t, t_rect)

    nbR = font.render('NBH R: {}'.format(config.nbhR), True, font_color, font_background)
    nbR_rect = nbR.get_rect()
    nbR_rect.centerx, nbR_rect.centery = WIDTH // 5 - 100, 394
    window.blit(nbR, nbR_rect)

    R = font.render('R zar.: {}'.format(config.R), True, font_color, font_background)
    R_rect = R.get_rect()
    R_rect.centerx, R_rect.centery = WIDTH // 5 - 100, 434
    window.blit(R, R_rect)

    s = font.render('Nbh: {}'.format(nbh), True, font_color, font_background)
    s_rect = s.get_rect()
    s_rect.centerx, s_rect.centery = WIDTH // 5 - 100, 155
    window.blit(s, s_rect)

    p = font.render('Periodic: {}'.format(per), True, font_color, font_background)
    p_rect = s.get_rect()
    p_rect.centerx, p_rect.centery = WIDTH // 5 - 103, 115
    window.blit(p, p_rect)

    t = font.render('Ilość w x: {}'.format(config.ix), True, font_color, font_background)
    t_rect = t.get_rect()
    t_rect.centerx, t_rect.centery = WIDTH // 2 - 120, 115
    window.blit(t, t_rect)

    t = font.render('Ilość w y: {}'.format(config.iy), True, font_color, font_background)
    t_rect = t.get_rect()
    t_rect.centerx, t_rect.centery = WIDTH // 2 + 160, 115
    window.blit(t, t_rect)

    mc = font.render('Iteracje: {}'.format(config.iteracje), True, font_color, font_background)
    mc_rect = mc.get_rect()
    mc_rect.centerx, mc_rect.centery = WIDTH // 2, 155
    window.blit(mc, mc_rect)

    k = font.render('kt: {}'.format(config.kt), True, font_color, font_background)
    k_rect = k.get_rect()
    k_rect.centerx, k_rect.centery = WIDTH // 2 + 310, 115
    window.blit(k, k_rect)

def draw():
    for button in buttons:
        button.draw()
    game_window.draw()


# ----------------------------RUNNING---------------------------------#
def running_get_events():
    global running
    global window_width
    global window_height
    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
            window_width = event.w
            window_height = event.h
            window = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
            window.fill(background)
            reset_game_resize(window_width, window_height)
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if mouse_on_grid(mouse_pos, window_width, window_height):
                click_cell(mouse_pos)
            else:
                for button in buttons:
                    button.click()


def running_update():
    nbh = ''
    peri = ''
    if nh == 0:
        nbh = 'Moore'
    if nh == 1:
        nbh = 'Neumann'
    if nh == 2:
        nbh = 'Pent'
    if nh == 3:
        nbh = 'Hex'
    if nh == 4:
        nbh = 'Rad'

    if periodic:
        peri = 'On'
    else:
        peri = 'Off'
    game_window.update()
    for button in buttons:
        button.update(mouse_pos)
    game_window.evaluate()


def running_draw():
    for button in buttons:
        button.draw()
    game_window.draw()


def mouse_on_grid(pos, width=800, height=800):
    if config.gridx < pos[0] < (width - 100) and config.gridy < pos[1] < (height - 20):
        return True
    else:
        return False


def click_cell(pos):
    if state == 'setting':
        grid_pos = [pos[0] - config.gridx, pos[1] - config.gridy]
        grid_pos[0] = grid_pos[0] // dx
        grid_pos[1] = grid_pos[1] // dy
        if game_window.grid[grid_pos[1]][grid_pos[0]].alive:
            game_window.grid[grid_pos[1]][grid_pos[0]].alive = False
        else:
            game_window.grid[grid_pos[1]][grid_pos[0]].alive = True


def check_cell(pos):
    if mouse_on_grid(pos, window_width, window_height):
        grid_pos = [pos[0] - config.gridx, pos[1] - config.gridy]
        grid_pos[0] = grid_pos[0] // dx
        grid_pos[1] = grid_pos[1] // dy
        return game_window.grid[grid_pos[1]][grid_pos[0]].alive
    return False


def make_buttons(width):
    buttons = []
    buttons.append(
        Button(window, width // 5 - 200, 40, 100, 30, text='Run', bgcolor=(28, 111, 51), hovercolor=(48, 200, 81),
               function=run_game))
    buttons.append(
        Button(window, width // 5 - 80, 40, 100, 30, text='Reset', bgcolor=(114, 14, 14), hovercolor=(200, 34, 34),
               function=reset_game))

    buttons.append(
        Button(window, width // 2 - 270, 40, 170, 30, text='Periodic On/Off', bgcolor=(205, 157, 66),
               hovercolor=(235, 207, 66),
               function=pertoggle))

    buttons.append(
        Button(window, width // 2 - 90, 40, 130, 30, text='Jednorodne', bgcolor=(18, 104, 135),
               hovercolor=(51, 168, 214),
               function=jednorodne))
    buttons.append(
        Button(window, width // 2 + 50, 40, 130, 30, text='Promien', bgcolor=(18, 104, 135),
               hovercolor=(51, 168, 214),
               function=radinit))

    buttons.append(
        Button(window, width // 2 + 195, 40, 100, 30, text='Losowe', bgcolor=(18, 104, 135), hovercolor=(51, 168, 214),
               function=losowe))
    buttons.append(
        Button(window, width // 2 + 305, 40, 100, 30, text='Podaj kt', bgcolor=(18, 104, 135), hovercolor=(51, 168, 214),
               function=ktinput))
    buttons.append(
        Button(window, width // 5 - 200, 460, 50, 30, text='+', bgcolor=(39, 232, 142), hovercolor=(0, 255, 137),
               function=iterationincrement))

    buttons.append(
        Button(window, width // 5 - 50, 460, 50, 30, text='-', bgcolor=(39, 232, 142), hovercolor=(0, 255, 137),
               function=iterationdecrement))

    buttons.append(
        Button(window, width // 2 - 230, 100, 50, 30, text='+', bgcolor=(39, 232, 142), hovercolor=(0, 255, 137),
               function=iXincrement))

    buttons.append(
        Button(window, width // 2 - 60, 100, 50, 30, text='-', bgcolor=(39, 232, 142), hovercolor=(0, 255, 137),
               function=iXdecrement))

    buttons.append(
        Button(window, width // 2 + 50, 100, 50, 30, text='+', bgcolor=(39, 232, 142), hovercolor=(0, 255, 137),
               function=iYincrement))

    buttons.append(
        Button(window, width // 2 + 220, 100, 50, 30, text='-', bgcolor=(39, 232, 142), hovercolor=(0, 255, 137),
               function=iYdecrement))

    buttons.append(
        Button(window, width // 5 - 160, 180, 120, 30, text='Moore', bgcolor=(28, 111, 51), hovercolor=(48, 161, 81),
               function=moore))

    buttons.append(
        Button(window, width // 5 - 160, 220, 120, 30, text='Neumann', bgcolor=(28, 111, 51), hovercolor=(48, 161, 81),
               function=neumann))

    buttons.append(
        Button(window, width // 5 - 160, 260, 120, 30, 30, text='Pent losowe', bgcolor=(28, 111, 51),
               hovercolor=(48, 161, 81),
               function=pent))

    buttons.append(
        Button(window, width // 5 - 160, 300, 120, 30, 30, text='Hex losowe', bgcolor=(28, 111, 51),
               hovercolor=(48, 161, 81),
               function=hex))

    buttons.append(
        Button(window, width // 5 - 160, 340, 120, 30, 30, text='Promien', bgcolor=(28, 111, 51),
               hovercolor=(48, 161, 81),
               function=rad))
    buttons.append(
        Button(window, width // 5 - 200, 380, 50, 30, text='+',bgcolor=(39, 232, 142), hovercolor=(0, 255, 137),
               function=nbhRincrement))

    buttons.append(
        Button(window, width // 5 - 50, 380, 50, 30, text='-', bgcolor=(39, 232, 142), hovercolor=(0, 255, 137),
               function=nbhRdecrement))

    buttons.append(
        Button(window, width // 5 - 200, 420, 50, 30, text='+', bgcolor=(39, 232, 142), hovercolor=(0, 255, 137),
               function=grainRincrement))

    buttons.append(
        Button(window, width // 5 - 50, 420, 50, 30, text='-', bgcolor=(39, 232, 142), hovercolor=(0, 255, 137),
               function=grainRincrement))

    buttons.append(
        Button(window, width // 2 - 100, 140, 50, 30, text='+', bgcolor=(39, 232, 142), hovercolor=(0, 255, 137),
               function=iterincrement))

    buttons.append(
        Button(window, width // 2 + 60, 140, 50, 30, text='-', bgcolor=(39, 232, 142), hovercolor=(0, 255, 137),
               function=iterdecrement))

    buttons.append(
        Button(window, width // 2 - 240, 140, 130, 30, text='Monte Carlo', bgcolor=(255, 141, 74),
               hovercolor=(255, 104, 17),
               function=mc))

    buttons.append(
        Button(window, width // 2 + 120, 140, 130, 30, text='Energy', bgcolor=(255, 141, 74),
               hovercolor=(255, 104, 17),
               function=showenergy))
    return buttons

def ktinput():
    global entry
    root = tkinter.Tk()
    root.wm_title("Insert")
    topFrame = tkinter.Frame(root, width=200, height=150)
    topFrame.pack(side=tkinter.TOP)
    botFrame = tkinter.Frame(root, width=1, height=1)
    botFrame.pack(side=tkinter.BOTTOM)
    submit= tkinter.Button(topFrame, text="Submit", fg="red")
    label = tkinter.Label(topFrame, text="Współczynnik kt:")
    entry = tkinter.Entry(topFrame)
    label.grid(row=0, sticky=tkinter.W)
    entry.grid(row=0, column=2)
    submit.grid(row=0, column=3)
    root.attributes('-topmost', True)
    submit.bind("<Button-1>", get_kt)
    root.mainloop()


def get_kt(event):
    x = float(entry.get())
    if x < 0.1 or x > 6:
        return
    config.kt = x

def showenergy():
    global state
    state = 'setting'
    game_window.showenergy()

def mc():
    global state
    state = 'setting'
    if game_window.allalive():
        for i in range(0, config.iteracje):
            game_window.mmc()


def iterincrement():
    global state
    state = 'setting'
    config.iteracje += 1


def iterdecrement():
    global state
    state = 'setting'
    if config.iteracje > 0:
        config.iteracje -= 1


def iXincrement():
    global state
    state = 'setting'
    config.ix += 1


def iXdecrement():
    global state
    state = 'setting'
    if config.ix > 0:
        config.ix -= 1


def iYincrement():
    global state
    state = 'setting'
    config.iy += 1


def iYdecrement():
    global state
    state = 'setting'
    if config.iy > 0:
        config.iy -= 1


def nbhRincrement():
    global state
    state = 'setting'
    config.nbhR += 1


def nbhRdecrement():
    global state
    state = 'setting'
    if config.nbhR > 0:
        config.nbhR -= 1


def grainRincrement():
    global state
    state = 'setting'
    config.R += 1


def grainRdecrement():
    global state
    state = 'setting'
    if config.R > 0:
        config.R -= 1


def radinit():
    if config.R >= dx:
        r = config.R
        reset_game()
        global state
        state = 'setting'
        count = iterations
        for i in range(count):
            neighbours = []
            pos = (random.randint(config.gridx + 1, window_width - config.gridx - 1),
                   random.randint(config.gridy + 1, window_height - 41))
            for j in range(pos[0] - r, pos[0] + r, dx):
                for k in range(pos[1] - r, pos[1] + r, dy):
                    if j == pos[0] and k == pos[1]:
                        continue
                    neighbours.append(check_cell((j, k)))
            occurence_count = Counter(neighbours)
            x = [occurence_count.most_common(1)[0][0], occurence_count.most_common(1)[0][1]]
            if x[0] == False and len(neighbours) == x[1]:
                click_cell(pos)


def rad():
    global nh
    nh = 4
    reset_game()


def hex():
    global nh
    nh = 3
    reset_game()


def pent():
    global nh
    nh = 2
    reset_game()


def pertoggle():
    global periodic
    if periodic:
        periodic = False
    else:
        periodic = True
    reset_game()


def moore():
    global nh
    nh = 0
    reset_game()


def neumann():
    global nh
    nh = 1
    reset_game()


def iterationincrement():
    global state
    state = 'setting'
    global iterations
    iterations += 1


def iterationdecrement():
    global state
    state = 'setting'
    global iterations
    if iterations > 0:
        iterations -= 1


def losowe():
    reset_game()
    global state
    state = 'setting'
    mouse_pos = []
    count = iterations
    for i in range(count):
        mouse_pos.append((random.randint(config.gridx + 1, window_width - 101),
                          random.randint(config.gridy + 1, window_height - 41)))
    for pos in mouse_pos:
        if mouse_on_grid(pos, window_width - 100, window_height):
            click_cell(pos)
    update()
    draw()


def jednorodne():
    reset_game()
    global state
    state = 'setting'
    mouse_pos = []
    if (config.ix == 0 or config.iy == 0):
        return
    gridx = window_width - 200 - config.gridx
    gridy = window_height - 20 - config.gridy
    Dx = int(gridx / (config.ix + 1))
    Dy = int(gridy / (config.iy + 1))
    x = numpy.arange(0 + Dx, gridx, Dx)
    y = numpy.arange(0 + Dy, gridy, Dy)
    for i in x:
        for j in y:
            mouse_pos.append((config.gridx + i, config.gridy + j))

    for pos in mouse_pos:
        if(mouse_on_grid(pos,window_width, window_height)):
            click_cell(pos)
    update()
    draw()


def run_game():
    global state
    state = 'running'


def reset_game():
    global state
    state = 'setting'
    global game_window
    game_window = Game_window(window, config.gridx, config.gridy, window_width=window_width,
                              window_height=window_height, nbh=nh,
                              periodic=periodic)


def reset_game_resize(width, height):
    global state
    state = 'setting'
    global game_window
    game_window = Game_window(window, config.gridx, config.gridy, window_width=width, window_height=height, nbh=nh,
                              periodic=periodic)
    global iterations
    iterations = 0
    global counter
    counter = 0


global window_width
global window_height
global counter
global periodic

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
clock = pygame.time.Clock()
game_window = Game_window(window, config.gridx, config.gridy)
active = False
iterations = 0

font = pygame.font.SysFont('arial', 20, True)
font_color = (0, 0, 0)
font_background = (72, 210, 44)
buttons = make_buttons(WIDTH)
background = (102, 102, 102)
state = 'setting'
window.fill(background)
running = True
periodic = True
nh = 0

while running:
    mouse_pos = pygame.mouse.get_pos()
    if state == 'setting':
        get_events()
        update()
        draw()
    if state == 'running':
        running_get_events()
        running_update()
        running_draw()
    if game_window.allalive():
        state = 'setting'
    clock.tick(FPS)
    pygame.display.update()
pygame.quit()
sys.exit()
