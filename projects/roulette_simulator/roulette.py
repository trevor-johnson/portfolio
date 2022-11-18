# import libraries
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from collections import Counter
import re
import string 


class col:
    """used for colored text printouts in the command line"""
    E = '\033[0m'
    R = '\033[0;37;41m'
    B = '\033[0;37;40m'
    G = '\033[0;37;42m'
    blue = '\033[94m'


class PlayerInfo:
    """An object of class PlayerInfo will contain many attributes about the player

    Attributes:
        player_name
        player_dob - year, month, day can be in any order but separated by '-'
        chips - current chip count
        chip_history - list of historical chip counts

    Methods:
        update_chips(n) - setter method to change the chip count. Also appends to chip_history
        log_spins(result) - keep track of historical roulette spins the player made
        log_setups(setup, subsetup) - keep track of historical gamble selections
        __str__ and __repr__ mehods return all player info
    """

    def __init__(self, player_name="", player_dob="", chips=1000):
        self.player_name = player_name
        self.player_dob = player_dob
        if chips == "":
            self.chips = 1000
        else:
            self.chips = int(chips)
        # player history
        self.chip_history = [self.chips]
        self.spin_history = []
        self.setup_history = []
        self.subsetup_history = []

    def update_chips(self, n):
        self.chips += n
        self.chip_history.append(self.chips)

    def log_spins(self, result):
        self.spin_history.append(result)

    def log_setups(self, setup, subsetup):
        self.setup_history.append(setup)
        self.subsetup_history.append(subsetup)

    def __str__(self):
        return "Name: " + self.player_name + "\n" + "DOB: " + self.player_dob + "\n" + "Chips: " + str(self.chips)

    def __repr__(self):
        return self.__str__()


class RouletteWheel:
    """Takes an object of class PlayerInfo as input, and builds a roulette wheel.
    Certain numbers are more likely to appear based on the player name
    and DOB.

    Attributes:
        roulette_df - dataframe of bets and odds to be used in later functions

    Methods:
        table_printout() - returns a picture of a roulette table
        return_df() - returns the roulette_df attribute
    """

    def __init__(self, playerinfo):
        if isinstance(playerinfo, type(PlayerInfo())):
            self.playerinfo = playerinfo

            # build roulette wheel df
            self.original_nums = list(map(lambda x: str(x), range(1, 37))) + ["0", "00"]
            # name scores, and dob scores
            self.player_info_nums = [str(ord(i) - 96) for i in self.playerinfo.player_name.lower()] + list(re.sub("-|/","", self.playerinfo.player_dob))
            self.all_nums = self.original_nums + self.player_info_nums
            self.probs = np.array(list(Counter(self.all_nums).values())) / len(self.all_nums)

            self.roulette_df = pd.DataFrame({
                "numbers": self.original_nums,
                "Colors": ["Red", "Black"] * 5 + ["Black", "Red"] * 4 + ["Black"] +
                          ["Black", "Red"] * 4 + ["Red", "Black"] * 4 + ["Red"] + ["Green"] * 2,
                "Evens_Odds": ["Even" if i % 2 == 0 else "Odd" for i in range(1, 37)] + [None, None],
                "probs": self.probs,
                # For certain types of simple bets, we can set up when this row wins
                "Street": ['1-3'] * 3 + ['4-6'] * 3 + ['7-9'] * 3 + ['10-12'] * 3 + ['13-15'] * 3 + ['16-18'] * 3 +
                          ['19-21'] * 3 + ['22-24'] * 3 + ['25-27'] * 3 + ['28-30'] * 3 + ['31-33'] * 3 + [
                              "34-36"] * 3 + [None, None],
                "Column": ["Column 1", "Column 2", "Column 3"] * 12 + [None, None],
                "Dozen": ["1-12"] * 12 + ["13-24"] * 12 + ["25-36"] * 12 + [None, None],
                "Lows_Highs": ["1-18"] * 18 + ["19-36"] * 18 + [None, None]
            })
        else:
            raise Exception("Input must be of type PlayerInfo")

    def table_printout(self):
        print(f"""
           / ̅ ̅ ̅|-------------------------------------------------------------------|
          /    |{col.R} 3 {col.E}|{col.B} 6 {col.E}|{col.R} 9 {col.E}|{col.R} 12 {col.E}|{col.B} 15 {col.E}|{col.R} 18 {col.E}|{col.R} 21 {col.E}|{col.B} 24 {col.E}|{col.R} 27 {col.E}|{col.R} 30 {col.E}|{col.B} 33 {col.E}|{col.R} 36 {col.E}| Column 3 |
         / {col.G} 0 {col.E} |----------------|-------------------|-------------------|----------|
        |------|{col.B} 2 {col.E}|{col.R} 5 {col.E}|{col.B} 8 {col.E}|{col.B} 11 {col.E}|{col.R} 14 {col.E}|{col.B} 17 {col.E}|{col.B} 20 {col.E}|{col.R} 23 {col.E}|{col.B} 26 {col.E}|{col.B} 29 {col.E}|{col.R} 32 {col.E}|{col.B} 35 {col.E}| Column 2 |
         \ {col.G} 00 {col.E}|----------------|-------------------|-------------------|----------|
          \    |{col.R} 1 {col.E}|{col.B} 4 {col.E}|{col.R} 7 {col.E}|{col.B} 10 {col.E}|{col.B} 13 {col.E}|{col.R} 16 {col.E}|{col.R} 19 {col.E}|{col.B} 22 {col.E}|{col.R} 25 {col.E}|{col.B} 28 {col.E}|{col.B} 31 {col.E}|{col.R} 34 {col.E}| Column 1 |
           \___|----------------|-------------------|-------------------|----------|
               |    1st Dozen   |     2nd Dozen     |     3rd Dozen     |          
               |--------------------------------------------------------|
               |  1-18  |  Even |{col.R}   Red   {col.E}|{col.B}  Black  {col.E}|  Odd  |   19-36   | 
               |________|_______|_________|_________|_______|___________|
        """)

    def return_df(self):
        return self.roulette_df


