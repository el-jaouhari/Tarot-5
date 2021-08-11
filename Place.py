from Player import *

class Place:
    def __init__(self, i):
        self.Player=0
        self.num= i
    def showPlace(self):
        print("[", self.num, "]", self.Player.getName(), end=" : ")
        if self.isEmpty():
            print("-", end="  ")
        else:
            self.Player.showCards()

    def isEmpty(self):
        return self.Player==0

    def getPtrPlayer(self):
        return self.Player

    def setPtrPlayer(self, j):
        self.Player=j

