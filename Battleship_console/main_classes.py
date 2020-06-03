
from display import *
from exceptions import *


class Cell(IViewable):
    def __init__(self, coord):
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
        else:
            return False


"------------------------------------------------"


class Field(IViewable):
    def __init__(self):
        self.__cellsList = [[Cell((i, j)) for j in range(10)] for i in range(10)]
        self.__shipsCount = 0  # к-сть непотоплених кораблів
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

    def placeShip(self, ship):
        self.setShipsList(ship)
        self.__shipsCount += 1
        shipElements = ship.elements
        for x, y in shipElements:
            self.cellsList[x][y].belongsTo = ship

    def sinkShip(self, ship):
        shipElements = ship.elements
        for x, y in shipElements:
            adjcells = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1), (x + 1, y + 1), (x + 1, y - 1), (x - 1, y + 1),
                        (x - 1, y - 1)]
            for adjx, adjy in adjcells:
                if (adjx < 0 or adjx > 9 or adjy < 0 or adjy > 9):
                    continue
                else:
                    self.cellsList[adjx][adjy].hitCell()

    def getRenderInfo(self):
        """Повертає інформацію для графічного відображення."""
        return [[self.cellsList[x][y].getRenderInfo() for y in range(10)]
                for x in range(10)]


##########################################################################