class GambleSetup:
    """Contains all the info about how the user wants to gamble.

    Attributes:
        gamble_dict - dictionary on setup options
        gamble_df - dataframe of subsetup options (i.e. the specific bet options: red, odds, 1 7 or 23 etc.)
        setup - the users chosen strategy setup (i.e. Columns, Colors, etc.)
        subsetup - the user's selected options (i.e. which numbers to gamble on)
        wager = amount user wants to gamble per selected option. 

    Methods:
        gamble_setup() - prompts input statements for user to specify overall gamble type
        return_setup() - getter method to printout the setup the user selected
        return_subsetup() - getter method to printout the subsetup (specific numbers) user selected
        return_payout() - getter method to prinout the potential payout for their strategy setup
    """

    # each object of class GambleSetup will have wheel options
    # and a gamble_df with gambling options
    def __init__(self):
        self.gamble_dict = {
            1: "Straight-up (any number 1-36, '0', or '00') [PAYOUT = 35:1]",
            2: "Split (any 2 numbers side by side) [PAYOUT = 17:1]",
            3: "Street (any 3 numbers in a row) [PAYOUT = 11:1]",
            4: "Six Line (a group of 6 numbers in 2 rows side by side) [PAYOUT = 5:1]",
            5: "Columns (Horizontal long column) [PAYOUT = 2:1]",
            6: "Dozens (1-12, 13-24, 25-36) [PAYOUT = 2:1]",
            7: "Lows/Highs (half table) (1-18, 19-36) [PAYOUT = 1:1]",
            8: "Colors (red, black) [PAYOUT = 1:1]",
            9: "Evens/Odds [PAYOUT = 1:1]"
        }

        self.gamble_df = pd.DataFrame({
            "row": list(range(1, 10)),
            "setup": ["Straight-up", "Split", "Street", "Six_Line", "Column", "Dozen", "Lows_Highs",
                      "Colors", "Evens_Odds"],
            "options": [["1-36", "0", "00"], ["2 numbers side by side"],
                        ["1-3", "4-6", "7-9", "10-12", "13-15", "16-18", "19-21", "22-24", "25-27", "28-30",
                         "31-33", "34-36"],
                        ["6 numbers in 2 rows"],
                        ["Column 1", "Column 2", "Column 3"],
                        ["1-12", "13-24", "25-36"],
                        ["1-18", "19-36"],
                        ["Red", "Black"],
                        ["Even", "Odd"]],
            "payout": [35, 17, 11, 5, 2, 2, 1, 1, 1]
        })

        # default values:
        self.setup = 0
        self.subsetup = 0
        self.wager = ""

    # Setter method to set the gambling type.
    # Later the object will have the necessary parameters to 
    # sample from the roulette wheel
    # based on inputs into this object.
    def gamble_setup(self):

        s = "Pick a gambling strategy. Type just one of the numbers below to select: \n\n"
        for i in range(1, len(self.gamble_dict) + 1):
            s += str(i) + ": " + self.gamble_dict[i] + "\n"

        while self.setup == "" or self.setup not in [str(i) for i in range(1,10)]:
            self.setup = input(s+"\n")
        
        self.setup = int(self.setup)

        # error checking
        if self.setup not in [i for i in range(11)]:
            raise Exception("Invalid input, start over")

        # define payout
        self.payout = self.gamble_df["payout"][
            self.gamble_df["row"] == self.setup
            ].item()

        self.wager = ""
        if self.setup == 1:
            while self.wager in string.ascii_letters:
                self.wager = input("Enter wager amount per number:\n")
            self.wager = int(self.wager)

            subsetup1 = input("Straight-up. Enter a list of numbers, '0', or '00' separated by commas or spaces.\
                \nAny invalid inputs will be as if you just tossed your chips in the trash.\n")
            self.subsetup = re.split(" |,", subsetup1.strip())

        elif self.setup == 2:
            while self.wager in string.ascii_letters:
                self.wager = input("Enter wager amount per number pair:\n")
            self.wager = int(self.wager)

            subsetup1 = input("Split. Enter any two numbers that are side by side on the board, separated by commas or spaces.\nAny invalid inputs will be as if you just tossed your chips in the trash.\n")
            self.subsetup = re.split(" |,", subsetup1.strip())

        elif self.setup == 3:
            while self.wager in string.ascii_letters:
                self.wager = input("Enter wager amount:\n")
            self.wager = int(self.wager)

            self.subsetup = input("Street. Select an option:\n1: 1-3 \n2: 4-6 \n3: 7-9 \n4: 10-12 \n5: 13-15\
            \n6: 16-187: 19-21 \n8: 22-24 \n9: 25-27 \n10: 28-30 \n11: 31-33 \n12: 34-36\n")
            # if the user does not select a correct number, it asks them again
            while self.subsetup not in [str(i) for i in range(1, 13)]:
                self.subsetup = input("Street. Select an option:\n1: 1-3 \n2: 4-6 \n3: 7-9 \n4: 10-12 \n5: 13-15\
            \n6: 16-187: 19-21 \n8: 22-24 \n9: 25-27 \n10: 28-30 \n11: 31-33 \n12: 34-36\n")

        elif self.setup == 4:
            while self.wager in string.ascii_letters:
                self.wager = input("Enter wager amount:\n")
            self.wager = int(self.wager)

            self.subsetup = input("Six Line. Select an option:\n1: 1-6\n2: 4-9\n3: 7-12\n4: 10-15\n5: 13-18\
            \n6: 16-21 \n7: 19-24\n8: 22-27\n9: 25-30 \n10: 28-33 \n11: 31-36\n")
            while self.subsetup not in [str(i) for i in range(1, 12)]:
                self.subsetup = input("Six Line. Select an option:\n1: 1-6\n2: 4-9\n3: 7-12\n4: 10-15\n5: 13-18\
            \n6: 16-21 \n7: 19-24\n8: 22-27\n9: 25-30 \n10: 28-33 \n11: 31-36\n")

        elif self.setup == 5:
            while self.wager in string.ascii_letters:
                self.wager = input("Enter wager amount:\n")
            self.wager = int(self.wager)

            self.subsetup = input("Column. Select an option:\n\n1: Column 1\n2: Column 2\n3: Column 3\n")
            while self.subsetup not in ["1", "2", "3"]:
                self.subsetup = input("Column. Select an option:\n\n1: Column 1\n2: Column 2\n3: Column 3\n")

        elif self.setup == 6:
            while self.wager in string.ascii_letters:
                self.wager = input("Enter wager amount:\n")
            self.wager = int(self.wager)

            self.subsetup = input("Dozen. Select an option:\n\n1: 1-12\n2: 13-24\n3: 25-36\n")
            while self.subsetup not in ["1", "2", "3"]:
                self.subsetup = input("Dozen. Select an option:\n\n1: 1-12\n2: 13-24\n3: 25-36\n")

        elif self.setup == 7:
            while self.wager in string.ascii_letters:
                self.wager = input("Enter wager amount:\n")
            self.wager = int(self.wager)

            self.subsetup = input("Lows/Highs. Select an option:\n\n1: 1-18\n2: 19-36\n")
            while self.subsetup not in ["1", "2"]:
                self.subsetup = input("Lows/Highs. Select an option:\n\n1: 1-18\n2: 19-36\n")

        elif self.setup == 8:
            while self.wager in string.ascii_letters:
                self.wager = input("Enter wager amount:\n")
            self.wager = int(self.wager)

            self.subsetup = input("Colors. Select an option:\n\n1: Red\n2: Black\n")
            while self.subsetup not in ["1", "2"]:
                self.subsetup = input("Colors. Select an option:\n\n1: Red\n2: Black\n")

        elif self.setup == 9:
            while self.wager in string.ascii_letters:
                self.wager = input("Enter wager amount:\n")
            self.wager = int(self.wager)
            
            self.subsetup = input("Evens/Odds. Select an option:\n\n1: Evens\n2: Odds\n")
            while self.subsetup not in ["1", "2"]:
                self.subsetup = input("Evens/Odds. Select an option:\n\n1: Evens\n2: Odds\n")

        else:
            return "invalid selection"

    def return_setup(self):
        output = self.gamble_df["setup"][self.gamble_df["row"] == self.setup]
        return output

    def return_subsetup(self):
        if self.setup in [1, 2]:
            output = self.subsetup
        elif self.setup == 4:
            temp_dict = {1: "1-6", 2: '4-9', 3: '7-12', 4: '10-15', 5: '13-18',
                         6: '16-21', 7: '19-24', 8: '22-27', 9: '25-30', 10: '28-33', 11: '31-36'}
            output = temp_dict[int(self.subsetup)]
        else:
            output = list(self.gamble_df["options"][self.gamble_df["row"] == self.setup])[0][int(self.subsetup) - 1]

        return output

    def return_payout(self):
        return self.payout


