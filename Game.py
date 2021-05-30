#This file contains the game itself and appears in it

from tkinter import *

import random

from Deck import Deck

from DealerAI import Dealer


class Blackjack:

# init creates all windows and areas for buttons and images

    def __init__(self, master):

        self.__mainwindow = master

        self.__mainwindow.geometry("1500x900")

        self.__playerframe = Frame(self.__mainwindow, background="#8f0000")
        self.__playerframe.pack(side=BOTTOM, fill=BOTH)

        self.__dealerframe = Frame(self.__mainwindow, background="#8f0000")
        self.__dealerframe.pack(side=TOP, fill=X)

        self.__scoreboard = Frame(self.__mainwindow, background="#8f0000")
        self.__scoreboard.pack(side=LEFT, fill=Y)

        self.__splitcards = Frame(
            self.__mainwindow, background="#8f0000"
                                  )

        self.__buttonframe = Frame(self.__playerframe, background="#8f0000")
        self.__buttonframe.pack(side=LEFT, fill=Y)

        self.__pcardframe = Frame(self.__playerframe, bg="#8f0000")
        self.__pcardframe.pack(side=RIGHT, fill=BOTH)

        self.__pcard1 = Label(
            self.__pcardframe, bg="#8f0000"
                                )
        self.__pcard1.pack(side=RIGHT)

        self.__pcard2 = Label(
            self.__pcardframe, bg="#8f0000"
                                )
        self.__pcard2.pack(side=RIGHT)

        self.__dcardframe = Frame(self.__dealerframe, bg="#8f0000")
        self.__dcardframe.pack(side=RIGHT, fill=BOTH)

        self.__dcard1 = Label(
            self.__dcardframe, bg="#8f0000")
        self.__dcard1.pack(side=RIGHT)

        self.__dcard2 = Label(
            self.__dcardframe, bg="#8f0000")
        self.__dcard2.pack(side=RIGHT)

        self.__pscorevalue = IntVar()

        self.__playerscore = Label(
            self.__scoreboard, text=f"Player score: ", background="white",
            font=("Fredoka One", 20)
                                    )

        self.__dscorevalue = IntVar()

        self.__dealerscore = Label(
            self.__scoreboard, text=f"Dealer score: ", background="white",
            font=("Fredoka One", 20)
                                    )

        self.__bustedimage = PhotoImage(file="images/Busted.png")
        self.__hitimage = PhotoImage(file="images/Hit.png")
        self.__standimage = PhotoImage(file="images/Stand.png")
        self.__dealimage = PhotoImage(file="images/Deal.png")
        self.__exitimage = PhotoImage(file="images/Exit.png")
        self.__newgameimg = PhotoImage(file="images/NewGame.png")
        self.__victoryimage = PhotoImage(file="images/Victory.png")
        self.__defeatimage = PhotoImage(file="images/Defeat.png")
        self.__pushimage = PhotoImage(file="images/Push.png")
        self.__cardbackcolor = None
        self.__dcard2image = None

        self.__hit = Button(
            self.__buttonframe, image=self.__hitimage, bg="#8f0000",
            command=self.hit
                                )

        self.__stand = Button(
            self.__buttonframe, image=self.__standimage, bg="#8f0000",
            command=self.stand
                                )

        self.__deal = Button(
            self.__mainwindow, image=self.__dealimage, bg="LightCyan3",
            text="DEAL", font=("snap itc", 33), compound=BOTTOM,
            command=self.startgame
                                )
        self.__deal.pack(side=TOP)

        self.__quit = Button(
            self.__buttonframe, image=self.__exitimage, command=self.quit
                                )

        self.__playerbusted = Label(
            self.__pcardframe, image=self.__bustedimage, background="#8f0000"
                                        )

        self.__dealerbusted = Label(
            self.__dcardframe, image=self.__bustedimage, background="#8f0000"
                                        )

        self.__newgamebutton = Button(
            self.__mainwindow, image=self.__newgameimg, command=self.newgame
                                        )
        self.__newgamebutton.config(anchor=CENTER)

        self.__resultlabel = Label(self.__mainwindow, font=("snap itc", 30))
        self.__resultlabel.config(anchor=CENTER)

        self.__deck = Deck().return_list()
        self.__cardbacks = ["purple", "green", "red", "yellow", "gray", "blue"]
        self.__cardimages = {}
        self.__playercards = []
        self.__dealercards = []
        self.__dcardlabels = []
        self.__pcardlabels = []

    def startgame(self):
        """
        Starts the game and deals 2 cards to both players.
        :return:
        """
        # download the card images for later use
        self.load_card_images()

        #change the back of the card each time you play 
        self.shuffle_cardback()

        self.__dealerscore.pack(side=TOP)
        self.__playerscore.pack(side=BOTTOM)
        self.__stand.pack(side=TOP, fill=BOTH)
        self.__hit.pack(side=TOP, fill=BOTH)
        self.__quit.pack(side=TOP, fill=BOTH)

        # destroys the big game start button
        self.__deal.destroy()

        # take a random card from the shuffled deck to make sure
        # that the cards do not come in order.
        pcard1 = self.__deck.pop(random.randrange(len(self.__deck)))
        pcard2 = self.__deck.pop(random.randrange(len(self.__deck)))

        # add cards to the list that contains the player's cards
        self.__playercards.append(pcard1)
        self.__playercards.append(pcard2)

        # pictures of the cards are also added to the screen
        self.__pcard1.config(image=self.__cardimages[pcard1])
        self.__pcard2.config(image=self.__cardimages[pcard2])

        dcard1 = self.__deck.pop(random.randrange(len(self.__deck)))
        dcard2 = self.__deck.pop(random.randrange(len(self.__deck)))

        self.__dealercards.append(dcard1)

        # the dealer's score is calculated earlier by adding another card to the deck,
        # so that the value of the second card is not seen until the player has stood still
        # or if either player has blackjack
        self.calculate_dealer_score()
        self.__dealercards.append(dcard2)

        self.__dcard1.config(image=self.__cardimages[dcard1])
        self.__dcard2.config(image=self.__cardbackcolor)

        self.__dcard2image = self.__cardimages[dcard2]

        # upgrade players score
        self.calculate_player_score()
        self.update_scoreboard()
        self.calculate_dealer_score()

        # if either player has a blackjack program check
        # the winner immediately. Otherwise, the game will continue normally
        if self.check_if_dealer_blackjack():
            self.stand()

        if self.check_if_player_blackjack():
            self.stand()

    def check_if_player_blackjack(self):
        """
        Checks if the player has blackjack
        :return: True, if there is blackjack
                 False, if there is no blackjack
        """

        if self.__pscorevalue.get() == 21 and len(self.__playercards) == 2:
            return True

        else:
            return False

    def check_if_dealer_blackjack(self):
        """
        checks if the dealer has blackjack
        :return: True, if there is blackjack
                 False, if there is no blackjack
        """

        if self.__dscorevalue.get() == 21 and len(self.__dealercards) == 2:
            return True

        else:
            return False

    def shuffle_cardback(self):
        """
        Selects a random card from the back list
        :return:
        """

        color = random.randrange(len(self.__cardbacks))
        filename = "cards/{}_back.png".format(self.__cardbacks[color])
        self.__cardbackcolor = PhotoImage(file=filename)

    def calculate_player_score(self):
        """
        Selects a random card from the back list
        :return:
        """

        # because only one ace can get 11 points used ace = True
        # then when 11 points are given for the first ace so
        # acen is set to False and the other following aces become 1
        # point.

        ace = True
        score = 0

        for value in self.__playercards:

            # All picture cards are worth 10 points

            if value[0] == "J" or value[0] == "K" or value[0] == "Q":
                points = 10
                score += points

            # If the card is an ace the first one gets 11 points and the other one 1
            # point.

            elif value[0] == "A":

                if ace:
                    points = 11
                    score += points
                    ace = False

                else:
                    points = 1
                    score += points

            else:

                # Trying to change the second character of a value to an integer
                # in which case it is seen whether it is ten or one digit
                # number. Otherwise, the value of the first character of the card in points.
                # The cards are therefore listed in the format ArvoMaa.

                try:
                    int(value[1])
                    points = 10
                    score += points

                except ValueError:
                    score += int(value[0])

        self.__pscorevalue.set(score)

        # Because there may be a situation where the ace is given a value of 11
        # and the player gets more cards so that he would bust, i.e. score
        # are over 21 so in such a situation the score counter changes
        # the value of this one ace is 1 according to the rules of blackjack.
        # If a player does not have an ace nothing happens. The first ace
        # the value is thus 1 or 11 depending on the situation.

        ace = True

        if self.__pscorevalue.get() > 21:

            for value in self.__playercards:

                if value[0] == "A" and ace:
                    self.__pscorevalue.set(self.__pscorevalue.get() - 10)
                    ace = False

                else:
                    pass

        else:
            pass

    def calculate_dealer_score(self):
        """
        Calculates the dealer's score in the same way as the player's score
        that is, all things in the calculate_player_score method
        :return:
        """

        ace = True
        score = 0

        for value in self.__dealercards:

            if value[0] == "J" or value[0] == "K" or value[0] == "Q":
                points = 10
                score += points

            elif value[0] == "A":
                if ace:
                    points = 11
                    score += points
                    ace = False

                else:
                    points = 1
                    score += points

            else:

                try:
                    int(value[1])
                    points = 10
                    score += points

                except ValueError:
                    score += int(value[0])

        self.__dscorevalue.set(score)
        ace = True

        if self.__dscorevalue.get() > 21:

            for value in self.__dealercards:

                if value[0] == "A" and ace:
                    self.__dscorevalue.set(self.__dscorevalue.get()-10)
                    ace = False

                else:
                    pass

        else:
            pass

    def check_player_bust(self):
        """
        Checks if the player's score is over 21
        :return: True, if the score is more than 21
                 False, if the score is >= 21
        """

        if self.__pscorevalue.get() > 21:
            self.__playerbusted.pack(side=RIGHT)
            return True

        else:
            return False

    def check_dealer_bust(self):
        """
        chexk if the dealer's score is over 21
        :return: True, if the score is more than 21
                 False, if the score is <= 21
        """

        if self.__dscorevalue.get() > 21:
            self.__dealerbusted.pack(side=RIGHT)
            return True

        else:
            return False

    def update_scoreboard(self):
        """
        Updates the scoreboard
        :return:
        """
        self.__dealerscore.configure(
            text=f"Dealer score: {self.__dscorevalue.get()}"
        )

        self.__playerscore.configure(
            text=f"Player score: {self.__pscorevalue.get()}"
        )

    def update_player_score_if_hit(self):
        """
        Updates only the player's score to the leaderboard
        :return:
        """

        self.__playerscore.configure(
            text=f"Player score: {self.__pscorevalue.get()}"
        )

    def update_dealer_score_if_hit(self):
        """
        Updates only dealer points to the leaderboard
        :return:
        """

        self.__dealerscore.configure(
            text=f"Dealer score: {self.__dscorevalue.get()}"
        )

    def stand(self):
        """
        When the player presses the stand button, the hit and stand buttons are removed
        and start the dealer's turn and after the dealer's turn
        let's see which one won.
        :return:
        """

        #Disable hit and stand buttons 

        self.__hit["state"] = DISABLED
        self.__stand["state"] = DISABLED

        # puts the dealer's second card face up

        self.__dcard2.config(image=self.__dcard2image)
        self.update_scoreboard()

        # if a player has blackjack go straight to checking the winner
        # otherwise it is the turn of the dealer

        if not self.check_if_player_blackjack():

            # the loop condition is the Dealer class based on which
            # the dealer takes a new card or keeps his current hand

            while Dealer(self.__dscorevalue.get()).hit():

                new_card = self.__deck.pop(random.randrange(len(self.__deck)))
                self.__dealercards.append(new_card)

                # creating a new label with a picture of what the dealer receives
                # the card and label are added to the list for later use

                label = Label(
                    self.__dcardframe, image=self.__cardimages[new_card],
                    bg="#8f0000"
                )
                label.pack(side=RIGHT)

                self.__dcardlabels.append(label)
                self.calculate_dealer_score()
                self.update_dealer_score_if_hit()
                self.check_dealer_bust()

        self.checkwinner()

    def hit(self):
        """
        When the player presses the button, a new card is added to the screen and checked
        the player's score and, if applicable, the winner.
        :return:
        """

        # the same process as in the stand method
        new_card = self.__deck.pop(random.randrange(len(self.__deck)))

        self.__playercards.append(new_card)

        label = Label(self.__pcardframe, image=self.__cardimages[new_card],
                      bg="#8f0000")
        label.pack(side=RIGHT)

        self.__pcardlabels.append(label)

        self.calculate_player_score()

        self.update_player_score_if_hit()

        if self.check_player_bust():
            self.checkwinner()

    def load_card_images(self):
        """
        the same process as in the stand method
        so that they can be used.
        :return:
        """

        for card in self.__deck:
            filename = "cards/{}.png".format(card)
            image = PhotoImage(file=filename)
            self.__cardimages[str(card)] = image

    def checkwinner(self):
        """
        Check which one wins the game and add a win / loss image to the screen and
        a button that starts a new game
        :return:
        """
        # each condition results in a win or loss appearing on the screen
        # the image, hit and stand buttons will be disabled and will be displayed
        # new game button, where you can start a new game by name

        if self.check_player_bust() and self.check_dealer_bust():
            self.__resultlabel.config(
                text="DEALER WINS!", image=self.__defeatimage, compound=BOTTOM
            )
            self.__resultlabel.pack(side=LEFT)
            self.__newgamebutton.pack(side=RIGHT)
            self.__stand["state"] = DISABLED
            self.__hit["state"] = DISABLED

        if self.check_player_bust() and not self.check_dealer_bust():
            self.__resultlabel.config(
                text="DEALER WINS!", image=self.__defeatimage, compound=BOTTOM
            )
            self.__resultlabel.pack(side=LEFT)
            self.__newgamebutton.pack(side=RIGHT)
            self.__stand["state"] = DISABLED
            self.__hit["state"] = DISABLED

        if not self.check_player_bust() and self.check_dealer_bust():
            self.__resultlabel.config(image=self.__victoryimage)
            self.__resultlabel.pack(side=LEFT)
            self.__newgamebutton.pack(side=RIGHT)
            self.__stand["state"] = DISABLED
            self.__hit["state"] = DISABLED

        if self.check_if_dealer_blackjack() and not\
           self.check_if_player_blackjack():

            self.__resultlabel.config(
                text="DEALER WINS!", image=self.__defeatimage, compound=BOTTOM
            )
            self.__resultlabel.pack(side=LEFT)
            self.__newgamebutton.pack(side=RIGHT)
            self.__stand["state"] = DISABLED
            self.__hit["state"] = DISABLED

        if self.check_if_dealer_blackjack() and\
           self.check_if_player_blackjack():

            self.__resultlabel.config(
                text="PUSH", image=self.__pushimage, compound=BOTTOM
                                        )
            self.__resultlabel.pack(side=LEFT)
            self.__newgamebutton.pack(side=RIGHT)
            self.__stand["state"] = DISABLED
            self.__hit["state"] = DISABLED

        if not self.check_dealer_bust() and not self.check_player_bust():

            if self.__stand["state"] == DISABLED:

                if self.__pscorevalue.get() < self.__dscorevalue.get():
                    self.__resultlabel.config(
                        text="DEALER WINS", image=self.__defeatimage,
                        compound=BOTTOM
                                                )
                    self.__resultlabel.pack(side=LEFT)
                    self.__hit["state"] = DISABLED
                    self.__newgamebutton.pack(side=RIGHT)

                elif self.__pscorevalue.get() > self.__dscorevalue.get():
                    self.__resultlabel.config(image=self.__victoryimage)
                    self.__resultlabel.pack(side=LEFT)
                    self.__newgamebutton.pack(side=RIGHT)
                    self.__hit["state"] = DISABLED

                else:
                    self.__resultlabel.config(
                        text="PUSH", image=self.__pushimage, compound=BOTTOM
                                                )
                    self.__resultlabel.pack(side=LEFT)
                    self.__newgamebutton.pack(side=RIGHT)
                    self.__hit["state"] = DISABLED

        else:
            pass

    def reset_values(self):
        """
        The method, as its name implies, resets all changed values ​​to their initial state and
        remove a few images from view.
        :return:
        """

        self.__dscorevalue.set(0)
        self.__pscorevalue.set(0)

        self.__deck += self.__playercards + self.__dealercards

        self.__hit["state"] = NORMAL
        self.__stand["state"] = NORMAL

        self.update_scoreboard()

        self.__playerbusted.forget()
        self.__dealerbusted.forget()
        self.__resultlabel.forget()
        self.__newgamebutton.forget()

        self.__playercards = []
        self.__dealercards = []
        self.__pcardlabels = []
        self.__dcardlabels = []

    def newgame(self):
        """
        Destroys the labels of all cards, resets the changed values ​​and starts
        new game
        :return:
        """

        for label in self.__pcardlabels:
            label.destroy()

        for label in self.__dcardlabels:
            label.destroy()

        self.reset_values()
        self.startgame()

    def quit(self):
        """
        Closes the window and exits the program
        :return:
        """

        self.__mainwindow.destroy()

    def start(self):
        """
        Open the game window
        :return:
        """

        self.__mainwindow.mainloop()
