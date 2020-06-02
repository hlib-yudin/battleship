from colorama import init, Fore, Back, Style
from os import system
from tkinter import *
import tkinter.messagebox as messagebox
# ініціалізація модуля colorama
init(autoreset=True)


# IViewable -- інтерфейс для збору інформації від об'єктів, що
# відображатимуться на екрані
class IViewable():

    def getRenderInfo(self):
        """Збирає інформацію для виведення на екран."""
        pass


# IRender -- інтерфейс для відображення об'єктів на екран
class IRender():
    # TO DELETE
    def renderWhileArrangingShips(self, field, playerName):
        """Рендерить екран розстановки кораблів."""
        pass

    def render(self, field, fieldEnemy, showall=False):
        """Рендерить ігрові поля гравців."""
        pass

    def renderScreenEnterName(self, numOfPlayers):
        """Рендерить екран вводу імені гравців."""
        pass

    def renderScreenPrepareForTurn(self, playerName):
        """Рендерить екран передачі ходу іншому гравцю."""
        pass

    def printText(self, message):
        """Виводить текст на екран."""
        pass

    def inputCoords(self):
        """Чекає, коли гравець введе координати клітинки, повертає їх."""
        pass

    def inputEnter(self):
        """Чекає, коли гравець натисне Enter."""
        pass

    def printError(self, e):
        """Виводить повідомлення про помилку на екран."""
        pass

    def mainMenu(self):
        """Рендерить головне меню."""
        pass