class Results:
    """Contains info about the roulette spin results.

    Attributes:
        roulette_wheel_input: object of class RouletteWheel
        gamble_setup_input: object of class GambleSetup

    Methods:
        spin: randomly samples a number from the roulette wheel. Must proceed the other methods.
        evaluate_win: returns a boolean on whether or not the user won.
    """

    def __init__(self, player_info_input, roulette_wheel_input, gamble_setup_input):
        # inputs from other class objects
        self.chips = player_info_input.chips
        self.rw = roulette_wheel_input
        self.gs = gamble_setup_input
        self.payout = gamble_setup_input.payout
        self.wager = gamble_setup_input.wager
        
        # set defaults
        self.roulette_number = "0"
        self.win = False
        self.chip_delta = 0

    def spin(self):
        self.roulette_number = np.random.choice(
            self.rw.roulette_df["numbers"], size=1,
            p=self.rw.roulette_df["probs"])[0]

    def evaluate_win(self):
        gamblesetup = self.gs.return_setup()
        gamblesubsetup = self.gs.return_subsetup()

        row_num = list(self.rw.roulette_df["numbers"]).index(self.roulette_number)
        possible_wins = list(self.rw.roulette_df.iloc[row_num, :])

        # win is False until proven True
        if (gamblesetup == "Straight-up").bool():
            wager_multiplier = len(gamblesubsetup)
            if self.roulette_number in gamblesubsetup:
                self.win = True
                # if they bet on the same number multiple times, multiply the payout
                self.payout *= gamblesubsetup.count(self.roulette_number)
        
        elif (gamblesetup == "Split").bool():
            wager_multiplier = len(gamblesubsetup)/2
            if self.roulette_number in gamblesubsetup:
                self.win = True
                # if they bet on the same number multiple times, multiply the payout
                self.payout *= gamblesubsetup.count(self.roulette_number)

        elif (gamblesetup == "Six_Line").bool():
            wager_multiplier = 1
            spread = list(map(lambda x: int(x), gamblesubsetup.split("-")))
            if int(self.roulette_number) >= spread[0] and int(self.roulette_number) <= spread[1]:
                self.win = True

        elif gamblesetup.isin(["Street", "Column", "Dozen", "Lows_Highs", "Colors", "Evens_Odds"]).bool():
            wager_multiplier = 1
            if gamblesubsetup in possible_wins:
                self.win = True

        if self.win:
            self.chip_delta = self.wager*self.payout*wager_multiplier
            text = """
You win!
Roulette wheel result: {}
You wagered {} chips
Your payout: {}
Your profit: {}
New chip count: {}
            """.format(self.roulette_number, self.wager*wager_multiplier, self.wager*self.payout, self.chip_delta, self.chips + self.chip_delta)
            return text
        else:
            self.chip_delta = self.wager*wager_multiplier*-1
            text = """
You lose
Roulette wheel result: {}
You wagered {} chips
Your payout: {}
Your profit: {}
New chip count: {}
                """.format(self.roulette_number, self.chip_delta*-1, 0, self.chip_delta, self.chips + self.chip_delta)

        return text


