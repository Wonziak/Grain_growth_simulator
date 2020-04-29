import pygame

vec = pygame.math.Vector2


class Button:
    def __init__(self, surface, x, y, width, height, state='', id='', function=0, bgcolor=(255, 255, 255), border=True,
                 border_width=2,
                 bordercolor=(0, 0, 0), hovercolor=(255, 255, 255),
                 text=None, font_name='arial', text_size=20, text_color=(0, 0, 0), bold_text=True):
        self.type = 'button'
        self.x = x
        self.y = y
        self.pos = vec(x, y)
        self.width = width
        self.height = height
        self.surface = surface
        self.image = pygame.Surface((width, height))
        self.image2 = pygame.Surface((0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        self.state = state
        self.id = id
        self.function = function
        self.bgcolor = bgcolor
        self.hovercolor = hovercolor
        self.border = border
        self.border_width = border_width
        self.bordercolor = bordercolor
        self.text = text
        self.font_name = font_name
        self.text_size = text_size
        self.text_color = text_color
        self.bold_text = bold_text
        self.hovered = False

    def update(self, pos):
        if self.mouse_hovering(pos):
            self.hovered = True
        else:
            self.hovered = False

    def updatepos(self, width):
        self.x = width

    def draw(self):
        if self.border:
            self.image.fill(self.bordercolor)
            if self.hovered:
                pygame.draw.rect(self.image, self.hovercolor, (
                    self.border_width, self.border_width, self.width - (self.border_width * 2),
                    self.height - (self.border_width * 2)))
            else:
                pygame.draw.rect(self.image, self.bgcolor, (
                    self.border_width, self.border_width, self.width - (self.border_width * 2),
                    self.height - (self.border_width * 2)))
        else:
            self.image.fill(self.bgcolor)
        if len(self.text) > 0:
            self.show_text()
        self.surface.blit(self.image, self.pos)

    def click(self):
        if self.function != 0 and self.hovered:
            self.function()

    def show_text(self):
        font = pygame.font.SysFont(self.font_name, self.text_size, bold=self.bold_text)
        text = font.render(self.text, False, self.text_color)
        size = text.get_size()
        x, y = self.width // 2 - (size[0] // 2), self.height // 2 - (size[1] // 2)
        pos = vec(x, y)
        self.image.blit(text, pos)

    def mouse_hovering(self, pos):
        if self.pos[0] < pos[0] < self.pos[0] + self.width:
            if self.pos[1] < pos[1] < self.pos[1] + self.height:
                return True
        else:
            return False