# Graphic -- клас для відображення об'єктів графічним інтерфейсом
class Graphic(IRender):

    def __init__(self):
        """Створює графічне вікно, в якому буде вимальовуватись гра."""
        self.root = Tk()
        self.root.title = "Морский бій"
        self.root.geometry("800x470+100+100")
        self.backgroundImg = PhotoImage(file='../other_files/rsz_background.gif')

        # прапорець, що показує, чи натиснули на якусь кнопку
        self.clicked = False
        # атрибут для даних, отриманих від гравця
        self.enteredData = None

        #ширина рабочего поля
        self.width = 800
        #высота рабочего поля
        self.height = 400
        #self.messageFrameHeight = 50
        #self.buttonFrameHeight = 50
        #цвет фона холста
        self.bg = "white"
        #отступ между ячейками
        self.indent = 2
        #размер одной из сторон квадратной ячейки
        self.gauge = 32
        #смещение по y (отступ сверху)
        self.offset_y = 40
        #смещение по x пользовательского поля
        self.offset_x_user = 30
        #смещение по x поля компьютера
        self.offset_x_comp = 430

        #ініціалізація контейнерів для віджетів
        self.frame = Frame(self.root)
        self.frame.pack()
        self.messageFrame = Frame(self.frame)
        #self.messageFrame['height'] = self.messageFrameHeight
        self.messageFrame.pack()
        self.buttonsFrame = Frame(self.frame)
        self.buttonsFrame.pack()
        #self.menuFrame = Frame(self.root)
        
        # ініціалізація поля для малювання
        self.canv = Canvas(self.root)
        self.canv["height"] = self.height
        self.canv["width"] = self.width
        self.canv["bg"] = self.bg
        self.canv.pack()


    def printError(self, e):
        """Виводить повідомлення про помилку на екран."""
        messagebox.showerror("Ой!", e)


    def printText(self, text):
        """Виводить текст на екран."""
        # видаляємо контейнер зі старим текстом
        self.messageFrame.destroy()
        # і створюємо контейнер для нового
        self.messageFrame = Frame(self.frame)
        self.messageFrame.pack(side = BOTTOM)
        message = Label(self.messageFrame, text=text)
        message.pack(side = LEFT)
        # рендеринг
        self.root.update_idletasks()
        self.root.update()
        
    
    def clickOnCellHandler(self, event):
        """Повертає координати натиснутої клітинки.
        Спрацьовує, коли натиснули на клітинку."""
        letters = 'abcdefghij'
        
        for i in range(10):
            for j in range(10):
                # обчислюємо координату верхнього лівого кута кожної клітинки 
                xn = j*self.gauge + (j+1)*self.indent + self.offset_x_comp
                yn = i*self.gauge + (i+1)*self.indent + self.offset_y
                xk = xn + self.gauge
                yk = yn + self.gauge
                # з'ясовуємо, на яку саме клітинку клікнув користувач
                if event.x >= xn and event.x <= xk and event.y >= yn and event.y <= yk:
                    letter = letters[j]
                    self.clicked = True
                    self.enteredData = letter + str(i)

                # якщо умова вище не виконалась, це означає, що гра в режимі розстановки
                # тоді координата xn буде іншою
                xn = j*self.gauge + (j+1)*self.indent + self.offset_x_user
                xk = xn + self.gauge
                # з'ясовуємо, на яку саме клітинку клікнув користувач
                if event.x >= xn and event.x <= xk and event.y >= yn and event.y <= yk:
                    letter = letters[j]
                    self.clicked = True
                    self.enteredData = letter + str(i)

        
    def randomButtonHandler(self):
        """Обробник події натискання кнопки випадкової розстановки кораблів."""
        self.clicked = True
        self.enteredData = 'r'
        self.buttonsFrame.destroy()


    def enterButtonHandler(self):
        """Обробник події натискання кнопки закінчення розстановки кораблів."""
        self.clicked = True
        self.enteredData = ''
        self.buttonsFrame.destroy()


    def inputCoords(self):
        """У циклі чекає, коли користувач натисне на клітинку, повертає її координати."""
        self.clicked = False
        self.enteredData = None
        # коли користувач натисне на клітинку, спрацює clickOnCellHandler,
        # який змінить змінну self.clicked на False -- це забезпечить вихід із циклу
        while not self.clicked:
            self.root.update_idletasks()
            self.root.update()
        return self.enteredData


    def inputEnterHandler(self):
        """Обробник події натискання кнопки Enter."""
        self.clicked = True


    def inputEnter(self):
        """Чекає, поки гравець не натисне кнопку Enter на екрані."""
        enterButton = Button(self.messageFrame, text='Enter', command=self.inputEnterHandler, bd=1)
        enterButton.pack(side = RIGHT)
        
        self.clicked = False
        while not self.clicked:
            self.root.update_idletasks()
            self.root.update()
        enterButton.destroy()


    def renderScreenEnterName(self, numOfPlayers):
        """Відображає екран для вводу імен гравців.
        Повертає імена цих гравців (або гравця, якщо він один)."""
        self.canv.delete('all')
        self.setBackground()

        # контейнер для полів вводу і кнопок
        entryFrame = Frame(self.frame)
        entryFrame.pack()
        entries = Frame(entryFrame)
        entries.pack(side = LEFT)
        
        if numOfPlayers == 2:
            playerName1, playerName2 = '', ''
            row1 = Frame(entries)
            row1.pack()
            label1 = Label(row1, text="Введіть ім'я першого гравця: ")
            entry1 = Entry(row1, width = 30)
            label1.pack(side = LEFT)
            entry1.pack(side = RIGHT)

            row2 = Frame(entries)
            row2.pack()
            label2 = Label(row2, text="Введіть ім'я другого гравця:   ")
            entry2 = Entry(row2, width = 30)
            label2.pack(side = LEFT)
            entry2.pack(side = RIGHT)

            def getNames():
                """Записує у змінні playerName значення з полів вводу."""
                nonlocal playerName1, playerName2, notEntered
                playerName1 = entry1.get()
                playerName2 = entry2.get()
                notEntered = False
                #print(playerName1, playerName2, notEntered)

            # кнопка для вводу
            enterButton = Button(entryFrame, text="Ввести", command= getNames )
            enterButton.pack(side = RIGHT)

            notEntered = True
            while notEntered:
                self.root.update_idletasks()
                self.root.update()
            entryFrame.destroy()
            return playerName1, playerName2

        elif numOfPlayers == 1:
            playerName = ''
            row = Frame(entries)
            row.pack()
            label = Label(row, text="Введіть ваше ім'я: ")
            entry = Entry(row, width = 30)
            label.pack(side = LEFT)
            entry.pack(side = RIGHT)

            def getName():
                nonlocal playerName, notEntered
                playerName = entry.get()
                notEntered = False

            enterButton = Button(entryFrame, text="Ввести", command= getName )
            enterButton.pack(side = RIGHT)

            notEntered = True
            while notEntered:
                self.root.update_idletasks()
                self.root.update()
            entryFrame.destroy()
            return playerName


    def renderScreenPrepareForTurn(self, playerName):
        """Рендерить екран передачі ходу іншому гравцю."""
        self.canv.delete('all')
        self.setBackground()
        self.printText(f"Гравець {playerName}, приготуйтесь! Натисніть Enter, щоб продовжити.")
        self.inputEnter()

    
    def renderWhileArrangingShips(self, field, playerName):
        """Відображає поле поточного гравця під час розстановки кораблів.
        field -- інформація про поле поточного гравця
        field: list[10][10]: True / False
        """
        self.canv.delete('all')
        #создание поля для пользователя
        #перебор строк
        for i in range(10):
            #перебор столбцов
            for j in range(10):
                xn = j*self.gauge + (j+1)*self.indent + self.offset_x_user
                xk = xn + self.gauge
                yn = i*self.gauge + (i+1)*self.indent + self.offset_y
                yk = yn + self.gauge
                #добавление прямоугольника на холст с тегом в формате:
                #префикс_строка_столбец
                cell = self.canv.create_rectangle(xn,yn,xk,yk,tag = "my_"+str(i)+"_"+str(j), fill='blue')
                self.canv.tag_bind(cell, "<Button-1>", self.clickOnCellHandler)
                # якщо там корабель -- фарбуємо в жовтий
                if field[i][j]:
                    self.canv.itemconfig("my_"+str(i)+"_"+str(j), fill="yellow")

        #добавление букв и цифр
        for i in reversed(range(10)):
            #цифры пользователя
            xc = self.offset_x_user - 15
            yc = i*self.gauge + (i+1)*self.indent + self.offset_y + round(self.gauge/2)
            self.canv.create_text(xc,yc,text=str(i))
        #буквы
        symbols = "abcdefghij"
        for i in range(10):
            #буквы пользователя
            xc = i*self.gauge + (i+1)*self.indent + self.offset_x_user + round(self.gauge/2)
            yc = self.offset_y - 15
            self.canv.create_text(xc,yc,text=symbols[i])
                
        # кнопки вводу і рандому
        self.buttonsFrame.destroy()
        self.buttonsFrame = Frame(self.frame)
        self.buttonsFrame.pack()
        randomButton = Button(self.buttonsFrame, text='Random', command = self.randomButtonHandler)
        randomButton.pack(side = LEFT)
        enterButton = Button(self.buttonsFrame, text='Завершити розстановку', command = self.enterButtonHandler)
        enterButton.pack(side = RIGHT)

        # відображаємо все це на екран
        self.printText(f"{playerName}, розставте кораблі!")


    def paintMiss(self, xn, yn):
        """Малює крапку на клітинці."""
        self.canv.create_oval(xn+(self.gauge/2-3), yn+(self.gauge/2-3), 
            xn+(self.gauge/2+3), yn+(self.gauge/2+3), fill="white")


    def paintCross(self,xn,yn):
        """Малює хрестик на клітинці."""
        xk = xn + self.gauge
        yk = yn + self.gauge
        self.canv.create_line(xn+2,yn+2,xk-2,yk-2,width="3", fill='black')
        self.canv.create_line(xk-2,yn+2,xn+2,yk-2,width="3", fill='black')


    def paintCell(self, i, j, player, cellInfo, showall=False):
        """Розфарбовує вказану клітинку."""
        isHitStatus = cellInfo['isHitStatus']
        shipStatus = cellInfo['shipStatus']

        if player == "currPlayer":
            tag = f"my_{i}_{j}"
            # координати клітинки
            xn = j*self.gauge + (j+1)*self.indent + self.offset_x_user
            yn = i*self.gauge + (i+1)*self.indent + self.offset_y

            if isHitStatus == True and shipStatus == 'not belongs':
                #print(Style.BRIGHT + Fore.WHITE + Back.BLUE + '•', end='')
                self.canv.itemconfig(tag, fill="blue")
                self.paintMiss(xn, yn)
            elif isHitStatus == False and shipStatus == 'not belongs':
                #print(Back.BLUE + ' ',end='')
                self.canv.itemconfig(tag, fill="blue")
            elif isHitStatus == True and shipStatus == 'sunk':
                #print(Fore.BLACK + Back.WHITE + 'X', end='')
                self.canv.itemconfig(tag, fill="white")
                self.paintCross(xn, yn)
            elif isHitStatus == True and shipStatus == 'not sunk':
                #print(Fore.BLACK + Back.RED + 'X', end='')
                self.canv.itemconfig(tag, fill="red")
                self.paintCross(xn, yn)
            elif isHitStatus == False and shipStatus == 'not sunk':
                #print(Back.YELLOW + ' ', end='')
                self.canv.itemconfig(tag, fill="yellow")

        elif player == "currEnemy":
            tag = f"nmy_{i}_{j}"
            # координати клітинки
            xn = j*self.gauge + (j+1)*self.indent + self.offset_x_comp
            yn = i*self.gauge + (i+1)*self.indent + self.offset_y

            if not showall:
                if not isHitStatus:
                    self.canv.itemconfig(tag, fill='blue')
                elif shipStatus == 'not belongs':
                    self.canv.itemconfig(tag, fill='blue')
                    self.paintMiss(xn, yn)
                elif shipStatus == 'sunk':
                    self.canv.itemconfig(tag, fill='white')
                    self.paintCross(xn, yn)
                elif shipStatus == 'not sunk':
                    self.canv.itemconfig(tag, fill='red')
                    self.paintCross(xn, yn)
                
            else:
                if isHitStatus == True and shipStatus == 'not belongs':
                    self.canv.itemconfig(tag, fill="blue")
                    self.paintMiss(xn, yn)
                elif isHitStatus == False and shipStatus == 'not belongs':
                    self.canv.itemconfig(tag, fill="blue")
                elif isHitStatus == True and shipStatus == 'sunk':
                    self.canv.itemconfig(tag, fill="white")
                    self.paintCross(xn, yn)
                elif isHitStatus == True and shipStatus == 'not sunk':
                    self.canv.itemconfig(tag, fill="red")
                    self.paintCross(xn, yn)
                elif isHitStatus == False and shipStatus == 'not sunk':
                    self.canv.itemconfig(tag, fill="yellow")


    def render(self, field, fieldEnemy, showall=False):
        """Рендерить ігрові поля гравця і суперника."""
        self.canv.delete('all')
        
        #создание поля для пользователя
        #перебор строк
        for i in range(10):
            #перебор столбцов
            for j in range(10):
                xn = j*self.gauge + (j+1)*self.indent + self.offset_x_user
                xk = xn + self.gauge
                yn = i*self.gauge + (i+1)*self.indent + self.offset_y
                yk = yn + self.gauge
                #добавление прямоугольника на холст с тегом в формате:
                #префикс_строка_столбец
                self.canv.create_rectangle(xn,yn,xk,yk,tag = "my_"+str(i)+"_"+str(j))
                # розфарбовування залежно від того, чи є корабель, чи влучали в клітинку...
                self.paintCell(i, j, "currPlayer", field["cellsInfo"][i][j])

        #создание поля для компьютера
        #перебор строк
        for i in range(10):
            #перебор столбцов
            for j in range(10):
                xn = j*self.gauge + (j+1)*self.indent + self.offset_x_comp
                xk = xn + self.gauge
                yn = i*self.gauge + (i+1)*self.indent + self.offset_y
                yk = yn + self.gauge
                #добавление прямоугольника на холст с тегом в формате:
                #префикс_строка_столбец
                tag = "nmy_"+str(i)+"_"+str(j)
                cell = self.canv.create_rectangle(xn,yn,xk,yk,tag = tag)
                # розфарбовування залежно від того, чи є корабель, чи влучали в клітинку...
                self.paintCell(i, j, "currEnemy", fieldEnemy["cellsInfo"][i][j], showall)
                #клік по клітинці викликає функцію inputCoords
                self.canv.tag_bind(cell, "<Button-1>", self.clickOnCellHandler)              

        #добавление букв и цифр
        for i in reversed(range(10)):
            #цифры пользователя
            xc = self.offset_x_user - 15
            yc = i*self.gauge + (i+1)*self.indent + self.offset_y + round(self.gauge/2)
            self.canv.create_text(xc,yc,text=str(i))
            #цифры компьютера
            xc = self.offset_x_comp - 15
            yc = i*self.gauge + (i+1)*self.indent + self.offset_y + round(self.gauge/2)
            self.canv.create_text(xc,yc,text=str(i))
        #буквы
        symbols = "abcdefghij"
        for i in range(10):
            #буквы пользователя
            xc = i*self.gauge + (i+1)*self.indent + self.offset_x_user + round(self.gauge/2)
            yc = self.offset_y - 15
            self.canv.create_text(xc,yc,text=symbols[i])

            #буквы компьютера
            xc = i*self.gauge + (i+1)*self.indent + self.offset_x_comp + round(self.gauge/2)
            yc = self.offset_y - 15
            self.canv.create_text(xc,yc,text=symbols[i])

        
        # відображаємо
        self.root.update_idletasks()
        self.root.update()


    def setBackground(self):
        """Встановлює зображення на задньому плані."""
        self.canv.create_image(0, 0, image=self.backgroundImg, anchor=NW)


    def singlePlayButtonHandler(self):
        """Обробник події натискання кнопки 'Почати гру з роботом'."""
        self.clicked = True
        self.enteredData = '1'
        self.buttonsFrame.destroy()


    def multiPlayButtonHandler(self):
        """Обробник події натискання кнопки 'Почати гру з гравцем'."""
        self.clicked = True
        self.enteredData = '2'
        self.buttonsFrame.destroy()


    def mainMenu(self):
        """Виводить на екран головне меню, повертає вибір користувача.
        1 -- почати гру з роботом
        2 -- почати гру з гравцем
        0 -- вийти з гри"""
        self.canv.delete('all')
        self.setBackground()
        self.printText('Вітаємо в Battleship!')
        self.buttonsFrame = Frame(self.frame)
        self.buttonsFrame.pack(side=BOTTOM)
        newSinglePlayButton = Button(self.buttonsFrame, text='Нова гра з роботом', command = self.singlePlayButtonHandler)
        newSinglePlayButton.pack(side=LEFT)
        newMultiPlayButton = Button(self.buttonsFrame, text='Нова гра з гравцем', command = self.multiPlayButtonHandler)
        newMultiPlayButton.pack(side=RIGHT)

        # чекаємо, коли гравець натисне на якусь кнопку
        self.clicked = False
        while not self.clicked:
            self.root.update_idletasks()
            self.root.update()
        self.messageFrame.destroy()
        return self.enteredData


