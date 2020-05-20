from colorama import init, Fore, Back, Style
from os import system
# ініціалізація модуля colorama
init(autoreset=True)


# IViewable -- інтерфейс для збору інформації від об'єктів, що
# відображатимуться на екрані
class IViewable():

    def getRenderInfo(self):
        pass


# IRender -- інтерфейс для відображення об'єктів на екран
class IRender():

    def renderWhileArrangingShips(self, field, playerName, message):
        pass

    def render(self, message=None, field=None, fieldEnemy=None):
        pass

# Graphic -- клас для відображення об'єктів графічним інтерфейсом
class Graphic(IRender):

    def renderWhileArrangingShips(self, field, playerName, message):
        pass

    def render(self, message=None, field=None, fieldEnemy=None):
        pass


# Console -- клас для відображення об'єктів консольним інтерфейсом
class Console(IRender):

    def renderWhileArrangingShips(self, field, playerName, message=None):
        """Відображає поле поточного гравця під час розстановки кораблів.
        field -- інформація про поле поточного гравця
        field: list[10][10]: True / False
        """

        self.clear()
        print('Розстановка кораблів\n')
        print('{:41s}'.format(playerName))
        print('    a   b   c   d   e   f   g   h   i   j  ')
        print('  ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐')
        for i in range(10): # для всіх рядків
            # відображаємо поле поточного гравця
            print('{} │'.format(i), end='')
            
            for j in range(10):# для всіх клітинок в одному рядку
                print(' ', end='')

                belongsTo = field[i][j]

                if not belongsTo:
                    print(Back.BLUE + ' ',end='')
                else:
                    print(Back.YELLOW + ' ', end='')
                
                print(' │', end='')
                if j == 9: print()

            if i != 9:
                print('  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤')
            else:
                print('  └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘')

        if message:
            print(message)




