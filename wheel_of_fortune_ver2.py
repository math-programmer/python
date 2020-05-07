
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

        Guess a letter, phrase or type  'exit' or 'pass':
        
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
num_human = getNumberBetween("Enter the number of human players, ",0,10)
num_computer = getNumberBetween("Enter the number of computer players, ",0,10) 
if num_computer > 0:
    difficulty = getNumberBetween("Enter the difficulty level for computer player",0,10)
# getting the name of human players and creating object instances
human_players = []
for iter in range(0,num_human):
    name = input("Enter the name of the human player{}\n".format(iter+1))
    human_players = [WOFHumanPlayer(name)]
# getting the name of computer players and creating object instances
computer_players = []
for iter in range(0,num_computer):
    name = input("Enter the name of the computer player{}\n".format(iter+1))
    computer_players = [WOFComputerPlayer(name,difficulty)]
players =  human_players + computer_players
if len(players) == 0:
    raise Exception("Zero Players, Minimum one player is required ")

category,phrase = getRandomCategoryAndPhrase()    
player_index = 0
guessed = []
winner = 0
x = 1

while True:
    print("playing starts.....")
    player = players[player_index]
    print("wheel spin for {}".format(player))
    wheel_prize = spinWheel()
    print(showBoard(category,obscurePhrase(phrase,guessed),guessed))
   
    if wheel_prize["type"] == "bankrupt":
        print("bakrupt")
        player.goBankrupt()
    elif wheel_prize["type"] == "cash":
        move = player.getMove(category,obscurePhrase(phrase,guessed),guessed)
        move = move.upper() 
        if move == "EXIT":
            break
        elif move != "PASS":
            if (len(move) == 1) and (move in LETTERS):
                if move in guessed:
                    print("the letter is already guessed, please try again")
                    continue
                if move in VOWELS:
                    if player.prizeMoney < VOWEL_COST:
                        print("not enough money to guess vowels")
                    else:
                        player.prizeMoney -= VOWEL_COST
                #check if the gussed letter is present or not
                guessed.append(move)
                count = phrase.count(move)
                if count != 0 :
                    if phrase == obscurePhrase(phrase,guessed):
                        winner = player
                        break
                    else:
                        print("there are {} of {}'s".format(count,move))
                        player.addMoney(wheel_prize["value"]*count)
                        if wheel_prize["prize"]:
                            player.addPrize(wheel_prize["prize"])                
                else:
                    print("there is no {} in the phrase".format(move))
                continue   
                
            elif move == phrase:
                print("the pharse guessed is correct")
                winner = player
                break
            else:
                print("Not a valid letter, Try Again")
                continue    
    player_index = (player_index + 1) % len(players) 
        
   
    