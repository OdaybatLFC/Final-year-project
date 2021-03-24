"""
Class that represents the player's cards GUI
"""

import pygame
from Box import Box


class CardBox(Box):

    def __init__(self, window, x, y, width, height):
        super(CardBox, self).__init__(window, x, y, width, height)
        self.thickness = 0
        self.card = None
        self.highlighted = False

    def highlight(self):
        pygame.image.save(self.window.screen, "img/screen.png")
        color = tuple(map(lambda i, j: i - j, self.color, (30, 30, 30)))
        self.clear(color)
        self.highlighted = True

    def isEmpty(self):
        if self.card is None:
            return True
        return False

    def insert(self, card):
        self.card = card
        if card.level == 1:
            self.color = (232, 236, 147)
        elif card.level == 2:
            self.color = (214, 130, 73)
        else:
            self.color = (116, 45, 45)
        self.clear(self.color)

    def remove(self):
        self.card = None
        self.color = (35, 45, 55)
        self.clear(self.color)

    def animate(self, arg):
        pygame.time.set_timer(pygame.USEREVENT, 100)
        iteration = 1
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    if arg == 0:
                        if iteration == 1:
                            self.resize(-5)
                        elif iteration == 2:
                            self.resize(10)
                        else:
                            self.resize(-5)
                            running = False
                    else:
                        if iteration == 1:
                            self.move(5, -10)
                        elif iteration == 2:
                            self.move(-5, 10)
                            running = False
                    iteration += 1

    def resize(self, i):
        self.clear((25, 35, 45))
        self.x += i
        self.clear(self.color)

    def move(self, x, y):
        self.clear((25, 35, 45))
        self.x += x
        self.y += x
        self.width += y
        self.height += y
        self.clear(self.color)

    def restore(self):
        self.highlighted = False
        screen = pygame.image.load("screen.png").convert()
        self.window.screen.blit(screen, (0, 0))
        self.clear(self.color)
