"""
Class that represent an element(cross, circle, square or triangle)
"""


class Element:

    def __init__(self, image, name):
        self.image = image
        self.highlighted = None
        self.name = name
        self.last = None
        self.color = self.loadColor()

    def getName(self):
        return self.name

    def loadColor(self):
        if self.name in ["cross", "triangle"]:
            return "red"
        else:
            return "blue"

    def getColor(self):
        return self.color
