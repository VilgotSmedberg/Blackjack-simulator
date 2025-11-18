import random

def initializeDeck(cards, suits):
    return [f"{card} of {suit}" for card in cards for suit in suits]

cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

deck = initializeDeck(cards, suits)

winners = []

target_games = 0

hit_wins = 0
hit_losses = 0
hit_pushes = 0

stand_wins = 0
stand_losses = 0
stand_pushes = 0

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
    if not deck:
        print("Deck is empty!")
        return None
    card = random.choice(deck)
    deck.remove(card) # remove the card from the deck in order to make sure it cant be drawn again
    return card
    
def hasBlackjack(hand):
    return 11 in hand and getHandValue(hand) == 21

def dealerHitUntil21(dealer_hand, deck):
    while getHandValue(dealer_hand) < 17:
        card = pickACard(deck, cards, suits)
        if card is None:
            break  # stop if no cards left
        dealer_hand.append(card)

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
        elif (player_hand_value == dealer_hand_value):
            print("It's a tie (push).")
            return "push"
        else:
            print("Dealer wins.")
            return "dealer"



def simulation():
    global stand_wins, hit_wins, target_games
    global hit_losses, hit_pushes, stand_losses, stand_pushes
    # global stand_wins, hit_wins, target_games

    deck = initializeDeck(cards, suits)

    hit_deck = []
    hit_hand = []
    stand_hand = []

    dealer_hand = []
    player_hand = []

    print(f"Number of cards in deck: {len(deck)}")

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

    dealer_value = 0
    player_value = 0

    # få värdet av dealers hand:
    dealer_value = getHandValue(dealer_hand)

    player_value = getHandValue(player_hand)

    print(f"Player value: {player_value}")
    print(f"Dealer value: {dealer_value}")

    player_target_value = 20
    dealer_target_upcard = 4 # den här ska ändras till endast ETT KORT, dealer_target_upcard 

    # om target inte uppfylls
    # print(dealer_hand)
    if ((player_value != player_target_value) or (getCardValue(dealer_hand[0]) != dealer_target_upcard)):
        print("Target didnt meet game")

    else: # simulationslogik 
        print("Target met game values! :)")
        target_games += 1

        #"""
        # SIMULATE HIT
        hit_hand = player_hand.copy()
        hit_deck = deck.copy()
        hit_hand.append(pickACard(hit_deck, cards, suits))
        print(f"Player hit.. and has hand {hit_hand}!")
        dealer_hit = dealer_hand.copy()
        dealerHitUntil21(dealer_hit, hit_deck)
        result_hit = checkWinner(hit_hand, dealer_hit)
        if result_hit == "player":
            hit_wins += 1
        elif result_hit == "dealer":
            hit_losses += 1
        else: 
            hit_pushes += 1

        # SIMULATE STAND (ingenting lol)
        stand_hand = player_hand.copy()
        dealer_stand = dealer_hand.copy()
        stand_deck = deck.copy()
        dealerHitUntil21(dealer_stand, stand_deck)
        result_stand = checkWinner(stand_hand, dealer_stand)
        if result_stand == "player":
            stand_wins += 1
        elif result_stand == "dealer":
            stand_losses += 1
        else:
            stand_pushes += 1
        
        # kolla vinnaren

        # dealer logik
        #"""

for g in range(0, 10000): # antal gånger simulationen ska köras
    print(f"Startar simulation #{g}")
    simulation()

print("-----")
print("   RESULTS   ")
print(f"Target games: {target_games}\n")
print((f"Hit wins: {hit_wins}"))
print((f"Hit losses: {hit_losses}"))
print(f"Stand wins: {stand_wins}")
print(f"Stand losses: {stand_losses}")

print("-----")
print(f"Hit win rate: {((hit_wins / target_games) * 100):.3f}%") 
print(f"Stand win rate: {((stand_wins / target_games) * 100):.3f}%")
print("-----")

total_hit = hit_wins + hit_losses + hit_pushes
total_stand = stand_wins + stand_losses + stand_pushes

ev_hit = (hit_wins - hit_losses) / total_hit
ev_stand = (stand_wins - stand_losses) / total_stand

print(f"EV (Hit): {ev_hit:.3f}")
print(f"EV (stand): {ev_stand:.3f}")

if (ev_hit > ev_stand):
    print("Hitting it better")
else:
    print("Standing is better")
