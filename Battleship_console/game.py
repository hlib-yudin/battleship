from display import *
from datetime import datetime
from main_classes import *
from exceptions import *
from time import sleep
from abc import ABC, abstractmethod
from random import randrange, choice
import uuid
import sqlite3

def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

@singleton
class Game(IViewable):
    """Клас, що відповідає за логіку гри."""

    def __init__(self):
        """Ініціалізатор класу."""
        self.__currentInterface = Console()
        self.__currentPlayer = None
        self.__currentEnemy = None  # гравець, який в даний момент не ходить
        self.__players = []
        self.__currentInterface.clear()

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

    # -------------------------------------------------------

    def swapPlayer(self):
        """Передає хід наступному гравцю."""
        self.__players.reverse()
        self.__currentPlayer = self.__players[0]
        self.__currentEnemy = self.__players[1]

    def startMultiPlay(self):
        """Проводить гру між гравцем і роботом."""

        self.currentInterface.clear()
        self.currentInterface.printShipsDecoration()
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
        self.currentPlayer.arrangeShips()
        self.currentEnemy.arrangeShips()

        # ігровий цикл
        while True:

            # просимо протилежного гравця відвернутися
            self.currentInterface.clear()
            self.currentInterface.printShipsDecoration()
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
            while moveResult:  # поки гравець не промахнеться

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
                        print('\n' + str(e))
                        input()
                        message = f'Гравець {self.currentPlayer.name}, ваш хід: '
                        self.currentInterface.render(field=renderInfo['field'],
                                                     fieldEnemy=renderInfo['fieldEnemy'],
                                                     message=message)

                moveResult = self.currentPlayer.makeMove(coords)  # = True, якщо гравець влучив

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
                print('\n' + "Вітаю з перемогою")
                top = input("Якщо бажаєте подивитися топ 5 гравців, натисніть 1")
                if top == '1': self.showTop()
                break

            input()
            self.swapPlayer()

        # повідомлення про кінець гри, відображення повністю всіх ігрових полів
        renderInfo = self.getRenderInfo()
        message = f'Гравець {winner.name} переміг!'
        self.currentInterface.render(field=renderInfo['field'],
                                     fieldEnemy=renderInfo['fieldEnemy'], message=message)
        input()

    def startSinglePlay(self):
        """Проводить гру з роботом."""

        self.currentInterface.clear()
        self.currentInterface.printShipsDecoration()

        # створюємо гравця
        playerName = input("Введіть ваше ім'я: ")
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
                message = "Гравець " + self.currentPlayer.name + " ходить... "
                self.currentInterface.render(fieldEnemy=renderInfo['field'],
                                             field=renderInfo['fieldEnemy'],
                                             message=message)
            else:
                message = "Гравець " + self.currentPlayer.name + ", ваш хід: "
                self.currentInterface.render(field=renderInfo['field'],
                                             fieldEnemy=renderInfo['fieldEnemy'],
                                             message=message)

            moveResult = True
            while moveResult != False:  # поки гравець не промахнеться

                correctInput = False
                while not correctInput:  # поки гравець не введе адекватні координати
                    try:
                        coords = self.currentPlayer.chooseCellCoord()
                        correctInput = True

                    except KeyboardInterrupt:
                        raise

                    # якщо chooseCellCoord видав помилку
                    except Exception as e:
                        print('\n' + str(e))

                        # message = f'Гравець {self.currentPlayer.name}, ваш хід: '
                        # self.currentInterface.render(field=renderInfo['field'],
                        #                              fieldEnemy=renderInfo['fieldEnemy'],
                        #                              message=message)

                moveResult = self.currentPlayer.makeMove(coords)

                # у випадку з роботом -- чекаємо 3 секунди, щоб він не походив
                # миттєво після ходу людини
                if isinstance(self.currentPlayer, Robot):
                    sleep(3)

                winner = self.checkForGameOver()
                if winner:  # якщо кінець гри
                    break

                if moveResult:  # якщо влучили

                    # для робота й людини -- різні повідомлення
                    if isinstance(self.currentPlayer, Player):
                        message = "Гравець " + self.currentPlayer.name + " влучив! Ходіть ще раз: "
                    else:
                        message = "Гравець " + self.currentPlayer.name + " влучив! Він ходить... "

                    # рендеримо
                    renderInfo = self.getRenderInfo()
                    if isinstance(self.currentPlayer, Player):
                        self.currentInterface.render(field=renderInfo['field'],
                                                     fieldEnemy=renderInfo['fieldEnemy'], message=message)
                    else:
                        self.currentInterface.render(fieldEnemy=renderInfo['field'],
                                                     field=renderInfo['fieldEnemy'], message=message)

            if winner:
                print('\n'+"Вітаю з перемогою")
                top = input("Якщо бажаєте подивитися топ 5 гравців, натисніть 1")
                if top == '1': self.showTop()
                break

            self.swapPlayer()

        # повідомлення про кінець гри, відображення повністю всіх ігрових полів
        renderInfo = self.getRenderInfo()
        message = f'Гравець {winner.name} переміг!'
        self.currentInterface.render(field=renderInfo['field'],
                                     fieldEnemy=renderInfo['fieldEnemy'], message=message)



    def saveScore(self, game_id, player, player_score, is_winner, game_datetime):
        conn = sqlite3.connect('battleship.sqlite')
        cur = conn.cursor()
        cur.execute('''INSERT OR IGNORE INTO Games (game_id, player, player_score, is_winner, game_datetime)
            VALUES ( ?, ?, ?, ?, ? )''', (game_id, player, player_score, is_winner, game_datetime))

        conn.commit()
        conn.close()


    def checkForGameOver(self):
        """Після кожного ходу перевіряє, чи закінчилася гра.
        Якщо так -- повертає переможця.
        Інакше -- повертає False."""
        player1, player2 = self.players
        winner = None
        loser = None
        # перевіряємо к-сть непотоплених кораблів у кожного гравця
        if player1.field.shipsCount == 0:
            winner = player2
            loser = player1
        elif player2.field.shipsCount == 0:
            winner = player1
            loser = player2
        else: return False
        game_id = str(uuid.uuid4())
        game_datetime = str(datetime.now())
        self.saveScore(game_id, winner.name, winner.score, "T", game_datetime)
        self.saveScore(game_id, loser.name, loser.score, "F", game_datetime)
        return winner

    def showTop(self):
        conn = sqlite3.connect('battleship.sqlite')
        cur = conn.cursor()
        cur.execute('''SELECT player, SUM(player_score)
                        FROM Games
                        GROUP BY player
                        ORDER BY SUM(player_score) DESC
                        LIMIT 5''')
        players = cur.fetchall()
        for row in players:
            print(row)


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

