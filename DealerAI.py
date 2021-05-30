"""
The AI ​​of a blackjack game dealer,
based on which the dealer chooses to hit or stand

"""


class Dealer:

    def __init__(self, score):

        self.__score = score

    def hit(self):

        if self.__score <= 16:
            return True

        else:
            return False
