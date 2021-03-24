"""
File for representing all cards in the game
"""

import random


class Card:

    def __init__(self, name, url):
        self.name = name
        self.imageURL = url

    def invoke(self, players, board, cell, deck):
        pass


class Special(Card):

    def __init__(self, name, url, level, prob):
        super().__init__(name, url)
        self.level = level
        self.prob = prob

    def block(self, players, i):
        if players[i].block and type(self) is not Block:
            print("card blocked")
            players[i].removeBlock()
            if i == 1:
                i = 0
            else:
                i = 1
            return 1 + self.block(players, i)
        return 0

    def activate(self, players, board, cell, deck):
        block = self.block(players, 1)
        if block % 2 == 1:
            return 4
        return self.invoke(players, board, cell, deck)

class Hidden(Card):

    def __init__(self, name, url):
        super().__init__(name, url)


class SmallDonation(Hidden):

    def invoke(self, players, board, cell, deck):
        players[0].updateScore(2)

class SmallSteal(Hidden):

    def invoke(self, players, board, cell, deck):
        players[0].updateScore(-2)

class HighFive(Hidden):

    def invoke(self, players, board, cell, deck):
        players[0].updateScore(5)

class TakeFive(Hidden):

    def invoke(self, players, board, cell, deck):
        players[0].updateScore(-5)

class Jackpot(Hidden):

    def invoke(self, players, board, cell, deck):
        players[0].updateScore(10)

class WhereDidMyElementsGo(Hidden):

    def invoke(self, players, board, cell, deck):
        if players[0].id == "X":
            color = "red"
        else:
            color = "blue"
        cells = board.getElements(color)
        for i in range(2):
            try:
                currentCell = random.choice(cells)
                cells.remove(currentCell)
                currentCell.remove()
            except:
                print("Index out of bound!")

class Bomb(Hidden):

    def invoke(self, players, board, cell, deck):
        cell.remove()
        vectors = [(0, 0), (0, 1), (0, -1),
                   (1, 0), (1, 1), (1, -1),
                   (-1, 0), (-1, 1), (-1, -1)]
        for (rx, ry) in vectors:
            try:
                board.getBoard()[cell.x+rx][cell.y+ry].remove()
            except:
                print("Index out of bound!")

class BadLuck(Hidden):

    def invoke(self, players, board, cell, deck):
        cell.remove()

class Hoover(Hidden):

    def invoke(self, players, board, cell, deck):
        red = board.getElements("red")
        blue = board.getElements("blue")
        for i in range(3):
            try:
                redCell = random.choice(red)
                blueCell = random.choice(blue)
                redCell.remove()
                blueCell.remove()
                red.remove(redCell)
                blue.remove(blueCell)
            except:
                print("Index out of bound!")

class OneMore(Hidden):

    def invoke(self, player, board, cell, deck):
        return 1

class Reverse(Hidden):

    def invoke(self, players, board, cell, deck):
        players[0].swap()


class Defense(Hidden):

    def invoke(self, players, board, cell, deck):
        players[0].insertCard(Block("block", "img/cards/17.png", 1, 0.25))

class SpecialGift(Hidden):

    def invoke(self, players, board, cell, deck):
        players[0].insertCard(deck.draw(1))

class MoreSpecial(Hidden):

    def invoke(self, players, board, cell, deck):
        players[0].insertCard(deck.draw(2))

class Wow(Hidden):

    def invoke(self, players, board, cell, deck):
        players[0].insertCard(deck.draw(3))

class Swapper(Hidden):

    def invoke(self, players, board, cell, deck):
        red = board.getElements("red")
        blue = board.getElements("blue")
        for i in range(3):
            try:
                rand = random.choice(red)
                rand2 = random.choice(blue)
                elem1 = rand.element
                elem2 = rand2.element
                rand.insert(elem2)
                rand2.insert(elem1)
            except:
                print("Index out of bound!")

class Block(Special):

    def __init__(self, name, url, level, prob):
        super().__init__(name, url, level, prob)
        self.active = False

    def invoke(self, players, board, cell, deck):
        self.active = not self.active
        players[0].updateBlock()
        if self.active:
            self.imageURL = "img/cards/17(1).png"
        else:
            self.imageURL = "img/cards/17.png"

class Empty(Special):

    def invoke(self, players, board, cell, deck):
        return 1

class Take(Special):

    def invoke(self, players, board, cell, deck):
        players[0].updateScore(5)
        return 1

class Remove(Special):

    def invoke(self, players, board, cell, deck):
        red = board.getElements("red")
        blue = board.getElements("blue")
        if len(red) > 1 and len(blue) > 1:
            for i in range(2):
                redCell = random.choice(red)
                blueCell = random.choice(blue)
                redCell.remove()
                blueCell.remove()
                red.remove(redCell)
                blue.remove(blueCell)
            return 1
        return 0

class Camouflage(Special):

    def invoke(self, players, board, cell, deck):
        # players[2].__class__ = Player
        return 2

class Booster(Special):

    def invoke(self, players, board, cell, deck):
        players[0].booster = 5
        return 1

class Steal(Special):

    def invoke(self, players, board, cell, deck):
        players[1].updateScore(-5)
        players[0].updateScore(5)
        return 1

class RobTheBank(Special):

    def invoke(self, players, board, cell, deck):
        players[1].updateScore(-10)
        players[0].updateScore(10)
        return 1

class Clean(Special):

    def invoke(self, players, board, cell, deck):
        cells = board.getElements(players[1].currElem.color)
        if len(cells) < 3:
            return 0
        for i in range(3):
            currentCell = random.choice(cells)
            currentCell.remove()
            cells.remove(currentCell)
        return 1

class ScoreSwap(Special):

    def invoke(self, players, board, cell, deck):
        players[0].score, players[1].score = players[1].score, players[0].score
        return 1

class PlayersSwap(Special):

    def invoke(self, players, board, cell, deck):
        t1 = type(players[0])
        t2 = type(players[1])
        players[1].__class__ = t1
        players[0].__class__ = t2
        return 3
