"""
Class that represent the window of the game
"""
import pygame
import ctypes

from BoardBox import BoardBox
from Menu import Menu
from PlayerBox import PlayerBox

ctypes.windll.user32.SetProcessDPIAware()
true_res = (ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1))


class Window:

    def __init__(self, width, height):
        self.width, self.height = width, height
        self.full_screen = False
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill((25, 35, 45))
        self.menu = Menu(self, self.width, self.height)
        self.boardBox = None
        self.playerX = None
        self.playerO = None

    def loadBoxes(self):
        self.boardBox = BoardBox(self, (self.width - self.height + 5) / 2 + 2.5, 5, self.height - 10,
                                 self.height - 10)
        self.playerX = PlayerBox(self, 5, 10, (self.width - self.height + 5) / 2 - 10, self.height - 20)
        self.playerO = PlayerBox(self, (self.width - self.height + 5) / 2 + self.height + 1, 10,
                                 (self.width - self.height + 5) / 2 - 10,
                                 self.height - 20)

    def draw(self):
        self.boardBox.draw()
        self.playerX.color = (255, 0, 0)
        self.playerO.color = (0, 0, 255)
        self.playerX.draw()
        self.playerO.draw()

    def updateScreen(self):
        if self.full_screen:
            self.screen = pygame.display.set_mode((1366, 768))
            res = (1366, 768)

        else:
            self.screen = pygame.display.set_mode(true_res, pygame.FULLSCREEN)
            res = true_res
        self.full_screen = not self.full_screen
        self.width, self.height = res
        self.menu.resize(res)
