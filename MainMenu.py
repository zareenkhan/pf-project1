"""

Game rules:
-The goal of blackjack is to beat the dealer's hand without going over 21.
-Face cards are worth 10. Aces are worth 1 or 11, whichever makes a better
 hand.
-Each player starts with two cards, one of the dealer's cards is hidden
 until the end.
-To 'Hit' is to ask for another card. To 'Stand' is to hold your total and
end your turn.
-If you go over 21 you bust, and the dealer wins regardless of the dealer's
 hand.
-If you are dealt 21 from the start (Ace & 10), you got a blackjack.
-Dealer will hit until his/her cards total 17 or higher.

Instructions:

When the program starts running, it opens a main menu window with
2 buttons. One can close the window and exit the program and the other button
let's start the game itself. The Play button opens a new window where the game works.
the game is started by pressing the large image / button in the window, which
above reads DEAL. The player and dealer are then dealt
the first cards. The player has both cards visible and the dealer
again, the first card appears normally and the second shows only the back.
The program also has a function where the back of the card changes each time you play.
Even when the program is running. When the player and the dealer have
The cards dealt to the player have two options Hit or Stand. When you press Hit-
option the player gets a new card. The hit button can be pressed as long as
player score <= 21 but it doesn't always make sense to ask for a new one
cards but keep the current hand. This function can be performed by pressing
Stand button. Once the player has pressed the stand button, the dealer begins
turn. As the rules read the dealer must hit whenever his
the value of his hand is <= 16 and must be fixed when it is> 16. If neither is
"busted" i.e. the value of the hand has exceeded 21 so we see the dealer's turn
after which one has won. The winner can also be seen in special situations
in the past, for example, if either has "blackjack" or cards
the value is 21 when 2 cards are dealt to both. When the program is
announced the winner can the player press the "new game" button that appears
on the screen to start a new game.

"""


from tkinter import *

from Game import Blackjack


class Mainmenu:

    # the main menu window is created in init
    def __init__(self):

        self.__mainmenu = Tk()

        imagename1 = "images/Menu.png"

        self.__canvas = Canvas(self.__mainmenu, width=1230, height=762)
        self.__canvas.pack()

        img1 = PhotoImage(file=imagename1)
        self.__canvas.background = img1
        self.__canvas.create_image(0, 0, anchor=NW, image=img1)

        self.__img2 = PhotoImage(file="images/Play.png")
        self.__img3 = PhotoImage(file="images/Quit.png")

        self.__playbutton = Button(
            self.__canvas, justify=LEFT, command=self.play
                                   )
        self.__playbutton.config(image=self.__img2)
        self.__playbutton.place(x=420, y=480)

        self.__quitbutton = Button(
            self.__canvas, command=self.quit, justify=LEFT
                                   )
        self.__quitbutton.config(image=self.__img3)
        self.__quitbutton.place(x=420, y=620)

    def play(self):
        """
        Destroys the main menu window and opens the game window
        :return:
        """

        self.__mainmenu.destroy()
        Blackjack(Tk()).start()

    def quit(self):
        """
        Destroys the main menu window
        :return:
        """

        self.__mainmenu.destroy()

    def start(self):
        """
        Open the main menu window
        :return:
        """

        self.__mainmenu.mainloop()


def main():

    Mainmenu().start()


if __name__ == "__main__":
    main()
