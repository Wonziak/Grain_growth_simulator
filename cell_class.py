import pygame, random, math
import config
from collections import Counter

colors = []


class Cell:
    def __init__(self, surface, grid_x, grid_y, rows=(config.HEIGHT - 200 - config.gridx) / config.dy,
                 cols=(config.WIDTH - 200 - config.gridx) / config.dx):
        self.owncolor = (random.randint(1, 254), random.randint(1, 254), random.randint(1, 254))
        self.energycolor=0
        self.ocb=0
        self.dx = config.dx
        self.dy = config.dy
        self.cols = cols
        self.rows = rows
        self.alive = False
        self.surface = surface
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.x_sr = random.uniform(0, self.dx) + self.grid_x * self.dx
        self.y_sr = random.uniform(0, self.dy) + self.grid_y * self.dy
        self.image = pygame.Surface((self.dx, self.dy))
        self.rect = self.image.get_rect()
        self.neighbours = []
        self.alive_neighbours = 0
        self.alive_neighbours_color_list = []
        self.energy = 0

    def update(self):
        self.rect.topleft = (self.grid_x * self.dx, self.grid_y * self.dy)

    def draw(self):
        if self.alive:
            self.image.fill(self.owncolor)
        else:
            self.image.fill((0, 0, 0))
            pygame.draw.rect(self.image, (255, 255, 255), (1, 1, 18, 18))
        self.surface.blit(self.image, (self.grid_x * self.dx, self.grid_y * self.dy))

    def get_neighbours(self, grid, nh, periodic):
        if periodic:
            if nh == 0:  # moore
                neighbour_list = [[1, 1], [-1, -1], [-1, 1], [1, -1], [0, -1], [0, 1], [1, 0], [-1, 0]]
                for neighbour in neighbour_list:
                    neighbour[0] += self.grid_x
                    neighbour[1] += self.grid_y
                for neighbour in neighbour_list:
                    if neighbour[0] < 0:
                        neighbour[0] += self.cols
                    if neighbour[1] < 0:
                        neighbour[1] += self.rows
                    if neighbour[0] > self.cols - 1:
                        neighbour[0] -= self.cols
                    if neighbour[1] > self.rows - 1:
                        neighbour[1] -= self.rows
                for neighbour in neighbour_list:
                    try:
                        self.neighbours.append(grid[neighbour[1]][neighbour[0]])
                    except:
                        continue
            if nh == 1:  # neumann
                neighbour_list = [[0, -1], [0, 1], [1, 0], [-1, 0]]
                for neighbour in neighbour_list:
                    neighbour[0] += self.grid_x
                    neighbour[1] += self.grid_y
                for neighbour in neighbour_list:
                    if neighbour[0] < 0:
                        neighbour[0] += self.cols
                    if neighbour[1] < 0:
                        neighbour[1] += self.rows
                    if neighbour[0] > self.cols - 1:
                        neighbour[0] -= self.cols
                    if neighbour[1] > self.rows - 1:
                        neighbour[1] -= self.rows
                for neighbour in neighbour_list:
                    try:
                        self.neighbours.append(grid[neighbour[1]][neighbour[0]])
                    except:
                        continue
            if nh == 2:  # pentagonalne losowe
                case = random.randint(0, 3)
                if case == 0:
                    neighbour_list = [[0, -1], [0, 1], [1, 0], [1, 1], [1, -1]]
                if case == 1:
                    neighbour_list = [[0, -1], [0, 1], [-1, 0], [-1, -1], [-1, 1]]
                if case == 2:
                    neighbour_list = [[-1, 0], [0, 1], [1, 0], [-1, 1], [1, 1]]
                if case == 3:
                    neighbour_list = [[0, -1], [1, 0], [-1, 0], [-1, -1], [1, -1]]
                for neighbour in neighbour_list:
                    neighbour[0] += self.grid_x
                    neighbour[1] += self.grid_y
                for neighbour in neighbour_list:
                    if neighbour[0] < 0:
                        neighbour[0] += self.cols
                    if neighbour[1] < 0:
                        neighbour[1] += self.rows
                    if neighbour[0] > self.cols - 1:
                        neighbour[0] -= self.cols
                    if neighbour[1] > self.rows - 1:
                        neighbour[1] -= self.rows
                for neighbour in neighbour_list:
                    try:
                        self.neighbours.append(grid[neighbour[1]][neighbour[0]])
                    except:
                        continue
            if nh == 3:  # hex
                case = random.randint(0, 1)
                if case == 0:
                    neighbour_list = [[-1, 1], [1, -1], [0, -1], [0, 1], [1, 0], [-1, 0]]
                if case == 1:
                    neighbour_list = [[1, 1], [-1, -1], [0, -1], [0, 1], [1, 0], [-1, 0]]
                for neighbour in neighbour_list:
                    neighbour[0] += self.grid_x
                    neighbour[1] += self.grid_y
                for neighbour in neighbour_list:
                    if neighbour[0] < 0:
                        neighbour[0] += self.cols
                    if neighbour[1] < 0:
                        neighbour[1] += self.rows
                    if neighbour[0] > self.cols - 1:
                        neighbour[0] -= self.cols
                    if neighbour[1] > self.rows - 1:
                        neighbour[1] -= self.rows
                for neighbour in neighbour_list:
                    try:
                        self.neighbours.append(grid[neighbour[1]][neighbour[0]])
                    except:
                        continue
            if nh == 4:  # promien
                if config.nbhR >= config.dx:
                    r = config.nbhR
                    neighbour_list = []
                    for i in range(int(0 - (r / self.dx)), int((r / self.dx))):
                        for j in range(int(0 - (r / self.dy)), int((r / self.dy))):
                            if i == 0 and j == 0:
                                continue
                            neighbour_list.append([i, j])
                    for neighbour in neighbour_list:
                        neighbour[0] += self.grid_x
                        neighbour[1] += self.grid_y
                    for neighbour in neighbour_list:
                        if neighbour[0] < 0:
                            neighbour[0] += self.cols
                        if neighbour[1] < 0:
                            neighbour[1] += self.rows
                        if neighbour[0] > self.cols - 1:
                            neighbour[0] -= self.cols
                        if neighbour[1] > self.rows - 1:
                            neighbour[1] -= self.rows
                    for neighbour in neighbour_list:
                        if math.sqrt(((neighbour[0] * self.dx + random.uniform(0, self.dx)) - self.x_sr) ** 2 + (
                                (neighbour[1] * self.dy + random.uniform(0, self.dy)) - self.y_sr) ** 2) < r:
                            try:
                                self.neighbours.append(grid[neighbour[1]][neighbour[0]])
                            except:
                                continue
        else:  # absorpcyjne
            if nh == 0:  # moore
                neighbour_list = [[1, 1], [-1, -1], [-1, 1], [1, -1], [0, -1], [0, 1], [1, 0], [-1, 0]]
                for neighbour in neighbour_list:
                    neighbour[0] += self.grid_x
                    neighbour[1] += self.grid_y

                for neighbour in neighbour_list:
                    if neighbour[0] < 0 or neighbour[1] < 0 or neighbour[0] > (self.cols - 1) or neighbour[1] > (
                            self.rows - 1):
                        neighbour_list.remove(neighbour)
                for neighbour in neighbour_list:
                    try:
                        self.neighbours.append(grid[neighbour[1]][neighbour[0]])
                    except:
                        continue
            if nh == 1:
                neighbour_list = [[0, -1], [0, 1], [1, 0], [-1, 0]]
                for neighbour in neighbour_list:
                    neighbour[0] += self.grid_x
                    neighbour[1] += self.grid_y
                for neighbour in neighbour_list:
                    if neighbour[0] < 0 or neighbour[1] < 0 or neighbour[0] > (self.cols - 1) or neighbour[1] > (
                            self.rows - 1):
                        neighbour_list.remove(neighbour)
                for neighbour in neighbour_list:
                    try:
                        self.neighbours.append(grid[neighbour[1]][neighbour[0]])
                    except:
                        continue
            if nh == 2:  # pentagonalne losowe
                case = random.randint(0, 3)
                if case == 0:
                    neighbour_list = [[0, -1], [0, 1], [1, 0], [1, 1], [1, -1]]
                if case == 1:
                    neighbour_list = [[0, -1], [0, 1], [-1, 0], [-1, -1], [-1, 1]]
                if case == 2:
                    neighbour_list = [[-1, 0], [0, 1], [1, 0], [-1, 1], [1, 1]]
                if case == 3:
                    neighbour_list = [[0, -1], [1, 0], [-1, 0], [-1, -1], [1, -1]]
                for neighbour in neighbour_list:
                    neighbour[0] += self.grid_x
                    neighbour[1] += self.grid_y

                for neighbour in neighbour_list:
                    if neighbour[0] < 0 or neighbour[1] < 0 or neighbour[0] > (self.cols - 1) or neighbour[1] > (
                            self.rows - 1):
                        neighbour_list.remove(neighbour)
                for neighbour in neighbour_list:
                    try:
                        self.neighbours.append(grid[neighbour[1]][neighbour[0]])
                    except:
                        continue
            if nh == 3:
                case = random.randint(0, 1)
                if case == 0:
                    neighbour_list = [[-1, 1], [1, -1], [0, -1], [0, 1], [1, 0], [-1, 0]]
                if case == 1:
                    neighbour_list = [[1, 1], [-1, -1], [0, -1], [0, 1], [1, 0], [-1, 0]]
                for neighbour in neighbour_list:
                    neighbour[0] += self.grid_x
                    neighbour[1] += self.grid_y
                for neighbour in neighbour_list:
                    if neighbour[0] < 0 or neighbour[1] < 0 or neighbour[0] > (self.cols - 1) or neighbour[1] > (
                            self.rows - 1):
                        neighbour_list.remove(neighbour)
                for neighbour in neighbour_list:
                    try:
                        self.neighbours.append(grid[neighbour[1]][neighbour[0]])
                    except:
                        continue
            if nh == 4:  # promien
                if config.nbhR >= config.dx:
                    r = config.nbhR
                    neighbour_list = []
                    for i in range(int(0 - (r / self.dx)), int((r / self.dx))):
                        for j in range(int(0 - (r / self.dy)), int((r / self.dy))):
                            if i == 0 and j == 0:
                                continue
                            neighbour_list.append([i, j])
                    for neighbour in neighbour_list:
                        neighbour[0] += self.grid_x
                        neighbour[1] += self.grid_y
                    for neighbour in neighbour_list:
                        if math.sqrt(((neighbour[0] * self.dx + random.uniform(0, self.dx)) - self.x_sr) ** 2 + (
                                (neighbour[1] * self.dy + random.uniform(0, self.dy)) - self.y_sr) ** 2) < r:
                            try:
                                self.neighbours.append(grid[neighbour[1]][neighbour[0]])
                            except:
                                continue

    def live_neighbours(self):
        count = 0
        for neighbour in self.neighbours:
            if neighbour.alive:
                count += 1
        self.alive_neighbours = count

    def get_neighbour_color(self):
        nbcollist = []
        for neighbour in self.neighbours:
            if neighbour.alive:
                nbcollist.append(neighbour.owncolor)
        occurence_count = Counter(nbcollist)
        self.alive_neighbours_color_list = nbcollist
        return occurence_count.most_common(1)[0][0]

    def neighbour_color_list(self):
        nbcollist = []
        for neighbour in self.neighbours:
            if neighbour.alive:
                nbcollist.append(neighbour.owncolor)
        self.alive_neighbours_color_list = nbcollist

    def calcEnergy(self):
        self.neighbour_color_list()
        energy = 0
        for nb in self.alive_neighbours_color_list:
            if nb != self.owncolor:
                energy += 1
        return energy

    def calcEnergyCol(self, color):
        self.neighbour_color_list()
        energy = 0
        for nb in self.alive_neighbours_color_list:
            if nb != color:
                energy += 1
        return energy

    def mc(self):
        self.neighbour_color_list()
        cbu = 0
        energy = 0
        for col in self.alive_neighbours_color_list:
            if self.energy > self.calcEnergyCol(col):
                cbu = col
                energy = self.calcEnergyCol(col)
        if energy != 0:
            self.owncolor = cbu
            self.energy = energy
            return 1

        if energy == 0:
            diffcols = []
            counter = 0
            for col in self.alive_neighbours_color_list:
                if self.owncolor == col:
                    counter += 1
                    continue
                diffcols.append(col)
            if counter < len(self.alive_neighbours_color_list):
                ran = random.uniform(0, 1)
                if ran<=math.exp(-(self.calcEnergyCol(diffcols[0])-self.energy)/config.kt):
                    self.owncolor = diffcols[0]
                    self.energy = self.calcEnergyCol(diffcols[0])
                    return 1