########################################################
########################################################
########################################################
########################################################

class AbsPlayer(ABC):
    def __init__(self, name):
        self.__name = name
        self.__score = 0
        self.__field = Field()

    @property
    def name(self):
        return self.__name


    @property
    def field(self):
        return self.__field

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, score):
        self.__score = score

    @name.setter
    def name(self, name):
        """Сеттер для поля name."""
        self.__name = name

    @field.setter
    def field(self, field):
        """Сеттер для поля field."""
        self.__field = field

    ##########
    def coordMap(self, length, orientation):  # Функція, що обирає координати для корабля
        # генерація точки з випадковими координатами

        coords = []
        stroka = randrange(10)  # номер рядку
        stolb = randrange(10)  # номер стовпчика
        shipCorrect = 1
        for i in range(length):

            # В залежності від напрямку генерувати нові точки корабля
            # 0 - горизонтально (збільшувати стовпець), 1 - вертикально (збільшувати рядок)
            if stolb + i > 9 or stroka + i > 9:
                shipCorrect = 0
            if orientation == 0:
                coords.append((stroka, (stolb + i)))  # додаємо нову координату в список
            else:
                coords.append(((stroka + i), stolb))
        if (shipCorrect == 1):
            return coords  # якщо координати коректні(не виходять за межі поля), повертаємо їх
        else:
            return self.coordMap(length, orientation)  # якщо ні обираємо інш точку

    ##########
    def around_ship(self, coords):  # Функція, що вираховує точки, які оточують корабель

        aroundСoords = []
        for x, y in coords:
            adjcells = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1), (x + 1, y + 1), (x + 1, y - 1), (x - 1, y + 1),
                        (x - 1, y - 1)]
            for adjx, adjy in adjcells:
                if (adjx < 0 or adjx > 9 or adjy < 0 or adjy > 9):
                    continue
                else:
                    aroundСoords.append((adjx, adjy))
        result = list(set(aroundСoords))  # Містить також точки самого корабля
        return result

    ##########
    def randomArrangement(self):  # Функція генерації кораблів на полі

        countShips = 0  # Кількість згенерованих кораблів

        while countShips < 10:
            # масив зайнятих кораблями точок
            fleetArray = []
            # обнулити кількість кораблів
            countShips = 0
            # масив з флотом
            fleetShips = []
            # генерація кораблів (length - кількість палуб корабля)
            for length in reversed(range(1, 5)):
                # генерація необхідної кількості кораблів необхідної довжини
                for i in range(5 - length):
                    try_create_ship = 0
                    while 1:
                        try_create_ship += 1
                        # якщо кількість спроб перевищило 50, почати все заново
                        if try_create_ship > 50:
                            break

                            # випадкове розташування корабля (або горизонтальне, або вертикальне)
                        orientation = randrange(2)

                        # випадкове розташування корабля
                        shipCoords = self.coordMap(length, orientation)
                        """Якщо корабель може бути поставлений коректно, 
                        то його точки разом з точками, які оточують корабель, 
                        не перетинаються з вже зайнятими іншими кораблями точками поля"""

                        intersectArray = list(set(fleetArray) & set(self.around_ship(shipCoords) + shipCoords))
                        if len(intersectArray) == 0:
                            # створити екземпляр класу Ship
                            new_ship = Ship(length, shipCoords)
                            # додати в масив з усіма зайнятими точками точки самого корабля
                            fleetArray += shipCoords
                            fleetShips.append(new_ship)  # додати в масив кораблів новій корабель
                            countShips += 1
                            break
        print(fleetArray)
        for ship in fleetShips:
            self.field.placeShip(ship)

        # print(fleetArray)

    ##########


    def makeMove(self, coord):
        x = coord[0]
        y = coord[1]
        enemyField = Game().currentEnemy.field
        enemyField.cellsList[x][y].hitCell()
        if enemyField.cellsList[x][y].belongsTo != None:
            ship = enemyField.cellsList[x][y].belongsTo
            ship.increaseHitCount()

            if ship.checkIfSunk():
                enemyField.decreaseShipsCount()
                enemyField.sinkShip(ship)
                self.addscore(ship.size)
            return True
        return False

    def addscore(self, length):
        self.score += 5 - length

    @abstractmethod
    def chooseCellCoord(self):
        """метод, що обирає координати пострілу"""



