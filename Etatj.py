from Card import *
class Etatj:
    def __init__(self):
        self.aType=[ 1, 1, 1, 1, 1, 1, 1]

    def setType(self, i, b):
        self.aType[i]=b

    def getType(self, i):
        return self.aType[i]

    def restart(self):
        self.aType = [1, 1, 1, 1, 1, 1, 1]
