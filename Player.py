from Table import *
from Etat import *
from Etatj import *
from Card import *

from math import comb

class Player:
    def __init__(self, table, name, position):
        self.name=name
        self.cards = []
        self.team = 0
        self.ench = 0
        self.points = 0
        self.position = position
        self.excuse = 0
        self.table=table
        self.partners=[]
        self.statut=Etatj()
        self.pli=[]
        self.ptsBonusMisere = 0
        self.ptsBonusPoignee = 0
        self.ptsPetit = 0
        self.probabilities=[]
        self.coefi = []
        self.order = []
        self.orderi = []
        self.value = []
        self.corder = []
        self.misereTete=True
        self.misereAtout=True
        self.poignee=True
        self.doublepoignee=True

    def setName(self, name):
        self.name=name

    def addCard(self, c):
        self.cards.append(c)

    def showCards(self):
        print(self.name,"  cartes :")
        for i in range(len(self.cards)):
            print(i+1, ": ", end="")
            if i+1<10: print(" ", end="")
            self.cards[i].showCard()

    def showProb(self):
        self.probability()
        print(self.name)
        for i in range(len(self.cards)):
            print(i + 1, ": ", end="")
            if i + 1 < 10: print("  ", end="")
            print(round(self.orderi[i]+1,3), "  ", self.coefi[i], "  ")
            self.cards[i].showCard()
            print("  ", self.probabilities[i])

    def getName(self):
        return self.name

    def countPli(self):
        points=0
        for card in self.pli:
            points+=card.getValue()
        if self.excuse==1 : points-=0.5
        elif self.excuse==2 : points+=0.5
        return points

    def addPli(self, c):
        self.pli.append(c)

    def organize(self):
        j=len(self.cards)
        i=0
        for c in range(0,7):
            while i<j:
                if self.cards[i].getType()==c:
                    card=self.cards[i]
                    self.cards.remove(card)
                    j-=1
                    i=-1
                i+=1

        for j in range(len(self.cards)):
            for i in range(len(self.cards)-1):
                if self.cards[i].getType()==self.cards[i+1].getType() and self.cards[i].getNum()>self.cards[i+1].getNum():
                    self.cards[i],self.cards[i+1]=self.cards[i+1],self.cards[i]

    def getEnch(self):
        return self.ench

    def haveCard(self, t, n):
        for card in self.cards:
            if card.getNum()==n and card.getType()==t:
                return True
        return  False

    def setTeam(self, team):
        self.team=team

    def getTeam(self):
        return self.team

    def addPartener(self, p):
        self.partners.append(p)

    def restart(self):
        self.cards = []
        self.team = 0
        self.ench = 0
        self.excuse = 0
        self.statut.restart()
        self.ptsBonusMisere = 0
        self.ptsBonusPoignee = 0
        self.ptsPetit = 0
        self.pli = []

    def addPoints(self, p):
        self.points+= p

    def getPoints(self):
        return self.points

    def numCard(self, t):
        n=0
        for card in self.cards:
            if card.getType()==t:
                n+=1
        return n

    def setExcuse(self, e):
        self.excuse=e

    def getExcuse(self):
        return self.excuse

    def haveAtout(self, a):
        for i in range(a,22):
            if self.haveCard(5, i):
                return True
        return False

    def longue(self):
        dict={}
        for i in range(1,5):
            dict[i]=self.numCard(i)
        dict=sorted(dict.items(), key=lambda t:t[1])
        return [t[0] for t in dict]

    def ptot1(self, t): #proba d'etre coupé
        n=len(self.cards)
        ptot1=0
        if t==5:
            n1=abs(21-self.table.statut.numColor(t)-self.numCard(t))
        else:
            n1=abs(14-self.table.statut.numColor(t)-self.numCard(t))

        n2=abs(78-self.table.statut.cardSize()-n1-len(self.cards))

        prob0=comb(n2,n)/comb(n1+n2,n)

        if n2-n<0:
            prob1=0
        else:
            prob1=comb(n2-n,n)/comb(n1+n2-n,n)

        if n2-2*n<0:
            prob2=0
        else:
            prob2=comb(n2-2*n,n)/comb(n1+n2-2*n,n)

        if n2-3*n<0:
            prob3=0
        else:
            prob3=comb(n2-3*n, n)/comb(n1+n2-3*n,n)

        if self.table.restPlayers(self.team)==0:
            ptot1=0
        elif self.table.restPlayers(self.team)==1:
            ptot1=prob0
        elif self.table.restPlayers(self.team)==2:
            ptot1=2*prob0-prob0*prob1
        elif self.table.restPlayers(self.team)==3:
            ptot1=3*prob0-3*prob0*prob1+prob0*prob1*prob2
        elif self.table.restPlayers(self.team)==4:
            ptot1=4*prob0-6*prob0*prob1+4*prob0*prob1*prob2-prob0*prob1*prob2*prob3

        for i in range(0,5):
            if self.table.getPlacePtrCard(i)==None:
                if self.table.getPlacePtrPlayer(i).statut.getType(t)==0 and self.table.getPlacePtrPlayer(i).statut.getType(5)==1:
                    ptot1=1
        return ptot1


    def ptot2(self, t, u):
        ptot2=0
        n = abs(len(self.cards))
        n1=abs(self.table.statut.numBetter(t,u)-self.numBetter(t,u))
        n2=abs(75-self.table.statut.cardSize()-n1-n)
        prob0=comb(n2,n)/comb(n1+n2,n)
        if n2-n<0:
            prob1=0
        else:
            prob1=comb(n2-n,n)/comb(n1+n2-n,n)
        if n2-2*n<0:
            prob2=0
        else:
            prob2=comb(n2-2*n,n)/comb(n1+n2-2*n,n)
        if n2-3*n<0:
            prob3=0
        else:
            prob3=comb(n2-3*n ,n)/comb(n1+n2-3*n ,n)
        if self.table.restPlayers(self.team)==0:
            ptot2=1
        elif self.table.restPlayers(self.team)==1:
            ptot2=prob0
        elif self.table.restPlayers(self.team)==2:
            ptot2=prob0*prob1
        elif self.table.restPlayers(self.team)==3:
            ptot2=prob0*prob1*prob2
        elif self.table.restPlayers(self.team)==4:
            ptot2=prob0*prob1*prob2*prob3

        for i in range(0, 5):
            if self.table.getPlacePtrCard(i) is None and self.table.statut.getTeams()==True and self.table.getPlacePtrPlayer(i).getTeam()==self.team:
                if self.table.getPlacePtrPlayer(i).statut.getType(t) == 0 and self.table.getPlacePtrPlayer(i).statut.getType(5) == 1:
                    ptot2 = 1
        return ptot2

    def prob(self, t, u):
        prob=self.ptot1(t)+(1-self.ptot1(t))*(1-self.ptot2(t,u))
        if t==6:
            prob=1
        if t==5:
            if self.table.getColor()==5 or self.table.getColor()==6 or self.table.getColor()==0:
                prob=1-self.ptot2(t,u)
            else:
                prob=self.ptot1(self.table.getColor())*(1-self.ptot2(t,u))
        return prob

    def probability(self):
        self.probabilities=[0]*len(self.cards)
        for i in range(len(self.cards)):
            if self.table.pliSize()!=0 and self.table.statut.getTeams()==True and self.table.getPlacePtrPlayer(self.table.winner()).getTeam()==self.team:
                if (self.table.getPlacePtrCard(self.table.winner()).getType()==self.cards[i].getType() and self.table.getPlacePtrCard(self.table.winner()).getNum() > self.cards[i].getNum()) or (self.table.getPlacePtrCard(self.table.winner()).getType()==5 and self.cards[i].getType()!=5) or self.cards[i].getType()==6:
                    self.probabilities[i]=self.prob(self.table.getPlacePtrCard(self.table.winner()).getType(), self.table.getPlacePtrCard(self.table.winner()).getNum())
                else:
                    self.probabilities[i] = self.prob(self.cards[i].getType(), self.cards[i].getNum())
            else:
                self.probabilities[i] = self.prob(self.cards[i].getType(), self.cards[i].getNum())

            for j in range(5):
                if self.table.getPlacePtrCard(j) is not None:
                    if (self.table.getPlacePtrCard(j).getType()==self.cards[i].getType() and self.table.getPlacePtrCard(j).getNum() > self.cards[i].getNum()) or (self.table.getPlacePtrCard(j).getType()==5 and self.cards[i].getType()!=5):
                        self.probabilities[i]=1
        self.Order()

    def Order(self):
        self.coefi=[]
        self.order=[]
        self.orderi=[]
        self.value=[]
        self.corder=[0]*len(self.probabilities)
        for j in range(len(self.cards)):
            if self.cards[j].getNum()==21:
                self.coefi.append(0.5-2*0.5*self.probabilities[j])
            else:
                self.coefi.append(self.cards[j].getValue()-2*self.cards[j].getValue()*self.probabilities[j])
        self.corder=self.coefi
        for j in range(len(self.corder)):
            min=0
            for i in range(len(self.corder)):
                if self.corder[i]<=self.corder[min]:
                    min=i

            self.corder[min]=10000000
            self.order.append(min)
        self.orderi=list(reversed(self.order))
        for i in range(len(self.orderi)):
            self.value.append(self.cards[self.orderi[i]])
        i=0
        while i < len(self.value)-1:
            y=0
            for h in range(len(self.partners)):
                if self.partners[h].statut.getType(self.value[i+1].getType()-1)==0 and self.value[i+1].getType()!=5:
                    y=1

            if self.coefi[self.orderi[i]]==self.coefi[self.orderi[i+1]] and (self.table.statut.getTeams()==False or (self.table.statut.getTeams()==True and y==0)) and  ((self.value[i].getType()==self.value[i+1].getType() and self.value[i].getNum()>self.value[i+1].getNum())  or self.numCard(self.value[i].getType())<self.numCard(self.value[i+1].getType())):
                self.value[i],self.value[i+1]=self.value[i+1],self.value[i]
                self.orderi[i],self.orderi[i+1]=self.orderi[i+1],self.orderi[i]
                i=-1
            i+=1

    def setBoolean(self):
        if self.haveCard(5,1)==False or self.haveCard(5,21)==False or self.haveCard(6,1) == False:
            for i in range(1,5):
                for j in range(11,15):
                    if self.haveCard(i,j):
                        self.misereTete = False
                        break
        else:
            self.misereTete = True

        for i in range(1,22):
            if self.haveCard(5,i) or self.haveCard(6,1):
                self.misereAtout = False
                break
        if self.numCard(5)+self.numCard(6)<8:
            self.poignee = False

        if self.numCard(5)+self.numCard(6)<10:
            self.doublepoignee = False

    def getPtsBonusMisere(self):
        return self.ptsBonusMisere
    def getPtsBonusPoignee(self):
        return self.ptsBonusPoignee
    def getPtsPetit(self):
        return self.ptsPetit
    def getPli(self):
        return self.pli
    def numRoi(self):
        n=0
        for i in range(1,5):
            if  self.haveCard(i,14):
                n+=1
        return n
    def petitAuBout(self):
        d=0
        if len(self.cards)==1 and self.haveCard(5,1):
            for j in range(len(self.table.getPlaces())):
                if self.table.getPlacePtrPlayer(j).numCard(5)==0:
                    d+=1
        if d==4:
            self.ptsPetit = 10
        else:
            self.ptsPetit = 0

    def getPosi(self):
        return self.position

    def numBetter(self, c, n):
        p=0
        for card in self.cards:
            if card.getType() == c and card.getNum() > n:
                p += 1
        return p







