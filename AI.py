from Player import Player
from Table import *
from math import sqrt
import random
from datetime import datetime
random.seed(datetime.now())

class AI(Player):
    def __init__(self,table, name, position, b):
        self.active = b
        Player.__init__(self, table, name, position)

    def encheres(self):
        self.ench=1
        atout=0
        nbbout=0
        a=0
        somme=0
        for card in self.cards:
            if card.getType()==5:
                atout += pow(card.getCoef(),0.25)
                if card.getNum()==1 or card.getNum()==21:
                    nbbout+=1
            elif card.getType()==6:
                nbbout+=1
                atout+=pow(card.getCoef(),0.25)
            else:
                if self.numCard(card.getType())==1:
                    card.setCoef(card.getCoef()*sqrt(0.7))
                elif self.numCard(card.getType())==2:
                    card.setCoef(card.getCoef()*sqrt(0.25))
                elif self.numCard(card.getType())==3:
                    card.setCoef(card.getCoef()*sqrt(0.125))
                elif self.numCard(card.getType())==4:
                    card.setCoef(card.getCoef()*sqrt(0.25))
                else:
                    card.setCoef(card.getCoef() * sqrt(0.5))
                a+=card.getCoef()
        atout-=pow(nbbout, 1.7)
        for i in range(1,5):
            if self.numCard(i) == 0:
                somme+=3
            elif self.numCard(i) == 1:
                somme+=0.8
            elif self.numCard(i) == 2:
                somme += 0.25
            elif self.numCard(i) == 3:
                somme += 0.125
            elif self.numCard(i) == 4:
                somme += 0.25
            else:
                somme += 0.8
        value=(1+a/70+somme/15)*atout
        if value>12: self.ench=2
        if value>18: self.ench=3
        if value>25: self.ench=4
        if value>30: self.ench=5
        if self.ench <= self.table.getEnch():
            self.ench=1
        else : self.table.setEnch(self.ench)

    def chooseRoi(self):
        self.team=1
        n=0
        if not self.haveCard(1,14) or not self.haveCard(2,14) or not self.haveCard(3,14) or not self.haveCard(4,14):
            if not self.haveCard(self.longue()[2],14):
                n=self.longue()[2]
            elif not self.haveCard(self.longue()[1],14) and self.numCard(self.longue()[1])<4:
                n = self.longue()[1]
            elif not self.haveCard(self.longue()[0], 14):
                n = self.longue()[0]
            elif not self.haveCard(self.longue()[1], 14):
                n = self.longue()[1]
            elif not self.haveCard(self.longue()[3], 14):
                n = self.longue()[3]
        else :
            n = self.longue()[3]
        if self.table.test==False:
            print(self.name,"a appelé le Roi de", end=" ")
            if n==1 :
                print("Pique")
                self.table.setColorRoi(1)
            if n==2 :
                print("Pique")
                self.table.setColorRoi(2)
            if n==3 :
                print("Pique")
                self.table.setColorRoi(3)
            if n==4 :
                print("Pique")
                self.table.setColorRoi(4)
        self.table.addTeam(self)
        self.table.setColorRoi(n)
        if not self.table.cardChien(n,14) and self.table.getCardPtrPlayer(n,14).getName()!=self.name:
            self.partners.append(self.table.getCardPtrPlayer(n,14))
            self.table.addTeam(self.table.getCardPtrPlayer(n,14))
            self.table.getCardPtrPlayer(n, 14).setTeam(1)
            self.table.setType(1)
            self.table.setTeams()
        else:
            self.table.setType(2)
            self.table.setTeams()

    def play(self):
        #strategy=1
        p=1
        self.probability()
        #self.showProb()
        i=-1
        while 1:
            i += 1
            if i > len(self.order) - 1:
                i = 0
                p = p + 1
            if self.active:
                n = self.orderi[i]
            else:
                n = random.randrange(len(self.cards))
            if self.table.getColor() == 0 or self.table.getColor() == 6:
                if len(self.cards) == 15 and self.cards[n].getType() == self.table.getColorRoi():
                    if self.cards[n].getNum() != 14:
                        continue
                if self.haveCard(5, 21) and (not self.haveCard(5, 1)):
                    if self.table.statut.isPlayed(5, 1) == False and self.table.statut.getTeams() == True:
                        n = self.rangCard(5, 21)
                if self.active:
                    if self.cards[n].getType() == 5 and p == 1 and len(self.cards) != 1:
                        continue
                self.table.setColor(self.cards[n].getType())
            elif self.cards[n].getType() != self.table.getColor():
                if self.cards[n].getType() != 5 and (self.numCard(self.table.getColor()) != 0 or
                        self.numCard(5) != 0) and self.cards[n].getType() != 6:
                    continue

                if self.cards[n].getType() == 5 and ((self.cards[n].getNum() < self.table.getAtout() and self.haveAtout(
                        self.table.getAtout())) or self.numCard(self.table.getColor()) != 0):
                    continue
                if self.cards[n].getType() == 5:
                    if self.active:
                        if self.table.test == False:
                            print(self.name, " n'a plus de", end=' ')
                            if self.table.getColor() == 1:
                                print("Pique")
                            if self.table.getColor() == 2:
                                print("Trefle")
                            if self.table.getColor() == 3:
                                print("Carreau")
                            if self.table.getColor() == 4:
                                print("Carre")
                    self.statut.setType(self.table.getColor(), 0)
                elif self.cards[n].getType() != 6:
                    if self.table.getColor() == 5:
                        self.statut.setType(5, 0)
                        if self.table.test == False:
                            print(self.name, "n'a plus d'Atout")
                        else:
                            self.statut.setType(self.table.getColor(), 0)
                            self.statut.setType(5, 0)
                            if self.table.test == False:
                                print(self.name, " n'a plus de", end=' ')
                                if self.table.getColor() == 1:
                                    print("Pique ni d'Atout")
                                if self.table.getColor() == 2:
                                    print("Trefle ni d'Atout")
                                if self.table.getColor() == 3:
                                    print("Carreau ni d'Atout")
                                if self.table.getColor() == 4:
                                    print("Carre ni d'Atout")
                elif self.table.getColor() == 5:
                    if self.cards[n].getType() == 5 and self.cards[
                        n].getNum() < self.table.getAtout() and self.haveAtout(self.table.getAtout()):
                        continue
                if self.cards[n].getType() == 5 and self.cards[n].getNum() > self.table.getAtout():
                    self.table.setAtout(self.cards[n].getNum())
                if self.cards[n].getType() == self.table.getColorRoi() and self.cards[n].getNum() == 14:
                    self.table.statut.setTeams(True)
            self.table.addPli(self.cards[n], self.position)
            self.cards.remove(self.cards[n])

            break
    def seeChien(self):
        pass
    def chien(self):
        self.organize()
        vlongue=self.longue()
        nbGivenCard=0
        if nbGivenCard<3 and self.numCard(vlongue[3])<4 and not self.haveCard(vlongue[3],14) and vlongue[3]!=self.table.getColorRoi() and self.numCard(vlongue[3])!=0:
            for i in range(14):
                if self.rangCard(vlongue[3],i)!=-1:
                    self.addPli(self.cards[self.rangCard(self.longue()[3],i)])
                    self.cards.remove(self.cards[self.rangCard(vlongue[3],i)])
                    self.organize()
                    nbGivenCard+=1

            if nbGivenCard<3 and self.numCard(5)>5 and self.numCard(vlongue[2])<4-nbGivenCard and self.numCard(vlongue[2])!=0 and not self.haveCard(vlongue[2],14) and vlongue[2]!=self.table.getColorRoi():
                for i in range(14):
                    if self.rangCard(vlongue[2], i) != -1:
                        self.addPli(self.cards[self.rangCard(self.longue()[2], i)])
                        self.cards.remove(self.cards[self.rangCard(vlongue[2], i)])
                        self.organize()
                        nbGivenCard += 1

            elif nbGivenCard<3 and self.numCard(5)>5 and self.numCard(vlongue[1])<4-nbGivenCard and self.numCard(vlongue[1])!=0 and not self.haveCard(vlongue[1],14) and vlongue[1]!=self.table.getColorRoi():
                for i in range(14):
                    if self.rangCard(vlongue[1], i) != -1:
                        self.addPli(self.cards[self.rangCard(self.longue()[1], i)])
                        self.cards.remove(self.cards[self.rangCard(vlongue[1], i)])
                        self.organize()
                        nbGivenCard += 1
            elif nbGivenCard<3 and self.numCard(5)>5 and self.numCard(vlongue[0])<4-nbGivenCard and self.numCard(vlongue[0])!=0 and not self.haveCard(vlongue[0],14) and vlongue[0]!=self.table.getColorRoi():
                for i in range(14):
                    if self.rangCard(vlongue[0], i) != -1:
                        self.addPli(self.cards[self.rangCard(self.longue()[0], i)])
                        self.cards.remove(self.cards[self.rangCard(vlongue[0], i)])
                        self.organize()
                        nbGivenCard += 1
        elif nbGivenCard<3 and self.numCard(vlongue[2])<4  and not self.haveCard(vlongue[2],14) and vlongue[2]!=self.table.getColorRoi() and self.numCard(vlongue[2])!=0:
            for i in range(14):
                if self.rangCard(vlongue[0], i) != -1:
                    self.addPli(self.cards[self.rangCard(self.longue()[2], i)])
                    self.cards.remove(self.cards[self.rangCard(vlongue[2], i)])
                    self.organize()
                    nbGivenCard += 1

            if nbGivenCard < 3 and self.numCard(5) > 5 and self.numCard(vlongue[1]) < 4 - nbGivenCard and self.numCard(
                    vlongue[1]) != 0 and not self.haveCard(vlongue[1], 14) and vlongue[1] != self.table.getColorRoi():
                for i in range(14):
                    if self.rangCard(vlongue[1], i) != -1:
                        self.addPli(self.cards[self.rangCard(self.longue()[1], i)])
                        self.cards.remove(self.cards[self.rangCard(vlongue[1], i)])
                        self.organize()
                        nbGivenCard += 1
            if nbGivenCard < 3 and self.numCard(5) > 5 and self.numCard(vlongue[0]) < 4 - nbGivenCard and self.numCard(
                    vlongue[0]) != 0 and not self.haveCard(vlongue[0], 14) and vlongue[0] != self.table.getColorRoi():
                for i in range(14):
                    if self.rangCard(vlongue[1], i) != -1:
                        self.addPli(self.cards[self.rangCard(self.longue()[0], i)])
                        self.cards.remove(self.cards[self.rangCard(vlongue[0], i)])
                        self.organize()
                        nbGivenCard += 1
        elif nbGivenCard<3 and self.numCard(vlongue[1])<4  and not self.haveCard(vlongue[1],14) and vlongue[1]!=self.table.getColorRoi() and self.numCard(vlongue[1])!=0:
            for i in range(14):
                if self.rangCard(vlongue[1], i) != -1:
                    self.addPli(self.cards[self.rangCard(self.longue()[1], i)])
                    self.cards.remove(self.cards[self.rangCard(vlongue[1], i)])
                    self.organize()
                    nbGivenCard += 1
            if nbGivenCard < 3 and self.numCard(5) > 5 and self.numCard(vlongue[0]) < 4 - nbGivenCard and self.numCard(
                    vlongue[0]) != 0 and not self.haveCard(vlongue[0], 14) and vlongue[0] != self.table.getColorRoi():
                for i in range(14):
                    if self.rangCard(vlongue[1], i) != -1:
                        self.addPli(self.cards[self.rangCard(self.longue()[0], i)])
                        self.cards.remove(self.cards[self.rangCard(vlongue[0], i)])
                        self.organize()
                        nbGivenCard += 1

        elif nbGivenCard<3 and self.numCard(vlongue[0])<4  and not self.haveCard(vlongue[1],14) and vlongue[0]!=self.table.getColorRoi() and self.numCard(vlongue[0])!=0:
            for i in range(14):
                if self.rangCard(vlongue[0], i) != -1:
                    self.addPli(self.cards[self.rangCard(self.longue()[0], i)])
                    self.cards.remove(self.cards[self.rangCard(vlongue[0], i)])
                    self.organize()
                    nbGivenCard += 1
        t=True
        while t:
            t=False
            if nbGivenCard<3 and self.singletRoi(3-nbGivenCard):
                for i in range(5):
                    if self.numCard(i)<=3-nbGivenCard+1 and self.haveCard(i, 14) and self.numCard(i)!=1:
                        for j in range(1,14):
                            if self.rangCard(i,j)!=-1:
                                self.addPli(self.cards[self.rangCard(i,j)])
                                self.cards.remove(self.cards[self.rangCard(i, j)])
                                self.organize()
                                nbGivenCard += 1
                                t=True
        t=True
        while t:
            t=False
            if nbGivenCard<3 and self.sigletRoiCall(3-nbGivenCard) and not self.haveCard(self.table.getColorRoi(), 14):
                for j in range(13,0,-1):
                    if self.rangCard(self.table.getColorRoi(),j)!=-1:
                        self.addPli(self.cards[self.rangCard(self.table.getColorRoi(), j)])
                        self.cards.remove(self.cards[self.rangCard(self.table.getColorRoi(), j)])
                        self.organize()
                        nbGivenCard += 1
                        t=True

        t=True
        while t:
            t=False
            if self.numRoi()+self.numCard(5)+self.numCard(6)==len(self.cards):
                for i in range(1,4-nbGivenCard):
                    if self.haveCard(5,1):
                        self.addPli(self.cards[self.numRoi()+1])
                        if self.table.test == False  :
                            print(" Le joueur ", self.name, " a mis au chien le", end=" ")
                            self.cards[self.numRoi() + 1].showCard()
                        self.cards.remove(self.cards[self.numRoi()+1])
                        self.organize()
                    else:
                        self.addPli(self.cards[self.numRoi()])
                        if self.table.test == False  :
                            print(" Le joueur ", self.name, " a mis au chien le", end=" ")
                            self.cards[self.numRoi()].showCard()
                        self.cards.remove(self.cards[self.numRoi()])
                        self.organize()
            elif nbGivenCard<3:
                for j in range(13, 0,-1):
                    for i in range(1, 5):
                        if self.rangCard(i,j)!=-1:
                            self.addPli(self.cards[self.rangCard(i,j)])
                            self.cards.remove(self.cards[self.rangCard(i,j)])
                            self.organize()
                            nbGivenCard+=1
                            t=True

    def singletRoi(self, n):
        for i in range(1,5):
            if self.numCard(i)<=(n+1) and self.haveCard(i,14) and self.numCard(i)!=1:
                return True
        return False

    def sigletRoiCall(self, n):
        if self.numCard(self.table.getColorRoi())<=n and not self.haveCard(self.table.getColorRoi(),14) and self.numCard(self.table.getColorRoi())!=1:
            return True
        return False

    def announce(self):
        if self.misereTete:
            if self.table.test==False:
                print("Le joueur ", self.name, " a annoncé une misere de tete")
            self.ptsBonusMisere+=10
        if self.misereAtout:
            if self.table.test==False:
                print("Le joueur ", self.name, " a annoncé une misere d'Atout")
            self.ptsBonusMisere+=10
        if self.poignee:
            if self.doublepoignee:
                if self.table.test == False:
                    print("Le joueur ", self.name, " a annoncé une double poignee")
                self.ptsBonusPoignee+=30
                self.showPoignee(2)
            else:
                if self.table.test == False:
                    print("Le joueur ", self.name, " a annoncé une double poignee")
                self.ptsBonusPoignee+=20
                if self.table.test == False:
                    self.showPoignee(1)

    def showPoignee(self, n):
        k=self.numCard(5)
        print("Poignee montrée")
        if n==1:
            if self.haveCard(6,1):
                if k==7 or k==8:
                    for i in range(14-k,22-k):
                        self.cards[i].showCard()
                        print()
                if k>8:
                    for i in range(14-k,21-k):
                        self.cards[i].showCard()
                        print()
                    self.cards[13].showCard()
                    print()
            if self.haveCard(6, 1)==False :
                if k==8:
                    for i in range(15-k, 23-k):
                        self.cards[i].showCard()
                        print()
                if k>8:
                    for i in range(14-k,21-k):
                        self.cards[i].showCard()
                        print("  ")
                    self.cards[14].showCard()
                    print()
        if n==2:
            if self.haveCard(6, 1):
                if k==9 or k==10:
                    for i in range(14-k,24-k):
                        self.cards[i].showCard()
                        print("  ")
                if k>10:
                    for i in range(14-k, 23-k):
                        self.cards[i].showCard()
                        print()
                    self.cards[13].showCard()
                    print()
            if self.haveCard(6, 1)==False:
                if k==0:
                    for i in range(15-k, 25-k):
                        self.cards[i].showCard()
                        print()
                if k>10:
                    for i in range(15-k, 24-k):
                        self.cards[i].showCard()
                        print()
                    self.cards[14].showCard()
                    print()

    def rangCard(self, n, v):
        if self.haveCard(n,v):
            for i in range(0,len(self.cards)+1):
                if self.cards[i].getType()==n and self.cards[i].getNum()==v:
                    return i
        else:
            return -1
















