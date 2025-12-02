from abc import ABC, abstractmethod
from random import shuffle
from time import sleep

class Card:

    def __init__(self,name : str):
        if name == '1':

            name = 'A'

        if name in ['J','Q','K']:
            self.points = 10
        elif name == 'A':
            self.points = 11
        else:
            self.points = int(name)

        self.name = name

    def value(self,score : int) -> int:
        
        if self.name == 'A' and score + 11 > 21:
            return 1
        
        return self.points

    def __str__(self):
        s  = ""
        s += self.name
        return s

class GameState:

    def __init__(self):

        self.dealer_hand = []
        self.player_hand = []
        self.deck = []
        self.turn = 0
            
        #4 of 1- 10 = 40
        #4 of J Q K = 12

        for i in range(1,11):
            self.deck.append(Card(str(i)))
            self.deck.append(Card(str(i)))
            self.deck.append(Card(str(i)))
            self.deck.append(Card(str(i)))

        for i in range(4):
            self.deck.append(Card("J"))
            self.deck.append(Card("Q"))
            self.deck.append(Card("K"))
        
        shuffle(self.deck)

    def player_score(self) -> int:

        player_score = 0
        aces = []
        #As will not work as expected if they come first,sort arrays        
        for card in self.player_hand:
            if card.name == 'A':
                aces.append(card)
            else:
                player_score = player_score + card.value(player_score)

        for card in aces:
            player_score = player_score + card.value(player_score)
        
        return player_score


    def serialize(self) -> dict[str: any]:
        
        pcards = []
        dcards = []
        turn = self.turn 
        deck = []
        for card in self.player_hand:
            pcards.append(card.name)
        
        for card in self.dealer_hand:
            dcards.append(card.name)


        for card in self.deck:
            deck.append(card.name)

        return {

            "phand" : pcards,
            "dhand" : dcards,
            "turn" : turn,
            "deck" : deck 

        }

    def to_state(self, d : dict[str : any]):

        turn = d["turn"]
        deck_names = d["deck"]
        pcard_names = d["phand"]
        dcard_names = d["dhand"]
        deck = []
        pcards = []
        dcards = []

        for name in deck_names:
            deck.append(Card(name))

        for name in pcard_names:
            pcards.append(Card(name))

        for name in dcard_names:
            dcards.append(Card(name)) 
    
        self.turn = turn
        self.deck = deck
        self.player_hand = pcards
        self.dealer_hand = dcards


    def dealer_score(self,hide : bool = False) -> int:
        dealer_score = 0
        
        if hide:
            return self.dealer_hand[0].value(0)

        if hide:
            return self.dealer_hand[0].value(dealer_score)

        
        aces = []
        #As will not work as expected if they come first,sort arrays
        for card in self.dealer_hand:
            if card.name == 'A':
                aces.append(card)
            else:
                dealer_score = dealer_score + card.value(dealer_score)
        for card in aces:
            dealer_score = dealer_score + card.value(dealer_score)
        
        return dealer_score

    def actions(self,score : int) -> list[int]:

        #0 is stay, 1 is hit
        if score > 21:
            return [0]
        return [0,1]

    def draw_card(self) -> Card:
        card = self.deck.pop()
        return card

    def deal_cards(self,amt : int,player : int = None):

        if player is None:
            player = self.turn

        if player == 0:
            p = self.player_hand
        
        elif player == 1:
            p = self.dealer_hand 
        
        for i in range(amt):
        
            card = self.draw_card()
            p.append(card)

            #(custom) bubble sort the hands so As come last
            #for i in range(p)
    
    def is_over(self) -> bool:
        return self.turn > 1

    def hit(self):
       
        self.deal_cards(1)
    
    def stay(self):

        #0 -> 1 : player ends, dealer begins
        #1 -> 2 : game ends
        self.turn += 1
        print(f"NEW TURN IS {self.turn}")

    #breaks if -> GameState
    def result(self,action):

        action = int(action)

        if self.turn == 0:
            score = self.player_score()
        else:
            score = self.dealer_score()
        
        if self.is_over():
            raise ValueError("Cannot act on a finished game")

        if action not in self.actions(score) and self.turn == 0 :
            raise ValueError(f"Illegal action, actions are {type(self.actions(score))}, got {type(action)}")

        elif action == 1:
            self.hit()
            
        #player hits and goes beyond
        if self.turn == 0 and self.player_score() > 21:
            self.turn = self.turn + 1

        #dealer hits and goes beyond
        if self.turn == 1 and self.dealer_score() > 21:
            self.turn = self.turn + 1

        if action == 0:
            self.stay()
        return self

    def get_winner(self) -> int:

    #either player is above 21 or below dealer, who isnt above 21   
        if self.player_score() > 21 or self.player_score() < self.dealer_score() <= 21:
            print("YOU LOSE")
            return -1
        #player is above dealer, but not 21 or dealer is above 21
        elif 21 >= self.player_score() > self.dealer_score() or self.dealer_score() > 21:
            print("YOU WIN")
            return 1
        #both are tied
        elif self.player_score() == self.dealer_score():
                print("IT'S A TIE")
                return 0



