'''
random --> provides a function to exit the program
sys --> provides a function to exit the program
'''
import random
import sys

values = {'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8,
          'nine': 9, 'ten': 10, 'jack': 10, 'queen': 10, 'king': 10, 'ace': "TBD"}

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')


class Card:
    '''
    All cards have a suit, a rank and a value.
    '''
    # defines card suit, rank, value
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank.lower()]

    # print value
    def __str__(self):
        return (self.rank + " of " + self.suit).lower()

    def __repr__(self):
        return (self.rank + " of " + self.suit).lower()


class Deck:
    '''
    Constituting the deck with a for loop until all card combinations are in the deck
    '''
    def __init__(self):
        self.all_cards = []
        for suit in suits:
            for rank in ranks:
                self.all_cards.append(Card(suit, rank))

    def shuffle(self):
        '''
        To be used before game starts
        :return: a shuffled deck
        '''
        random.shuffle(self.all_cards)

    def is_ace_choice_valid(self, answer, accepted_values):
        return str(answer).isdigit() is True and int(answer) in accepted_values

    def deal_one(self):
        '''
        Adds one cards to the hand. if it's an ace, you have to choose the value.
        :return: a Card
        '''
        new_card = self.all_cards.pop()
        accepted_values = [1, 11]
        if new_card.rank == "Ace":
            print("an ace has been drawn.")
            answer = input("Does this ace count as 1 or 11?")
            while not self.is_ace_choice_valid(answer, accepted_values):
                print("please, only write 1 or 11.")
                answer = input("Does this ace count as 1 or 11?")
            new_card.value = int(answer)
        return new_card

new_deck = Deck()
new_deck.shuffle()


class Player:
    '''
    the human player of this came
    '''
    def __init__(self, money):
        self.money = money
        self.cards = []
        self.bet_amount = 0
        self.card_value = 0

    # TODO this check method does no check
    def check_bank(self):
        '''
        a string telling you how much money you got
        :return: a printed str
        '''
        return print(f'You still have {self.money} to bet.')

    def bet(self):
        '''
        betting the money.
        :return: an input and an update of self.bet_amount
        '''
        allowed_range = range(1, self.money + 1)

        while str(self.bet_amount).isdigit() is False or int(self.bet_amount) not in allowed_range:
            self.bet_amount = input("How much do you want to bet?")
            if self.bet_amount.isdigit() is False:
                print("hey, please input only integers from 1 to however much you can afford!")
                continue
            if self.bet_amount == "0":
                print("you have to bet something!")
                continue
            if int(self.bet_amount) > self.money:
                print("you don't have THAT kind of money.")
                continue
        print(f"alright, you will bet {self.bet_amount}")

        self.bet_amount = int(self.bet_amount)
        self.money -= self.bet_amount

    # TODO if you call it "add money" is more reusable.
    def add_won_money(self):
        '''
        if you win, it will add double the money you bet
        :return: update to money
        '''
        self.money += self.bet_amount * 2

    # TODO methods are usually actions -> update card value
    def card_value_update(self):
        '''
        to use every time a new card is drawn
        :return: an update to card.value
        '''
        self.card_value = 0
        for card in self.cards:
            self.card_value += card.value

    def hit(self):
        '''
        if the player decides to hit (add a card)
        :return: new card in hand, check for bust/win
        '''
        self.cards.append(new_deck.deal_one())
        self.card_value_update()
        visual_during_game()
        check_bust(player)
        check_twentyone(player)


player = Player(15)


class Dealer:
    '''
    the computer dealer
    '''
    def __init__(self):
        self.cards = []
        self.card_value = 0

    # TODO methods are usually actions
    def card_value_update(self):
        '''
        to use every time a new card is drawn
        :return: an update to card.value
        '''
        self.card_value = 0
        for card in self.cards:
            self.card_value += card.value

    def hit(self):
        '''
        adding a card to the dealer's deck
        :return:a Card
        '''
        check_twentyone(dealer)
        print("the dealer draws a card...")
        self.cards.append(new_deck.deal_one())
        self.card_value_update()
        visual_during_game()
        check_bust(dealer)
        check_twentyone(dealer)


