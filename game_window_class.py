import copy
import config
from cell_class import *

vec = pygame.math.Vector2
global energ
energ = 0


class Game_window:
    def __init__(self, screen, x, y, window_width=config.WIDTH, window_height=config.HEIGHT, nbh=0, periodic=True):

        self.changedcells = []
        self.periodic = periodic
        self.neighbourhood = nbh
        self.screen = screen
        self.pos = vec(x, y)
        self.dx = config.dx
        self.dy = config.dy
        self.width, self.height = window_width - 200 - config.gridx, window_height - 200
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.rows = self.height // self.dx
        self.cols = self.width // self.dy
        self.grid = [[Cell(self.image, x, y, self.rows, self.cols) for x in range(self.cols)] for y in range(self.rows)]
        for row in self.grid:
            for cell in row:
                cell.get_neighbours(self.grid, self.neighbourhood, self.periodic)

    def update(self):
        self.rect.topleft = self.pos
        for row in self.grid:
            for cell in row:
                cell.update()

    def draw(self):
        self.image.fill((255, 255, 255))
        for row in self.grid:
            for cell in row:
                cell.draw()
        self.screen.blit(self.image, (self.pos.x, self.pos.y))

    def reset_grid(self):
        self.grid = [[Cell(self.image, x, y, self.rows, self.cols) for x in range(self.cols)] for y in range(self.rows)]

    def evaluate(self):
        new_grid = copy.copy(self.grid)

        for row in self.grid:
            for cell in row:
                cell.live_neighbours()  # zlicz żywych sąsiadów każdej komórki

        for yidx, row in enumerate(self.grid):
            for xidx, cell in enumerate(row):
                if cell.alive == False:
                    if cell.alive_neighbours != 0:
                        cell.alive = True
                        cell.owncolor = cell.get_neighbour_color()
        self.grid = new_grid

    def allalive(self):
        for yidx, row in enumerate(self.grid):
            for xidx, cell in enumerate(row):
                if cell.alive is False:
                    return False
        return True

    def calcAllEnergy(self):
        if self.allalive():
            for yidx, row in enumerate(self.grid):
                for xidx, cell in enumerate(row):
                    cell.energy = cell.calcEnergy()

    def mmc(self):
        if self.allalive():
            self.calcAllEnergy()
            randommed = self.grid
            random.shuffle(randommed)
            for yidx, row in enumerate(randommed):
                for xidx, cell in enumerate(row):
                    cell.mc()


    def showenergy(self):
        self.calcAllEnergy()
        global energ
        energ += 1
        if energ % 2 == 1:
            for yidx, row in enumerate(self.grid):
                for xidx, cell in enumerate(row):
                    col = 0
                    if cell.energy == 0:
                        cell.ocb = cell.owncolor
                        cell.owncolor = (40, 100, 100)
                        continue
                    else:
                        col = (255 - (cell.energy * 8), 255 - (cell.energy * 17), 255 - (cell.energy * 20))
                    cell.ocb = cell.owncolor
                    cell.owncolor = col
        else:
            for yidx, row in enumerate(self.grid):
                for xidx, cell in enumerate(row):
                    cell.owncolor = cell.ocb
