from display import *
from game import *

class Cell(IViewable):
    """Клас, що відповідає за одну клітинку на ігровому полі."""
    # прибрати колір???

    def __init__(self, coords, color='blue'):
        """Ініціалізатор класу."""
        self.__coords = coords # координати клітинки
        self.__isHit = False # чи влучили в клітинку, чи ні
        self.__belongsTo = None # якому кораблю належить клітинка (None, якщо жодному)
        self.__color = color # колір клітинки


    @property
    def coords(self):
        """Геттер для поля coords."""
        return self.__coords 

    @property
    def isHit(self):
        """Геттер для поля isHit."""
        return self.__isHit
    
    def hitCell(self):
        """Змінює статус клітинки на 'влучили'."""
        if self.__isHit == False:
            self.__isHit = True

    @property
    def belongsTo(self):
        """Геттер для поля belongsTo."""
        return self.__belongsTo

    @belongsTo.setter
    def belongsTo(self, belongsTo):
        """Сеттер для поля belongsTo."""
        self.__belongsTo = belongsTo

    @property
    def color(self):
        """Геттер для поля color."""
        return self.__color

    @color.setter
    def color(self, color):
        """Сеттер для поля color."""
        self.__color = color

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


class Ship():
    """"Клас, що відповідає за один корабель."""

    def __init__(self, size, elements):
        """Ініціалізатор класу."""
        self.__size = size # к-сть клітинок, які займає корабель
        self.__elements = elements # координати клітинок, з яких складається корабель
        self.__hitCount = 0 # к-сть елементів корабля, в які влучили

    @property
    def size(self):
        """Геттер для поля size."""
        return self.__size

    @size.setter
    def size(self, size):
        """Сеттер для поля size."""
        self.__size = size

    @property
    def elements(self):
        """Геттер для поля elements."""
        return self.__elements

    @property
    def hitCount(self):
        """Геттер для поля hitCount."""
        return self.__hitCount

    def increaseHitCount(self):
        """Збільшує к-сть влучень в корабель на 1."""
        self.__hitCount += 1

    def checkIfSunk(self):
        """Перевіряє, чи потоплений корабель."""
        if self.hitCount == self.size:
            return True
        return False


class Field(IViewable):
    """Клас, що відповідає за ігрове поле."""

    def __init__(self):
        """Ініціалізатор класу."""
        self.__cellsList = [[Cell((i, j)) for j in range(10)] for i in range(10)]
        self.__shipsCount = 0 # к-сть непотоплених кораблів
        self.__shipsList = []

    @property
    def cellsList(self):
        """Геттер для поля cellsList."""
        return self.__cellsList

    @property
    def shipsCount(self):
        """Геттер для поля shipsCount."""
        return self.__shipsCount

    def decreaseShipsCount(self):
        """Зменшує к-сть непотоплених кораблів на 1."""
        self.__shipsCount -= 1

    @property
    def shipsList(self):
        """Геттер для поля shipsList."""
        return self.__shipsList

    #@shipsList.setter
    #def shipsList(self, shipsList):
    #    """Сеттер для поля shipsList."""
    #    self.__shipsList = shipsList

    def sinkShip(self, ship):
        """Змінює в усіх клітинках, що межують з кораблем, поле isHit на True.
        При цьому вважається, що всі елементи корабля вже потоплені."""
        shipElements = ship.elements

        # проходимо по всіх клітинках корабля
        for x, y in shipElements:
            # шукаємо сусідні клітинки до кожного елемента корабля
            adjCells = ((x-1, y), (x+1, y), (x, y-1), (x, y+1),
                        (x-1, y-1), (x-1, y+1), (x+1, y-1), (x+1, y+1))
            
            # проходимо по всіх сусідніх клітинках
            for adjx, adjy in adjCells:

                # якщо клітинка виходить за межі поля -- пропускаємо
                if adjx < 0 or adjx > 9 or adjy < 0 or adjy > 9:
                    continue
                self.cellsList[adjx][adjy].hitCell()


    def placeShip(self, ship):
        """Розміщує корабель на ігровому полі, змінює атрибут belongsTo
        клітинок, які тепер належать кораблю, додає корабель до списку кораблів
        shipsList."""
        cells = ship.elements
        for x, y in cells:
            self.cellsList[x][y].belongsTo = ship
        self.shipsList.append(ship)


    def getRenderInfo(self):
        """Повертає інформацію для графічного відображення."""
        return [[self.cellsList[x][y].getRenderInfo() for y in range(10)] 
            for x in range(10)]


    # def display(self):
    #     """ТИМЧАСОВА ФУНКЦІЯ
    #     Відображає ігрове поле на екрані."""
    #     for cellList in self.cellsList:
    #         for cell in cellList:

    #             if not cell.belongsTo:
    #                 if cell.isHit:
    #                     print('*', end=' ')
    #                 else:
    #                     print('0', end=' ')
    #             else:
    #                 if cell.isHit:
    #                     print('X', end = ' ')
    #                 else:
    #                     print('S', end=' ')
    #         print()

    

f = Field()
ship1 = Ship(3, ((0,0), (0,1), (0,2)))
ship2 = Ship(2, ((2, 2), (2,3)))
f.placeShip(ship1)
f.placeShip(ship2)
f.cellsList[0][0].hitCell()
ship1.increaseHitCount()
f.cellsList[0][1].hitCell()
ship1.increaseHitCount()
f.cellsList[0][2].hitCell()
ship1.increaseHitCount()
f.sinkShip(ship1)
f.cellsList[2][3].hitCell()

# замість Field.getRenderInfo буде Game.getRenderInfo
renderInfo = f.getRenderInfo()
console = Console()
console.render(field = dict(
        playerName='Player 1',
        cellsInfo=renderInfo
    ), fieldEnemy = dict(
        playerName='Player 1',
        cellsInfo=renderInfo
))
# f.display()

"""game = Game()
game.players = [1, 2]
game.currentPlayer = game.players[0]
game.swapPlayer()"""
