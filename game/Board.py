"""
Class representing the board and its data
"""


from Cell import Cell
from Observable import Observable
import random
from Element import Element


class Board(Observable):

    def __init__(self, rows, cols):
        super(Board, self).__init__()
        self.rows = rows
        self.cols = cols
        self.board = []

    # loading the board with empty cells
    def loadBoard(self):
        board = []
        for y in range(self.rows):
            row = []
            for x in range(self.cols):
                row += [Cell(y, x)]
            board += [row]
        self.board = board

    # inserting hidden cards in the board
    def insertHiddenCards(self, cards):
        rows = int(self.rows/4)
        cols = int(self.cols/4)
        for rx in range(4):
            for ry in range(4):
                x = random.choice(list(range(rows*rx, rows + rows*rx)))
                y = random.choice(list(range(cols*ry, cols + cols*ry)))
                card = random.choice(cards)
                self.board[x][y].setHidden(card)
                cards.remove(card)

    # method that returns all the cells that have elements from same color on the board
    def getElements(self, color):
        cells = []
        for x in range(self.rows):
            for y in range(self.cols):
                cell = self.board[x][y]
                if cell.hasElement():
                    if cell.element.color == color:
                        cells += [cell]
        return cells

    @staticmethod
    def removeEmpty(array):
        while [] in array:
            array.remove([])
        for i in range(len(array)):
            array[i] = sorted(array[i], key=lambda x: x[0])
            array[i] = sorted(array[i], key=lambda y: y[1])
        return array

    # used to check if two cells are equal (i.e have same element or color)
    @staticmethod
    def equals(target, dest, arg):
        if dest.hasElement() and target.hasElement():
            if arg == "name":
                if dest.getElement().getName() == target.getElement().getName():
                    return True
            else:
                if dest.getElement().getColor() == target.getElement().getColor():
                    return True
        return False

    '''
    For below functions argument [rx, ry] is the position vector
    It directs in which way the target in coordinates (x, y) is going
    either up[0,-1], down[0,1] left[-1,0], right[1,0]
    or diagonally[1,1]/[-1,1]/[1,-1]/[-1,-1]
    '''

    # recursive function for counting the sequences length(e.g OOO = 3)
    def countSeq(self, target, x, y, rx, ry, arg):
        if not 0 <= x < self.rows or not 0 <= y < self.cols:
            return []
        if self.equals(target, self.board[x][y], arg):
            return [(x, y)] + self.countSeq(target, x + rx, y + ry, rx, ry, arg)
        return []

    # method for analysing sequences and returning the score made
    def analyse(self, x, y, rx, ry):
        score = 0
        three, four, five = [], [], []
        counter = self.countSeq(self.board[x][y], x + rx, y + ry, rx, ry, "name") + [(x, y)]
        counter += self.countSeq(self.board[x][y], x - rx, y - ry, rx*(-1), ry*(-1), "name")
        if len(counter) in [3, 4]:
            score = len(counter)
            if len(counter) == 3:
                three += counter
            else:
                four += counter
        elif len(counter) > 4:
            score = 100
            return score, three, four, five
        counter = self.countSeq(self.board[x][y], x + rx, y + ry, rx, ry, "color") + [(x, y)]
        counter += self.countSeq(self.board[x][y], x - rx, y - ry, rx*(-1), ry*(-1), "color")
        if len(counter) == 5:
            score = 5
            five += counter
        return score, [three], [four], [five]

    # function for calculating each stat
    def calcStats(self, x, y, i):
        stat = self.analyse(x, y, 1, 0)[i] # checks row
        stat += self.analyse(x, y, 0, 1)[i] # checks column
        stat += self.analyse(x, y, 1, 1)[i] # check diagonal 1
        stat += self.analyse(x, y, 1, -1)[i] # check diagonal 2
        if type(stat) is list:
            return self.removeEmpty(stat)
        return stat

    # function that checks each possible sequence that can be made after a move
    def checkSeq(self, x, y):
        score = self.calcStats(x, y, 0)    # here we estimate each stat
        three = self.calcStats(x, y, 1) # for example variable 'four' stores the number
        four = self.calcStats(x, y, 2)     # of times 'Four of a Kind' has been made after
        five = self.calcStats(x, y, 3)      # inserting an element in coordinates (x,y)
        full_house = []
        for rx in [1, -1]:
            for ry in [1, -1]:
                check = self.isFullHouse(x, y, rx, ry)
                if len(check) == 4:  # here we check for full house
                    score += 10
                    full_house += [check]
        if score == 0:
            return 1, [], [], [], []
        else:
            return score, three, four, five, full_house

    # method for checking if a full house has been made
    def isFullHouse(self, x, y, rx, ry):
        if 0 <= x + rx < self.rows and 0 <= y + ry < self.cols:
            c1 = self.board[x][y]
            c2 = self.board[x + rx][y]
            c3 = self.board[x][y + ry]
            c4 = self.board[x + rx][y + ry]
            cells = [c1, c2, c3, c4]
            conditions = []
            for i in range(4):
                if not cells[i].hasElement():
                    return []
                for j in range(i+1, 4):
                    conditions += [self.equals(cells[i], cells[j], "name")]
            if not any(conditions):
                return [(c1.x, c1.y), (c2.x, c2.y),(c3.x, c3.y),(c4.x, c4.y)]
        return []

    def getBoard(self):
        return self.board

    def map(self, parsedBoard):
        for i in range(self.rows):
            for j in range(self.cols):
                element = Element(None, parsedBoard[i][j])
                cell = Cell(i, j)
                if element.name is not None:
                    cell.insert(element)
                self.board[i][j] = cell

