#Category to clarify card handling



class Card:

    def __init__(self, maa, arvo):

        self.__maa = maa
        self.__arvo = arvo

    def __str__(self):

        return self.__arvo + self.__maa

    def maa(self):

        return self.__maa

    def arvo(self):

        return self.__arvo
