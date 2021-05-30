
#The program creates and shuffles a deck of cards for a game of blackjack


import random

from Card import Card

korttiarvot = [
 "A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"
]

maat = [
 "S", "H", "D", "C"
]


class Deck:

    def __init__(self):

# create a deck of cards using the Card class
        self.__kortit = [
            str(Card(maa, arvo)) for arvo in korttiarvot for maa in maat
                         ]
        random.shuffle(self.__kortit)

    def return_list(self):

        return self.__kortit
