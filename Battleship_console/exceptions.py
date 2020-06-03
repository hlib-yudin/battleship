class WrongCoordinates(Exception):
    def __init__(self):
        self.message = "Немає клітинки з такими координатами!"

    def __str__(self):
        return self.message


class CellIsAlreadyHit(Exception):
    def __init__(self, coords):
        self.coords = coords

    def __str__(self):
        return "Ви вже обирали клітинку з координатами {}{}! ".format(chr(self.coords[1] + 97), self.coords[0])


class NotCoordinates(Exception):
    """Виключення, пов'язане з некоректним вводом даних."""

    def __str__(self):
        return "Ви ввели некоректні дані!"


class WrongNumberOfElements(Exception):
    """Виключення, пов'язане з вибором неправильної кількості елементів кораблів."""

    def __init__(self, numberOfElements):
        self.numberOfElements = numberOfElements

    def __str__(self):
        return "Занадто багато/мало елементів кораблів! ({}/20)".format(
            self.numberOfElements)


class TouchingShips(Exception):
    """Виключення, пов'язане з неправильним розміщенням кораблів:
    вони перетинаються чи дотикаються."""

    def __init__(self, coords):
        column = chr(coords[1] + 97)
        row = str(coords[0])
        self.coords = column + row

    def __str__(self):
        return "Кораблі перетинаються/дотикаються одне до одного! ({})".format(
            self.coords)


class TooLongShip(Exception):
    """Виключення, пов'язане з задовгим кораблем."""

    def __init__(self, coords):
        column = chr(coords[1] + 97)
        row = str(coords[0])
        self.coords = column + row

    def __str__(self):
        return "Занадто довгий корабель! ({})".format(self.coords)


class WrongNumberOfShips(Exception):
    """Виключення, пов'язане з некоректною кількістю кораблів."""

    def __init__(self, numberOfShips):
        self.numberOfShips = numberOfShips

    def __str__(self):
        return "Занадто багато/мало кораблів! ({}/10)".format(
            self.numberOfShips)


class WrongSetOfShips(Exception):
    """Виключення, пов'язане з неправильним набором кораблів
    (наприклад, 2 чотирипалубних)."""

    def __init__(self, shipLengthList):
        self.shipLengthDict = {
            1: shipLengthList.count(1),
            2: shipLengthList.count(2),
            3: shipLengthList.count(3),
            4: shipLengthList.count(4),
        }

    def __str__(self):
        return f'''Неправильний набір кораблів!
1-палубні: {self.shipLengthDict[1]}/4
2-палубні: {self.shipLengthDict[2]}/3
3-палубні: {self.shipLengthDict[3]}/2
4-палубні: {self.shipLengthDict[4]}/1'''
