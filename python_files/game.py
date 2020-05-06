from display import *
from os import system
from main_classes import *

class Game(IViewable):
    """Клас, що відповідає за логіку гри."""


    def __init__(self):
        """Ініціалізатор класу."""
        self.__currentInterface = Console()
        self.__currentPlayer = None
        self.__currentEnemy = None # гравець, який в даний момент не ходить
        self.__players = []
        system('mode con: cols=113 lines=34')

    @property
    def currentInterface(self):
        """Геттер для поля currentInterface."""
        return self.__currentInterface

    @property
    def players(self):
        """Геттер для поля players."""
        return self.__players

    @players.setter
    def players(self, players):
        """Сеттер для поля players."""
        self.__players = players

    @property
    def currentPlayer(self):
        """Геттер для поля currentPlayer."""
        return self.__currentPlayer

    @currentPlayer.setter
    def currentPlayer(self, currentPlayer):
        """Сеттер для поля currentPlayer."""
        self.__currentPlayer = currentPlayer

    @property
    def currentEnemy(self):
        """Геттер для поля currentEnemy."""
        return self.__currentEnemy

    @currentEnemy.setter
    def currentEnemy(self, currentEnemy):
        """Сеттер для поля currentEnemy."""
        self.__currentEnemy = currentEnemy

