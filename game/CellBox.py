"""
Class that represents each cell GUI
"""
import pygame
from Box import Box


class CellBox(Box):

    def __init__(self, window, x, y, width, height):
        super(CellBox, self).__init__(window, x, y, width, height)  #
        self.thickness = 1
        self.color = (127, 127, 127)
        self.elemImage = None
        self.highImage = None
        self.lastImage = None

    # check if cell is empty (i.e has no elements)
    def isEmpty(self):
        if self.elemImage is None:
            return True
        return False

    def build(self):
        z = self.thickness
        pygame.draw.rect(self.window.screen, (195, 195, 195), (self.x + z, self.y + z, self.width - z, self.height - z),
                         0)

    def changeImage(self, arg):
        if arg == 1:
            img = self.lastImage
        else:
            img = self.elemImage
        try:
            self.window.screen.blit(img, (self.x + self.thickness, self.y + self.thickness))
        except:
            pass
        pygame.display.update()

    # insert an element in the cell
    def insert(self, element, arg):
        self.elemImage = element.image
        self.highImage = element.highlighted
        self.lastImage = element.last
        self.animate(arg)
        self.thickness = 1
        self.changeImage(1)
        pygame.display.update()

    def insertHighlighted(self, color):
        pygame.draw.rect(self.window.screen, color, (self.x + self.thickness, self.y + self.thickness,
                                                     self.width-self.thickness*2, self.height-self.thickness*2),
                                                      self.thickness*2)
        pygame.display.update()

    def remove(self):
        self.elemImage = None
        self.animate(3)
        self.build()

    # restoring the cell in its current original state
    def restore(self):
        if self.isEmpty():
            self.thickness = 1
            self.build()
            pygame.display.update()
            # self.fill(self.fillColor)

    def animate(self, arg):
        z = self.thickness
        if arg in [1, 3]:
            pygame.time.set_timer(pygame.USEREVENT, 50)
        elif arg == 2:
            pygame.time.set_timer(pygame.USEREVENT, 100)
        iteration = 1
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    if arg == 1:
                        if iteration in [1, 3]:
                            elem = pygame.transform.scale(self.elemImage, (int(self.width) - 2, int(self.height) - 2))
                            self.window.screen.blit(elem, (self.x + 2, self.y + 2))
                            pygame.display.update()
                        elif iteration in [2, 4]:
                            self.window.screen.blit(self.elemImage, (self.x + 1, self.y + 1))
                            pygame.display.update()
                        else:
                            running = False
                    elif arg == 2:
                        if iteration == 1:
                            pygame.draw.rect(self.window.screen, (150, 195, 95),
                                             (self.x + 1, self.y + 1, self.width - 1, self.height - 1), 0)
                        if iteration == 2:
                            pygame.draw.rect(self.window.screen, (150, 95, 45),
                                             (self.x + 1, self.y + 1, self.width - 1, self.height - 1), 0)
                        if iteration == 3:
                            pygame.draw.rect(self.window.screen, (150, 195, 95),
                                             (self.x + 1, self.y + 1, self.width - 1, self.height - 1), 0)
                        if iteration == 4:
                            running = False
                        pygame.display.update()
                    elif arg == 3:
                        if iteration == 1:
                            pygame.draw.rect(self.window.screen, (100, 100, 100),
                                             (self.x + z, self.y + z, self.width - z, self.height - z), 0)
                            pygame.display.update()
                        else:
                            running = False
                    iteration += 1