class Player(ABC):
    
    @abstractmethod
    def __init__(self):
        pass
    
    #1 means hit, 2 means stay 
    @abstractmethod
    def get_move(self,state : GameState) -> int:
        pass

class HumanPlayer(Player):

    def __init__(self):
        self.name = "Human"
    
    def terminal_input(self):
        print("Hit or pass?")
        res = input()
        if res:
            return 1
        return 0

    def get_move(self,state : GameState) -> int:

            return self.terminal_input()

class Dealer(Player):

    def __init__(self):
            self.name = "House"

    def get_move(self,state : GameState) -> int:

        if state.dealer_score() < 17:
            
            return 1

        else:
            return 0

class BlackJack:

    def __init__(self, state : GameState = None):
        if state:
            self.state = state

            self.dealer = Dealer()      #not sure if necessary but could avoid errors
            self.player = HumanPlayer() #not sure if necessary but could avoid errors
        else:
            self.state = GameState()
            self.dealer = Dealer()
            self.player = HumanPlayer()

            self.state.deal_cards(2,0)
            print(f"PLAYER HAND = {self.state.player_hand}")
            self.state.deal_cards(2,1)
            print(f"DEALER HAND = {self.state.dealer_hand}")

   
    def play_game(self):
        
        while not self.state.is_over():
            

            if self.state.turn == 0:
                score = self.state.player_score()
            else:
                score = self.state.dealer_score()
            legal_actions = self.state.actions(score)
            
            if self.state.turn == 0:
                for card in self.state.player_hand:
                    print(card.name)
                print(f"your score: {self.state.player_score()}")
            
            hide = self.state.turn == 0
            print(f"dealer score: {self.state.dealer_score(hide = hide)}")
            if hide:
                sleep(0.5)
            move = -1 
            if self.state.turn == 0:
                
                while move not in legal_actions:
                
                    move = self.player.get_move(self.state)

            elif self.state.turn == 1:
                if self.state.player_score() > 21:
                    self.state.turn = 2
                    move = 2
                else:
                    while move not in legal_actions:
               
                        move = self.dealer.get_move(self.state)
            if move != 2:
                new_state = self.state.result(move)
                self.state = new_state
        print("final results:")
        print(f"your score : {self.state.player_score()}")
        print(f"house score : {self.state.dealer_score()}")


        if self.state.turn == 1:
            print(f"dealer score: {self.state.dealer_score(hide = False)}")
            sleep(0.5)
        
        if self.state.player_score() > 21 or self.state.player_score() < self.state.dealer_score() <= 21:
            print("YOU LOSE")
        elif 21 >= self.state.player_score() > self.state.dealer_score() or self.state.dealer_score() > 21:
            print("YOU WIN")
        elif self.state.player_score() == self.state.dealer_score():
            print("IT'S A TIE")
    
        

if __name__ == '__main__':
    bj = BlackJack()
    bj.play_game()
    #pl = HumanPlayer()
    #x = pl.get_move(bj.state)
    #print(x)
