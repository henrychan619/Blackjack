#Python project - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
win = 0
loss = 0
score = win - loss

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

hand_value = 0

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.list = []

    def __str__(self):
        # return a string representation of a hand
        ans = ""
        for i in range(len(self.list)):
            ans += self.list[i].suit + self.list[i].rank + " "
        return "Hand contains " + ans

    def add_card(self, card):
        self.card = card
        self.list.append(self.card)# add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        global hand_value
        hand_value = 0
        apresent = False
        for i in self.list:
            value = VALUES.get(i.rank)    
            hand_value += value
            if "A" in i.rank:
                apresent = True
        if apresent and hand_value < 12:
            hand_value += 10
        return hand_value
  
    def draw(self, canvas, pos):
        counter = 0
        for i in self.list:
            card = Card(i.suit, i.rank)
            card.draw(canvas, [pos[0]+ counter*72, pos[1]])
            counter += 1

        
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        # create a Deck object
        for i in SUITS:
            for j in RANKS:
                ans = Card(i, j)
                self.deck.append(ans)
        random.shuffle(self.deck)

    def shuffle(self):
        # shuffle the deck 
        # use random.shuffle()
        return random.shuffle(self.deck)

    def deal_card(self):
       # deal a card object from the deck
       return random.choice(self.deck)
    
    def __str__(self):
        # return a string representing the deck
        ans3 = ""
        for i in range(len(self.deck)):
            ans3 += self.deck[i].suit + self.deck[i].rank + " "
        return "Deck contains " + ans3

global test_deck
#define event handlers for buttons
def deal():
    global outcome, in_play, player, dealer, loss, win, score, canvas
    
    if in_play == True:
        loss += 1
        score = win - loss
    global test_deck
    test_deck = Deck()
    test_deck.shuffle()
    
    player = Hand()
    a1 = test_deck.deal_card()
    player.add_card(a1)
    a2 = test_deck.deal_card()
    player.add_card(a2)
    
    
    print "Player " + str(player)
    print player.get_value()
    outcome = "Hit or deal?"
    
    dealer = Hand()
    b1 = test_deck.deal_card()
    dealer.add_card(b1)
    print "Dealer " + str(dealer)
    print dealer.get_value()    
    b2 = test_deck.deal_card()
    dealer.add_card(b2)
    
    in_play = True

def hit():
    
    global test_deck,outcome, in_play, win, loss, score
    a3 = test_deck.deal_card()
    player.add_card(a3)
    
    if player.get_value() <= 21:
      
        print "Player" + str(player)
        print player.get_value()
    else:
        print "Player" + str(player)
        print player.get_value()
        print "You have busted!"
        loss += 1
        score = win - loss
        outcome = "You have busted! New deal?"
        in_play = False
        # if the hand is in play, hit the player
   
    # if busted, assign a message to outcome, update in_play and score

    
def stand():
    global outcome, in_play, win, loss, score
    if player.get_value() >	21:
        print "You have busted!"
        outcome = "You have busted! No stand! New deal?"
        in_play = False
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    else:
        while dealer.get_value() < 17:
            b3 = test_deck.deal_card()
            dealer.add_card(b3)
            if dealer.get_value() > 21:
                print "dealer busted! You win"
                win += 1
                score = win - loss
                outcome = "dealer busted, you win! New deal?"
                in_play = False
    print "Dealer " + str(dealer)
    print dealer.get_value()        
    # assign a message to outcome, update in_play and score
    if player.get_value() <= 21 and dealer.get_value() <= 21:
        if player.get_value() > dealer.get_value():
            print "You win! "
            outcome = "You win! New deal?"
            win += 1
            score = win - loss
            in_play = False
        else:
            print "You lose!" 
            outcome = "You lose! New deal?"
            loss += 1
            score = win - loss
            in_play = False

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below

    player.draw(canvas, [200, 400])
    canvas.draw_text("Your card: ", [80, 450], 25, "Black")
    
    dealer.draw(canvas, [200, 200])
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [236,248], CARD_BACK_SIZE)    
    canvas.draw_text("Dealer's card: ", [50, 250], 25, "Black")
    
    canvas.draw_text("Blackjack", [200, 150], 50, "Black")
    canvas.draw_text(str(outcome), [50, 50], 25, "Black")
    canvas.draw_text("Score: " +str(score), [500, 50], 25, "Black")
    canvas.draw_text("Value: ", [490, 525], 25, "Black")
    canvas.draw_text(str(player.get_value()), [560,525], 25, "Black")
    
    
    # initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()
