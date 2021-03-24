"""
Class for storing Observable objects
"""


class Observable(object):

    def __init__(self):
        self.observers = []

    def addObserver(self, observer):
        self.observers += [observer]

    def removeObservers(self):
        self.observers = []

    def notifyObservers(self):
        for observer in self.observers:
            observer.update(self)
