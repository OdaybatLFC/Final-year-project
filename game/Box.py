"""
Abstract class the represents an empty box that will
be placed in the window.
"""
import pygame


class Box(object):

    def __init__(self, window, x, y, width, height):
        self.window = window
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.thickness = 5  # border thickness dy default
        self.color = (25, 35, 45)
        self.visible = False

    # clear the window with the specified color (i.e make it blank)
    def clear(self, color):
        pygame.draw.rect(self.window.screen, color, (self.x, self.y, self.width, self.height), 0)
        self.visible = False
        pygame.display.flip()

    # fixed method
    def paint(self):
        pygame.draw.rect(self.window.screen, self.color, (self.x, self.y, self.width, self.height), self.thickness)
        self.visible = True

    # abstract method
    def build(self):
        pass

    # Template Method Design Pattern
    def draw(self):
        self.paint()
        self.build()
        pygame.display.flip()

    # check if user mouse cursor is on the box
    def onBox(self, x, y):
        if self.x < x < self.width + self.x and self.y < y < self.height + self.y:
            return True
        return False

    # method for highlighting the box
    def highlight(self):
        t = self.thickness
        pygame.draw.rect(self.window.screen, self.color, (self.x + t, self.y + t, self.width - t, self.height - t), 0)
        pygame.display.update()