# Console -- клас для відображення об'єктів консольним інтерфейсом
class Console(IRender):

    def __init__(self):
        self.clear()


    def printError(self, e):
        print('\n' + str(e))
        input()


    def printText(self, message):
        print(message)


    def inputCoords(self):
        print("a3 -- обрати клітинку а3")
        return(input("Ваш вибір: "))
        

    def inputEnter(self):
        input()


    def renderScreenEnterName(self, numOfPlayers):
        """Рендерить екран вводу імені."""
        self.clear()
        self.printShipsDecoration()
        if numOfPlayers == 2:
            playerName1 = input("Введіть ім'я першого гравця: ")
            playerName2 = input("Введіть ім'я другого гравця: ")
            return playerName1, playerName2
        elif numOfPlayers == 1:
            playerName = input("Введіть ваше ім'я: ")
            return playerName


    def renderScreenPrepareForTurn(self, playerName):
        """Рендерить екран передачі ходу іншому гравцеві."""
        self.clear()
        self.printShipsDecoration()
        print(f"Гравець {playerName}, приготуйтеся!")
        print("Натисніть Enter, щоб продовжити: ", end = '')
        input()


    def renderWhileArrangingShips(self, field, playerName):
        """Відображає поле поточного гравця під час розстановки кораблів.
        field -- інформація про поле поточного гравця
        field: list[10][10]: True / False
        """

        self.clear()
        print(f"{playerName}, розставте кораблі!\n")
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

        print('''
r -- випадкова розстановка
Порожній рядок -- закінчити розстановку\n''')


    def render(self, field, fieldEnemy, showall=False):
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
                    
                    if not showall:
                        if not isHitStatus:
                            print(Back.BLUE + ' ', end='')
                        elif shipStatus == 'not belongs':
                            print(Style.BRIGHT + Fore.WHITE + Back.BLUE + '•', end='')
                        elif shipStatus == 'sunk':
                            print(Fore.BLACK + Back.WHITE + 'X', end='')
                        elif shipStatus == 'not sunk':
                            print(Fore.BLACK + Back.RED + 'X', end='')
                    
                    # якщо показуємо все поле ворога
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
                return option
        

    def clear(self):
        """Очищує консоль, налаштовує її розмір."""
        system('cls')
        system('mode con: cols=113 lines=34')