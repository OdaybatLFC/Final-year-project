"""
Class that represents each cell data
"""


class Cell:

    def __init__(self, x, y):
        self.element = None
        self.hidden = None
        self.x = x
        self.y = y

    def hasElement(self):
        if self.element is not None:
            return True
        return False

    def hasHidden(self):
        if self.hidden is not None:
            return True
        return False

    def insert(self, elem):
        self.element = elem

    def setHidden(self, card):
        self.hidden = card

    def remove(self):
        self.element = None

    def getElement(self):
        return self.element

