from tkinter import *
from random import *
import random

class case:
    def __init__(self, value, x, y, row, col, mainBlock, isShow = False):
        self.value = value
        self.coordonate = (row, col, mainBlock)
        self.isShow = isShow
        self.x = x + 49
        self.y = y + 49
        self.placeholder = StringVar()
        self.placeholder.set(self.value)
    def createCase(self):
        self.input = Entry(window, justify='center', state='normal', font=("Purisa", 30))
        self.canvas = canvas.create_window(self.x, self.y, window = self.input, height=99, width=99 )
        blocks[self.coordonate] = self
    def showPlaceholder(self):
        self.input['textvariable'] = self.placeholder
        self.input['state'] = 'disabled'
        self.isShow = True
    def deleteCase(self):
        canvas.delete(self.canvas)
    def correction(self):
        if self.input.get():
            if self.value == int(self.input.get()):
                self.input['fg'] = 'green'
            if self.value != int(self.input.get()):
                self.input['fg'] = 'red'
        else:
            pass

class buttonDifficulty:
    def __init__(self, window, value, text):
        self.value = value
        self.text = text
        self.window = window
    def createButton(self):
        if difficultyLevel == self.value:
            self.button = Button(self.window, text=self.text, bg='red')
        else:
            self.button = Button(self.window, text=self.text, activebackground=None)
        self.button['command'] = lambda:createSudoko(self.value)
        self.button.pack()
    def deleteButton(self):
        print('deltedbutton')
        self.button.destroy()

def createBigblock():
    x = 0
    y = 0
    i = 0
    while i < 9:
        i = i + 1
        canvas.tag_raise(canvas.create_rectangle(x, y, x+300, y+300, width=6))
        x = x + 300
        if i%3 == 0:
            x = 0
            y = y + 300

def pickNumber(row, col, mainBlock):
    fullList = [1,2,3,4,5,6,7,8,9]
    newList = []
    rowList = getBlocks(row, 'row')
    #print('rowlist', rowList)
    colList = getBlocks(col, 'col')
    #print('colList', colList)
    mainBlockList = getBlocks(mainBlock, 'mainBlock')
    #print('mainBlockList', mainBlockList)
    newList.extend(rowList)
    newList.extend(colList)
    newList.extend(mainBlockList)
    newArray = []
    for number in fullList:
        if number not in newList:
            newArray.append(number)
    if len(newArray) > 0:
        randomNumber = newArray[randrange(0,len(newArray))]
        return randomNumber
    else:
        return False

def getMainBlock(row, col):
    if row<3:
        if col<3:
            mainBlock = 0
        if 3 <= col < 6:
            mainBlock = 1
        if col>=6:
            mainBlock = 2
    if 3 <= row < 6:
        if col<3:
            mainBlock = 3
        if 3 <= col <6:
            mainBlock = 4
        if col>=6:
            mainBlock = 5
    if row>=6:
        if col<3:
            mainBlock = 6
        if 3 <= col <6:
            mainBlock = 7
        if col>=6:
            mainBlock = 8
    return mainBlock

def createCol(x, y, i):
    for j in range(9): #col
        mainBlock = getMainBlock(i, j)
        number = pickNumber(i,j, mainBlock)
        if number is False:
           return False
        else:
            newCase = case(number, x, y, i ,j ,mainBlock, False)
            newCase.createCase()
            if (j+1)%3 == 0:
                x = x + 103
            else:
                x = x + 99

def createRow(y):
    i = 0
    while i < 9 : #row
        x = 0
        if createCol(x, y, i) == False:
            #print('row', actualRow)
            deleteRows(i)
            #print('row', actualRow)
        else:
            if (i+1)%3 == 0:
                y = y + 103
            else:
                y = y + 99
            i = i + 1

def getBlocks(index, type):
    newArray = []
    if type == 'row':
        blocksList = [item for item in blocks if item[0] == index] #compréhension de liste
    if type == 'col':
        blocksList = [item for item in blocks if item[1] == index]
    if type == 'mainBlock':
        blocksList = [item for item in blocks if item[2] == index]
    for i in range(len(blocksList)):
        blockId = blocksList[i]
        value = blocks[blockId].value
        newArray.append(value)
    return newArray

def deleteRows(rowIndex):
      #print(rowIndex)
    rowBlocks = [item for item in blocks if item[0] == rowIndex]
    for i in range(len(rowBlocks)):
        blockId = rowBlocks[i]
        block = blocks[blockId]
        block.deleteCase()
        del blocks[blockId]

def createSudoko(difficulty):
    global difficultyLevel
    difficultyLevel = difficulty
    createBigblock()
    y = 0
    createRow(y)
    showNumber(difficulty)


def showNumber(difficulty):
    numberToShow  = 0
    i = 0
    if difficulty == 1:
        numberToShow = 15
    if difficulty == 2:
        numberToShow = 10
    if difficulty == 3:
        numberToShow = 7
    while i < numberToShow:
        block = random.choice(list(blocks.values()))
        if block.isShow == True:
            pass
        else:
            block.showPlaceholder()
            i = i +1


def correction():
    for i in blocks.values():
        i.correction()

def getDifficulty():
    filewin = Toplevel(window)
    buttonList = []
    buttonNovice = buttonDifficulty(filewin, 1, 'Novice')
    buttonNovice.createButton()
    buttonNormal = buttonDifficulty(filewin, 2, 'Normal')
    buttonNormal.createButton()
    buttonExpert = buttonDifficulty(filewin, 3, 'Expert')
    buttonExpert.createButton()

blocks = {}
window = Tk()

menubar = Menu(window)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=getDifficulty)
filemenu.add_command(label="Close", command=window.destroy)

menubar.add_cascade(label="File", menu=filemenu)



difficultyLevel = 0
canvas = Canvas(window, height = 900, width = 900, bg = 'white')
canvas.pack()
correctionButton = Button(window,text='Correction', command=correction)
correctionButton.pack()


#canvas.create_window(50, 50, window=e1, height=100, width=100, state='disabled')
window.config(menu=menubar)
window.mainloop()