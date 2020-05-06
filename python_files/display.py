from colorama import init, Fore, Back, Style
from os import system
# ініціалізація модуля colorama
init(autoreset=True)


def clear():
    """Очищує консоль."""
    system('cls')


# IViewable -- інтерфейс для збору інформації від об'єктів, що
# відображатимуться на екрані
class IViewable():

    def getRenderInfo(self):
        pass


# IRender -- інтерфейс для відображення об'єктів на екран
class IRender():

    def render(self):
        pass


# Graphic -- клас для відображення об'єктів графічним інтерфейсом
class Graphic(IRender):

    def render(self):
        pass


# Console -- клас для відображення об'єктів консольним інтерфейсом
class Console(IRender):

    def render(self, message=None, field=None, fieldEnemy=None, showall=False):
        """Відображає гру на екран.
        field -- інформація про поле поточного гравця
        field: {
            playerName: str,
            cellsInfo: list[10][10]
        }
        fieldEnemy -- аналогічна інформація про поле гравця, який зараз не ходить
        showall -- показує, чи показувати поле ворога повністю, чи приховувати
        """
        # TO DO
        # ┌└├┤┐─│┘┬ ┴ ┼
        # ┌───┐
        # │ Х │
        # ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤

        # очистимо консоль
        clear()
        
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

                    # якщо приховуємо інформацію
                    if not showall:
                        if not isHitStatus:
                            print(Back.BLUE + ' ', end='')
                        elif shipStatus == 'not belongs':
                            print(Style.BRIGHT + Fore.WHITE + Back.BLUE + '•', end='')
                        elif shipStatus == 'sunk':
                            print(Fore.BLACK + Back.WHITE + 'X', end='')
                        elif shipStatus == 'not sunk':
                            print(Fore.BLACK + Back.RED + 'X', end='')
                    
                    # якщо показуємо все поле
                    else:
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

                    if j == 9: print()
                    

                if i != 9:
                    print('  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤' + ' ' * 20 +
                          '  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤')
                else:
                    print('  └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘' + ' ' * 20 +
                          '  └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘')

        if message:
            print(message)