import random

suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']

def get_shuffled_deck():
    deck = []
    for suit in suits:
        for i, rank in enumerate(ranks):
            if i == 0:
                num = 11
            elif i >= 9:
                num = 10
            else:
                num = i + 1
            deck.append({'Suit': suit, 'Rank': rank, 'Value': num})

    random.shuffle(deck)
    return deck

def get_value_of_hand(hand):
    sum_val = sum(card['Value'] for card in hand)
    if sum_val > 21:
        sum_val = sum(1 if card['Value'] == 11 else card['Value'] for card in hand)
    return sum_val

def is_hand_bust(hand):
    return get_value_of_hand(hand) > 21

def is_hand_blackjack(hand):
    return len(hand) == 2 and get_value_of_hand(hand) == 21

def dump_hand(hand):
    return ', '.join([dump_card(card) for card in hand])

def dump_card(card):
    return f"{card['Rank']} of {card['Suit']}"

deck = get_shuffled_deck()
card_ndx = -1

def deal_card():
    global card_ndx, deck
    if card_ndx < 0:
        print('Deck empty, reshuffling deck')
        deck = get_shuffled_deck()
        card_ndx = len(deck) - 1
    card_ndx -= 1
    return deck[card_ndx]

def write_to_pipe_and_log(msg):
    print(msg)

while True:
    print('Starting new game -----------------------------------------')
    player_hand = [deal_card()]
    dealer_hand = [deal_card()]

    player_hand.append(deal_card())
    dealer_hand.append(deal_card())

    print(f"Dealer's hand is {dump_card(dealer_hand[0])}, hole card")
    print(f"Player's hand is {dump_hand(player_hand)}")

    player_dealt_blackjack = is_hand_blackjack(player_hand)
    dealer_dealt_blackjack = is_hand_blackjack(dealer_hand)

    if player_dealt_blackjack and dealer_dealt_blackjack:
        print("Both the Dealer and Player get BLACKJACK. The game is a push")
    elif is_hand_blackjack(player_hand):
        print("Player gets BLACKJACK and wins!")
    elif is_hand_blackjack(dealer_hand):
        print("Dealer gets BLACKJACK and wins!")
    else:
        dealer_busts = False
        player_busts = False

        # Player's turn
        while True:
            stand = False
            invalid_key = False
            print("H for HIT or S for STAY")
            print("YOURMOVE: ")
            command = input()

            if command == "H":
                pass
            elif command == "S":
                stand = True
            else:
                invalid_key = True

            if invalid_key:
                print(f"Sorry, didn't recognize command: {command}")
                continue
            elif stand:
                print(f"Player stands with hand {dump_hand(player_hand)}")
                break
            else:
                new_card = deal_card()
                player_hand.append(new_card)
                print(f"Player drew a {dump_card(new_card)}, updated hand {dump_hand(player_hand)}")
                if is_hand_bust(player_hand):
                    player_busts = True
                    break

        # Dealer's turn
        print(f"Dealer's hand is {dump_hand(dealer_hand)}")
        if not player_busts:
            while True:
                dealer_sum = get_value_of_hand(dealer_hand)
                if dealer_sum > 21:
                    dealer_busts = True
                    break
                elif dealer_sum >= 17:
                    print(f"Dealer stands with {dump_hand(dealer_hand)}")
                    break

                new_card = deal_card()
                dealer_hand.append(new_card)
                print(f"Dealer draws {dump_card(new_card)}, updated hand {dump_hand(dealer_hand)}")
                import time
                time.sleep(1)

        # Determine who won
        if player_busts:
            print(f"Player busts with {dump_hand(player_hand)}")
            print(f"Dealer wins with {dump_hand(dealer_hand)}")
        elif dealer_busts:
            print(f"Dealer busts with {dump_hand(dealer_hand)}")
            print(f"Player wins with {dump_hand(player_hand)}")
        else:
            dealer_sum = get_value_of_hand(dealer_hand)
            player_sum = get_value_of_hand(player_hand)
            if dealer_sum > player_sum:
                msg = f"Dealer wins with {dump_hand(dealer_hand)}"
            elif player_sum > dealer_sum:
                msg = f"Player wins with {dump_hand(player_hand)}"
            else:
                msg = 'The game is a push'
            print(msg)

    print('ROUNDOVER')
    print('NEWDEAL')
    command = input()
    if command == 'EXIT':
        break

    import time
    time.sleep(2)

print('Game exiting')
