import random

cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
winners = []

target_games = 0

deck = []

hit_wins = 0
stand_wins = 0

# def check_if_card_in_use(card):

# konvertera till blackjack-värde
def getCardValue(card):
    rank = card.split(' ')[0] # dra ut värdet från kortet, ex 7 från '7 of Hearts'
    if rank in ['J', 'Q', 'K']:
        return 10
    elif rank == 'A':
        return 1 # eller 1
    else:
        return int(rank)
    
def getHandValue(hand):
    hand_value = 0
    for card in hand:
        value = getCardValue(card)
        hand_value += value
        return hand_value

def pickACard(deck, cards, suits):
    card_found = False
    while not card_found:
        card = random.choice(cards)
        suit = random.choice(suits)
        card_name = f"{card} of {suit}"
        if card_name not in deck:
            deck.append(card_name)
            card_found = True
            return card_name
        else:
            print(f"{card} of {suit} already in use!")
        

def dealerHitUntil21(dealer_hand):
    dealer_hand_value = getHandValue(dealer_hand)
    while (dealer_hand_value < 17):
        card = pickACard(deck, cards, suits)
        dealer_hand.append(card)
        dealer_hand_value = getHandValue(dealer_hand)

def checkWinner(player_hand, dealer_hand):
    player_hand_value = getHandValue(player_hand)
    dealer_hand_value = getHandValue(dealer_hand)

    if (player_hand_value > 21):
        print("Player busted. Value above 21")
        return "dealer"
    else:
        if (dealer_hand_value > 21):
            print("Dealer busted. Value above 21")
            return "player"
        elif (player_hand_value > dealer_hand_value):
            print("Player value more than dealer value. Player win.")
            return "player"


def simulation():
    global target_games
    deck = []

    dealer_hand = []
    player_hand = []

    print(f"Deck: {deck}")

    # ge dealer 2 kort
    for i in range(0, 2):
        card = pickACard(deck, cards, suits)
        dealer_hand.append(card)

    # ge player 2 kort 
    for r in range(0, 2):
        card = pickACard(deck, cards, suits)
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

    player_target_value = 20
    dealer_target_value = 5

    # om target inte uppfylls
    if ((player_value != player_target_value) or (dealer_value != dealer_target_value)):
        print("Target didnt meet game")

    else: # simulationslogik 
        print("Target met game values!! :)")
        target_games = target_games + 1


        """
        # simulera alltid hit
        card = pickACard(deck, cards, suits)
        player_hand.append(card)

        # simulera alltid stand (ingenting lol)
        
        # kolla vinnaren

        # dealer logik
        dealerHitUntil21(dealer_hand)

        winner = checkWinner()
        winners.append(winner)
        """

for g in range(0, 100000): # antal gånger simulationen ska köras
    print("Startar ny simulation")
    simulation()


print(winners)
print(target_games)
