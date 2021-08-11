class Card:
    def __init__(self, type, num):
        self.type = type
        self.num = num

        if type == 6:
            self.value = 4.5
            self.coef = 6450
        elif type == 5:
            if num == 1 or num == 21:
                self.value = 4.5
            else:
                self.value = 0.5
                self.coef = num
            if num == 1: self.coef = 6350;
            if num == 21: self.coef = 6550
        elif num == 14:
            self.value = 4.5
            self.coef = 10
        elif num == 13:
            self.value = 3.5
            self.coef = 3.5
        elif num == 12:
            self.value = 2.5
            self.coef = 2
        elif num == 11:
            self.value = 1.5
            self.coef = 1
        else:
            self.value = 0.5
            self.coef = 0

    def showCard(self):
        if self.type != 6: print(self.num, end=" ")
        if self.type == 1: print("Pique")
        elif self.type == 2: print("Trefle")
        elif self.type == 3: print("Carreau")
        elif self.type == 4: print("Coeur")
        elif self.type == 5: print("Atout")
        elif self.type == 6: print("Excuse")

    def getType(self):
        return self.type

    def getNum(self):
        return self.num

    def getValue(self):
        return self.value

    def getCoef(self):
        return self.coef

    def setCoef(self, c):
        self.coef = c