'''
random --> provides a function to exit the program
sys --> provides a function to exit the program
'''
import random
import string
import sys

values = {'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8,
          'nine': 9, 'ten': 10, 'jack': 10, 'queen': 10, 'king': 10, 'ace': "TBD"}

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')


class InputLayer:

    def ask_bet_amount(self) -> int:
        allowed_bet_range = False
        while allowed_bet_range == False:
            bet_amount = input("How much do you want to bet?")
            if bet_amount.isdigit() is False:
                print("hey, please input only integers from 1 to however much you can afford!")
                continue
            if bet_amount == "0":
                print("you have to bet something!")
                continue
            if int(bet_amount) > game_master.player.money:
                print("you don't have THAT kind of money.")
                continue
            else:
                allowed_bet_range = True
        return bet_amount

    def ask_ace_value_input(self, new_card) -> int:
        accepted_values = [1, 11]
        if new_card.rank == "Ace":
            print("an ace has been drawn.")
            new_card.value = input("Does this ace count as 1 or 11?")
            while str(new_card.value).isdigit() is False or int(new_card.value) not in accepted_values:
                print("please, only write 1 or 11.")
                new_card.value = input("Does this ace count as 1 or 11?")
        return new_card.value

    def does_user_want_to_draw(self) -> bool:
        while True:
            hit_answer = input("Do you want another card? type Y or N").upper()
            if hit_answer not in ("Y", "N"):
                print("Invalid input! Do you want another card, Y or N?")
                continue
            return hit_answer == "Y"

    def does_user_want_to_play_again(self) -> bool:
        new_play = input("Do want to play again? press Y if yes").upper()
        return new_play == "Y"


class Card:
    """
    All cards have a suit, a rank and a value.
    """

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
        """
        To be used before game starts
        :return: a shuffled deck
        """
        random.shuffle(self.all_cards)

    def deal_one(self) -> Card:
        """
        Adds one cards to the hand. if it's an ace, you have to choose the value.
        :return: a Card
        """
        new_card = self.all_cards.pop()

        new_card.value = int(game_master.input.ask_ace_value_input(new_card))
        return new_card


class Player:
    def __init__(self):
        self.cards = []
        self.card_value = 0

    def take_card(self, card):
        self.cards.append(card)
        self.update_card_value()

    def update_card_value(self):
        '''
        to use every time a new card is drawn
        :return: an update to card.value
        '''
        self.card_value = 0
        for card in self.cards:
            self.card_value += card.value

    def is_winning(self) -> bool:
        return self.card_value == 21

    def reset(self):
        self.cards = []

class User(Player):
    """
    the human player of this came
    """

    def __init__(self, money):
        Player.__init__(self)
        self.money = money
        self.bet_amount = 0

    def set_bet_amount(self, bet_amount):
        """
        betting the money.
        :return: an input and an update of self.bet_amount
        """
        self.bet_amount = int(bet_amount)
        self.money -= self.bet_amount

    def reset(self):
        self.cards = []
        self.bet_amount = ""


class Dealer(Player):
    """
    the computer dealer
    """

    def __init__(self):
        Player.__init__(self)

    def hit(self):
        """
        adding a card to the dealer's deck
        :return:a Card
        """
        print("the dealer draws a card...")
        self.cards.append(game_master.deck.deal_one())
        self.update_card_value()


class GameStatus:
    ending_reason: string

    def __init__(self):
        self.is_user_the_winner = False
        self.is_game_finished = False

    def set_to_lost(self, reason):
        self.ending_reason = reason
        self.is_user_the_winner = False
        self.is_game_finished = True

    def set_to_win(self, reason):
        self.ending_reason = reason
        self.is_user_the_winner = True
        self.is_game_finished = True

    def reset(self):
        self.is_game_finished = False
        self.is_user_the_winner = False
        self.ending_reason = ""


