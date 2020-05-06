from abc import ABC, abstractmethod
from random import randrange


class Cell:
  def  __init__(self, coord):
    self.__coord = coord
    self.__isHit = False
    self.__belongsTo = None
    self.__color = 'blue'

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

  @property
  def color(self):
      return self.__color

  #@color.setter
  def setcolor(self, color):
      self.__color = color

  def hitCell(self):
      if self.__isHit == False:
          self.__isHit = True


"------------------------------------------------"

class Ship:
  def __init__(self, size, elements):
    self.__size = size
    self.__hitCount = 0
    self.__elements = elements


  @property
  def getSize(self):
      return self.__size

  @property
  def getHitCount(self):
      return self.__hitCount

  @property
  def elements(self):
      return self.__elements




  def size(self, size):
      self.__size = size

  def increaseHitCount(self):
      self.__hitCount += 1

  def checkIfSunk(self):

      if self.__hitCount == self.__size:
          return True
      else :
          return False


"------------------------------------------------"

class Field:
  def __init__(self):
    self.__cellsList = [[Cell((i, j)) for j in range(10)] for i in range(10)]
    self.__shipsCount = 0 # к-сть непотоплених кораблів
    self.__shipsList = [0]*10


  @property
  def cellsList(self):
      return self.__cellsList

  @property
  def shipsCount(self):
      return self.__shipsCount

  @property
  def shipsList(self):
      return self.__shipsList

  @property
  def decreaseShipsCount(self):
      self.__shipsCount -= 1

  def setShipsList(self, ship):
      self.shipsList.append(ship)

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




##########################################################################
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

    @name.setter
    def name(self, name):
        """Сеттер для поля name."""
        self.__name = name

    @field.setter
    def field(self, field):
        """Сеттер для поля field."""
        self.__field = field

##########
    def coord_map(self, length, orientation):
        # генерация точки со случайными координатами
        ship_point = [randrange(10), randrange(10)]
        coords = []
        stroka = ship_point[0]
        stolb = ship_point[1]
        ship_correct = 1
        for i in range(length):

            # в зависимости от направления генерировать новые точки корабля
            # 0 - горизонт (увеличивать столбец), 1 - вертикаль (увеличивать строку)
            if stolb + i > 9 or stroka + i > 9:
                ship_correct = 0
            if orientation == 0:
                coords.append((stroka, (stolb + i)))
            else:
                coords.append(((stroka + i), stolb))
        if (ship_correct == 1):
            return coords
        else:
            return self.coord_map(length, orientation)


##########
    def around_ship(self, coords):

        around_coords = []
        for x, y in coords:
            adjcells = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1), (x + 1, y + 1), (x + 1, y - 1), (x - 1, y + 1),
                        (x - 1, y - 1)]
            for adjx, adjy in adjcells:
                if (adjx < 0 or adjx > 9 or adjy < 0 or adjy > 9):
                    continue
                else:
                    around_coords.append((adjx, adjy))
        # result = list(map(list, {tuple(x) for x in around_coords}))
        result = list(set(around_coords + coords))
        return result

##########
    def randomArrangement(self):
        # функция генерации кораблей на поле
        # количество сгенерированных кораблей
        count_ships = 0

        while count_ships < 10:
            # массив занятых кораблями точек
            fleet_array = []
            # обнулить количество кораблей
            count_ships = 0
            # массив с флотом
            fleet_ships = []
            # генерация кораблей (length - палубность корабля)
            for length in reversed(range(1, 5)):
                # генерация необходимого количества кораблей необходимой длины
                for i in range(5 - length):
                    # генерация точки со случайными координатами, пока туда не установится корабль
                    try_create_ship = 0
                    while 1:
                        try_create_ship += 1
                        # если количество попыток превысило 50, начать всё заново
                        if try_create_ship > 50:
                            break

                            # случайное расположение корабля (либо горизонтальное, либо вертикальное)
                        orientation = randrange(2)

                        # случайное расположение корабля
                        ship_coords = self.coord_map(length, orientation)
                        # если корабль может быть поставлен корректно и его точки не пересекаются с уже занятыми точками поля
                        # пересечение множества занятых точек поля и точек корабля:

                        intersect_array = list(set(fleet_array) & set(self.around_ship(ship_coords)))
                        if len(intersect_array) == 0:
                            # создать экземпляр класса Ship
                            new_ship = Ship(length, ship_coords)
                            # добавить в массив со всеми занятыми точками точки самого корабля
                            fleet_array += ship_coords
                            fleet_ships.append(new_ship)
                            count_ships += 1
                            break
        for ship in fleet_ships:
            self.field.setShipsList(ship)
            self.field.placeShip(ship)

        print(fleet_array)
##########

    def display(self):

        for cellList in self.field.cellsList:
            for cell in cellList:

                if not cell.belongsTo:
                    if cell.isHit:
                        print('*', end='  ')
                        cell.setcolor('grey')
                    else:
                        print('0', end='  ')
                else:
                    if cell.isHit:
                        print('X', end='  ')
                        cell.setcolor('red')
                    else:
                        print('%', end='  ')
            print()




class Player(AbsPlayer):
    def print_name(self):
        print(self.name)



new_player = Player("Dasha")
new_player.randomArrangement()
"""new_player.field.cellsList[0][1].hitCell()
new_player.field.cellsList[1][4].hitCell()
new_player.field.cellsList[2][0].hitCell()
new_player.field.cellsList[3][5].hitCell()
new_player.field.cellsList[0][1].hitCell()
new_player.field.cellsList[5][2].hitCell()
new_player.field.cellsList[2][1].hitCell()
new_player.field.cellsList[3][9].hitCell()"""
new_player.display()
