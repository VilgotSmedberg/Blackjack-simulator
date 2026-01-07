import random

NUMBER_OF_DECKS = 6         
HIT_SOFT_17 = True           
BLACKJACK_PAYOUT = 1.5
ALLOW_SURRENDER = True       

def createShoe(decks):
    single = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
    shoe = single * (4 * decks)
    random.shuffle(shoe)
    return shoe

shoe = createShoe(NUMBER_OF_DECKS)

def pickACard():
    global shoe
    if len(shoe) < 15:
        shoe = createShoe(NUMBER_OF_DECKS)
    return shoe.pop()

def getHandValue(hand):
    total = sum(hand)
    aces = hand.count(11)
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total

def isSoft(hand):
    return 11 in hand and getHandValue(hand) <= 21

def isBlackjack(hand):
    return sorted(hand) == [10, 11]

def playDealer(hand):
    while True:
        v = getHandValue(hand)
        if v < 17:
            hand.append(pickACard())
        elif v == 17 and isSoft(hand) and HIT_SOFT_17:
            hand.append(pickACard())
        else:
            break

def simulateRound(player, dealer_up, action):
    dealer = [dealer_up, pickACard()]
    bet = 1

    if isBlackjack(player):
        if isBlackjack(dealer):
            return 0
        return BLACKJACK_PAYOUT * bet

    if action == "surrender" and ALLOW_SURRENDER:
        return -0.5 * bet

    if action == "stand":
        pass
    elif action == "hit":
        player.append(pickACard())
    elif action == "double":
        bet = 2
        player.append(pickACard())

    if getHandValue(player) > 21:
        return -bet

    playDealer(dealer)

    pv = getHandValue(player)
    dv = getHandValue(dealer)

    if dv > 21: return bet
    if pv > dv: return bet
    if pv < dv: return -bet
    return 0

def EV(hand, dealer, action, sims=10000):
    total = 0
    for _ in range(sims):
        total += simulateRound(hand[:], dealer, action)
    return total / sims

def generateBasicStrategy():
    actions = ["hit", "stand", "double"] + (["surrender"] if ALLOW_SURRENDER else [])
    deck = [2,3,4,5,6,7,8,9,10,10,10,10,11]

    print("\n Använder ruleset")
    print(f"{NUMBER_OF_DECKS} kortlekar - H17 {HIT_SOFT_17} - BJ: {BLACKJACK_PAYOUT} - Surrender: {ALLOW_SURRENDER}")

    # -------- SOFT TOTALS (8 → 20) --------
    for total in range(8, 21):  
        for dealer in [2,3,4,5,6,7,8,9,10,11]:

            # hitta första hand som ger total + är soft
            hand_found = None
            for a in deck:
                for b in deck:
                    hand = [a, b]
                    if isSoft(hand) and getHandValue(hand) == total:
                        hand_found = hand
                        break
                if hand_found:
                    break

            if not hand_found:
                continue

            best_ev = float("-inf")
            best_action = None
            for act in actions:
                ev = EV(hand_found, dealer, act)
                if ev > best_ev:
                    best_ev = ev
                    best_action = act

            print(f"soft {total} vs {dealer}: {best_action} (EV {best_ev:.3f})")

    # -------- HARD TOTALS (8 → 20) --------
    for total in range(8, 21): 
        for dealer in [2,3,4,5,6,7,8,9,10,11]:

            # hitta första hand som ger total + inte är soft
            hand_found = None
            for a in deck:
                for b in deck:
                    hand = [a, b]
                    if not isSoft(hand) and getHandValue(hand) == total:
                        hand_found = hand
                        break
                if hand_found:
                    break

            if not hand_found:
                continue

            best_ev = float("-inf")
            best_action = None
            for act in actions:
                ev = EV(hand_found, dealer, act)
                if ev > best_ev:
                    best_ev = ev
                    best_action = act

            print(f"hard {total} vs {dealer}: {best_action} (EV {best_ev:.3f})")

if __name__ == "__main__":
    generateBasicStrategy()
