"""
Class that represents the Board GUI
"""
from Box import Box
from CellBox import CellBox
from Observer import Observer
import pygame


class BoardBox(Box, Observer):
    rows = cols = 16  # by default

    def __init__(self, window, x, y, width, height):
        super(BoardBox, self).__init__(window, x, y, width, height)  #
        self.board = []
        self.color = (25, 35, 45)
        self.cardImage = None
        self.last = None

    def setSize(self, row, col):
        self.rows = row
        self.cols = col

    # building the board by drawing all its cells and saving the data as we will need it
    def build(self):
        thick = 2 * self.thickness
        width = height = int((self.width - 2 * self.thickness) / self.rows)
        for y in range(self.cols):
            row = []
            for x in range(self.rows):
                cell = CellBox(self.window, self.x + thick + x * width, self.y + thick + y * height, width, height)
                row += [cell]
                cell.draw()
            self.board += [row]

    def getBoard(self):
        return self.board

    def getCellWidth(self):
        return (self.width - 2 * self.thickness) / self.rows  # the length of a square in the board

    # method for converting the cell coordinates to its position in the grid
    def getCellPosition(self, x, y):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col].onBox(x, y):
                    return row, col
        return -1, -1

    def drawCardInfo(self, card, condition):
        if condition:
            pygame.image.save(self.window.screen, "screen.png")
        url = card.imageURL
        info = pygame.image.load(url).convert()
        info = pygame.transform.scale(info, (int(self.window.width / 3), int(self.window.height / 3))).convert()
        self.cardImage = info
        pygame.draw.rect(self.window.screen, (0, 0, 0),
                         (self.window.width / 3 + 5, self.window.height / 3 + 5,
                          self.window.width / 3 - 5, self.window.height / 3 - 5), 10)

        self.window.screen.blit(info, (self.window.width / 3, self.window.height / 3))

        pygame.display.update()

    def animateSequence(self, arr):
        pygame.time.set_timer(pygame.USEREVENT, 100)
        cell, image, i = None, None, 0
        for inner in arr:
            for seq in inner:
                if len(seq) >= 3:
                    running = True
                    while running:
                        for event in pygame.event.get():
                            if event.type == pygame.USEREVENT:
                                if cell is not None:
                                    if cell not in self.last:
                                        cell.changeImage(2)
                                    else:
                                        cell.changeImage(1)
                                if i == len(seq):
                                    running = False
                                    continue
                                try:
                                    x, y = seq[i]
                                    cell = self.board[x][y]
                                    cell.insertHighlighted((0, 0, 0))
                                except:
                                    print("Sequence animation error")
                                    running = False
                                    break
                                i += 1

    def hiddenCardsAnimation(self, card):
        pygame.time.set_timer(pygame.USEREVENT, 50)
        iteration = 1
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    if iteration == 1:
                        pygame.image.save(self.window.screen, "img/screen.png")
                    elif iteration == 2:
                        self.drawCardInfo(card, True)
                        pygame.time.set_timer(pygame.USEREVENT, 0)
                    iteration += 1
                if event.type is pygame.MOUSEBUTTONDOWN and event.button == 1:
                    (x, y) = pygame.mouse.get_pos()
                    if self.window.width / 3 < x < 2 * self.window.width / 3:
                        if self.window.height / 3 < y < 2 * self.window.height / 3:
                            screen = pygame.image.load("img/screen.png").convert()
                            self.window.screen.blit(screen, (0, 0))
                            pygame.time.set_timer(pygame.USEREVENT, 50)
                            running = False
        self.closeCardInfo(card)


    def closeCardInfo(self, card):
        pygame.time.set_timer(pygame.USEREVENT, 50)
        iteration = 1
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    if iteration == 1:
                        info = pygame.transform.scale(self.cardImage, (int(self.window.width / 3) - 20,
                                                        int(self.window.height / 3) - 20))
                        self.window.screen.blit(info, (self.window.width / 3 + 10, self.window.height / 3 + 10))
                    elif iteration == 2:
                        self.drawCardInfo(card, False)
                    else:
                        running = False
                        screen = pygame.image.load("img/screen.png").convert()
                        self.window.screen.blit(screen, (0, 0))
                    pygame.display.update()
                    iteration += 1

    def update(self, observable):
        for x in range(self.rows):
            for y in range(self.cols):
                if observable.board[x][y].hasElement() and self.board[x][y].isEmpty():
                    if self.last is not None:
                        for last in self.last:
                            last.changeImage(2)
                    self.board[x][y].insert(observable.board[x][y].element, 1)
                    self.last = [self.board[x][y]]
                elif not observable.board[x][y].hasElement() and not self.board[x][y].isEmpty():
                    self.board[x][y].remove()
                elif observable.board[x][y].hasElement() and not self.board[x][y].isEmpty():
                    if not observable.board[x][y].element.image == self.board[x][y].elemImage:
                        self.board[x][y].insert(observable.board[x][y].element, 3)
                        self.last += [self.board[x][y]]
