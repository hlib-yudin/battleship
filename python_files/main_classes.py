from abc import ABC, abstractmethod
from random import randrange, choice
from display import *


class Cell(IViewable):
    def  __init__(self, coord):
        self.__coord = coord
        self.__isHit = False
        self.__belongsTo = None

    @property
    def getCoord(self):
        return self.__coord

    @property
    def isHit(self):
        return self.__isHit

    @property
    def belongsTo(self):
        return self.__belongsTo


    @belongsTo.setter
    def belongsTo(self, belongsTo):
        self.__belongsTo = belongsTo



    def hitCell(self):
        if self.__isHit == False:
            self.__isHit = True

    def getRenderInfo(self):
        """Повертає інформацію для графічного відображення."""

        # з'ясовуємо, чи влучили в клітинку, чи ні, та статус корабля, якому вона належить
        # (потоплений/не потоплений/не належить кораблю)
        if self.isHit:
            isHitStatus = True
        else:
            isHitStatus = False

        if not self.belongsTo:
            shipStatus = 'not belongs'
        elif self.belongsTo.checkIfSunk():
            shipStatus = 'sunk'
        else:
            shipStatus = 'not sunk'

        return dict(
            isHitStatus=isHitStatus,
            shipStatus=shipStatus
        )


"------------------------------------------------"

class Ship:
  def __init__(self, size, elements):
    self.__size = size
    self.__hitCount = 0
    self.__elements = elements


  @property
  def size(self):
      return self.__size

  @size.setter
  def size(self, size):
      self.__size = size

  # def getHitCount(self):
  #     return self.__hitCount
  #
  # def setHitCount(self, hitCount):
  #      self.__hitCount = hitCount
  #
  #
  # hitCount = property(getHitCount, setHitCount)
  ################################################################
  @property
  def hitCount(self):
      return self.__hitCount
  #
  # @hitCount.setter
  # def hitCount(self):
  #     self.__hitCount += 1

  def increaseHitCount(self):
      self.__hitCount += 1

  @property
  def elements(self):
      return self.__elements

  @elements.setter
  def elements(self, elements):
      """Сеттер для поля size."""
      self.__elements = elements



  def checkIfSunk(self):

      if self.__hitCount == self.__size:
          return True
      else :
          return False


"------------------------------------------------"

class Field(IViewable):
    def __init__(self):
        self.__cellsList = [[Cell((i, j)) for j in range(10)] for i in range(10)]
        self.__shipsCount = 0 # к-сть непотоплених кораблів
        self.__shipsList = []


    @property
    def cellsList(self):
        return self.__cellsList

    @property
    def shipsCount(self):
        return self.__shipsCount

    @property
    def shipsList(self):
        return self.__shipsList


    def decreaseShipsCount(self):
        self.__shipsCount -= 1

    def setShipsList(self, ship):
        self.shipsList.append(ship)
        self.__shipsCount += 1

    def placeShip(self, ship):
        self.setShipsList(ship)
        shipElements = ship.elements
        for x, y in shipElements:
            self.cellsList[x][y].belongsTo = ship



    def sinkShip(self, ship):
        shipElements = ship.elements
        for x, y in shipElements:
            adjcells = [(x+1, y), (x-1, y), (x, y+1), (x, y-1), (x+1, y+1), (x+1, y-1), (x-1, y+1),  (x-1, y-1)]
            for adjx, adjy in  adjcells:
                if (adjx < 0 or adjx > 9 or adjy < 0 or adjy > 9):
                    continue
                else:
                    self.cellsList[adjx][adjy].hitCell()

    
    def getRenderInfo(self):
        """Повертає інформацію для графічного відображення."""
        return [[self.cellsList[x][y].getRenderInfo() for y in range(10)] 
            for x in range(10)]




##########################################################################
class AbsPlayer(ABC):
    def __init__(self, name, game):
        self.__name = name
        self.__score = 0
        self.__field = Field()
        self.__game = game


    @property
    def name(self):
        return self.__name

    @property
    def game(self):
        return self.__game

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
    def coordMap(self, length, orientation):     # Функція, що обирає координати для корабля
        # генерація точки з випадковими координатами

        coords = []
        stroka = randrange(10) # номер рядку
        stolb = randrange(10) # номер стовпчика
        shipCorrect = 1
        for i in range(length):

            # В залежності від напрямку генерувати нові точки корабля
            # 0 - горизонтально (збільшувати стовпець), 1 - вертикально (збільшувати рядок)
            if stolb + i > 9 or stroka + i > 9:
                shipCorrect = 0
            if orientation == 0:
                coords.append((stroka, (stolb + i))) # додаємо нову координату в список
            else:
                coords.append(((stroka + i), stolb))
        if (shipCorrect == 1):
            return coords  # якщо координати коректні(не виходять за межі поля), повертаємо їх
        else:
            return self.coordMap(length, orientation) # якщо ні обираємо інш точку


