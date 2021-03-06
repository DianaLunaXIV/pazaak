import random
import sys

def start_game():
    player1_name = input("Player 1, please enter your name: ")
    opponent_choice = input("Would you like to play against the computer, or against a friend? ").lower()
    if "c" in opponent_choice:
        wager = input("Please enter how many credits you want to wager on the game: ")
        game_against_computer(wager, player1_name)
    elif "f" in opponent_choice:
        player2_name = input("Player 2, please enter your name: ")
        wager = input("How many credits will be wagered by each player? ")
        game_against_friend(wager, player1_name, player2_name)
    else: 
        print("Please type either 'computer' or 'friend' into the console.")


class PazaakMainDeck:
    def __init__(self):
        self.counter = 0
        self.contents = {1: 4, 2: 4, 3: 4, 4: 4, 5: 4, 6: 4, 7: 4, 8: 4, 9: 4, 10: 4}
    
    def reset_main_deck(self):
        self.contents = {1: 4, 2: 4, 3: 4, 4: 4, 5: 4, 6: 4, 7: 4, 8: 4, 9: 4, 10: 4}
        self.counter = 0
        print("Main deck reset.")

    def has_card(self, key):
        if self.contents[key] > 0:
            return True
        else:
            return False

    def draw(self):
        deck_choice = int(random.randint(1, 10))
        while not self.has_card(deck_choice):
            deck_choice = int(random.randint(1,10))
        self.contents[deck_choice] -= 1
        self.counter += 1
        return deck_choice
        
class Player:
    def __init__(self, name, credits=1000):
        self.player_name = name
        self.credit_total = credits
        self.card_count = 0
        self.card_value = 0
        self.is_standing = False
        self.has_forfeited = False

    def change_card_value(self, card):
        self.card_value += card
        self.card_count += 1
        return self.card_value
    
    def get_card_value(self):
        return self.card_value
    
    def change_credit_value(self, value):
        self.credit_total += value
        return self.credit_total
    
    def get_credit_value(self):
        return self.credit_total

class PazaakGame:
    def __init__(self, wager, player1="Player 1", player2="computer", cpu=True):
        self.wager = wager
        self.opponent_is_computer = cpu
        self.main_deck = PazaakMainDeck()
        self.round_count = 1
        self.player1 = Player(player1)
        self.player2 = Player(player2)
        self.game_is_over = False

    
    def cycle_round(self):
        print(f"Wager for this match: {self.wager}")
        print(f"Current scores: \n {self.player1.player_name}: {self.player1.get_card_value()} \n {self.player2.player_name}: {self.player2.get_card_value()} ")
        self.round_count += 1
        print(f"Round #{self.round_count}:")
    
    def player_turn(self, player):
        current_player_name = player.player_name
        print(f"{current_player_name}'s turn:\n")
        if player.is_standing is False:
            card_drawn = self.main_deck.draw()
            print(f"{current_player_name} draws {card_drawn} from the main deck.")
            player.change_card_value(card_drawn)
            
            if current_player_name != "computer":
                player_choice = input("Stand, End Turn, or Forfeit?").lower()
            else:
                player_choice = "end turn"
                return
            
            if "s" in player_choice:
                player.is_standing = True
                print(f"{current_player_name} is standing with {player.get_card_value()}.")
                return
            elif "f" in player_choice:
                player.has_forfeited = True
            else:
                print(f"{current_player_name} ends their turn with {player.get_card_value()}.")
        else:
            print(f"{current_player_name} is standing with {player.get_card_value()}.")
            return
    

    def win_condition_to_print(self):
        player1_value = self.player1.get_card_value()
        player2_value = self.player2.get_card_value()
        player1_forfeit = self.player1.has_forfeited
        player2_forfeit = self.player2.has_forfeited

        if player1_value == 20 and player2_value != 20:
            return f"{self.player1.player_name} wins with 20!"
        elif player2_value == 20 and player1_value != 20:
            return f"{self.player2.player_name} wins with 20!"
        elif player1_value > player2_value and self.player2.is_standing and not player1_value > 20:
            return f"{self.player1.player_name} wins with {player1_value} against {self.player2.player_name}'s standing {player2_value}."
        elif player2_value > player1_value and self.player1.is_standing and not player2_value > 20:
            return f"{self.player2.player_name} wins with {player2_value} against {self.player1.player_name}'s standing {player1_value}."
        elif player1_value > 20:
            return f"{self.player1.player_name} has busted out. {self.player2.player_name} wins with {player2_value}."
        elif player2_value > 20:
            return f"{self.player2.player_name} has busted out. {self.player1.player_name} wins with {player1_value}."
        elif player2_value > 20 and player1_value > 20:
            return f"Both {self.player1.player_name} and {self.player2.player_name} busted out. Draw!"
        elif player1_forfeit and not player2_forfeit:
            return f"{self.player1.player_name} has forfeited. \n {self.player2.player_name} wins with {player2_value}!"
        elif player2_forfeit and not player1_forfeit:
            return f"{self.player2.player_name} has forfeited. \n {self.player1.player_name} wins with {player1_value}!"
        elif player1_forfeit and player2_forfeit:
            return f"Both players have forfeited.\n {self.player1.player_name} : {self.player2.player_name}\n {player1_value} : {player2_value} \n Draw!"
        else:
            return f"Current scores: \n {self.player1.player_name}: {player1_value} \n {self.player2.player_name}: {player2_value} "
        
    def evaluate_score(self):
        string_to_print = self.win_condition_to_print()
        if "Current scores" not in string_to_print:
            self.game_is_over = True
            self.main_deck.reset_main_deck()
            print(string_to_print)
        else:
            self.cycle_round()

def game_over():
    player_choice = input("Return to main menu? (y/n)")

    if "y" in player_choice:
        start_game()
    else:
        sys.exit("Thanks for playing!")

def game_against_computer(wager, player_name):
    cpu_game = PazaakGame(wager, player_name)
    while cpu_game.game_is_over is False:
        cpu_game.player_turn(cpu_game.player1)
        cpu_game.player_turn(cpu_game.player2)
        cpu_game.evaluate_score()
    game_over()

    
def game_against_friend(wager, player1_name, player2_name):
    two_player_game = PazaakGame(wager, player1_name, player2_name, False)
    while two_player_game.game_is_over is False:
        two_player_game.player_turn(two_player_game.player1)
        two_player_game.player_turn(two_player_game.player2)
        two_player_game.evaluate_score()
    game_over()

start_game()