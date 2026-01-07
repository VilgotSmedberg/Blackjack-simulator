import random
import itertools
from collections import defaultdict

# tweakregler
NUM_DECKS = 1
HIT_SOFT_17 = False
ALLOW_DOUBLE_AFTER_SPLIT = True
SIMULATIONS_PER_DECISION = 50_000
BLACKJACK_PAYOUT = 1.5



def draw_card():
    card = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11])  
    return card


def hand_value(hand):
    total = sum(hand)
    aces = hand.count(11)
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total


def is_soft(hand):
    return 11 in hand and hand_value(hand) <= 21


def is_blackjack(hand):
    return len(hand) == 2 and hand_value(hand) == 21


def play_dealer_hand(hand):
    while True:
        value = hand_value(hand)
        if value < 17 or (value == 17 and is_soft(hand) and HIT_SOFT_17):
            hand.append(draw_card())
        else:
            break
    return hand_value(hand)



def simulate_round(player_hand, dealer_card, action):

    player = player_hand[:]
    dealer = [dealer_card, draw_card()]


    if is_blackjack(player):
        if is_blackjack(dealer):
            return 0
        return BLACKJACK_PAYOUT

    if action == "stand":
        player_total = hand_value(player)
    elif action == "hit":
        while hand_value(player) < 21:
            player.append(draw_card())
            if hand_value(player) >= 17:
                break
        player_total = hand_value(player)
    elif action == "double":
        player.append(draw_card())
        player_total = hand_value(player)
        bet = 2
    else:
        raise ValueError("Invalid action")

    dealer_total = play_dealer_hand(dealer)


    bet = 1 if action != "double" else 2
    if player_total > 21:
        return -bet
    elif dealer_total > 21:
        return bet
    elif player_total > dealer_total:
        return bet
    elif player_total < dealer_total:
        return -bet
    else:
        return 0



def simulate_ev(player_hand, dealer_upcard, action):
    total = 0
    for _ in range(SIMULATIONS_PER_DECISION):
        total += simulate_round(player_hand, dealer_upcard, action)
    return total / SIMULATIONS_PER_DECISION


def generate_basic_strategy():
    actions = ["hit", "stand", "double"]
    strategy = {}

    for player_total in range(5, 22):
        for dealer_card in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]:
            best_action = None
            best_ev = float("-inf")
            for action in actions:
                ev = simulate_ev([player_total], dealer_card, action)
                if ev > best_ev:
                    best_ev = ev
                    best_action = action
            strategy[(player_total, dealer_card)] = best_action
            print(f"Player {player_total} vs Dealer {dealer_card}: {best_action} (EV={best_ev:.3f})")

    return strategy



if __name__ == "__main__":
    strategy = generate_basic_strategy()

    print("\n\n Final table")
    for (player, dealer), move in sorted(strategy.items()):
        print(f"Player {player:>2} vs Dealer {dealer:>2} → {move}")