##########
    def around_ship(self, coords): # Функція, що вираховує точки, які оточують корабель

        aroundСoords = []
        for x, y in coords:
            adjcells = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1), (x + 1, y + 1), (x + 1, y - 1), (x - 1, y + 1),
                        (x - 1, y - 1)]
            for adjx, adjy in adjcells:
                if (adjx < 0 or adjx > 9 or adjy < 0 or adjy > 9):
                    continue
                else:
                    aroundСoords.append((adjx, adjy))
        result = list(set(aroundСoords)) # Містить також точки самого корабля
        return result

##########
    def randomArrangement(self):    # Функція генерації кораблів на полі

        countShips = 0 # Кількість згенерованих кораблів

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
        for ship in fleetShips:
            self.field.placeShip(ship)

        # print(fleetArray)
##########

    def display(self):
        i = 0
        print("   0__1__2__3__4__5__6__7__8__9")
        for cellList in self.field.cellsList:
            print(i, end='| ')
            for cell in cellList:

                if cell.belongsTo == None:
                    if cell.isHit:
                        print('*', end='  ')

                    else:
                        print('0', end='  ')
                else:
                    if cell.isHit:
                        print('X', end='  ')

                    else:
                        print('@', end='  ')
            print()
            i += 1


    def makeMove(self, coord):
        x = coord[0]
        y = coord[1]
        enemyField = self.game.currentEnemy.field
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
    def __init__(self, name, game):
        super().__init__(name, game)

    def print_name(self):
        print(self.name)

    def chooseCellCoord(self):
        x = int(input("Введіть число від 0 до 9: "))
        leter = input("Введіть букву а-j: ")
        y = ord(leter)-97
        return (x, y)



class Robot(AbsPlayer):

    def __init__(self, name, game):
        super().__init__(name, game)
        self.availablePoints = [(i, j) for i in range(10) for j in range(10)]


    def chooseCellCoord(self, step=0, coord = ()):
        print(step)
        for x in range(10):
            for y in range(10):
                if self.field.cellsList[x][y].isHit == True:

                    if (self.availablePoints.count((x, y)) != 0): self.availablePoints.remove((x, y))
        #если step = 0, то генерировать случайные точки

        if len(coord) != 0:
            coordList = [(coord[0]+1, coord[1]), (coord[0]-1, coord[1]), (coord[0], coord[1]+1), (coord[0], coord[1]-1)]
            notCoordList = {(coord[0]+1, coord[1]+1), (coord[0]-1, coord[1]-1), (coord[0]-1, coord[1]+1), (coord[0]+1, coord[1]-1)}
            self.availablePoints = list(set(self.availablePoints).difference(notCoordList))
            Points = list(set(coordList) & set(self.availablePoints))
            # len_availablePoints = len(Points)
            if len(Points) == 0:
                 coord = choice(self.availablePoints)
                 print("KILL")
            else:
                coord = choice(Points)
        else:
            coord = choice(self.availablePoints)

        print(coord)
        if (self.makeMove(coord) == True):
           self.chooseCellCoord(step=1, coord = coord)






"""new_player = Robot("Robot")
new_player.randomArrangement()


new_player.chooseCellCoord()
new_player.chooseCellCoord()
new_player.chooseCellCoord()
new_player.chooseCellCoord()

new_player.chooseCellCoord()
new_player.chooseCellCoord()
new_player.chooseCellCoord()
new_player.chooseCellCoord()

new_player.chooseCellCoord()
new_player.chooseCellCoord()
new_player.chooseCellCoord()
new_player.chooseCellCoord()

new_player.chooseCellCoord()
new_player.chooseCellCoord()
new_player.chooseCellCoord()
new_player.chooseCellCoord()

new_player.chooseCellCoord()
new_player.chooseCellCoord()
new_player.chooseCellCoord()
new_player.chooseCellCoord()

new_player.chooseCellCoord()
new_player.chooseCellCoord()
new_player.chooseCellCoord()
new_player.chooseCellCoord()

new_player.display()
print("Your score is: ", new_player.score)"""