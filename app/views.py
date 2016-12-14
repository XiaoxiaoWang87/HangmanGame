from flask import Flask, render_template, request, redirect, url_for, flash, Markup
import random
import string
from app import app


#app = Flask(__name__)

def loadWords():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    inFile = open("app/static/words.txt", 'r')
    line = inFile.readline()
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def chooseWord(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

def isWordGuessed(secretWord, lettersGuessed):
    '''
    secretWord: string, the word the user is guessing
    lettersGuessed: list, what letters have been guessed so far
    returns: boolean, True if all the letters of secretWord are in lettersGuessed;
      False otherwise
    '''
    # FILL IN YOUR CODE HERE...

    for c in secretWord:
        if c not in lettersGuessed:
            return False
    return True

def getGuessedWord(secretWord, lettersGuessed):
    '''
    secretWord: string, the word the user is guessing
    lettersGuessed: list, what letters have been guessed so far
    returns: string, comprised of letters and underscores that represents
      what letters in secretWord have been guessed so far.
    '''
    # FILL IN YOUR CODE HERE...

    output = ''
    for c in secretWord:
        if c in lettersGuessed:
            output += c
        else:
            output += ' _ '
    return output


def getAvailableLetters(lettersGuessed):
    '''
    lettersGuessed: list, what letters have been guessed so far
    returns: string, comprised of letters that represents what letters have not
      yet been guessed.
    '''
    # FILL IN YOUR CODE HERE...
    output = ''
    for i in string.ascii_lowercase:
        if i not in lettersGuessed:
            output += i
    return output





#wordlist = loadWords()
wordlist = []
secretWord = ''

lettersGuessed = []
idx = 0

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start', methods = ['POST', 'GET'])
def start():

    global wordlist
    global secretWord
    global lettersGuessed
    global idx

    if request.method == 'POST' or request.method == 'GET':
        #if request.form['newGame'] == 'Start a New Game':

        wordlist = loadWords()
        secretWord = chooseWord(wordlist).lower()
        lettersGuessed = []
        idx = 0

        result = {}
        result['secretWord'] = secretWord
        result['secretWordLen'] = len(secretWord)
        result['message'] = ['']
        result['animation'] = [Markup(''.join(['&nbsp;'] * 19) + '++ - - - - ++'), 
                               Markup(''.join(['&nbsp;'] * 35) + '|||'), 
                               Markup(''.join(['&nbsp;'] * 35) + '|||'), 
                               Markup(''.join(['&nbsp;'] * 35) + '|||'), 
                               Markup(''.join(['&nbsp;'] * 35) + '|||'), 
                               Markup(''.join(['&nbsp;'] * 35) + '|||'),
                               Markup(''.join(['&nbsp;'] * 10) + '= = = = = = = = =')]
           
        return render_template("start.html", result = result)


@app.route('/play', methods = ['POST', 'GET'])
def play():

    global idx 
    global lettersGuessed
    global secretWord

    if request.method == 'POST' or request.method == 'GET':
     
        print(secretWord)
        message = []

        if idx < 8 and isWordGuessed(secretWord, lettersGuessed) == False:

            print idx

            guessInLowerCase = request.form['aGuess'].lower()

            if guessInLowerCase in lettersGuessed:
                message.append("You've already guessed that letter: " + getGuessedWord(secretWord, lettersGuessed))
            elif len(guessInLowerCase) != 1 or guessInLowerCase.isalpha() == False:
                message.append("You did not enter a letter. " + getGuessedWord(secretWord, lettersGuessed))
            else:
                lettersGuessed.append(guessInLowerCase)

                if guessInLowerCase in secretWord:
                    message.append('Good guess: ' + getGuessedWord(secretWord, lettersGuessed))
                else:
                    message.append("Oops! That letter is not in my word: " + getGuessedWord(secretWord, lettersGuessed))
                    idx += 1  
                
            # Only print the remaining guesses when not running out of guesses and not having guessed the word already 
            if idx <= 7 and isWordGuessed(secretWord, lettersGuessed) == False:
                message.append(Markup('You have ' + '<font size="4" color="blue"><b>' + str(8 - idx) + ' guesses' + '</font></b>' + ' left.'))

        if isWordGuessed(secretWord, lettersGuessed) == True:
            message.append(Markup('<font size="4" color="green"><b>' + "Congratulations, you won!!" + '</font></b>'))
        elif idx == 8:
            message.append(Markup('<font size="4"><b>' + "Sorry, you ran out of guesses. The word was " + '<font color="red">' + secretWord + '</font>' + "." + '</font></b>'))

        result = {}
        result['secretWord'] = secretWord
        result['secretWordLen'] = len(secretWord)
                  
        result['message'] = message

        if idx == 0:
            result['animation'] = [Markup(''.join(['&nbsp;'] * 19) + '++ - - - - ++'),
                                   Markup(''.join(['&nbsp;'] * 35) + '|||'),
                                   Markup(''.join(['&nbsp;'] * 35) + '|||'),
                                   Markup(''.join(['&nbsp;'] * 35) + '|||'),
                                   Markup(''.join(['&nbsp;'] * 35) + '|||'),
                                   Markup(''.join(['&nbsp;'] * 35) + '|||'),
                                   Markup(''.join(['&nbsp;'] * 10) + '= = = = = = = = =')]
        elif idx == 1:
            result['animation'] = [Markup(''.join(['&nbsp;'] * 19) + '++ - - - - ++'),
                                   Markup(''.join(['&nbsp;'] * 21) + '|' + ''.join(['&nbsp;'] * 13) +  '|||'),
                                   Markup(''.join(['&nbsp;'] * 35) + '|||'),
                                   Markup(''.join(['&nbsp;'] * 35) + '|||'),
                                   Markup(''.join(['&nbsp;'] * 35) + '|||'),
                                   Markup(''.join(['&nbsp;'] * 35) + '|||'),
                                   Markup(''.join(['&nbsp;'] * 10) + '= = = = = = = = =')]
        elif idx == 2:
            result['animation'] = [Markup(''.join(['&nbsp;'] * 19) + '++ - - - - ++'),
                                   Markup(''.join(['&nbsp;'] * 21) + '|' + ''.join(['&nbsp;'] * 13) +  '|||'),
                                   Markup(''.join(['&nbsp;'] * 20) + 'O' + ''.join(['&nbsp;'] * 12) +  '|||'),
                                   Markup(''.join(['&nbsp;'] * 35) + '|||'),
                                   Markup(''.join(['&nbsp;'] * 35) + '|||'),
                                   Markup(''.join(['&nbsp;'] * 35) + '|||'),
                                   Markup(''.join(['&nbsp;'] * 10) + '= = = = = = = = =')]
        elif idx == 3:
            result['animation'] = [Markup(''.join(['&nbsp;'] * 19) + '++ - - - - ++'),
                                   Markup(''.join(['&nbsp;'] * 21) + '|' + ''.join(['&nbsp;'] * 13) +  '|||'),
                                   Markup(''.join(['&nbsp;'] * 20) + 'O' + ''.join(['&nbsp;'] * 12) +  '|||'),
                                   Markup(''.join(['&nbsp;'] * 21) + '|' + ''.join(['&nbsp;'] * 13) +  '|||'),
                                   Markup(''.join(['&nbsp;'] * 35) + '|||'),
                                   Markup(''.join(['&nbsp;'] * 35) + '|||'),
                                   Markup(''.join(['&nbsp;'] * 10) + '= = = = = = = = =')]
        elif idx == 4:
            result['animation'] = [Markup(''.join(['&nbsp;'] * 19) + '++ - - - - ++'),
                                   Markup(''.join(['&nbsp;'] * 21) + '|' + ''.join(['&nbsp;'] * 13) +  '|||'),
                                   Markup(''.join(['&nbsp;'] * 20) + 'O' + ''.join(['&nbsp;'] * 12) +  '|||'),
                                   Markup(''.join(['&nbsp;'] * 18) + '/'+ ''.join(['&nbsp;'] * 2) + '|' + ''.join(['&nbsp;'] * 13) +  '|||'),
                                   Markup(''.join(['&nbsp;'] * 35) + '|||'),
                                   Markup(''.join(['&nbsp;'] * 35) + '|||'),
                                   Markup(''.join(['&nbsp;'] * 10) + '= = = = = = = = =')]
        elif idx == 5:
            result['animation'] = [Markup(''.join(['&nbsp;'] * 19) + '++ - - - - ++'),
                                   Markup(''.join(['&nbsp;'] * 21) + '|' + ''.join(['&nbsp;'] * 13) +  '|||'),
                                   Markup(''.join(['&nbsp;'] * 20) + 'O' + ''.join(['&nbsp;'] * 12) +  '|||'),
                                   Markup(''.join(['&nbsp;'] * 18) + '/'+ ''.join(['&nbsp;'] * 2) + '|' + ''.join(['&nbsp;'] * 2) + '\\' + ''.join(['&nbsp;'] * 10) +  '|||'),
                                   Markup(''.join(['&nbsp;'] * 35) + '|||'),
                                   Markup(''.join(['&nbsp;'] * 35) + '|||'),
                                   Markup(''.join(['&nbsp;'] * 10) + '= = = = = = = = =')]
        elif idx == 6:
            result['animation'] = [Markup(''.join(['&nbsp;'] * 19) + '++ - - - - ++'),
                                   Markup(''.join(['&nbsp;'] * 21) + '|' + ''.join(['&nbsp;'] * 13) +  '|||'),
                                   Markup(''.join(['&nbsp;'] * 20) + 'O' + ''.join(['&nbsp;'] * 12) +  '|||'),
                                   Markup(''.join(['&nbsp;'] * 18) + '/'+ ''.join(['&nbsp;'] * 2) + '|' + ''.join(['&nbsp;'] * 2) + '\\' + ''.join(['&nbsp;'] * 10) +  '|||'),
                                   Markup(''.join(['&nbsp;'] * 18) + '/'+ ''.join(['&nbsp;'] * 16) +  '|||'),
                                   Markup(''.join(['&nbsp;'] * 35) + '|||'),
                                   Markup(''.join(['&nbsp;'] * 10) + '= = = = = = = = =')]
        elif idx == 7:
            result['animation'] = [Markup(''.join(['&nbsp;'] * 19) + '++ - - - - ++'),
                                   Markup(''.join(['&nbsp;'] * 21) + '|' + ''.join(['&nbsp;'] * 13) +  '|||'),
                                   Markup(''.join(['&nbsp;'] * 20) + 'O' + ''.join(['&nbsp;'] * 12) +  '|||'),
                                   Markup(''.join(['&nbsp;'] * 18) + '/'+ ''.join(['&nbsp;'] * 2) + '|' + ''.join(['&nbsp;'] * 2) + '\\' + ''.join(['&nbsp;'] * 10) +  '|||'),
                                   Markup(''.join(['&nbsp;'] * 18) + '/'+ ''.join(['&nbsp;'] * 5) + '\\' + ''.join(['&nbsp;'] * 10) +  '|||'),
                                   Markup(''.join(['&nbsp;'] * 35) + '|||'),
                                   Markup(''.join(['&nbsp;'] * 10) + '= = = = = = = = =')]


        return render_template("start.html", result = result)


#if __name__ == '__main__':
#    #app.run(debug = True)
#    app.run(debug = True, host='0.0.0.0', port=80)