dealer = Dealer()

# TODO methods are usually actions
def player_turn():
    '''
    the player either does not respond properly, "hits" (wants another card) or leaves it.
    :return:
    '''
    check_twentyone(player)
    hit_decision = True
    while hit_decision is True:
        hit_answer = input("Do you want another card? type Y or N").upper()
        if hit_answer not in ("Y", "N"):
            print("Invalid input! Do you want another card, Y or N?")
            continue
        if hit_answer == "Y":
            player.hit()
            continue
        else:
            hit_decision = False

# TODO methods are usually actions
def dealer_turn():
    '''
    the player will keep hitting (drawing cards) until it has won over the user or busted.
    :return:
    '''
    while dealer.card_value < player.card_value:
        dealer.hit()
    lose_game()

# TODO methods are usually actions
def visual_during_game():
    '''
    the player needs a visual of what's going on at the table.
    :return:
    '''
    dealer_visual = dealer.cards[1:]
    print(f"Dealer's hand: covered card, {dealer_visual}")
    print(f"Your hand: {player.cards}")


def deal_starting_cards():
    '''
    dealing the starting cards: two each, updating the value of the hand every time and providing a visual for it.
    :return:
    '''
    print("--> dealing your cards now.")
    player.cards.append(new_deck.deal_one())
    player.cards.append(new_deck.deal_one())
    player.card_value_update()
    print("--> dealing the dealer's cards.")
    dealer.cards.append(new_deck.deal_one())
    dealer.cards.append(new_deck.deal_one())
    dealer.card_value_update()
    visual_during_game()


def print_score():
    '''
    used only in case of game ended.
    :return:
    '''
    print(f"Your score:{player.card_value}")
    print(f"Dealer's score: {dealer.card_value}")


def lose_game():
    '''
    the player loses the game. potential to start new game
    :return:
    '''
    print("sorry, you lost!")
    print_score()
    # TODO ask play again?
    play_again()
    sys.exit()


def win_game():
    '''
    the player wins the game! money is added and potential to start a new game.
    :return:
    '''
    print("you won!!")
    player.add_won_money()
    print_score()
    play_again()
    sys.exit()


def play_again():
    '''
    player prompted to play again if they has enough money to bet.
    if they want to play again, cards and bet amount will be reset.
    :return:
    '''
    if player.money > 0:
        new_play = input("want to play again? press Y if yes").upper()
        if new_play == "Y":
            # TODO game reset contains game reset
            # TODO do player reset
            player.cards = []
            player.bet_amount = ""
            dealer.cards = []
            play()
    print("thanks for playing! until next time!")


def check_bust(turn):
    '''
    Checking if player or dealer (turn input) have busted.
    :param turn: player or dealer
    :return:
    '''
    # TODO wht this function has notion of player variable
    if turn.card_value > 21:
        print("busted!")
        if turn == player:
            lose_game()
        else:
            win_game()

# TODO name coulc be more descriptive
def check_twentyone(turn):
    '''
    checking if player or dealer have won (by 21_
    :param turn: player or dealer
    :return:
    '''
    if turn.card_value == 21:
        print("21!!!")
        if turn == player:
            win_game()
        else:
            lose_game()



print("welcome to the game of BlackJack!")
print("reminder: face cards are worth 10.")
print("aces count as 1 or 11 - you get to pick when they're drawn!")


def play():
    '''
    game logic!
    :return:
    '''
    player.check_bank()
    player.bet()
    deal_starting_cards()
    player_turn()
    dealer_turn()

# TODO flying method invocation group them in a main()
play()


def main():
    # TODO all flying things around and
    play()
