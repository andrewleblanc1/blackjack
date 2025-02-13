#note: this was originally designed to work as a command line game
import random
class game:
    def __init__(self):
        # represents all cards in the deck
        self.unshuffledDeck = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52]
        # represents empty deck that unshuffled deck values will be inserted into randomly
        self.shuffledDeck = []
        # represents each cards image
        self.deckimg ={1: "2s",2:"2d",3:"2c",4:"2h",5: "3s",6:"3d",7:"3c",8:"3h",9: "4s",10:"4d",11:"4c",12:"4h",13: "5s",14:"5d",15:"5c",16:"5h",
           17: "6s",18:"6d",19:"6c",20:"6h", 21: "7s",22:"7d",23:"7c",24:"7h",25: "8s",26:"8d",27:"8c",28:"8h",29: "9s",30:"9d",31:"9c",32:"9h",
           33: "10s",34:"10d",35:"10c",36:"10h",37: "jacks",38:"jackd",39:"jackc",40:"jackh",41: "queens",42:"queend",43:"queenc",44:"queenh",
           45: "kings",46:"kingd",47:"kingc",48:"kingh",49: "aces",50:"aced",51:"acec",52:"aceh"}
        #represent each cards values (0 is a placeholder)
        self.deckValues =  [0,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6,7,7,7,7,8,8,8,8,9,9,9,9,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,11,11,11,11]
        #placeholders
        self.result = ""
        self.playerHand = []
        self.playerValue = 0
        self.dealerHand = []
        self.dealerValue = 0
        self.playerimg = []
        self.dealerimg = []
        self.blackjack = False


    # calculates player value according ensuring that if the aces value of 11 puts their hand over 21, the value of the ace is reverted to 1
    def calculatePlayerValue(self):
        self.playerValue = 0
        numAces = 0
        self.playerHand.sort()
        for card in self.playerHand:
            if card == 49 or card == 50 or card == 51 or card == 52:
                numAces += 1
        if numAces == 4:
            for card in self.playerHand:
                if card == 49 or card == 50 or card ==51 or card ==52:
                    if self.playerValue > 7:
                        self.playerValue += 1
                    else:
                        self.playerValue += self.deckValues[card]
                else:
                    self.playerValue += self.deckValues[card]
        if numAces == 3:
            for card in self.playerHand:
                if card == 49 or card == 50 or card ==51 or card ==52:
                    if self.playerValue > 8:
                        self.playerValue += 1
                    else:
                        self.playerValue += self.deckValues[card]
                else:
                    self.playerValue += self.deckValues[card]
        if numAces == 2:
            for card in self.playerHand:
                if card == 49 or card == 50 or card ==51 or card ==52:
                    if self.playerValue > 9:
                        self.playerValue += 1
                    else:
                        self.playerValue += self.deckValues[card]
                else:
                    self.playerValue += self.deckValues[card]
        if numAces == 1:
            for card in self.playerHand:
                if card == 49 or card == 50 or card ==51 or card ==52:
                    if self.playerValue > 10:
                        self.playerValue += 1
                    else:
                        self.playerValue += self.deckValues[card]
                else:
                    self.playerValue += self.deckValues[card]
        if numAces == 0:
            for card in self.playerHand:
                self.playerValue += self.deckValues[card]
    # calculates dealer value according ensuring that if the aces value of 11 puts their hand over 21, the value of the ace is reverted to 1
    def calculateDealerValue(self):
        self.dealerValue = 0
        numAces = 0
        self.dealerHand.sort()
        for card in self.dealerHand:
            if card == 49 or card == 50 or card == 51 or card == 52:
                numAces += 1
        if numAces == 4:
            for card in self.dealerHand:
                if card == 49 or card == 50 or card == 51 or card == 52:
                    if self.dealerValue > 7:
                        self.dealerValue += 1
                    else:
                        self.dealerValue += self.deckValues[card]
                else:
                    self.dealerValue += self.deckValues[card]
        if numAces == 3:
            for card in self.dealerHand:
                if card == 49 or card == 50 or card == 51 or card == 52:
                    if self.dealerValue > 8:
                        self.dealerValue += 1
                    else:
                        self.dealerValue += self.deckValues[card]
                else:
                    self.dealerValue += self.deckValues[card]
        if numAces == 2:
            for card in self.dealerHand:
                if card == 49 or card == 50 or card == 51 or card == 52:
                    if self.dealerValue > 9:
                        self.dealerValue += 1
                    else:
                        self.dealerValue += self.deckValues[card]
                else:
                    self.dealerValue += self.deckValues[card]
        if numAces == 1:
            for card in self.dealerHand:
                if card == 49 or card == 50 or card ==51 or card ==52:
                    if self.dealerValue > 10:
                        self.dealerValue += 1
                    else:
                        self.dealerValue += self.deckValues[card]
                else:
                    self.dealerValue += self.deckValues[card]
        if numAces == 0:
            for card in self.dealerHand:
                self.dealerValue += self.deckValues[card]
    # Draws cards until dealer has a value greater than or equal to 1
    def runoff(self):
        self.calculateDealerValue()
        if self.playerValue > 21:
            self.result = "bust :("
            return
        if self.playerValue == 21 and len(self.playerHand) == 2:
            self.result = "Blackjack!"
            self.blackjack = True
            return
        while self.dealerValue < 17:
            self.addDealerCard()
            self.calculateDealerValue()

    # checks if user value is over 21
    def checkbust(self):
        self.calculatePlayerValue()
        if self.playerValue > 21:
            self.result = "bust :("
            return True
        return
    # checks if user value is 21 - only used when game is started
    def checkblackjack(self):
        self.calculatePlayerValue()
        if self.playerValue == 21:
            self.result = "Blackjack!"
            self.blackjack = True
    # uses a random number generator to take cards from the unshuffled deck and insert them into the shuffled deck list
    def shuffleDeck(self):
        while len(self.unshuffledDeck) > 0:
            newCard = random.randint(0,len(self.unshuffledDeck)-1)
            self.shuffledDeck.append(self.unshuffledDeck[newCard])
            self.unshuffledDeck.pop(newCard)
    # adds a card to the players hand from shuffled deck
    def addPlayerCard(self):
        newCard = self.shuffledDeck.pop(0)
        self.playerHand.append(newCard)
        self.playerimg.append(self.deckimg[newCard])
    # adds a card to the dealers hand from shuffled deck
    def addDealerCard(self):
        newCard = self.shuffledDeck.pop(0)
        self.dealerHand.append(newCard)
        self.dealerimg.append(self.deckimg[newCard])
    # starts the game by giving the player and dealer two cards
    def startGame(self):
        self.shuffleDeck()
        self.addPlayerCard()
        self.addDealerCard()
        self.addPlayerCard()
        self.addDealerCard()
        self.calculatePlayerValue()
    # gets result depending on if the user or dealer has gone over 21 or whoever has the better hand
    def getResult(self):
        self.calculatePlayerValue()
        if self.result == "Blackjack!":
            return
        if self.result == "bust :(":
            return
        if self.playerValue > 21:
            self.result = "House Wins!"
            return
        if self.dealerValue > 21:
            self.result = "Player Wins!"
            return
        if self.playerValue > self.dealerValue:
            self.result = "Player Wins!"
        elif self.playerValue == self.dealerValue:
            self.result = "Push"
        else:
            self.result = "House Wins!"

