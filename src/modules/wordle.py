import random
from collections import Counter
from rich.prompt import Prompt
from rich import print
from .words import words


class Wordle:

    def __init__(self):
        self.words:list = words.get('five_letter')
        self.valid_words:list = words.get("valid_word")
        self.chosen_word:str = self._select_word()
        self.max_words = 5
        self.user_guess:str = ""


    def get_user_guess(self, remaining:int = None):
        self.user_guess = Prompt.ask(f"\n\n[gray]Guess your word ({remaining} guess left) [/gray]").strip()
        if len(self.user_guess) != self.max_words:
            print('\n [red]--- Wait a minute.... That ain\'t a five letter word !!!! --- \n')
            self.get_user_guess(remaining=remaining)
        elif self.user_guess not in self.words and self.user_guess not in self.valid_words:
            print('\n [red]--- Oops! Not a valid word!!!! --- \n')  
            self.get_user_guess(remaining=remaining)
        
    def _select_word(self):
        random_index = int(
            random.random() * len(self.words)
            )
        return self.words[random_index].lower()

    def is_correct_guess(self):
        return self.chosen_word.lower() == self.user_guess.lower()

    def check_word(self):
        user_guess_validated  = []

        ## Stings converted to list
        user_guess = list(self.user_guess)
        system_word = list(self.chosen_word)    

        ## Count of each words is in the list
        guess_count = dict(Counter(user_guess))
        correct_count = dict(Counter(system_word))


        ## Check for exact match
        for idx, ltr in enumerate(user_guess):
            temp = {'letter': ltr, 'index':idx}
            if ltr == system_word[idx]:
                print(idx, ltr, "matches")
                correct_count[ltr] -= 1
                temp['color'] = 'spring_green2'
                user_guess_validated.append(temp)
            else:
                temp['color'] = 'grey84'
                user_guess_validated.append(temp)

        ## Sort the Validated result with index key
        user_guess_validated = sorted(user_guess_validated, key=lambda x: x['index'])

        ## Check for letter presence in the correct word
        for idx, ltr in enumerate(user_guess):
            if ltr in system_word:
                ## Exceute only when there is a remaining letter on the correct word
                if correct_count[ltr] != 0:
                    ## If its already found to be an exact match, ignore it else, change it to orange1
                    if user_guess_validated[idx]['color'] != "spring_green2":
                        user_guess_validated[idx]['color'] = 'orange1'
                        ## Once Changed reduce the count
                        correct_count[ltr] -= 1
                    ## If the count is negative, automatically assume the letter is not present.
                    elif correct_count[ltr] < 1:
                        user_guess_validated[idx]['color'] = 'grey84'


        ## Check if the word is correct directly
        if self.is_correct_guess():
            return True, user_guess_validated

        return False, user_guess_validated


