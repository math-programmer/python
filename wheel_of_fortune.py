
import random
import json
import time 

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
VOWELS = "AEIOU"
VOWEL_COST = 10
#class declaration for wheel of fortune player
class WOFPlayer():
    def __init__(self,name):
        self.name = name 
        self.prizeMoney = 0
        self.prizes = []
    def addMoney(self,amount):
        self.prizeMoney += amount
    def goBankrupt(self):
        self.prizeMoney = 0
    def addPrize(self,prize):
        self.prizes.append(prize)
    def __str__(self):
        return "{} (${})".format(self.name,self.prizeMoney)
#class declaration for wheel of fortune human player
class WOFHumanPlayer(WOFPlayer):
    def getMove(self,category, obscuredPhrase, guessed):
        user_input = input("""
        {} has ${}

        Category : {}
        Phrase : {}
        Guessed: {}

        Guess a letter, phase or type  'exit' or 'pass':
        
        """.format(self.name,self.prizeMoney,category,obscuredPhrase,guessed))
        return user_input
#class declaration for wheel of fortune computer player
class WOFComputerPlayer(WOFPlayer):
    SORTED_FREQUENCIES = "ZQXJKVBPYGFWMUCLDRHSNIOATE"
    def __init__(self,name,difficulty):
        super().__init__(name)
        self.difficulty = difficulty
    # to decide the computer move depending on the difficulty level 
    def smartCoinFlip(self):
        """ decide semi randomly whether to make a "good" move or "bad" move by choosing 
        a random number between 1 and 10 and returning the True if that random number is greater 
        than difficulty and False if less """
        
        random_number = random.randint(1,10)
        if random_number <= self.difficulty:
            return True
        else:
            return False

    def getPossibleLetters(self,guessed):
        """ guessed = a list of guessed characters
        This method should return a list of letters that can be guessed. 
        These should be characters that are in LETTERS ('ABCDEFGHIJKLMNOPQRSTUVWXYZ') but not in the guessed parameter.
        Additionally, if this player doesn’t have enough prize money to guess a vowel (VOWEL_COST), then vowels (VOWELS: 'AEIOU') should not be included
        """
        possible_letters = []
        if self.prizeMoney >= VOWEL_COST :
            for letter in LETTERS:
                if letter not in guessed:
                    possible_letters.append(letter)
        else:
            for letter in LETTERS:
                if (letter not in guessed) and (letter not in VOWELS):
                    possible_letters.append(letter)
        return possible_letters
    
    def getMove(self, category, obscuredPhrase, guessed):
        """ Returns a valid move for the computer player that follows the rules explained below: 
         1. if there aren’t any letters that can be guessed, return 'pass' 
         2. if there are letters to guess, use smartCoinFLip() method to decide whether to make a "good" move or "bad" move
         
         Parameters: 
         self : object instance 
         category : a string which defines the category of the phrase
         obscuredPhrase :  a string consits of letters for guessed and "_" for not guessed
         guessed : a list of letters that can be guessed  
         
         Returns :
        a string whcih is a letter 

        """
        move_state = self.smartCoinFlip()
        possible_letter_index = []
        possible_letters = self.getPossibleLetters(guessed)
        if len(possible_letters) > 0:
            if move_state:
                for letter in possible_letters:
                    possible_letter_index.append(self.SORTED_FREQUENCIES.index(letter))
                possible_letter_index_sorted = sorted(possible_letter_index)
                possible_move = self.SORTED_FREQUENCIES[possible_letter_index_sorted[-1]]
                return possible_move
            elif not move_state:
                possible_move = random.choice(possible_letters)
                return possible_move
            else:
                raise Exception("error in random selection of move, check the coinFLip() method" )
        else:
            return "pass"

# function definition to get a number between min and max
def getNumberBetween(prompt,min,max):
    """ iterate till user input a value between min:minimum and max:maximum 
    cross check if the value is valid """

    user_input = input(prompt+" ,"+ "a number between {} and {} \n".format(min,max)) # for the first time input 
    while True:
        try :             # handling the error using try-except 
            user_input = int(user_input) # have to be a number
            if user_input < min:
                errmsg = "please enter a number atleast {}".format(min)
            elif user_input > max:
                errmsg = "please enter a number atmost {}".format(max)
            else:
                return user_input # if the number is correct then return will exit the loop 
        except ValueError:          # error handling 
            errmsg = "enter a valid number"
        
        user_input = input(prompt + " ," +errmsg+'\n') # loop user input

