import random
from rich.prompt import Prompt
from rich import print
from .words import words


class Wordle:

    def __init__(self):
        self.words:list = words.get('five_letter')
        self.chosen_word:str = self._select_word()
        self.max_words = 5
        self.user_guess:str = ""


    def get_user_guess(self, remaining:int = None):
        self.user_guess = Prompt.ask(f"\n\n[gray]Guess your word ({remaining} guess left) [/gray]").strip()
        if len(self.user_guess) != self.max_words:
            print('\n [red]--- Wait a minute.... That ain\'t a five letter word !!!! --- \n')
            self.get_user_guess(remaining=remaining)
        elif self.user_guess not in self.words:
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
        user_guess = list(self.user_guess)
        system_word = list(self.chosen_word)
        # print(Columns(user_guess))
            

        for idx, user_word in enumerate(user_guess):
            temp = {'letter': user_word}
            if user_word == system_word[idx]:
                temp['color'] = 'spring_green3'
            elif user_word in system_word:
                temp['color'] = 'orange1'
            else:
                temp['color'] = 'grey84'
            user_guess_validated.append(temp)

        ## Check if the word is correct directly
        if self.is_correct_guess():
            return True, user_guess_validated

        return False, user_guess_validated


