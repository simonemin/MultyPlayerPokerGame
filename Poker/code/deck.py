import random

class Deck():
    
    def __init__(self):
        semi = ['Fiori', 'Picche', 'Cuori', 'Quadri']
        valori = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.deck = []
        for seme in semi:
            for valore in valori:
                self.deck.append([valore,seme])
        random.shuffle(self.deck)
        random.shuffle(self.deck)
    
    def stampa(self):
        print(self.deck)
    
    def dealCard(self):
        return self.deck.pop()

class Player():
    def __init__(self, id, name) -> None:
        self.id = id
        self.name = name
        self.hand = []
        self.status = 'waiting'
        self.chips = 1000
        self.pot = 0
    
    # Setter
    def set_hand(self, cards):
        self.hand.append(cards)
    
    def set_status(self, status):
        self.status = status

    def set_chips(self, num):
        self.chips += num
    
    def set_pot(self, bet):
        self.pot += bet
    
    # Getter
    def get_id(self):
        return self.id
    
    def get_name(self):
        return self.name
    
    def get_hand(self):
        return self.hand
    
    def get_status(self):
        return self.status
    
    def get_chips(self):
        return self.chips
    











        