#-------------------------------------------------------

    def swapPlayer(self):
        """Передає хід наступному гравцю."""
        self.__players.reverse()
        self.__currentPlayer = self.__players[0]
        self.__currentEnemy = self.__players[1]

    # def startSinglePlay(self):
    #     """Проводить гру між гравцем і роботом."""

    #     # створюємо гравців
    #     self.players = [Player(), Robot()]
    #     self.currentPlayer = self.players[0]
    #     self.currentEnemy = self.players[1]
    #     winner = None

    #     # розставляємо кораблі
    #     # TO DO

    #     # рендеримо ігрові поля
    #     renderInfo = self.getRenderInfo()
    #     self.currentInterface.render(field=renderInfo['field'], 
    #         fieldEnemy=renderInfo['fieldEnemy'],
    #         message=f'Гравець {self.currentPlayer}, ваш хід: ')

    #     # ігровий цикл
    #     while True:
    #         # спочатку ходить людина, потім -- робот

    #         # хід гравця
    #         # якщо гравець влучив -- перевіряємо, чи закінчена гра
    #         # якщо гра не закінчена, то даємо гравцю право походити знову
    #         moveResult = False            
    #         while not moveResult: # поки гравець не промахнеться

    #             moveResult = self.currentPlayer.makeMove() # = True, якщо гравець влучив

    #             # перевірка кінця гри
    #             if moveResult:
    #                 winner = self.checkForGameOver()
    #                 if winner:
    #                     break

    #             # на основі результату ходу формуємо повідомлення
    #             if moveResult:
    #                 message = f'Гравець {self.currentPlayer} влучив! Ходіть ще раз: '
    #             else:
    #                 message = f'Гравець {self.currentEnemy}, ваш хід: '

    #             # рендеримо ігрові поля після кожного ходу
    #             # наступний блок коду потрібен, щоб поле людини завжди рендерилось
    #             # зліва, а поле робота -- справа
    #             renderInfo = self.getRenderInfo()
    #             if isinstance(self.currentPlayer, Robot):
    #                 self.currentInterface.render(fieldEnemy=renderInfo['field'], 
    #                     field=renderInfo['fieldEnemy'], message=message)
    #             else:
    #                 self.currentInterface.render(field=renderInfo['field'], 
    #                     fieldEnemy=renderInfo['fieldEnemy'], message=message)


    #         if winner:
    #             break

    #         self.swapPlayer()

    #     # повідомлення про кінець гри, відображення повністю всіх ігрових полів
    #     renderInfo = self.getRenderInfo()
    #     message = f'Гравець {winner.name} переміг!'
    #     self.currentInterface.render(field=renderInfo['field'], 
    #         fieldEnemy=renderInfo['fieldEnemy'], message=message, showall=True)
        
        




    def startMultiPlay(self):
        """Проводить гру між гравцем і роботом."""

        # створюємо гравців
        playerName1 = input("Введіть ім'я першого гравця: ")
        playerName2 = input("Введіть ім'я другого гравця: ")

        player1, player2 = Player(playerName1, self), Player(playerName2, self)
        self.players = [player1, player2]
        self.currentPlayer = self.players[0]
        self.currentEnemy = self.players[1]
        winner = None

        # розставляємо кораблі
        # TO DO
        self.currentPlayer.randomArrangement()
        self.currentEnemy.randomArrangement()

        # ігровий цикл
        while True:

            # просимо протилежного гравця відвернутися
            clear()
            print(f"Гравець {self.currentPlayer.name}, приготуйтеся!")
            input("Натисніть Enter, щоб продовжити: ")

            # рендеримо ігрові поля
            renderInfo = self.getRenderInfo()
            self.currentInterface.render(field=renderInfo['field'], 
                fieldEnemy=renderInfo['fieldEnemy'],
                message=f'Гравець {self.currentPlayer.name}, ваш хід: ')


            # хід гравця
            # якщо гравець влучив -- перевіряємо, чи закінчена гра
            # якщо гра не закінчена, то даємо гравцю право походити знову
            moveResult = True            
            while moveResult: # поки гравець не промахнеться

                coords = self.currentPlayer.chooseCellCoord()
                moveResult = self.currentPlayer.makeMove(coords) # = True, якщо гравець влучив

                # перевірка кінця гри
                if moveResult:
                    winner = self.checkForGameOver()
                    if winner:
                        break

                # на основі результату ходу формуємо повідомлення
                if moveResult:
                    message = 'Ви влучили! Ходіть ще раз: '
                else:
                    message = 'Натисніть Enter, щоб продовжити: '

                # рендеримо ігрові поля після кожного ходу
                renderInfo = self.getRenderInfo()
                
                self.currentInterface.render(field=renderInfo['field'], 
                    fieldEnemy=renderInfo['fieldEnemy'], message=message)


            if winner:
                break

            input()
            self.swapPlayer()

        # повідомлення про кінець гри, відображення повністю всіх ігрових полів
        renderInfo = self.getRenderInfo()
        message = f'Гравець {winner.name} переміг!'
        self.currentInterface.render(field=renderInfo['field'], 
            fieldEnemy=renderInfo['fieldEnemy'], message=message, showall=True)


    def checkForGameOver(self):
        """Після кожного ходу перевіряє, чи закінчилася гра.
        Якщо так -- повертає переможця.
        Інакше -- повертає False."""
        player1, player2 = self.players

        # перевіряємо к-сть непотоплених кораблів у кожного гравця
        if player1.field.shipsCount == 0:
            return player2
        elif player2.field.shipsCount == 0:
            return player1
        return False
        

    def getRenderInfo(self):
        """Збирає інформацію про всю гру для виведення.
        Повертає структуру, яка буде передана методу Console.render().
        Структура:
        { 
            field : dict(
                playerName='Player 1',
                cellsInfo=player1.field.getRenderInfo()
            ), 
            fieldEnemy : dict(
                playerName='Player 2',
                cellsInfo=player2.field.getRenderInfo()
        }"""

        player1, player2 = self.players
        playerName1, playerName2 = player1.name, player2.name
        renderInfo1, renderInfo2 = player1.field.getRenderInfo(), player2.field.getRenderInfo()

        return {
            'field': {
                'playerName': playerName1,
                'cellsInfo': renderInfo1
            },
            'fieldEnemy': {
                'playerName': playerName2,
                'cellsInfo': renderInfo2
            }
        }





game = Game()
game.startMultiPlay()