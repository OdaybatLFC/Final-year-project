"""
Class the displays the player information
"""
import pygame

from Box import Box
from CardBox import CardBox
from Observer import Observer


class PlayerBox(Box, Observer):

    def __init__(self, window, x, y, width, height):
        super(PlayerBox, self).__init__(window, x, y, width, height)
        self.isActive = True
        margin = self.thickness + 5
        self.infoBox = Box(self.window, self.x + margin, self.y + margin, self.width - 2 * margin, self.height / 6)
        self.cardBox = Box(self.window, self.x + margin, self.height / 5 + margin, self.width - 4 * self.thickness,
                           self.height / 2)
        self.unknownBox = Box(self.window, self.x + margin, 3 * self.height / 4, self.width - 2 * margin,
                              self.height / 4)
        self.cards = []

    def build(self):
        size = int(self.width / len("Current") / 2)
        currElemFont = pygame.font.SysFont("monospace", size)
        currElem = currElemFont.render("Current", 1, (255, 255, 0))
        self.drawCards()
        self.window.screen.blit(currElem, (self.x + size*2, self.unknownBox.height * 2 / 3 + self.unknownBox.y))
        currElem2 = currElemFont.render("element:", 1, (255, 255, 0))
        self.window.screen.blit(currElem2, (self.x + size*2,
                                            self.unknownBox.height * 2 / 3 + self.unknownBox.y
                                            + currElem.get_rect().height))

    def drawCards(self):
        margin = self.cardBox.width / 40
        i = 1
        for x in [margin * 7, self.cardBox.width / 2 + margin * 2]:
            for y in [margin * 4, self.cardBox.height / 3 + margin * 4, 2 * self.cardBox.height / 3 + margin * 4]:
                self.cards += [CardBox(self.cardBox.window, self.cardBox.x + x, self.cardBox.y + y - 10,
                                       3 * self.cardBox.width / 8 - margin * 4, self.cardBox.height / 3 - margin * 4)]
                i += 1
        for card in self.cards:
            card.clear((35, 45, 55))

    def drawCircle(self, color):
        pygame.draw.circle(self.window.screen, color, (int(self.x+self.width/2), int(self.y+4*self.height/5)),
                           int(self.width/8))

    # method for activating the player box
    def start(self):
        self.isActive = True
        highlightBox = self.highlight()
        highlightBox.color = (45, 55, 65)
        highlightBox.draw()
        self.drawCircle(self.color)

    # opposite of start
    def stop(self):
        self.isActive = False
        highlightBox = self.highlight()
        highlightBox.color = (25, 35, 45)
        highlightBox.draw()
        self.drawCircle((25, 35, 45))

    # method for indicating whose turn it is
    def highlight(self):
        x = self.x + self.thickness
        y = self.y + self.thickness
        width = self.width - 2 * self.thickness
        height = self.height - 2 * self.thickness
        highlightBox = Box(self.window, x, y, width, height)
        highlightBox.thickness = 8
        return highlightBox

    def update(self, observable):
        self.infoBox.clear((25, 35, 45))
        if not self.isActive:
            self.start()
        else:
            self.stop()

        cards = observable.cards
        for i in range(len(cards)):
            cardBox = self.cards[i]
            if cards[i] is not None and self.cards[i].isEmpty():
                self.cards[i].insert(cards[i])
            if not cardBox.isEmpty() and cards[i] is None:
                cardBox.remove()
                cardBox.clear((35, 45, 55))

        if observable.booster > 0:
            booster = "(x2)"
        else:
            booster = ""

        name = "Player " + observable.id + observable.initials
        size = int(self.width / len(name)) + 4
        nameFont = pygame.font.SysFont("monospace", size)
        name = nameFont.render(name, 1, (255, 255, 0))
        scoreFont = pygame.font.SysFont("monospace", size-5)
        score = scoreFont.render("Score: " + str(observable.score) + booster, 1, (255, 255, 0))
        w, h = name.get_rect().width, name.get_rect().height
        self.window.screen.blit(name, (self.x + self.width / 2 - w/2, self.y + 20))
        self.window.screen.blit(score, (self.x + self.width / 2 - w/2, self.y + h + 20))
        width = observable.currElem.image.get_rect().width
        self.window.screen.blit(observable.currElem.highlighted, (self.x + self.width / 2 + 20,
                                                                  self.height - width - 15))

        pygame.display.update()
