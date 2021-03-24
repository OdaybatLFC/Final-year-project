"""
Controller class that gets information from the view and the model
"""
import pygame
import glob

from Element import Element
from Players import *
from Window import Window
from Deck import Deck
from Board import Board

class Game:
    pygame.init()

    def __init__(self):
        self.window = Window(1366, 768)
        self.players = {}
        self.board = Board(16, 16)
        self.deck = Deck()
        self.stats = []

    # loading the images as python object
    def loadElements(self):
        elements = {}
        size = int(self.window.boardBox.getCellWidth()) - 1
        images = glob.glob("img/elements/*.png")
        dictionary = {}
        for image in images:
            elem = pygame.image.load(image)
            elem = pygame.transform.scale(elem, (size, size))
            dictionary[image[13:][:-4]] = elem
        for name in ["circle", "cross", "square", "triangle"]:
            elements[name] = Element(dictionary[name], name)
            elements[name].highlighted = dictionary[name + "H"]
            elements[name].last = dictionary[name + "B"]
        return elements

    def notifyAndUpdate(self):
        self.board.notifyObservers()
        self.players["current"].notifyObservers()
        self.players["next"].notifyObservers()
        self.stats[0] += 1

    def start(self, arg):
        menu = self.window.menu
        menu.draw(arg)
        running, run, status = True, False, None
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type is pygame.MOUSEBUTTONDOWN and event.button == 1:
                    status = menu.update()
                    if status in [1, 2]:
                        run, running = True, False
                    if status == 0:
                        running = False
                        pygame.quit()
        if run and status is not None:
            self.run(status)

    def getAI(self, player, arg):
        if self.window.menu.choices["AI" + arg] == "Random":
            return RandomAI(player)
        elif self.window.menu.choices["AI" + arg] == "M1":
            return MiniMax(player, 1)
        elif self.window.menu.choices["AI" + arg] == "M2":
            return MiniMax(player, 2)
        else:
            return MCTS(player)

    def initialize(self):
        window = self.window
        menu = window.menu
        self.board.removeObservers()
        self.deck.loadCards()
        self.board.loadBoard()
        window.loadBoxes()
        window.boardBox.setSize(self.board.rows, self.board.cols)
        self.board.insertHiddenCards(self.deck.hidden)
        elements = self.loadElements()
        if menu.choices["mode"] == "Multiplayer":
            self.players["current"] = Player("X")
            self.players["next"] = Player("O")
        elif menu.choices["mode"] == "vs AI":
            if menu.choices["Player"] == "X":
                self.players["current"] = Player("X")
                self.players["next"] = self.getAI("O", "")
            else:
                self.players["next"] = Player("O")
                self.players["current"] = self.getAI("X", "")
        else:
            self.players["current"] = self.getAI("X", "1")
            self.players["next"] = self.getAI("O", "2")
        self.players["current"].opponent = self.players["next"]
        self.players["next"].opponent = self.players["current"]
        self.players["current"].initialize(elements)
        self.players["next"].initialize(elements)
        self.players["current"].addObserver(window.playerX)
        self.players["next"].addObserver(window.playerO)
        self.board.addObserver(window.boardBox)
        window.draw()
        self.window.playerX.isActive = False
        self.players["current"].notifyObservers()
        self.players["next"].notifyObservers()
        self.stats = [0, {"X": [], "O": []}, time.time()]

    @staticmethod
    def checkWin(player):
        if player.score >= 100:
            return True
        return False

    # method that runs the game
    def run(self, arg):
        if arg == 1:
            self.initialize()
        else:
            screen = pygame.image.load("img/screen.png").convert()
            self.window.screen.blit(screen, (0, 0))
            pygame.display.update()
        boardBox = self.window.boardBox
        currentCell, lastCell, currentCard, lastCard = None, None, None, None
        running, camo, camoType = True, False, None
        start_time, end_time = time.time(), 0
        while running:
            playerBox = self.window.playerX
            if type(self.players["current"]) == Player:
                if self.players["current"].id == "X":
                    playerBox = self.window.playerX
                else:
                    playerBox = self.window.playerO
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.image.save(self.window.screen, "img/screen.png")
                        self.start(4)
                        running = False
                        break

                if type(self.players["current"]) == Player:
                    if event.type is pygame.MOUSEBUTTONDOWN and event.button == 1:
                        (x, y) = pygame.mouse.get_pos()
                        if boardBox.onBox(x, y):
                            (row, col) = boardBox.getCellPosition(x, y)
                            if (row, col) != (-1, -1):
                                currentCell = self.board.getBoard()[row][col]
                                if not currentCell.hasElement():
                                    self.players["current"].playMove(currentCell)

                                    if currentCell.hidden is not None:
                                        boardBox.board[row][col].animate(2)

                                    self.board.notifyObservers()

                                    oneMore = None
                                    if currentCell.hidden is not None:
                                        boardBox.hiddenCardsAnimation(currentCell.hidden)
                                        oneMore = currentCell.hidden.invoke([self.players["current"],
                                                                             self.players["next"]], self.board,
                                                                            currentCell, self.deck)
                                        currentCell.setHidden(None)

                                    if currentCell.hasElement():
                                        score, three, four, five, full_house = self.board.checkSeq(row, col)
                                        boardBox.animateSequence([three, four, five, full_house])
                                        self.players["current"].updateScore(score)
                                        self.players["current"].updateStat(len(three))
                                        self.players["current"].drawCard([four, five, full_house], self.deck)

                                    if self.checkWin(self.players["current"]):
                                        self.window.screen.fill((25, 35, 45))
                                        running = False
                                        break

                                    self.notifyAndUpdate()
                                    end_time = time.time()
                                    self.stats[1][self.players["current"].id] += [end_time - start_time]
                                    start_time = end_time
                                    if camo:
                                        self.players["current"].__class__ = camoType
                                        camo = False

                                    if oneMore is None:
                                        self.players["current"], self.players["next"] = self.players["next"], \
                                                                                        self.players["current"]
                                    currentCell = boardBox.getBoard()[row][col]

                        if playerBox.cardBox.onBox(x, y):
                            for i in range(len(playerBox.cards)):
                                cardBox = playerBox.cards[i]
                                if cardBox.card is not None:
                                    if cardBox.onBox(x, y):
                                        arg = cardBox.card.activate([self.players["current"], self.players["next"]],
                                                                    self.board, currentCell, self.deck)
                                        cardBox.animate(arg)
                                        if type(cardBox.card) == Block:
                                            boardBox.drawCardInfo(cardBox.card, False)
                                        if arg in [1, 2, 3, 4]:
                                            cardBox.remove()
                                            cardBox.restore()
                                            self.players["current"].removeCard(i)

                                            if arg == 2:
                                                camoType = type(self.players["next"])
                                                self.players["next"].__class__ = Player
                                                camo = True
                                            if arg == 3:
                                                self.players["current"].initials, self.players["next"].initials = \
                                                    self.players["next"].initials, \
                                                    self.players["current"].initials

                                            self.players["current"], self.players["next"] = self.players["next"], \
                                                                                            self.players["current"]
                                            self.notifyAndUpdate()
                                            end_time = time.time()
                                            self.stats[1][self.players["current"].id] += [end_time- start_time]
                                            start_time = end_time

                                        break

                else:
                    oneMore = None
                    cell = self.players["current"].playMove(self.board)
                    if cell.hidden is not None:
                        boardBox.board[cell.x][cell.y].animate(2)
                        self.board.notifyObservers()
                        oneMore = cell.hidden.invoke([self.players["current"], self.players["next"]],
                                                     self.board, cell, self.deck)
                        cell.setHidden(None)
                    score, three, four, five, full_house = self.board.checkSeq(cell.x, cell.y)
                    boardBox.animateSequence([three, four, five, full_house])
                    self.players["current"].updateScore(score)

                    self.players["current"].updateStat(len(three))
                    self.players["current"].drawCard([four, five, full_house], self.deck)

                    self.notifyAndUpdate()
                    end_time = time.time()
                    self.stats[1][self.players["current"].id] += [end_time- start_time]
                    start_time = end_time
                    if self.checkWin(self.players["current"]):
                        running = False
                        break

                    if oneMore is None:
                        self.players["current"], self.players["next"] = self.players["next"], \
                                                                        self.players["current"]

                if event.type is pygame.MOUSEMOTION:
                    (x, y) = pygame.mouse.get_pos()
                    if boardBox.onBox(x, y):
                        (row, col) = boardBox.getCellPosition(x, y)
                        if (row, col) != (-1, -1):
                            currentCell = boardBox.getBoard()[row][col]
                            if currentCell.isEmpty():
                                currentCell.highlight()
                        if currentCell != lastCell and lastCell is not None:
                            try:
                                lastCell.restore()
                            except:
                                pass
                        lastCell = currentCell
                    else:
                        currentCell = None
                        if lastCell is not None:
                            try:
                                lastCell.restore()
                            except:
                                pass

                    if type(self.players["current"]) == Player:
                        if currentCard is not None:
                            if not currentCard.onBox(x, y) and currentCard.highlighted:
                                currentCard.restore()
                        if playerBox.cardBox.onBox(x, y):
                            for cardBox in playerBox.cards:
                                if cardBox.onBox(x, y):
                                    if not cardBox.highlighted and not cardBox.isEmpty():
                                        currentCard = cardBox
                                        currentCard.highlight()
                                        boardBox.drawCardInfo(currentCard.card, True)

        if self.checkWin(self.players["current"]):
            self.stats[2] = round(time.time() - self.stats[2])
            self.stats += [[self.players["current"], self.players["next"]]]
            self.window.menu.winMessage(self.stats)
            self.start(3)


# Running the application
game = Game()
game.start(0)
