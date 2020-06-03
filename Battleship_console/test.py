def chooseCellCoord(self):
    # """Метод обирання координат.
    # Може видати виключення, якщо дані не коректні."""

    coords = input("Введіть букву а-j та число від 0 до 9: ")
    return (self.checkCellCoords(coords[1], coords[0]))


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

        x = int(x)
        y = ord(y) - 97
        if self.game.currentEnemy.field.cellsList[x][
            y].isHit == True:  # перевіряємо чи не обирав користувач цю клітину раніше
            raise CellIsAlreadyHit((x, y))
    return (x, y)

s = "dfgfdgdf"
print(s[1:])