########################################################


class Player(AbsPlayer):
    def __init__(self, name):
        super().__init__(name)

    def print_name(self):
        print(self.name)

    def chooseCellCoord(self):
        # """Метод обирання координат.
        # Може видати виключення, якщо дані не коректні."""

        coords = input("Введіть букву а-j та число від 0 до 9: ")
        if  self.checkCellCoords(coords[1:], coords[0]):
            x = int(coords[1:])
            y = ord(coords[0]) - 97

        if Game().currentEnemy.field.cellsList[x][y].isHit == True:  # перевіряємо чи не обирав користувач цю клітину раніше
            raise CellIsAlreadyHit((x, y))
        return (x, y)

    def checkCellCoords(self, x, y):
        def isOk(value, type):  # допоміжна функція, яка перевіряє чи коректне значення ввів користувач
            try:
                if type == 0:
                    value = int(value)  # перевіряємо чи є х числом
                else:
                    value = ord(value) - 97  # перевіряємо чи є y літерою

                if not (value >= 0 and value <= 9):  # введена координата виходить за межі поля
                    raise WrongCoordinates

            except (ValueError, TypeError):  # введено неправильний тип даних
                raise NotCoordinates

            return True

        if (isOk(x, 0) and isOk(y, 1)):  # перевіряємо чи коректні значення ввів користувач
            return True
        else: return False



    def arrangeShips(self):
            """Проводить розстановку кораблів."""

            # для робота все просто
            if isinstance(self, Robot):
                self.randomArrangement()
                return

            # 1. отримати від гравця поле з кораблями
            # 2. перевірити, чи порушує розстановка кораблів правила гри
            # якщо так -- помилка, чекаємо, коли гравець зробить нормальну розстановку
            # 3. якщо ні -- зберігаємо розстановку
            ############################################################################
            # 1. отримання даних

            # тимчасове поле; False -- клітинка не належить до корабля,
            # True -- належить
            tempField = [[False for j in range(11)] for i in range(11)]
            numberOfClickedCells = 0

            # наступний блок коду відбуватиметься, поки гравець не введе коректну розстановку
            arrangementCorrect = False
            while not arrangementCorrect:

                endOfArrangement = False
                Game().currentInterface.renderWhileArrangingShips(tempField, self.name)

                # поки гравець не завершив розставляти кораблі
                while not endOfArrangement:

                    # поки гравець не введе адекватні дані
                    correctInput = False
                    while not correctInput:

                        try:
                            # користувач вводить координати клітинки; щоб завершити, він
                            # вводить порожнй рядок; для випадкової розстановки він вводить 'r'
                            print('''
    a3 -- обрати клітинку а3
    r -- випадкова розстановка
    Порожній рядок -- закінчити розстановку\n''')
                            coords = input('Ваш вибір: ')

                            if coords == '':
                                endOfArrangement = True
                            elif coords == 'r':
                                self.randomArrangement()
                                return
                            else:
                                self.checkCellCoords(coords[1:], coords[0])
                                x = int(coords[1:])
                                y = ord(coords[0]) - 97
                                tempField[x][y] = not tempField[x][y]
                                if tempField[x][y]:
                                    numberOfClickedCells += 1
                                else:
                                    numberOfClickedCells -= 1

                                # рендеримо
                                Game().currentInterface.renderWhileArrangingShips(tempField, self.name)

                            correctInput = True

                        # якщо гравець ввів неадекватні дані
                        except Exception as e:
                            print(e)
                            input()
                            # self.game.currentInterface.renderWhileArrangingShips(tempField, self.name)
                ##########################################################################
                # 2. перевірка правильності розстановки

                # TO DO: try-except
                try:
                    # якщо обраних клітинок не 20, то розстановка вже не правильна
                    if numberOfClickedCells != 20:
                        raise WrongNumberOfElements(numberOfClickedCells)

                    # проходимо по ігровому полю, шукаємо кораблі, пропускаємо порожні клітинки
                    # shipElementsList -- список оброблених клітинок корабля
                    # shipList -- список сформованих кораблів
                    # forbiddenCellList -- множина клітинок, на яких не дозволено бути кораблю
                    shipElementsList = []
                    shipList = []
                    forbiddenCellSet = set()
                    for x in range(10):
                        for y in range(10):

                            # якщо знайшли якийсь необроблений елемент корабля --
                            # то це або початок корабля, або однопалубний корабель
                            if tempField[x][y] and ((x, y) not in shipElementsList):
                                shipElementsList.append((x, y))
                                u, v = x, y
                                shipLength = 1

                                # починаємо формувати корабель
                                currentShip = [(u, v)]

                                # клітинки, що оточують дану клітинку знизу по діагоналі,
                                # мають бути вільні
                                forbiddenCellSet.add((u + 1, v - 1))
                                forbiddenCellSet.add((u + 1, v + 1))

                                if (u, v) in forbiddenCellSet:  # клітинка на забороненій території
                                    raise TouchingShips((u, v))

                                # далі визначаємо орієнтацію корабля (вправо чи вниз),
                                # оброблюємо наступні елементи корабля

                                # якщо є клітинка справа -- йдемо вправо до кінця корабля
                                if tempField[u][v + 1]:
                                    endOfShip = False
                                    while not endOfShip:
                                        v = v + 1
                                        shipLength += 1

                                        if shipLength == 5:  # занадто довгий корабель
                                            raise TooLongShip((u, v))

                                        if (u, v) in shipElementsList:  # клітинка в двох кораблях
                                            raise TouchingShips((u, v))

                                        if (u, v) in forbiddenCellSet:  # клітинка на забороненій території
                                            raise TouchingShips((u, v))

                                        shipElementsList.append((u, v))
                                        currentShip.append((u, v))
                                        forbiddenCellSet.add((u + 1, v - 1))
                                        forbiddenCellSet.add((u + 1, v + 1))

                                        # перевіряємо, чи наступна клітинка -- теж елемент корабля
                                        # інакше формуємо корабель
                                        if tempField[u][v + 1]:
                                            continue
                                        else:
                                            endOfShip = True
                                            shipList.append(currentShip)


                                # якщо є клітинка знизу -- все аналогічно
                                elif tempField[u + 1][v]:
                                    endOfShip = False
                                    while not endOfShip:
                                        u = u + 1
                                        shipLength += 1

                                        if shipLength == 5:  # занадто довгий корабель
                                            raise TooLongShip((u, v))

                                        if (u, v) in shipElementsList:  # клітинка в двох кораблях
                                            raise TouchingShips((u, v))

                                        if (u, v) in forbiddenCellSet:  # клітинка на забороненій території
                                            raise TouchingShips((u, v))

                                        shipElementsList.append((u, v))
                                        currentShip.append((u, v))
                                        forbiddenCellSet.add((u + 1, v - 1))
                                        forbiddenCellSet.add((u + 1, v + 1))

                                        # перевіряємо, чи наступна клітинка -- теж елемент корабля
                                        # інакше формуємо корабель
                                        if tempField[u + 1][v]:
                                            continue
                                        else:
                                            endOfShip = True
                                            shipList.append(currentShip)


                                # якщо корабель однопалубний -- просто додаємо його
                                else:
                                    shipList.append(currentShip)

                    # ми перевірили, чи стоять кораблі так, як треба
                    # тепер перевіримо їхню кількість
                    if len(shipList) != 10:
                        raise WrongNumberOfShips(len(shipList))

                    # також перевіримо, щоб були 1 чотирипалубний, 2 трипалубні кораблі...
                    shipLengthList = list(map(len, shipList))
                    if not (shipLengthList.count(1) == 4
                            and shipLengthList.count(2) == 3
                            and shipLengthList.count(3) == 2
                            and shipLengthList.count(4) == 1):
                        raise WrongSetOfShips(shipLengthList)

                    ########################################################################################
                    # 3. якщо помилок нема -- розстановка закінчена, зберігаємо кораблі в player.field
                    for ship in shipList:
                        shipToSave = Ship(len(ship), ship)
                        self.field.placeShip(shipToSave)
                    arrangementCorrect = True

                # інакше -- виводимо помилку, гравець перероблює своє поле
                except Exception as e:
                    print(e)
                    input()


