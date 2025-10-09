import random

cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
deck = []

def pickACard():
    card = random.choice(cards)
    suit = random.choice(suits)
    if f"{card} of {suit}" not in deck:
        deck.append(f"{card} of {suit}")
        return f"{card} of {suit}"
    else:
        print(f"{card} of {suit} already in use!")
        return pickACard()
        

# def check_if_card_in_use(card):

# konvertera till blackjack-värde
def getCardValue(card):
    rank = card.split(' ')[0] # dra ut värdet från kortet, ex 7 från '7 of Hearts'
    if rank in ['J', 'Q', 'K']:
        return 10
    elif rank == 'A':
        return 11 # eller 1
    else:
        return int(rank)

dealer_hand = []
player_hand = []

# ge dealer 2 kort
for i in range(0, 2):
    card = pickACard()
    dealer_hand.append(card)

# ge player 2 kort 
for i in range(0, 2):
    card = pickACard()
    player_hand.append(card)

print(f"Player hand: {player_hand}")
print(f"Dealer hand: {dealer_hand}")
print(deck)

dealer_value = 0
player_value = 0

# få värdet av dealers hand:
for card in dealer_hand:
    dealer_value += getCardValue(card)

for card in player_hand:
    player_value += getCardValue(card)

print(f"Player value: {player_value}")
print(f"Dealer value: {dealer_value}")
