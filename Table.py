from Person import *
from AI import *
from Place import *
from Etat import *
from Card import *
import random
import os
from datetime import datetime

random.seed(datetime.now())


class Table:

    def __init__(self):
        self.statut = Etat()
        self.teams = []
        self.cards = []
        self.ench = 0
        self.pli = [None, None, None, None, None]
        self.qui = random.randrange(5)
        self.le = self.qui
        self.win = []
        self.part = 1
        self.type = 0
        self.color = 0
        self.places = [0, 0, 0, 0, 0]
        for i in range(5):
            self.places[i] = Place(i + 1)
        self.test = False
        self.colorRoi = 0
        self.first = 0

    def showTable(self):
        for i in range(5):
            self.places[i].showPlace()

    def showPlayer(self):
        self.places[0].showPlace()

    def placeIsEmpty(self, p):
        return self.places[p].isEmpty()

    def getPlacePtrPlayer(self, p):
        return self.places[p].getPtrPlayer()

    def getPlacePtrCard(self, p):
        return self.pli[p]

    def setPlacePtrPlayer(self, p, player):
        self.places[p].setPtrPlayer(player)

    def createCards(self):
        for i in range(1, 5):
            for j in range(1, 15):
                card = Card(i, j)
                self.cards.append(card)

        for i in range(1, 22):
            card = Card(5, i)
            self.cards.append(card)
        card = Card(6, 1)
        self.cards.append(card)

    def showCards(self):
        for i in range(len(self.cards)):
            print(i + 1, end=" : ")
            self.cards[i].showCard()
            print()

    def distributeCards(self):
        for i in range(0, 5):
            for j in range(0, 15):
                n = len(self.cards) * random.random()
                self.places[i].getPtrPlayer().addCard(self.cards[int(n)])
                self.cards.remove(self.cards[int(n)])
        for i in range(0, 5):
            self.places[i].getPtrPlayer().organize()

    def action(self):
        for i in range(self.qui, self.qui + 5):
            d = i
            if d > 4: d = d - 5
            self.places[d].getPtrPlayer().play()

    def createPlayers(self, name):
        self.places[0].setPtrPlayer(AI(self, name, 0, True))
        self.places[1].setPtrPlayer(AI(self, "AI1", 1, True))
        self.places[2].setPtrPlayer(AI(self, "AI2", 2, True))
        self.places[3].setPtrPlayer(AI(self, "AI3", 3, True))
        self.places[4].setPtrPlayer(AI(self, "AI4", 4, True))

    def addPli(self, c, i):
        self.pli[i] = c

    def showPli(self):
        print("TABLE :")
        for d in range(self.qui, self.qui + 5):
            i = d
            if i > 4: i = i - 5
            print( self.places[i].getPtrPlayer().getName(), end=" : ")
            if self.pli[i] is not None:
                self.pli[i].showCard()
            else:
                print("-")

    def showEnch(self):
        for d in range(self.qui, self.qui + 5):
            i = d
            if i > 4: i = i - 5
            print(self.places[i].getPtrPlayer().getName(), end=" : ")
            if self.places[i].getPtrPlayer().getEnch() is not None:
                print(self.places[i].getPtrPlayer().getEnch())
            else:
                print("-")

    def pliSize(self):
        size = 0
        for pl in self.pli:
            if pl != 0 and pl is not None:
                size += 1
        return size

    def setColor(self, t):
        self.color = t

    def getColor(self):
        return self.color

    def clearPli(self):
        self.pli = [None, None, None, None, None]

    def showPoints(self):
        print("POINTS :")
        if self.type == 1:
            print(self.teams[0].getName(), " et ", self.teams[1].getName(), ": ",
                  self.teams[0].countPli() + self.teams[1].countPli())
            print(self.teams[2].getName(), ",", self.teams[3].getName(), " et ", self.teams[4].getName(), ": ",
                  self.teams[2].countPli() + self.teams[3].countPli() + self.teams[4].countPli())
        elif self.type == 2:
            print(self.teams[0].getName(), ": ", self.teams[0].countPli())
            print(self.teams[1].getName(), ",", self.teams[2].getName(), ",", self.teams[3].getName(), " et ",
                  self.teams[4].getName(), ": ",
                  self.teams[1].countPli() + self.teams[2].countPli() + self.teams[3].countPli() + self.teams[
                      4].countPli())

    def fin(self):
        bouts = 0
        points = 0
        for j in range(2):
            for i in range(len(self.teams[j].getPli())):
                if self.teams[j].getPli()[i].getType() == 6:
                    bouts += 1
                if self.teams[j].getPli()[i].getType() == 5 and self.teams[j].getPli()[i].getNum() == 1:
                    bouts += 1
                if self.teams[j].getPli()[i].getType() == 5 and self.teams[j].getPli()[i].getNum() == 21:
                    bouts += 1
        if bouts == 0: points = 56
        if bouts == 1: points = 51
        if bouts == 2: points = 41
        if bouts == 3: points = 36
        if self.type == 1:
            pts = self.teams[0].countPli() + self.teams[1].countPli()
            if pts >= points:
                print(self.teams[0].getName()," et ", self.teams[1].getName(), " ont gagné le match avec ", bouts, "bouts")
                diff = pts - points
                pts = 25 + diff
                if self.teams[0].getEnch() == 3:
                    pts = pts * 2
                if self.teams[0].getEnch() == 4:
                    pts = pts * 4
                if self.teams[0].getEnch() == 5:
                    pts = pts * 6
                self.teams[0].addPoints(2 * pts + 4 * (
                        self.teams[0].getPtsBonusMisere() + self.teams[0].getPtsBonusPoignee() + self.teams[
                    0].getPtsPetit()) - self.teams[1].getPtsBonusMisere() - self.teams[1].getPtsBonusPoignee() -
                                        self.teams[2].getPtsBonusMisere() + self.teams[2].getPtsBonusPoignee() -
                                        self.teams[3].getPtsBonusMisere() + self.teams[3].getPtsBonusPoignee() -
                                        self.teams[4].getPtsBonusMisere() + self.teams[4].getPtsBonusPoignee()
                                        - self.teams[1].getPtsPetit() - self.teams[2].getPtsPetit() - self.teams[
                                            3].getPtsPetit() - self.teams[4].getPtsPetit())
                self.teams[1].addPoints(pts + 4 * (
                        self.teams[1].getPtsBonusMisere() + self.teams[1].getPtsBonusPoignee() + self.teams[
                    1].getPtsPetit()) - self.teams[0].getPtsBonusMisere() - self.teams[0].getPtsBonusPoignee() -
                                        self.teams[2].getPtsBonusMisere() +
                                        self.teams[2].getPtsBonusPoignee() - self.teams[3].getPtsBonusMisere() +
                                        self.teams[3].getPtsBonusPoignee() - self.teams[4].getPtsBonusMisere() +
                                        self.teams[4].getPtsBonusPoignee() - self.teams[0].getPtsPetit() -
                                        self.teams[2].getPtsPetit() - self.teams[3].getPtsPetit() - self.teams[
                                            4].getPtsPetit())
                self.teams[2].addPoints(-pts + 4 * (
                        self.teams[2].getPtsBonusMisere() - self.teams[2].getPtsBonusPoignee() + self.teams[
                    2].getPtsPetit()) - self.teams[0].getPtsBonusMisere() - self.teams[0].getPtsBonusPoignee() -
                                        self.teams[1].getPtsBonusMisere() -
                                        self.teams[1].getPtsBonusPoignee() - self.teams[3].getPtsBonusMisere() +
                                        self.teams[3].getPtsBonusPoignee() - self.teams[4].getPtsBonusMisere() +
                                        self.teams[4].getPtsBonusPoignee() - self.teams[0].getPtsPetit() -
                                        self.teams[1].getPtsPetit() - self.teams[3].getPtsPetit() - self.teams[
                                            4].getPtsPetit())
                self.teams[3].addPoints(-pts + 4 * (
                        self.teams[3].getPtsBonusMisere() - self.teams[3].getPtsBonusPoignee() + self.teams[
                    3].getPtsPetit()) - self.teams[0].getPtsBonusMisere() - self.teams[0].getPtsBonusPoignee() -
                                        self.teams[1].getPtsBonusMisere() -
                                        self.teams[1].getPtsBonusPoignee() - self.teams[2].getPtsBonusMisere() +
                                        self.teams[2].getPtsBonusPoignee() - self.teams[4].getPtsBonusMisere() +
                                        self.teams[4].getPtsBonusPoignee() - self.teams[0].getPtsPetit() -
                                        self.teams[1].getPtsPetit() - self.teams[2].getPtsPetit() - self.teams[
                                            4].getPtsPetit())
                self.teams[4].addPoints(-pts + 4 * (
                        self.teams[4].getPtsBonusMisere() - self.teams[4].getPtsBonusPoignee() + self.teams[
                    4].getPtsPetit()) - self.teams[0].getPtsBonusMisere() - self.teams[0].getPtsBonusPoignee() -
                                        self.teams[1].getPtsBonusMisere() -
                                        self.teams[1].getPtsBonusPoignee() - self.teams[2].getPtsBonusMisere() +
                                        self.teams[2].getPtsBonusPoignee() - self.teams[3].getPtsBonusMisere() +
                                        self.teams[3].getPtsBonusPoignee() - self.teams[0].getPtsPetit() -
                                        self.teams[1].getPtsPetit() - self.teams[2].getPtsPetit() - self.teams[
                                            3].getPtsPetit())

            else:
                print(self.teams[2].getName(), ", ", self.teams[3].getName(), " et ", self.teams[4].getName(), " ont gagné le match.")
                diff = points - pts
                pts = 25 + diff
                if self.teams[0].getEnch() == 3:
                    pts = pts * 2
                if self.teams[0].getEnch() == 4:
                    pts = pts * 4
                if self.teams[0].getEnch() == 5:
                    pts = pts * 6
                self.teams[0].addPoints(-2 * pts + 4 * (
                        self.teams[0].getPtsBonusMisere() - self.teams[0].getPtsBonusPoignee() + self.teams[
                    0].getPtsPetit()) - self.teams[1].getPtsBonusMisere() + self.teams[1].getPtsBonusPoignee() -
                                        self.teams[2].getPtsBonusMisere() - self.teams[2].getPtsBonusPoignee() -
                                        self.teams[3].getPtsBonusMisere() - self.teams[3].getPtsBonusPoignee() -
                                        self.teams[4].getPtsBonusMisere() - self.teams[4].getPtsBonusPoignee()
                                        - self.teams[1].getPtsPetit() - self.teams[2].getPtsPetit() - self.teams[
                                            3].getPtsPetit() - self.teams[4].getPtsPetit())
                self.teams[1].addPoints(-pts + 4 * (
                        self.teams[1].getPtsBonusMisere() - self.teams[1].getPtsBonusPoignee() + self.teams[
                    1].getPtsPetit()) - self.teams[0].getPtsBonusMisere() + self.teams[0].getPtsBonusPoignee() -
                                        self.teams[2].getPtsBonusMisere() -
                                        self.teams[2].getPtsBonusPoignee() - self.teams[3].getPtsBonusMisere() -
                                        self.teams[3].getPtsBonusPoignee() - self.teams[4].getPtsBonusMisere() -
                                        self.teams[4].getPtsBonusPoignee() - self.teams[0].getPtsPetit() -
                                        self.teams[2].getPtsPetit() - self.teams[3].getPtsPetit() - self.teams[
                                            4].getPtsPetit())
                self.teams[2].addPoints(pts + 4 * (
                        self.teams[2].getPtsBonusMisere() + self.teams[2].getPtsBonusPoignee() + self.teams[
                    2].getPtsPetit()) - self.teams[0].getPtsBonusMisere() + self.teams[0].getPtsBonusPoignee() -
                                        self.teams[1].getPtsBonusMisere() +
                                        self.teams[1].getPtsBonusPoignee() - self.teams[3].getPtsBonusMisere() -
                                        self.teams[3].getPtsBonusPoignee() - self.teams[4].getPtsBonusMisere() -
                                        self.teams[4].getPtsBonusPoignee() - self.teams[0].getPtsPetit() -
                                        self.teams[1].getPtsPetit() - self.teams[3].getPtsPetit() - self.teams[
                                            4].getPtsPetit())
                self.teams[3].addPoints(pts + 4 * (
                        self.teams[3].getPtsBonusMisere() + self.teams[3].getPtsBonusPoignee() + self.teams[
                    3].getPtsPetit()) - self.teams[0].getPtsBonusMisere() + self.teams[0].getPtsBonusPoignee() -
                                        self.teams[1].getPtsBonusMisere() +
                                        self.teams[1].getPtsBonusPoignee() - self.teams[2].getPtsBonusMisere() -
                                        self.teams[2].getPtsBonusPoignee() - self.teams[4].getPtsBonusMisere() -
                                        self.teams[4].getPtsBonusPoignee() - self.teams[0].getPtsPetit() -
                                        self.teams[1].getPtsPetit() - self.teams[2].getPtsPetit() - self.teams[
                                            4].getPtsPetit())
                self.teams[4].addPoints(pts + 4 * (
                        self.teams[4].getPtsBonusMisere() + self.teams[4].getPtsBonusPoignee() + self.teams[
                    4].getPtsPetit()) - self.teams[0].getPtsBonusMisere() + self.teams[0].getPtsBonusPoignee() -
                                        self.teams[1].getPtsBonusMisere() +
                                        self.teams[1].getPtsBonusPoignee() - self.teams[2].getPtsBonusMisere() -
                                        self.teams[2].getPtsBonusPoignee() - self.teams[3].getPtsBonusMisere() -
                                        self.teams[3].getPtsBonusPoignee() - self.teams[0].getPtsPetit() -
                                        self.teams[1].getPtsPetit() - self.teams[2].getPtsPetit() - self.teams[
                                            3].getPtsPetit())
        elif self.type == 2:
            pts = self.teams[0].countPli()
            if pts >= points:
                print(self.teams[0].getName(), " a gagné le match avec ", bouts,
                      "bouts")
                diff = pts - points
                pts = 25 + diff
                if self.teams[0].getEnch() == 3:
                    pts = pts * 2
                if self.teams[0].getEnch() == 4:
                    pts = pts * 4
                if self.teams[0].getEnch() == 5:
                    pts = pts * 6
                self.teams[0].addPoints(4 * pts + 4 * (
                        self.teams[0].getPtsBonusMisere() + self.teams[0].getPtsBonusPoignee() + self.teams[
                    0].getPtsPetit()) - self.teams[1].getPtsBonusMisere() + self.teams[1].getPtsBonusPoignee() -
                                        self.teams[2].getPtsBonusMisere() + self.teams[2].getPtsBonusPoignee() -
                                        self.teams[3].getPtsBonusMisere() + self.teams[3].getPtsBonusPoignee() -
                                        self.teams[4].getPtsBonusMisere() + self.teams[4].getPtsBonusPoignee()
                                        - self.teams[1].getPtsPetit() - self.teams[2].getPtsPetit() - self.teams[
                                            3].getPtsPetit() - self.teams[4].getPtsPetit())
                self.teams[1].addPoints(-pts + 4 * (
                        self.teams[1].getPtsBonusMisere() - self.teams[1].getPtsBonusPoignee() + self.teams[
                    0].getPtsPetit()) - self.teams[0].getPtsBonusMisere() - self.teams[0].getPtsBonusPoignee() -
                                        self.teams[2].getPtsBonusMisere() +
                                        self.teams[2].getPtsBonusPoignee() - self.teams[3].getPtsBonusMisere() +
                                        self.teams[3].getPtsBonusPoignee() - self.teams[4].getPtsBonusMisere() +
                                        self.teams[4].getPtsBonusPoignee() - self.teams[0].getPtsPetit() -
                                        self.teams[2].getPtsPetit() - self.teams[3].getPtsPetit() - self.teams[
                                            4].getPtsPetit())
                self.teams[2].addPoints(-pts + 4 * (
                        self.teams[2].getPtsBonusMisere() - self.teams[2].getPtsBonusPoignee() + self.teams[
                    0].getPtsPetit()) - self.teams[0].getPtsBonusMisere() - self.teams[0].getPtsBonusPoignee() -
                                        self.teams[1].getPtsBonusMisere() +
                                        self.teams[1].getPtsBonusPoignee() - self.teams[3].getPtsBonusMisere() +
                                        self.teams[3].getPtsBonusPoignee() - self.teams[4].getPtsBonusMisere() +
                                        self.teams[4].getPtsBonusPoignee() - self.teams[0].getPtsPetit() -
                                        self.teams[1].getPtsPetit() - self.teams[3].getPtsPetit() - self.teams[
                                            4].getPtsPetit())
                self.teams[3].addPoints(-pts + 4 * (
                        self.teams[3].getPtsBonusMisere() - self.teams[3].getPtsBonusPoignee() + self.teams[
                    0].getPtsPetit()) - self.teams[0].getPtsBonusMisere() - self.teams[0].getPtsBonusPoignee() -
                                        self.teams[1].getPtsBonusMisere() +
                                        self.teams[1].getPtsBonusPoignee() - self.teams[2].getPtsBonusMisere() +
                                        self.teams[2].getPtsBonusPoignee() - self.teams[4].getPtsBonusMisere() +
                                        self.teams[4].getPtsBonusPoignee() - self.teams[0].getPtsPetit() -
                                        self.teams[1].getPtsPetit() - self.teams[3].getPtsPetit() - self.teams[
                                            4].getPtsPetit())

                self.teams[4].addPoints(-pts + 4 * (
                        self.teams[4].getPtsBonusMisere() - self.teams[4].getPtsBonusPoignee() + self.teams[
                    0].getPtsPetit()) - self.teams[0].getPtsBonusMisere() - self.teams[0].getPtsBonusPoignee() -
                                        self.teams[1].getPtsBonusMisere() +
                                        self.teams[1].getPtsBonusPoignee() - self.teams[2].getPtsBonusMisere() +
                                        self.teams[2].getPtsBonusPoignee() - self.teams[3].getPtsBonusMisere() +
                                        self.teams[3].getPtsBonusPoignee() - self.teams[0].getPtsPetit() -
                                        self.teams[1].getPtsPetit() - self.teams[3].getPtsPetit() - self.teams[
                                            4].getPtsPetit())

            else:
                print(self.teams[1].getName(), ", ", self.teams[2].getName(), ", ", self.teams[3].getName(), " et ", self.teams[4].getName(),
                      " ont gagné le match.")
                diff = points - pts
                pts = 25 + diff
                if self.teams[0].getEnch() == 3:
                    pts = pts * 2
                if self.teams[0].getEnch() == 4:
                    pts = pts * 4
                if self.teams[0].getEnch() == 5:
                    pts = pts * 6
                self.teams[0].addPoints(-4 * pts + 4 * (
                        self.teams[0].getPtsBonusMisere() - self.teams[0].getPtsBonusPoignee() + self.teams[
                    0].getPtsPetit()) - self.teams[1].getPtsBonusMisere() - self.teams[1].getPtsBonusPoignee() -
                                        self.teams[2].getPtsBonusMisere() - self.teams[2].getPtsBonusPoignee() -
                                        self.teams[3].getPtsBonusMisere() - self.teams[3].getPtsBonusPoignee() -
                                        self.teams[4].getPtsBonusMisere() - self.teams[4].getPtsBonusPoignee()
                                        - self.teams[1].getPtsPetit() - self.teams[2].getPtsPetit() - self.teams[
                                            3].getPtsPetit() - self.teams[4].getPtsPetit())
                self.teams[1].addPoints(pts + 4 * (
                        self.teams[1].getPtsBonusMisere() + self.teams[1].getPtsBonusPoignee() + self.teams[
                    1].getPtsPetit()) - self.teams[0].getPtsBonusMisere() + self.teams[0].getPtsBonusPoignee() -
                                        self.teams[2].getPtsBonusMisere() -
                                        self.teams[2].getPtsBonusPoignee() - self.teams[3].getPtsBonusMisere() -
                                        self.teams[3].getPtsBonusPoignee() - self.teams[4].getPtsBonusMisere() -
                                        self.teams[4].getPtsBonusPoignee() - self.teams[0].getPtsPetit() -
                                        self.teams[2].getPtsPetit() - self.teams[3].getPtsPetit() - self.teams[
                                            4].getPtsPetit())
                self.teams[2].addPoints(pts + 4 * (
                        self.teams[2].getPtsBonusMisere() + self.teams[2].getPtsBonusPoignee() + self.teams[
                    2].getPtsPetit()) - self.teams[0].getPtsBonusMisere() + self.teams[0].getPtsBonusPoignee() -
                                        self.teams[1].getPtsBonusMisere() -
                                        self.teams[1].getPtsBonusPoignee() - self.teams[3].getPtsBonusMisere() -
                                        self.teams[3].getPtsBonusPoignee() - self.teams[4].getPtsBonusMisere() -
                                        self.teams[4].getPtsBonusPoignee() - self.teams[0].getPtsPetit() -
                                        self.teams[1].getPtsPetit() - self.teams[3].getPtsPetit() - self.teams[
                                            4].getPtsPetit())
                self.teams[3].addPoints(pts + 4 * (
                        self.teams[3].getPtsBonusMisere() + self.teams[3].getPtsBonusPoignee() + self.teams[
                    3].getPtsPetit()) - self.teams[0].getPtsBonusMisere() + self.teams[0].getPtsBonusPoignee() -
                                        self.teams[1].getPtsBonusMisere() -
                                        self.teams[1].getPtsBonusPoignee() - self.teams[2].getPtsBonusMisere() -
                                        self.teams[2].getPtsBonusPoignee() - self.teams[4].getPtsBonusMisere() -
                                        self.teams[4].getPtsBonusPoignee() - self.teams[0].getPtsPetit() -
                                        self.teams[1].getPtsPetit() - self.teams[2].getPtsPetit() - self.teams[
                                            4].getPtsPetit())
                self.teams[4].addPoints(pts + 4 * (
                        self.teams[4].getPtsBonusMisere() + self.teams[4].getPtsBonusPoignee() + self.teams[
                    4].getPtsPetit()) - self.teams[0].getPtsBonusMisere() + self.teams[0].getPtsBonusPoignee() -
                                        self.teams[1].getPtsBonusMisere() -
                                        self.teams[1].getPtsBonusPoignee() - self.teams[2].getPtsBonusMisere() -
                                        self.teams[2].getPtsBonusPoignee() - self.teams[3].getPtsBonusMisere() -
                                        self.teams[3].getPtsBonusPoignee() - self.teams[0].getPtsPetit() -
                                        self.teams[1].getPtsPetit() - self.teams[2].getPtsPetit() - self.teams[
                                            3].getPtsPetit())

    def showPointsInd(self):
        print("\n POINTS ")
        for i in range(5):
            print(self.teams[i].getName(), " : ", self.teams[i].getPoints())

    def verify(self, d):
        for i in range(5):
            if self.pli[i].getType() == self.color:
                winner = i
                c = self.pli[i]
            elif self.pli[i].getType() == 5:
                winner = i
                c = self.pli[i]
                self.color = 5
        for i in range(5):
            if self.pli[i].getType() == c.getType():
                if self.pli[i].getNum() > c.getNum():
                    winner = i
                    c = self.pli[i]
        for i in range(5):
            self.statut.addCarte(self.pli[i])

        if d != 15:
            for i in range(len(self.pli)):
                if self.pli[i].getType() == 6:
                    if self.test == False:
                        print("Excuse retourne")
                    self.places[i].getPtrPlayer().addPli(self.pli[i])
                    self.places[i].getPtrPlayer().setExcuse(1)
                    self.pli.remove(self.pli[i])
                    self.places[winner].getPtrPlayer().setExcuse(2)
                    break

        elif d == 15:
            for i in range(len(self.pli)):
                if self.pli[i].getType() == 6:
                    if self.test == False:
                        print(" L'excuse a ete jouee au dernier tour, le gagnant la recupere")
        self.transPli(winner)
        if self.test == False:
            print("Le turn a ete gagne par ", self.places[winner].getPtrPlayer().getName())
            self.clearPli()
            self.qui = winner

    def transPli(self, v):
        for i in range(len(self.pli)):
            self.places[v].getPtrPlayer().addPli(self.pli[i])

    def encheres(self):
        f = 0
        p = 0
        self.ench = 0
        print("ENCHERES")
        for i in range(self.qui, self.qui + 5):
            d = i
            if d > 4: d = d - 5
            self.places[d].getPtrPlayer().encheres()
        for i in range(0, 5):
            if self.places[i].getPtrPlayer().getEnch() > 0:
                f = self.places[i].getPtrPlayer().getEnch()
                p = i
        self.showEnch()
        if f == 1:
            self.ench = 10
        else:
            print(self.places[p].getPtrPlayer().getName(), "a apelle le", end=" ")
            if f == 2: print("Prise")
            if f == 3: print("Garde")
            if f == 4: print("Garde sans le chien")
            if f == 5: print("Garde contre le chien")
            self.places[p].getPtrPlayer().chooseRoi()
            if f == 2 or f == 3:
                self.places[p].getPtrPlayer().seeChien()
                self.places[p].getPtrPlayer().addCard(self.cards[0])
                self.places[p].getPtrPlayer().addCard(self.cards[1])
                self.places[p].getPtrPlayer().addCard(self.cards[2])
                self.places[p].getPtrPlayer().chien()
            elif f == 4:
                self.teams[0].addPli(self.cards[0])
                self.teams[0].addPli(self.cards[1])
                self.teams[0].addPli(self.cards[2])
            elif f == 5:
                self.teams[4].addPli(self.cards[0])
                self.teams[4].addPli(self.cards[1])
                self.teams[4].addPli(self.cards[2])

    def encheres2(self):
        f = 0
        self.ench = 0
        for i in range(self.qui, self.qui + 5):
            d = i
            if d > 4: d = d - 5
            self.places[d].getPtrPlayer().encheres()
        for i in range(0, 5):
            if self.places[i].getPtrPlayer().getEnch() > 0:
                f = self.places[i].getPtrPlayer().getEnch()
                p = i
        self.showEnch()
        if f == 1:
            self.ench = 10
        else:
            self.places[p].getPtrPlayer().chooseRoi()
            if f == 2 or f == 3:
                self.places[p].getPtrPlayer().seeChien()
                self.places[p].getPtrPlayer().addCard(self.cards[0])
                self.places[p].getPtrPlayer().addCard(self.cards[1])
                self.places[p].getPtrPlayer().addCard(self.cards[2])
                self.places[p].getPtrPlayer().chien()
            elif f == 4:
                self.teams[0].addPli(self.cards[0])
                self.teams[0].addPli(self.cards[1])
                self.teams[0].addPli(self.cards[2])
            elif f == 5:
                self.teams[4].addPli(self.cards[0])
                self.teams[4].addPli(self.cards[1])
                self.teams[4].addPli(self.cards[2])

    def getCardPtrPlayer(self, c, n):
        for i in range(5):
            if self.places[i].getPtrPlayer().haveCard(c, n):
                return self.places[i].getPtrPlayer()



    def setTeams(self):
        for i in range(5):
            if self.places[i].getPtrPlayer().getTeam() != 1:
                self.places[i].getPtrPlayer().setTeam(2)
                self.addTeam(self.places[i].getPtrPlayer())
        if self.type == 1:
            self.teams[1].addPartener(self.teams[0])
            self.teams[2].addPartener(self.teams[3])
            self.teams[2].addPartener(self.teams[4])
            self.teams[3].addPartener(self.teams[2])
            self.teams[3].addPartener(self.teams[4])
            self.teams[4].addPartener(self.teams[2])
            self.teams[4].addPartener(self.teams[3])
        elif self.type == 2:
            self.teams[1].addPartener(self.teams[2])
            self.teams[1].addPartener(self.teams[3])
            self.teams[1].addPartener(self.teams[4])
            self.teams[2].addPartener(self.teams[3])
            self.teams[2].addPartener(self.teams[4])
            self.teams[2].addPartener(self.teams[1])
            self.teams[3].addPartener(self.teams[2])
            self.teams[3].addPartener(self.teams[4])
            self.teams[3].addPartener(self.teams[1])
            self.teams[4].addPartener(self.teams[3])
            self.teams[4].addPartener(self.teams[2])
            self.teams[4].addPartener(self.teams[1])

    def addTeam(self, j):
        self.teams.append(j)

    def setEnch(self, e):
        self.ench = e

    def getEnch(self):
        return int(self.ench)

    def restart(self):
        for i in range(5):
            self.places[i].getPtrPlayer().restart()
        self.cards.clear()
        self.clearPli()
        self.color = 0
        self.qui = 0
        self.ench = 0
        self.type = 0
        self.le = 0
        self.colorRoi = 0
        self.first = 0
        self.teams.clear()
        self.statut.restart()

    def play(self):
        print("<<<<<<<<<<<<<<<<<<<<<Tarot>>>>>>>>>>>>>>>>>>>>>>>>>")
        print("Inserez votre nom :")
        name = input()
        self.createPlayers(name)
        self.first = int(5 * random.random())
        while 1:
            self.first += 1
            self.createCards()
            self.distributeCards()
            self.getPlacePtrPlayer(0).showCards()
            self.getPlacePtrPlayer(1).showCards()
            self.getPlacePtrPlayer(2).showCards()
            self.getPlacePtrPlayer(3).showCards()
            self.getPlacePtrPlayer(4).showCards()
            if self.petitSec():
                self.restart()
                continue

            self.encheres()
            if self.ench == 10:
                print("Personne n'a appele le chien. Alors, les cartes sont redistribuees.")
                self.restart()
                print("JEU RECOMENCE - ARTIE ")
                continue

            for k in range(5):
                self.getPlacePtrPlayer(k).setBoolean()
                self.getPlacePtrPlayer(k).announce()
            self.getPlacePtrPlayer(4).showCards()
            for i in range(1, 16):
                print("ROUND", i)
                self.color = 0
                self.atout = 0
                self.getPlacePtrPlayer(0).showCards()
                if i == 15:
                    for j in range(len(self.places)):
                        self.getPlacePtrPlayer(j).petitAuBout()
                self.action()
                self.showPli()
                self.verify(i)
                print()
                self.showPoints()
            print("\n<<<<<<<<<<<<<<<<<<<<<<<LA PARTIE EST TERMINE<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
            self.fin()
            self.showPointsInd()
            print("Voulez-vous jouer une autre fois? (y/n)")
            faire = input()
            if faire == "y":
                self.part += 1
                self.le += 1
                if self.le > 4:
                    self.le = self.le - 5
                self.qui = self.le
                self.restart()
                print("NOUVEAU JEU - PARTIE ", self.part)
                #continue
            else:
                print("FIN JEU")
                break

    def cardChien(self, f, g):
        for card in self.cards:
            if card.getNum() == g and card.getType() == f:
                return True
        return False

    def showTeams(self):
        print("EQUIPES")
        for i in range(5):
            print(self.teams[i].getName(), " est l'equipe ", self.teams[i].getTeam())

    def setType(self, e):
        self.type = e

    def getType(self):
        return self.type

    def setAtout(self, a):
        self.atout = a

    def getAtout(self):
        return self.atout

    def verifyEncheres(self):
        for i in range(1000):
            self.createCards()
            self.distributeCards()
            self.getPlacePtrPlayer(1).organize()
            self.getPlacePtrPlayer(1).showCards()
            self.getPlacePtrPlayer(1).encheres()
            points = self.places[1].getPtrPlayer().getPoints()
            if self.places[1].getPtrPlayer().getEnch() == 1:
                print(points, " / Passe")
            if self.places[1].getPtrPlayer().getEnch() == 2:
                print(points, " / Prise")
            if self.places[1].getPtrPlayer().getEnch() == 3:
                print(points, " / Garde")
            if self.places[1].getPtrPlayer().getEnch() == 4:
                print(points, " / Garde sans")
            if self.places[1].getPtrPlayer().getEnch() == 5:
                print(points, " / Garde Avec")

            self.restart()

    def winner(self):
        for i in range(5):
            if self.pli[i] is not None:
                if self.pli[i].getType() == self.color:
                    winner = i
                    c = self.pli[i]
                elif self.pli[i].getType() == 5:
                    winner = i
                    c = self.pli[i]
        for i in range(5):
            if self.pli[i] is not None:
                if self.pli[i].getType() == c.getType():
                    if self.pli[i].getNum() > c.getNum():
                        winner = i
                        c = self.pli[i]
        return winner

    def getColorRoi(self):
        return self.colorRoi

    def setColorRoi(self, n):
        self.colorRoi = n

    def petitSec(self):
        for i in range(0, len(self.places)):
            if self.getPlacePtrPlayer(i).haveCard(5, 1) and self.getPlacePtrPlayer(i).numCard(
                    5) == 1 and self.getPlacePtrPlayer(i).haveCard(6, 1) == False:
                return True
            return False

    def getPlaces(self):
        return self.places




















