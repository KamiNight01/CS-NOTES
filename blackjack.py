#!/usr/bin/env python3

# ----------------------------------------------------------------------
# blackjack.py
# Dave Reed
# 08/01/2022
# ----------------------------------------------------------------------

from graphics import *
from CardDeck import *

# ----------------------------------------------------------------------

def drawCard(filename: str, x: int, y: int, window: GraphWin):
    """
    draw image specified by filename centered at (x, y) in window
    :param filename: filename for card - see cardInfo for details
    :param x: x-coordinate for center of card image
    :param y: y-coordinate for center of card image
    :param window: GraphWin to draw card in
    :return: None
    """
    
    p = Point(x, y)
    prefixes = ['cardset/', '../cardset/', './']
    for prefix in prefixes:
        fname = f'{prefix}{filename}'
        try:
            image = Image(p, fname)
            image.draw(window)
            return image
        except:
            pass
            
# ----------------------------------------------------------------------
    
    
def cardInfo(cardNumber) -> (int, str):
    """
    returns the blackjack value and and filename for card specified
    :param cardNumber: card 0 to 51
    :return: blackjack value 2-11 for card and filename - see below for these

    0-12 are the Ace-King of clubs
    13-25 are the Ace-King of spades
    26-38 are the Ace-King of hearts
    39-51 are the Ace-King of diamonds

    the blackjack value for the cards 2-9 are the corresponding
    number; 10, Jack, Queen, and King all have blackjack values of 10
    and an Ace has a value of 11

    filename is of the form: ##s.gif
    where ## is a two digit number (leading 0 if less than 10)
    and s is a letter corresponding to the suit value
    c for clubs, s for spades, h for hearts, d for diamonds
    """
    
    # calculate suit and face numbers
    suitNum = cardNumber // 13
    faceNum = cardNumber % 13
    
    # calculate blackjack value
    value = faceNum + 1
    if value > 10:
        value = 10
    elif value == 1:
        value = 11 or value == 1
        
    # calculate name of file
    # face is a number from 1 to 13 with leading zeros for 1-9
    suits = 'cshd'
    filename = f"{faceNum + 1:>02}{suits[suitNum]}.gif"
    return value, filename


# ---------------------------------------------

def main():


    # create window, card deck and shuffle it
    win = GraphWin('Blackjack', 800, 600)
    # in case use dark mode on Mac
    win.setBackground("white")

    deck = CardDeck()
    deck.shuffle()

    p_total = 0
    dealer_total = 0

    # create a Text object for the player's total below the cards
    p_total_text = Text(Point(100, 200), f"Player Total: {p_total}")
    p_total_text.setSize(10)
    p_total_text.setStyle("bold")
    p_total_text.setTextColor("black")
    p_total_text.draw(win)


    # dealer total
    dealer_total_text = Text(Point(100, 400), f"Dealer Total: {dealer_total}")
    dealer_total_text.setSize(10)
    dealer_total_text.setStyle("bold")
    dealer_total_text.setTextColor("black")
    dealer_total_text.draw(win)

    # deal a card and display it
    card = deck.dealOne()
    value, filename = cardInfo(card)
    drawCard(filename, 100, 100, win)
    p_total += value

    # deal a card and display it
    card2 = deck.dealOne()
    value, filename = cardInfo(card2)
    drawCard(filename, 200, 100, win)
    p_total += value

    p_total_text.setText(f"Player Total: {p_total}")

    #create a hit me button
    box = Rectangle(Point(550, 220), Point(650, 240))
    box.setFill("lightblue")
    box.draw(win)

    # Add text inside the box
    hitText = Text(Point(600, 230), "HIT!")
    hitText.setSize(10)
    hitText.setStyle("bold")
    hitText.setTextColor("black")
    hitText.draw(win)

    # continue dealing if below 21 for player
    playerx = 300
    while p_total < 21:
        click_point = win.getMouse()
        if 550 < click_point.x < 650 and 220 < click_point.y < 240:
            card = deck.dealOne()
            value, filename = cardInfo(card)
            drawCard(filename, playerx, 100, win)
            p_total += value
            print(p_total)
            playerx += 100
            p_total_text.setText(f"Player Total: {p_total}")
            # create a Text object for the player's total below the cards

            if p_total > 21:
                break

    # -------------------------



    # wait for mouse click before closing window
    win.getMouse()
    win.close()
    
# ----------------------------------------------------------------------

if __name__ == '__main__':
    main()




#__________________________________________________________________________________________________________________________________________________________________________________________________________




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