class RouletteGraph:
    """Takes a PlayerInfo object as input, returns matplotlib plots

    Methods:
        spin_barchart() - returns barchart of spin history
        strategy_barchart() - returns barchart of historical strategy selections
        subsetup_barchart() - returns barchart of historical gamble selections
        chip_line() - time series plot of chip history
    """

    def __init__(self, playerinfo):
        self.pi = playerinfo

    def spin_barchart(self):
        x = self.pi.spin_history
        x_distinct = list(set(x))
        x_counts = [x.count(i) for i in x_distinct]
        plt.bar(x_distinct, x_counts, color = "green")
        plt.xlabel("Historical Roulette Numbers")
        plt.ylabel("Count")
        plt.show()
    
    def strategy_barchart(self):
        x = self.pi.setup_history
        x_distinct = list(set(x))
        x_counts = [x.count(i) for i in x_distinct]
        plt.bar(x_distinct, x_counts, color = "green")
        plt.xlabel("Historical Strategies")
        plt.ylabel("Count")
        plt.show()
    
    def subsetup_barchart(self):
        x = self.pi.subsetup_history
        x = list(map(lambda x: str(x), x))
        x_distinct = list(set(x))
        x_counts = [x.count(i) for i in x_distinct]
        plt.bar(x_distinct, x_counts, color = "green")
        plt.xlabel("Historical Selections")
        plt.ylabel("Count")
        plt.show()
    
    def chip_line(self):
        x = self.pi.chip_history
        move = [i for i in range(len(x))]
        plt.plot(move, x)
        plt.xlabel("Moves")
        plt.ylabel("Chip Count")
        plt.show()


