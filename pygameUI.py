import pygame
from abc import ABC, abstractmethod


class Button(ABC):
    def __init__(self, pos, width, height, function=None):
        self.pos = pos
        self.width = width
        self.height = height
        self.function = function

    @abstractmethod
    def draw(self, screen):
        pass

    def clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = event.pos
                if self.pos[0] <= x <= self.pos[0] + self.width and self.pos[1] <= y <= self.pos[1] + self.height:
                    if self.function:
                        self.function()


class TextButton(Button):
    def __init__(self, pos, width, height, text, colour, font_size, font_colour=(0, 0, 0), function=None):
        super().__init__(pos, width, height, function)
        self.text = text
        self.colour = colour
        self.font_size = font_size
        self.font_colour = font_colour
        self.font = pygame.font.SysFont("Calibre", self.font_size)

    def draw(self, screen):
        # fill
        pygame.draw.rect(screen, self.colour, (self.pos[0], self.pos[1], self.width, self.height))
        # border
        pygame.draw.rect(screen, "black", (self.pos[0], self.pos[1], self.width, self.height), 1)
        text = self.font.render(self.text, True, self.font_colour)
        text_surface = self.font.render(self.text, True, self.font_colour)
        text_width, text_height = text_surface.get_size()
        text_pos = (self.pos[0] + (self.width - text_width) // 2,
                    self.pos[1] + (self.height - text_height) // 2)
        screen.blit(text, text_pos)


class IconButton(Button):
    def __init__(self, pos, width, height, image_path, function=None):
        super().__init__(pos, width, height, function)
        self.width = width
        self.height = height
        self.image_path = image_path
        self.image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(self.image, (width, height))

    def draw(self, screen):
        screen.blit(self.image, self.pos)

    def update_image(self):
        self.image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
