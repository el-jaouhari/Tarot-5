from Card import *
class Etat:
    def __init__(self):
        self.cards=[]
        self.teams=False

    def addCarte(self, c):
        self.cards.append(c)

    def numColor(self, t):
        n=0
        for card in self.cards:
            if card.getType()==t:
                n+=1
        return n

    def isPlayed(self, n, c):
        for card in self.cards:
            if card.getType() == c and card.getNum()== n:
                return True
        return False

    def cardSize(self):
        return len(self.cards)

    def numBetter(self, n, c):
        p=0
        for card in self.cards:
            if card.getType() == c and card.getNum()> n:
                p+=1
        if c==5:
            t = 21
        else:
            t=14
        return t-p-n

    def restart(self):
        self.cards.clear()
        self.teams = False

    def setTeams(self, t):
        self.teams = t

    def getTeams(self):
        return self.teams