class ControlPanel:

    """Object will contain methods to navigate the classes above

    Methods:
        run_setups() - Initialize the game by prompting inputs to setup
        main_menu() - Display 4 main options of the game
        play_game() - Continues to ask user questions while playing the game
    """

    def __init__(self):
        self.Player1 = "0"
        self.RouletteWheel1 = "0"
        self.GambleSetup1 = "0"
    
    def run_setups(self):
        input(f"""
Get ready to gamble! 
Next I will ask for some player info. 
If you don't want to enter any player info, just keep pressing 'enter' to accept default values.
Press {col.blue}enter{col.E} to continue.\n\n""")

        self.Player1 = PlayerInfo(player_name=input("What is your name?"),
                     player_dob=input("Enter DOB (any numeric format seperated by '-' or '/'):"),
                     chips=input("How many chips do you want to buy (default = 1,000)?"))
        self.RouletteWheel1 = RouletteWheel(self.Player1)
        self.GambleSetup1 = GambleSetup()
    
    def main_menu(self):
        #decision = input(f"Welcome to the roulette table.\nWhat would you like to do?\n1: Start over and re-define player attributes\n2: View history (chip counts, and historical results)\n3: Quit\n4: Gamble!\n")
        decision = input(f"""
Welcome to the roulette table.
What would you like to do?
1: Start over and re-define player attributes
2: View history (chip counts, and historical results)
3: Quit
4: Gamble!\n\n""")
        return decision
    
    def play_game(self):

        while True:

            if self.Player1.chips <= 0:
                print(f"{col.R}You ran out of money. Game over.{col.E}")
                break

            decision = self.main_menu()

            # If player chooses to start over and re-define player attributes
            if decision == "1":
                self.Player1 = PlayerInfo(player_name=input("What is your name?"),
                                    player_dob=input("Enter DOB (any numeric format seperated by '-' or '/'):"),
                                    chips=input("How many chips do you want to buy?"))

                self.RouletteWheel1 = RouletteWheel(self.Player1)
                self.GambleSetup1 = GambleSetup()

            # If player chooses to view history
            elif decision == "2":
                
                rg = RouletteGraph(self.Player1)

                while True:
                    plot_select = int(input("Select graph type:\n1: Spin History\n2: Strategy History\n3: Selection History\n4: Chip History\n5: Go back\n"))

                    if plot_select == 1:
                        rg.spin_barchart()
                        continue
                    elif plot_select == 2:
                        rg.strategy_barchart()
                        continue
                    elif plot_select == 3:
                        rg.subsetup_barchart()
                        continue
                    elif plot_select == 4:
                        rg.chip_line()
                        continue
                    elif plot_select == 5:
                        break
                    else:
                        raise Exception("Invalid selection")

            # If player chooses to quit
            elif decision == "3":
                print("Thanks for playing")
                break

            # If player chooses to gamble
            elif decision == "4":

                self.RouletteWheel1.table_printout()
                input(f"Take a look at the roulette table\nPress {col.blue}enter{col.E} to continue")
                self.GambleSetup1.gamble_setup()
                Results1 = Results(player_info_input=self.Player1, roulette_wheel_input=self.RouletteWheel1, gamble_setup_input=self.GambleSetup1)
                Results1.spin()
                Results1.roulette_number
                print(Results1.evaluate_win())

                # store this historical results
                self.Player1.log_spins(Results1.roulette_number)
                self.Player1.log_setups(self.GambleSetup1.return_setup().item(), self.GambleSetup1.return_subsetup())
                self.Player1.update_chips(Results1.chip_delta)
                input(f"Press {col.blue}enter{col.E} to continue")
            else:
                print("Invalid selection")

#------------------------------------------------------------
#------------------------------------------------------------
# run game
game = ControlPanel()
game.run_setups()
game.play_game()
