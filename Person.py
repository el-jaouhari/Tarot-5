from Player import Player
from Table import *

class Person(Player):
    def __init__(self, table, name, position):
        Player.__init__(self, table, name, position)

    def chooseRoi(self):
        self.team=1
        print("Appel du Roi :")
        print("[1] Pique")
        print("[2] Trefle")
        print("[3] Carreau")
        print("[4] Coeur")
        c = int(input("Le roi choisi est : "))
        self.table.setColorRoi(c)
        self.table.addTeam(self)

        if not self.table.cardChien(c,14) and self.table.getCardPtrPlayer(c,14).getName()!=self.name:
            self.partners.append(self.table.getCardPtrPlayer(c,14))
            self.table.addTeam(self.table.getCardPtrPlayer(c, 14))
            self.table.getCardPtrPlayer(c, 14).setTeam(1)
            self.table.setType(1)
            self.table.setTeams()
        else:
            self.table.setType(2)
            self.table.setTeams()

    def encheres(self):
        self.table.showEnch()
        print("VOTRE DECISION")
        print("[1] Pas")
        print("[2] Prise")
        print("[3] Gard")
        print("[4] Gard sans le chien")
        print("[5] Gard contre le chien")
        while 1:
            self.ench=int(input("Votre décision est : "))
            if self.ench!=0 and self.ench<=self.table.getEnch():
                print("Rechoisissez.")
            elif self.ench!=0:
                self.table.setEnch(self.ench)
                break

    def play(self):
        self.table.showPli()
        while 1:
            card=int(input("Coisissez une carte : "))
            if card>len(self.cards):
                print("Cette carte n'existe pas.")
                continue
            n=card-1
            if self.table.getColor()==0 or self.table.getColor()==6:
                if len(self.cards)==15 and self.cards[n].getType()==self.table.getColorRoi():
                    if self.cards[n].getNum()!=14:
                        print("Vous ne pouvez pas jouer cette carte.")
                        continue
                self.table.setColor(self.cards[n].getType())
            elif self.cards[n].getType()!=self.table.getColor():
                if self.cards[n].getType()!=5 and (self.numCard(self.table.getColor())!=0 or self.numCard(5)!=0) and self.cards[n].getType()!=6:
                    print("Vous ne pouvez pas jouer cette carte.")
                    continue
                if self.cards[n].getType() == 5 and (self.cards[n].getNum()<self.table.getAtout() or self.numCard(self.table.getColor())!=0) and self.haveAtout(self.table.getAtout()):
                    print("Vous ne pouvez pas jouer cette carte.")
                    continue
                if self.cards[n].getType()==5:
                    self.statut.setType(self.table.getColor(), 0)
                elif self.cards[n].getType()!=6:
                    self.statut.setType(self.table.getColor(), 0)
                    self.statut.setType(5, 0)

            elif self.table.getColor()==5:
                if self.cards[n].getType()==5 and self.cards[n].getNum()<self.table.getAtout() and self.haveAtout(self.table.getAtout()):
                    print("Vous ne pouvez pas jouer cette carte.")
                    continue
            if self.cards[n].getType()==5 and self.cards[n].getNum()>self.table.getAtout():
                self.table.setAtout(self.cards[n].getNum())
            if self.cards[n].getType() == self.table.getColorRoi() and self.cards[n].getNum()==14:
                self.table.statut.setTeams(True)
            self.table.addPli(self.cards[n], self.position)
            self.cards.remove(self.cards[n])
            break

    def seeChien(self):
        self.table.showCards()

    def chien(self):
        self.organize()
        while len(self.cards)>15:
            print("Vos cartes")
            self.showCards()
            if len(self.cards)==18:
                print("Choisissez la premiere carte à jeter: ")
            elif len(self.cards)==17:
                print("Choisissez la deuxieme carte à jeter: ")
            elif len(self.cards)==16:
                print("Choisissez la troisieme carte à jeter: ")
            n=int(input())
            if n>len(self.cards):
                print("cette carte n'existe pas")
            elif self.cards[n-1].getType()==6 or self.cards[n-1].getType()==5 or self.cards[n-1].getNum()==14:
                print("Vous ne pouvez pas jeter cette carte.")
            elif self.numRoi()+self.numCard(5)+self.numCard(6)!=len(self.cards) and (self.cards[n-1].getType()==6 or self.cards[n-1].getType()==5 or self.cards[n-1].getNum()==14):
                print("Vous ne pouvez pas jeter cette carte.")
            elif self.cards[n-1].getType()==6 or self.cards[n-1].getNum()==1 or self.cards[n-1].getNum()==21 or (self.cards[n-1].getNum()==14 and self.cards[n-1].getType()!=14):
                print("Vous ne pouvez pas jeter cette carte.")
            else:
                print("Le joueur ", self.name, "a mis au chien le", end=" ")
                self.cards[n-1].showCard()
                self.addPli(self.cards[n-1])
                self.cards.remove(self.cards[n-1])

    def announce(self):
        if self.misereTete:
            print("Voulez vous annoncer une misere de tete ? (y/n)")
            while 1:
                n=input()
                if n=="y" or n=="Y":
                    self.ptsBonusMisere+=10
                    print("Le joueur ", self.name," a annoncé une misere de tete.")
                    break
                elif n=="n":
                    break
                else:
                    print("Veuillez rechoisir")

        if self.misereAtout:
            print("Voulez vous annoncer une misere d'Atout ? (y/n)")
            while 1:
                n=input()
                if n=="y":
                    self.ptsBonusMisere+=10
                    print("Le joueur ", self.name," a annoncé une misere d'Atout.")
                    break
                elif n=="n":
                    break
                else:
                    print("Veuillez rechoisir")

        if self.poignee:
            if self.doublepoignee:
                print("Voulez vous annoncer une double poignee ? (y/n)")
                while 1:
                    n=input()
                    if n=="y":
                        self.ptsBonusPoignee+=30
                        print("Le joueur ", self.name," a annoncé une double poignee")
                        self.showPoignee(2)
                        break
                    elif n=="n":
                        break
                    else:
                        print("Veuillez rechoisir")
            else:
                print("Voulez vous annoncer une poignee ? (y/n)")
                while 1:
                    n = input()
                    if n == "y":
                        self.ptsBonusPoignee += 20
                        print("Le joueur ", self.name, " a annoncé une poignee")
                        self.showPoignee(1)
                        break
                    elif n == "n":
                        break
                    else:
                        print("Veuillez rechoisir")

    def showPoignee(self, n):
        k=self.numCard(5)
        choice=[0]
        if n==1:
            print("Veuillez montrer 6 atouts autres que le plus petit et le plus grand: ")
            if self.haveCard(6,1):
                for i in range(1,7):
                    t=True
                    while t:
                        t=False
                        m=int(input())
                        for j in range(i):
                            if m<=15-k or m==14 or m>15 or m==choice[j]:
                                print("Erreur, choissisez une autre carte")
                                t=True
                        if t==False:
                            choice.append(m)
                print("Poignee montrée")
                self.cards[14-k].showCard()
                print()
                for i in range(1,6):
                    self.cards[choice[i]-1].showCard()
                    print()
                self.cards[13].showCard()
                print()
            else:
                for i in range(1, 7):
                    t = True
                    while t:
                        t = False
                        m = int(input())
                        for j in range(i):
                            if m <= 16 - k or m >= 15 or m == choice[j]:
                                print("Erreur, choissisez une autre carte")
                                t = True
                        if t == False:
                            choice.append(m)
                print("Poignee montrée")
                self.cards[15 - k].showCard()
                print()
                for i in range(1, 6):
                    self.cards[choice[i] - 1].showCard()
                    print()
                self.cards[14].showCard()
                print()

        if n==2:
            print("Veuillez montrer 8 atouts autres que le plus petit et le plus grand: ")
            if self.haveCard(6, 1):
                for i in range(1, 9):
                    t = True
                    while t:
                        t = False
                        m = int(input())
                        for j in range(i):
                            if m <= 15 - k or m == 14 or m > 15 or m == choice[j]:
                                print("Erreur, choissisez une autre carte")
                                t = True
                        if t == False:
                            choice.append(m)
                print("Poignee montrée")
                self.cards[14 - k].showCard()
                print()
                for i in range(1, 8):
                    self.cards[choice[i] - 1].showCard()
                    print()
                self.cards[13].showCard()
                print()
            else:
                for i in range(1, 9):
                    t = True
                    while t:
                        t = False
                        m = int(input())
                        for j in range(i):
                            if m <= 16 - k or m >= 15 or m == choice[j]:
                                print("Erreur, choissisez une autre carte")
                                t = True
                        if t is False:
                            choice.append(m)
                print("Poignee montrée")
                self.cards[15 - k].showCard()
                print()
                for i in range(1, 8):
                    self.cards[choice[i] - 1].showCard()
                    print()
                self.cards[14].showCard()
                print()







