import pygame

class Cell:

    def __init__(self, value, row, col, width , height):
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.placeholder = 0
        self.selected = False

    # PRIVATE METHODS
    def __draw_placeholder(self, screen, x, y, font):
        text = font.render(str(self.placeholder), 1, (128, 128, 128))
        screen.blit(text, (x + 5, y + 5))

    def __draw_value(self, screen, x, y, font, color):
        text = font.render(str(self.value), 1, color)
        screen.blit(font.render(str(self.value), 1, color), (x + (self.width / 2 - text.get_width() / 2), y + (self.height / 2 - text.get_height() / 2)))

    # PUBLIC METHODS
    def draw(self, screen, font, color):
        gap = self.width
        x = self.col * gap
        y = self.row * gap

        if self.placeholder != 0 and self.value == 0:
            self.__draw_placeholder(screen, x, y, font)
        elif not(self.value == 0):
            self.__draw_value(screen, x, y, font, color)

        if self.selected:
            pygame.draw.rect(screen, (0, 0, 255), (x, y, gap, gap), 4)

    def visual_solve_draw(self, screen, font, valid=True):
        gap = self.width
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(screen, (255, 255, 255), (x, y, gap, gap), 0)

        text = font.render(str(self.value), 1, (0, 0, 0))
        screen.blit(text, (x + (self.width / 2 - text.get_width() / 2), y + (self.height / 2 - text.get_height() / 2)))

        if valid:
            pygame.draw.rect(screen, (0, 255, 0), (x, y, gap, gap), 4)
        else:
            pygame.draw.rect(screen, (255, 0, 0), (x, y, gap, gap), 4)

    def set_value(self, value):
        self.value = value

    def set_placeholder(self, value):
        self.placeholder = value
