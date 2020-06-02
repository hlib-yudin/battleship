from display import *
from os import system
from main_classes import *
from exceptions import *
from time import sleep

class Game(IViewable):
    """Клас, що відповідає за логіку гри."""


    def __init__(self, interface):
        """Ініціалізатор класу."""
        self.__currentInterface = Graphic() if interface == '1' else Console()
        self.__currentPlayer = None
        self.__currentEnemy = None # гравець, який в даний момент не ходить
        self.__players = []

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


    def startMultiPlay(self):
        """Проводить гру між гравцем і гравцем."""

        #self.currentInterface.clear()
        #self.currentInterface.printShipsDecoration()
        # створюємо гравців
        playerName1, playerName2 = self.currentInterface.renderScreenEnterName(2)

        player1, player2 = Player(playerName1, self), Player(playerName2, self)
        self.players = [player1, player2]
        self.currentPlayer = self.players[0]
        self.currentEnemy = self.players[1]
        winner = None

        # розставляємо кораблі
        # TO DO
        self.currentPlayer.arrangeShips()
        self.currentEnemy.arrangeShips()

        # ігровий цикл
        while True:

            # просимо протилежного гравця відвернутися
            """self.currentInterface.clear()
            self.currentInterface.printShipsDecoration()
            print(f"Гравець {self.currentPlayer.name}, приготуйтеся!")
            input("Натисніть Enter, щоб продовжити: ")"""
            self.currentInterface.renderScreenPrepareForTurn(self.currentPlayer.name)

            # рендеримо ігрові поля
            renderInfo = self.getRenderInfo()
            self.currentInterface.render(field=renderInfo['field'], 
                fieldEnemy=renderInfo['fieldEnemy'])
            message = f'Гравець {self.currentPlayer.name}, ваш хід! '
            self.currentInterface.printText(message)


            # хід гравця
            # якщо гравець влучив -- перевіряємо, чи закінчена гра
            # якщо гра не закінчена, то даємо гравцю право походити знову
            moveResult = True            
            while moveResult: # поки гравець не промахнеться

                # поки гравець не введе адекватні координати
                correctInput = False
                while not correctInput:
                    try:
                        coords = self.currentPlayer.chooseCellCoord()
                        correctInput = True

                    except KeyboardInterrupt:
                        raise
                    
                    # якщо chooseCellCoord видав помилку
                    except Exception as e:
                        self.currentInterface.printError(e)
                        message = f'Гравець {self.currentPlayer.name}, ваш хід! '
                        self.currentInterface.render(field=renderInfo['field'], 
                            fieldEnemy=renderInfo['fieldEnemy'])
                        self.currentInterface.printText(message)

                moveResult = self.currentPlayer.makeMove(coords) # = True, якщо гравець влучив

                # перевірка кінця гри
                if moveResult:
                    winner = self.checkForGameOver()
                    if winner:
                        break

                # на основі результату ходу формуємо повідомлення
                if moveResult:
                    message = 'Ви влучили! Ходіть ще раз! '
                else:
                    message = 'Натисніть Enter, щоб продовжити: '

                # рендеримо ігрові поля після кожного ходу
                renderInfo = self.getRenderInfo()
                
                self.currentInterface.render(field=renderInfo['field'], 
                    fieldEnemy=renderInfo['fieldEnemy'])
                self.currentInterface.printText(message)


            if winner:
                break

            self.currentInterface.inputEnter()
            self.swapPlayer()

        # повідомлення про кінець гри, відображення повністю всіх ігрових полів
        renderInfo = self.getRenderInfo()
        message = f'Гравець {winner.name} переміг! Натисніть Enter, щоб продовжити: '
        self.currentInterface.render(field=renderInfo['field'], 
            fieldEnemy=renderInfo['fieldEnemy'])
        self.currentInterface.printText(message)
        self.currentInterface.inputEnter()
        

    def startSinglePlay(self):
        """Проводить гру з роботом."""
        
        #self.currentInterface.clear()
        #self.currentInterface.printShipsDecoration()

        # створюємо гравця
        playerName = self.currentInterface.renderScreenEnterName(1)
        self.players = [Player(playerName, self), Robot("Robot", self)]
        self.currentPlayer = self.players[0]
        self.currentEnemy = self.players[1]

        # розстановка кораблів
        self.currentPlayer.arrangeShips()
        self.currentEnemy.randomArrangement()

        winner = None
        while True:
            # спочатку ходить людина, потім -- робот

            # хід гравця
            # якщо гравець влучив -- перевіряємо, чи закінчена гра
            # якщо гра не закінчена, то даємо гравцю право походити знову

            # рендеримо поля
            renderInfo = self.getRenderInfo()
            if isinstance(self.currentPlayer, Robot):
                message = "Гравець "+ self.currentPlayer.name + " ходить... "
                self.currentInterface.render(fieldEnemy=renderInfo['field'], 
                    field=renderInfo['fieldEnemy'])
                self.currentInterface.printText(message)
            else:
                message = "Гравець "+ self.currentPlayer.name + ", ваш хід! "
                self.currentInterface.render(field=renderInfo['field'], 
                    fieldEnemy=renderInfo['fieldEnemy'])
                self.currentInterface.printText(message)

            moveResult = True
            while moveResult != False: # поки гравець не промахнеться

                correctInput = False
                while not correctInput: # поки гравець не введе адекватні координати
                    try:
                        coords = self.currentPlayer.chooseCellCoord()
                        correctInput = True

                    except KeyboardInterrupt:
                        raise
                    
                    # якщо chooseCellCoord видав помилку
                    except Exception as e:
                        self.currentInterface.printError(e)
                        message = f'Гравець {self.currentPlayer.name}, ваш хід! '
                        self.currentInterface.render(field=renderInfo['field'], 
                            fieldEnemy=renderInfo['fieldEnemy'])
                        self.currentInterface.printText(message)

                moveResult = self.currentPlayer.makeMove(coords)

                # у випадку з роботом -- чекаємо 3 секунди, щоб він не походив 
                # миттєво після ходу людини
                if isinstance(self.currentPlayer, Robot):
                    sleep(2)

                winner = self.checkForGameOver()
                if winner: # якщо кінець гри
                    break


                if moveResult: # якщо влучили
    
                    # для робота й людини -- різні повідомлення
                    if isinstance(self.currentPlayer, Player):
                        message = "Гравець "+ self.currentPlayer.name + " влучив! Ходіть ще раз! "
                    else:
                        message = "Гравець "+ self.currentPlayer.name + " влучив! Він ходить... "

                    # рендеримо
                    renderInfo = self.getRenderInfo()
                    if isinstance(self.currentPlayer, Player):
                        self.currentInterface.render(field=renderInfo['field'],
                            fieldEnemy=renderInfo['fieldEnemy'])
                        self.currentInterface.printText(message)
                    else:
                        self.currentInterface.render(fieldEnemy=renderInfo['field'],
                            field=renderInfo['fieldEnemy'])
                        self.currentInterface.printText(message)


            if winner:
                break

            self.swapPlayer()

        # повідомлення про кінець гри, відображення повністю всіх ігрових полів
        renderInfo = self.getRenderInfo()
        message = f'Гравець {winner.name} переміг! Натисніть Enter, щоб продовжити: '
        if isinstance(winner, Robot):
            self.currentInterface.render(field=renderInfo['fieldEnemy'],
                fieldEnemy=renderInfo['field'], showall=True)
        else:
            self.currentInterface.render(field=renderInfo['field'],
                fieldEnemy=renderInfo['fieldEnemy'])
        self.currentInterface.printText(message)
        self.currentInterface.inputEnter()


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


    
system('cls')      
interface = input("Введіть 1 для графічного інтерфейсу чи будь-яку іншу клавішу для консольного: ")

game = Game(interface)
quitChoosed = False
while not quitChoosed:
    option = game.currentInterface.mainMenu()
    if option == '1':
        game.startSinglePlay()
    elif option == '2':
        game.startMultiPlay()
    elif option == '0':
        quitChoosed = True