# function definition to get a random category and phrase from the collection of categories and phrases
def getRandomCategoryAndPhrase():

    """ 
    the function reads the categories and phrases from a  json file : phrases.json and return one random selection
    Parameters :
    no input Arguments
    
    Returns :
    A tuple of category and phrase 

    """
    with open("phrases.json") as file:
        file_content = file.read()
        data = json.loads(file_content) # data in dictonary format
    categories = list(data.keys()) # extracting the keys which are categories 
    random_category = random.choice(categories) 
    random_phrase = random.choice(data[random_category])
    return (random_category,random_phrase.upper())

# this function will return a random prize 
def spinWheel():
    """
    this function will returns a random prize from the list of prizes mimicking the spin of a wheel 
    the function will read a json file : wheel.json 

    Input Parameters :
    no input argument 

    Output Parameters :
    return a dictionary 

    """
    with open("wheel.json") as file:
        data = file.read()
        wheel = json.loads(data)
    wheelprize = random.choice(wheel)
    return wheelprize
# retuns current state of the board    
def showBoard(category, obscuredPhrase, guessed):
    return """
    Category : {}
    Phrase : {}
    Guessed : {}
    """ .format(category, obscuredPhrase, ",".join(sorted(guessed)))

#given a phrase and list of guessed letters , return an obscured version of the same 
def obscurePhrase(phrase,guessed):
    obscured_phrase = ""
    for letter in phrase:
        if (letter not in guessed) and (letter in LETTERS):
            obscured_phrase += "_"
        else:
            obscured_phrase += letter
    return obscured_phrase

  
##### game logic code######
print("="*30)
print(" "*10+"Wheel Of Fortune")
print("="*30)
print("\n")
num_human = getNumberBetween("enter the number of human players",0,10)
num_computer = getNumberBetween("enter the number of computer players",0,10)
#if there are computer players, please ask the difficulty level of them assuming all are with same difficulty
if num_computer > 0:
    difficulty = getNumberBetween("enter the difficulty level of the computer player",1,10)
#create player instances 
human_players = []
for iter in range(num_human):
    palyer_name = input("Enter the name of the player{}\n".format(iter+1))
    human_players.append(WOFHumanPlayer(palyer_name))
computer_players = []
for iter in range(num_computer):
    palyer_name = input("Enter the name of the computer player {}\n".format(iter+1))
    computer_players.append(WOFComputerPlayer(palyer_name,difficulty))
players = human_players + computer_players

if len(players) == 0:
    raise Exception("The game will play only withatleast one player")

category,phrase = getRandomCategoryAndPhrase()
guessed = []
playerIndex = 0
winner = False
while True:
    player = players[playerIndex]
    print(playerIndex)
    wheelprize = spinWheel()
    print("-"*30)
    print(showBoard(category,obscurePhrase(phrase,guessed),guessed))
    print(' '*20)
    print("{} wheel spins...".format(player.name))
    time.sleep(2)
    print("{}!".format(wheelprize["text"]))

    if wheelprize["type"] == "bankrupt":
        player.goBankrupt()
    elif wheelprize["type"] == "cash":
        move = player.getMove(category,obscurePhrase(phrase,guessed),guessed)
        move = move.upper()
        if move == "EXIT":
            break
        elif move != "PASS":
            if len(move) == 1:
                if move not in LETTERS:
                    print("Guess should be alphabets, Try Again")
                    continue
                if move in guessed:
                    print("Already guessed before, Try again")
                    continue
                if move in VOWELS:
                    if player.prizeMoney < VOWEL_COST :
                        print("Didnt have enough money to guess a vowel, Try Again")
                        continue
                    else:
                        player.prizeMoney -= VOWEL_COST
                        
                guessed.append(move)
                count = phrase.count(move)
                if count > 0 :
                    if count == 1:
                        print("There is one {}".format(move))
                    else:
                        print("There are {} {}'s".format(count,move))
                    
                    player.addMoney(count*wheelprize["value"])

                    if wheelprize["prize"] :
                        player.addPrize(wheelprize["prize"])
                    if obscurePhrase(phrase,guessed) == phrase:
                        winner = player
                        break
                    continue
                elif count == 0:
                    print("There is no {}".format(move))
            else:
                if move == phrase:
                    player.addMoney(wheelprize["value"])
                    if wheelprize["prize"]:
                        player.addPrize(wheelprize["prize"])
                    winner = player
                    break
                else:
                    print("{} is not the phrase".format(move))
    playerIndex = (playerIndex + 1)  % len(players)

if winner:
    print("{} wins! The phrase was {}".format(winner.name,phrase))
    print("{} won ${}".format(winner.name,winner.prizeMoney))
    if len(winner.prizes) > 0 :
        print("{} also won : ".format(winner.name))
        for prize in winner.prizes:
            print("{}".format(prize))
else:
    print("Nobody Wins")


            


            

            