#########################################################################
    def render(self, message=None, field=None, fieldEnemy=None):
        """Відображає гру на екран.
        field -- інформація про поле поточного гравця
        field: {
            playerName: str,
            cellsInfo: list[10][10] {
                                        isHitStatus = True / False,
                                        shipStatus = 'not belongs' / 'sunk' / 'not sunk'
                                    }
        }
        fieldEnemy -- аналогічна інформація про поле гравця, який зараз не ходить
        """
        # ┌└├┤┐─│┘┬ ┴ ┼
        # ┌───┐
        # │ Х │
        # ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤

        # очистимо консоль, налаштуємо її розмір
        self.clear()
        
        if field and fieldEnemy:
            # якщо передали ці аргументи -- відображаємо ігрові поля
            print('{:41s}{:20s}{:41s}'.format(field['playerName'], '',
                fieldEnemy['playerName']))
            print('    a   b   c   d   e   f   g   h   i   j  ' + ' ' * 20 +
                  '    a   b   c   d   e   f   g   h   i   j  ')
            print('  ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐' + ' ' * 20 +
                  '  ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐')

            for i in range(10): # для всіх рядків
                # спочатку відображаємо поле поточного гравця
                print('{} │'.format(i), end='')
                
                for j in range(10):# для всіх клітинок в одному рядку
                    print(' ', end='')

                    cellInfo = field['cellsInfo'][i][j]
                    isHitStatus = cellInfo['isHitStatus']
                    shipStatus = cellInfo['shipStatus']

                    if isHitStatus == True and shipStatus == 'not belongs':
                        print(Style.BRIGHT + Fore.WHITE + Back.BLUE + '•', end='')
                    elif isHitStatus == False and shipStatus == 'not belongs':
                        print(Back.BLUE + ' ',end='')
                    elif isHitStatus == True and shipStatus == 'sunk':
                        print(Fore.BLACK + Back.WHITE + 'X', end='')
                    elif isHitStatus == True and shipStatus == 'not sunk':
                        print(Fore.BLACK + Back.RED + 'X', end='')
                    elif isHitStatus == False and shipStatus == 'not sunk':
                        print(Back.YELLOW + ' ', end='')
                    
                    print(' │', end='')
                    

                # тепер переходимо до поля суперника
                # гравець бачить тільки ті клітинки суперника, в які він влучив
                # (але тільки якщо showall == False)
                print(' ' * 20 + '{} │'.format(i), end='')

                for j in range(10):# для всіх клітинок в одному рядку
                    print(' ', end='')

                    cellInfo = fieldEnemy['cellsInfo'][i][j]
                    isHitStatus = cellInfo['isHitStatus']
                    shipStatus = cellInfo['shipStatus']
                    
                    if not isHitStatus:
                        print(Back.BLUE + ' ', end='')
                    elif shipStatus == 'not belongs':
                        print(Style.BRIGHT + Fore.WHITE + Back.BLUE + '•', end='')
                    elif shipStatus == 'sunk':
                        print(Fore.BLACK + Back.WHITE + 'X', end='')
                    elif shipStatus == 'not sunk':
                        print(Fore.BLACK + Back.RED + 'X', end='')
                    
                    # якщо показуємо все поле ворога
                    # else:
                    #     if isHitStatus == True and shipStatus == 'not belongs':
                    #         print(Style.BRIGHT + Fore.WHITE + Back.BLUE + '•', end='')
                    #     elif isHitStatus == False and shipStatus == 'not belongs':
                    #         print(Back.BLUE + ' ',end='')
                    #     elif isHitStatus == True and shipStatus == 'sunk':
                    #         print(Fore.BLACK + Back.WHITE + 'X', end='')
                    #     elif isHitStatus == True and shipStatus == 'not sunk':
                    #         print(Fore.BLACK + Back.RED + 'X', end='')
                    #     elif isHitStatus == False and shipStatus == 'not sunk':
                    #         print(Back.YELLOW + ' ', end='')
                    
                    print(' │', end='')

                    if j == 9: print()
                    

                if i != 9:
                    print('  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤' + ' ' * 20 +
                          '  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤')
                else:
                    print('  └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘' + ' ' * 20 +
                          '  └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘')

        if message:
            print(message)



    def printShipsDecoration(self):
        print(r"""
              |    |    |                       
             )_)  )_)  )_)                    
            )___))___))___)\                 
           )____)____)_____)\                             |>
         _____|____|____|____\__                     |    |    |                            
---------\                   /---------             )_)  )_)  )_)                    
  ^^^^^ ^^^^^^^^^^^^^^^^^^^^^                      )___))___))___)\\
    ^^^^      ^^^^     ^^^    ^^                  )____)____)_____)\\
         ^^^^      ^^^                          _____|____|____|____\\__    
                                       ---------\                   /---------
                                         ^^^^^ ^^^^^^^^^^^^^^^^^^^^^
              |    |    |                   ^^^^      ^^^^     ^^^    ^^                    
             )_)  )_)  )_)                       ^^^^      ^^^
            )___))___))___)\                 
           )____)____)_____)\\               
         _____|____|____|____\\\__
---------\                   /---------
  ^^^^^ ^^^^^^^^^^^^^^^^^^^^^
    ^^^^      ^^^^     ^^^    ^^                  
         ^^^^      ^^^

""")

    def mainMenu(self):
        """Виводить головне меню на екран.
        Повертає 0 для виходу з гри, 1 для гри з роботом, 2 для гри з гравцем."""

        correctOption = False
        # поки не ввели коректне значення
        while not correctOption:

            self.clear()
            self.printShipsDecoration()
            # ┌└├┤┐─│┘┬ ┴ ┼
            print('''
┌──────────────┐
│ Морський бій │
└──────────────┘

1 -- почати гру з роботом
2 -- почати гру з іншим гравцем
0 -- вийти з гри

Ваш вибір: ''', end='')
            option = input()
            if option in ('0', '1', '2'):
                return int(option)
        

    def clear(self):
        """Очищує консоль, налаштовує її розмір."""
        system('cls')
        system('mode con: cols=113 lines=34')