import random


# Модель
class Player:
    def __init__(self, name):
        self.name = name
        self.wins = 0


class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def roll_dice(self):
        return random.randint(1, 6) + random.randint(1, 6)

    def play_round(self):
        score1 = self.roll_dice()
        score2 = self.roll_dice()
        result = None

        if score1 > score2:
            self.player1.wins += 1
            result = self.player1.name
        elif score2 > score1:
            self.player2.wins += 1
            result = self.player2.name
        return score1, score2, result


class GameView:
    @staticmethod
    def show_roll(player_name, score):
        print(f"{player_name} выбросил {score}")

    @staticmethod
    def show_round_winner(winner_name):
        print(f"{winner_name} выиграл раунд!")

    @staticmethod
    def show_tie():
        print("Ничья!")

    @staticmethod
    def show_statistics(player1, player2):
        print("Статистика игры:")
        print(f"{player1.name}: {player1.wins} побед")
        print(f"{player2.name}: {player2.wins} побед")


class GameController:
    def __init__(self, player1_name, player2_name):
        self.player1 = Player(player1_name)
        self.player2 = Player(player2_name)
        self.game = Game(self.player1, self.player2)
        self.view = GameView()

    def play_round(self):
        score1, score2, winner_name = self.game.play_round()
        self.view.show_roll(self.player1.name, score1)
        self.view.show_roll(self.player2.name, score2)

        if winner_name:
            self.view.show_round_winner(winner_name)
        else:
            self.view.show_tie()

    def show_statistics(self):
        self.view.show_statistics(self.player1, self.player2)


controller = GameController("Alice", "Bob")
controller.play_round()
controller.play_round()
controller.show_statistics()