class GameMaster:
    dealer = Dealer()
    player = User(15)
    input = InputLayer()

    deck = Deck()
    deck.shuffle()

    def __init__(self):
        self.game_status = GameStatus()

    def give_prize(self):
        """
        if you win, it will add double the money you bet
        :return: update to money
        """
        self.player.money += self.player.bet_amount * 2

    def deal_starting_cards(self):
        """
        dealing the starting cards: two each, updating the value of the hand every time and providing a visual for it.
        :return:
        """
        print("--> dealing your cards now.")
        self.player.take_card(self.deck.deal_one())
        self.player.take_card(self.deck.deal_one())

        print("--> dealing the dealer's cards.")
        self.dealer.take_card(self.deck.deal_one())
        self.dealer.take_card(self.deck.deal_one())

    def print_score(self):
        """
        used only in case of game ended.
        :return:
        """
        print(f"Your score:{self.player.card_value}")
        print(f"Dealer's score: {self.dealer.card_value}")

    def announce_won_game(self):
        print("you won!!")

    def check_dealer_end_game_conditions(self):
        if self.dealer.card_value > 21:
            self.game_status.set_to_win("the dealer busted!")
            return

        if self.dealer.is_winning():
            self.game_status.set_to_lost("the dealer got 21...")
            return

    def check_player_end_game_conditions(self):
        if self.player.is_winning():
            self.game_status.set_to_win("you got 21!")
            return

        if self.player.card_value > 21:
            self.game_status.set_to_lost("ah, you busted!")
            return

    def show_hands(self):
        """
        the player needs a visual of what's going on at the table.
        :return:
        """
        dealer_visual = self.dealer.cards[1:]
        print(f"Dealer's hand: covered card, {dealer_visual}")
        print(f"Your hand: {self.player.cards}")

    def reset_game(self):
        self.player.reset()
        self.dealer.reset()
        self.game_status.reset()

    def stop(self):
        print("thanks for playing! until next time!")
        self.print_score()
        sys.exit()

    def dealer_plays(self):
        """
        the player will keep hitting (drawing cards) until it has won over the user or busted.
        :return:
        """
        while self.is_game_finished() is False and self.dealer.card_value < self.player.card_value:
            self.dealer.hit()
            self.show_hands()
            self.check_dealer_end_game_conditions()

    def play_one_game(self):
        """
        game logic!
        :return:
        """
        self.announce_money()
        self.player.set_bet_amount(self.input.ask_bet_amount())
        self.deal_starting_cards()
        self.show_hands()
        self.check_end_game_conditions()

        self.user_plays()

        if self.is_game_finished():
            if self.game_status.is_user_the_winner:
                self.give_prize()
            self.announce_match_result()
            return

        self.dealer_plays()

        if self.game_status.is_user_the_winner:
            self.give_prize()
        self.announce_match_result()

    def user_plays(self):
        player_wants_to_draw = self.input.does_user_want_to_draw()
        while player_wants_to_draw and self.is_game_finished() is False:

            self.give_card_to_player()
            self.show_hands()
            self.check_player_end_game_conditions()

            if self.is_game_finished() is False:
                player_wants_to_draw = self.input.does_user_want_to_draw()

    def is_game_finished(self) -> bool:
        return self.game_status.is_game_finished

    def give_card_to_player(self):
        self.player.take_card(self.deck.deal_one())

    def announce_match_result(self):
        print(self.game_status.ending_reason)
        if self.game_status.is_user_the_winner:
            self.announce_won_game()
        else:
            self.announce_lost_game()
        self.print_score()
        self.announce_money()

    def check_end_game_conditions(self):
        self.check_player_end_game_conditions()
        if self.is_game_finished:
            return

        self.check_dealer_end_game_conditions()
        if self.is_game_finished:
            return

    def announce_money(self):
        '''
        a string telling you how much money you got
        :return: a printed str
        '''
        return print(f'You still have {self.player.money} to bet.')

    def announce_lost_game(self):
        print("sorry, you lost!")

    def play(self):
        while True:
            self.reset_game()
            self.play_one_game()

            if self.player.money <= 0 or self.input.does_user_want_to_play_again() is False:
                break

        self.stop()



game_master = GameMaster()


def main():
    print("welcome to the game of BlackJack!")
    print("reminder: face cards are worth 10.")
    print("aces count as 1 or 11 - you get to pick when they're drawn!")
    game_master.play()


main()
