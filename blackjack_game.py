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

class InputLayer:

    def check_bet_input(self):
        allowed_bet_range = False
        while allowed_bet_range == False:
            game_master.player.bet_amount = input("How much do you want to bet?")
            if game_master.player.bet_amount.isdigit() is False:
                print("hey, please input only integers from 1 to however much you can afford!")
                continue
            if game_master.player.bet_amount == "0":
                print("you have to bet something!")
                continue
            if int(game_master.player.bet_amount) > game_master.player.money:
                print("you don't have THAT kind of money.")
                continue
            else:
                allowed_bet_range = True
        return game_master.player.bet_amount

    def check_ace_value_input(self, new_card):
        accepted_values = [1, 11]
        if new_card.rank == "Ace":
            print("an ace has been drawn.")
            new_card.value = input("Does this ace count as 1 or 11?")
            while str(new_card.value).isdigit() is False or int(new_card.value) not in accepted_values:
                print("please, only write 1 or 11.")
                new_card.value = input("Does this ace count as 1 or 11?")
        return new_card.value


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


    def deal_one(self):
        '''
        Adds one cards to the hand. if it's an ace, you have to choose the value.
        :return: a Card
        '''
        new_card = self.all_cards.pop()

        new_card.value = int(game_master.input_layer.check_ace_value_input(new_card))
        return new_card


class Player:
    '''
    the human player of this came
    '''

    def __init__(self, money):
        self.money = money
        self.cards = []
        self.bet_amount = 0
        self.card_value = 0

    def bet(self):
        '''
        betting the money.
        :return: an input and an update of self.bet_amount
        '''

        game_master.input_layer.check_bet_input()
        print(f"alright, you will bet {self.bet_amount}")

        self.bet_amount = int(self.bet_amount)
        self.money -= self.bet_amount

    def update_card_value(self):
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
        self.cards.append(game_master.new_deck.deal_one())
        self.update_card_value()


class Dealer:
    '''
    the computer dealer
    '''

    def __init__(self):
        self.cards = []
        self.card_value = 0

    def update_card_value(self):
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
        game_master.check_end_game_conditions()
        print("the dealer draws a card...")
        self.cards.append(game_master.new_deck.deal_one())
        self.update_card_value()



class GameMaster:
    dealer = Dealer()
    player = Player(15)
    input_layer = InputLayer()

    new_deck = Deck()
    new_deck.shuffle()

    def announce_money(self):
        '''
        a string telling you how much money you got
        :return: a printed str
        '''
        return print(f'You still have {self.player.money} to bet.')

    def give_prize(self):
        '''
        if you win, it will add double the money you bet
        :return: update to money
        '''
        self.player.money += self.player.bet_amount * 2


    def deal_starting_cards(self):
        '''
        dealing the starting cards: two each, updating the value of the hand every time and providing a visual for it.
        :return:
        '''
        print("--> dealing your cards now.")
        self.player.cards.append(self.new_deck.deal_one())
        self.player.cards.append(self.new_deck.deal_one())
        self.player.update_card_value()
        print("--> dealing the dealer's cards.")
        self.dealer.cards.append(self.new_deck.deal_one())
        self.dealer.cards.append(self.new_deck.deal_one())
        self.dealer.update_card_value()
        self.show_hands()

    def print_score(self):
        '''
        used only in case of game ended.
        :return:
        '''
        print(f"Your score:{self.player.card_value}")
        print(f"Dealer's score: {self.dealer.card_value}")

    def lose_game(self):
        print("sorry, you lost!")
        self.print_score()
        self.ask_new_game()
        sys.exit()

    def win_game(self):
        print("you won!!")
        self.give_prize()
        self.print_score()
        self.ask_new_game()
        sys.exit()

    def check_twentyone_points(self):
        if self.player.card_value == 21:
            print("you got 21!")
            self.win_game()
        elif self.dealer.card_value == 21:
            print("the dealer got 21...")
            self.lose_game()

    def check_bust(self):
        if self.player.card_value > 21:
            print("ah, you busted!")
            self.lose_game()
        elif self.dealer.card_value > 21:
            print("the dealer busted!")
            self.win_game()

    def check_end_game_conditions(self):
        self.check_twentyone_points()
        self.check_bust()

    def show_hands(self):
        '''
        the player needs a visual of what's going on at the table.
        :return:
        '''
        dealer_visual = self.dealer.cards[1:]
        print(f"Dealer's hand: covered card, {dealer_visual}")
        print(f"Your hand: {self.player.cards}")

    def game_reset(self):
        self.player.cards = []
        self.player.bet_amount = ""
        self.dealer.cards = []

    def ask_new_game(self):
        '''
        player prompted to play again if they has enough money to bet.
        if they want to play again, cards and bet amount will be reset.
        :return:
        '''
        if self.player.money > 0:
            new_play = input("want to play again? press Y if yes").upper()
            if new_play == "Y":
                self.game_reset()
                self.play()
        print("thanks for playing! until next time!")

    def player_plays(self):
        self.check_end_game_conditions()
        hit_decision = True
        while hit_decision is True:
            hit_answer = input("Do you want another card? type Y or N").upper()
            if hit_answer not in ("Y", "N"):
                print("Invalid input! Do you want another card, Y or N?")
                continue
            if hit_answer == "Y":
                self.player.hit()
                self.show_hands()
                self.check_end_game_conditions()
                continue
            else:
                hit_decision = False

    def dealer_plays(self):
        '''
        the player will keep hitting (drawing cards) until it has won over the user or busted.
        :return:
        '''
        while self.dealer.card_value < self.player.card_value:
            self.dealer.hit()
            self.show_hands()
            self.check_end_game_conditions()
        self.lose_game()



    def play(self):
        '''
        game logic!
        :return:
        '''
        self.announce_money()
        self.player.bet()
        self.deal_starting_cards()
        self.player_plays()
        self.dealer_plays()


game_master = GameMaster()

def main():
    print("welcome to the game of BlackJack!")
    print("reminder: face cards are worth 10.")
    print("aces count as 1 or 11 - you get to pick when they're drawn!")
    game_master.play()


main()