class Robot(AbsPlayer):

    def __init__(self, name):
        super().__init__(name)
        self.availablePoints = [(i, j) for i in range(10) for j in range(10)]
        self.lastCoord = ()

    def chooseCellCoord(self):
        coord = self.lastCoord
        for x in range(10):
            for y in range(10):
                if Game().currentEnemy.field.cellsList[x][y].isHit == True:
                    if (self.availablePoints.count((x, y)) != 0):
                        self.availablePoints.remove((x, y))
        # если step = 0, то генерировать случайные точки

        if len(coord) != 0:
            coordList = [(coord[0] + 1, coord[1]), (coord[0] - 1, coord[1]), (coord[0], coord[1] + 1),
                         (coord[0], coord[1] - 1)]
            notCoordList = {(coord[0] + 1, coord[1] + 1), (coord[0] - 1, coord[1] - 1), (coord[0] - 1, coord[1] + 1),
                            (coord[0] + 1, coord[1] - 1)}
            self.availablePoints = list(set(self.availablePoints).difference(notCoordList))
            Points = list(set(coordList) & set(self.availablePoints))
            # len_availablePoints = len(Points)
            if len(Points) == 0:
                coord = choice(self.availablePoints)

            else:
                coord = choice(Points)
        else:
            coord = choice(self.availablePoints)
        if Game().currentEnemy.field.cellsList[coord[0]][coord[1]].belongsTo != None:    self.lastCoord = coord
        return coord






#################################
#################################
#################################
#################################
game = Game()
option = game.currentInterface.mainMenu()
if option == 1:
    game.startSinglePlay()
elif option == 2:
    game.startMultiPlay()
