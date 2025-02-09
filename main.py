import pygame, random
pygame.init()
pygame.mixer.init()


# CONSTANTS
WIDTH = 800
HEIGHT = 800
RED = (255, 0, 0)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
BLACK = (0,0,0)
WHITE = (255, 255, 255)
BGCOLOR = (30, 30, 30)
LIGHTGREY = (100, 100, 100)
DARKGREY = (200, 200, 200)
PURPLE = (100, 0, 100)
TURQUOISE = (48, 213, 200)
MAROON = (128, 0, 0)



window = pygame.display.set_mode((WIDTH, HEIGHT))
name = pygame.display.set_caption('Minesweeper!')
LEFTCLICK = 1
RIGHTCLICK = 3      # MOUSE BUTTONS


mines = []          # LIST OF BOXES THAT ARE MINES, USED IN chooseMines(), is a GLOBAL variable
numbers = []        # LIST OF BOXES WITH NUMBERS USED IN chooseNumbers(), is a GLOBAL variable
uncovered = []      # LIST OF BOXES THAT HAVE BEEN CLICKED
markedBoxes = []    # LIST OF BOXES THAT ARE FLAGGED
fullList = []       # USED IN zeroClickingLogic()
crashed = False
lastBoxClicked = None   # STORES THE LAST BOX CLICKED
boardFirst = True       # FIRST TIME BOARD INITIALIZATION
#inMenu = True
gamesWon = 0
gamesLost = 0
myfont1 = pygame.font.SysFont('Comic Sans MS', 30)      # FONT SIZE 30
myfont2 = pygame.font.SysFont('Comic Sans MS', 15)      # FONT SIZE 15

defaultSettings = False

clock = pygame.time.Clock()
FPS = 30

# IMAGES
flag = pygame.image.load(r'images\flag.png')
mineImage = pygame.image.load(r'images\mine.png')
crossImage = pygame.image.load(r'images\cross.png')


# CLASSES
class box(object):
    def __init__(self, row, column, number, shown = False):     # ROW IS X COORDINATE AND COLUMN IS Y IN BOX CARTESIAN SYSTEM
        self.width = 60
        self.height = 60
        self.row = row
        self.number = number        # THE NUMBER USED FOR PROGRAMMING EASE
        self.column = column
        self.shown = shown
        self.color = LIGHTGREY
        self.isMine = False
        self.isMarked = False
        self.y = 5 + ((self.width+4) * self.column) # row and column interchanged
        self.x = 5 + ((self.height+4) * self.row)
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.digit = None             # THE ACTUAL NUMBER IN THE BOX
        self.furtherUpdates = True

    def draw(self):
        pygame.draw.rect(window, self.color, self.hitbox)
        pygame.draw.rect(window, WHITE, (self.x, self.y, self.width, 4))
        pygame.draw.rect(window, WHITE, (self.x, self.y, 4, self.height))
        pygame.draw.rect(window, BLACK, (self.x, self.y + self.height - 4, self.width, 4))
        pygame.draw.rect(window, BLACK, (self.x + self.width - 4, self.y, 4, self.height))
        pygame.display.update()

    def drawUncoveredBox(self):
        pygame.draw.rect(window, DARKGREY, self.hitbox)
        pygame.display.update()


    def markFlag(self):
        window.blit(flag, (self.x, self.y+5))

    def unmarkFlag(self):
        self.draw()

    def findNeighbors(self):
        neighborsList = []
        for i in boxes:
            if self.row in [i.row-1, i.row, i.row+1]:                       # SAME X CARTESIAN     
                if self.column in [i.column-1, i.column, i.column+1]:       # SAME Y CARTESIAN
                    if (self.row == i.row) and (self.column == i.column):   # REMOVE SAME BOX
                        pass
                    else:
                        neighborsList.append(i)
                else:
                    pass
            else:
                pass
        return neighborsList

    def renderNumber(self):
        if self.digit == None:
            pass
        else:
            self.drawUncoveredBox()
            if self.digit == 1:
                numbertext = myfont1.render(str(self.digit), False, BLUE)
                window.blit(numbertext, (self.x+20, self.y+5))
            elif self.digit == 2:
                numbertext = myfont1.render(str(self.digit), False, GREEN)
                window.blit(numbertext, (self.x+20, self.y+5))
            elif self.digit == 3:
                numbertext = myfont1.render(str(self.digit), False, RED)
                window.blit(numbertext, (self.x+20, self.y+5))
            elif self.digit == 4:
                numbertext = myfont1.render(str(self.digit), False, PURPLE)
                window.blit(numbertext, (self.x+20, self.y+5))
            elif self.digit == 5:
                numbertext = myfont1.render(str(self.digit), False, MAROON)
                window.blit(numbertext, (self.x+20, self.y+5))
            elif self.digit == 6:
                numbertext = myfont1.render(str(self.digit), False, TURQUOISE)
                window.blit(numbertext, (self.x+20, self.y+5))

        #window.blit(numbertext, (self.x+20, self.y+5))

        self.furtherUpdates = False
        self.isMarked = False

    def showMine(self):
        window.blit(mineImage, (self.x, self.y))

    def doesNeighborHaveZero(self):
        zerosInNeighbors = []
        list_of_neighbors = self.findNeighbors()
        for i in list_of_neighbors:
            if i.digit == 0:
                zerosInNeighbors.append(i)

        return zerosInNeighbors        

    def renderNeighbors(self):
        for i in self.findNeighbors():
            i.drawUncoveredBox()
            pygame.display.update()

    def showCross(self):
        window.blit(crossImage, (self.x, self.y))
        


class button(object):
    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.text = text
        self.fontColor = WHITE


    def draw(self):
        textToRender = myfont1.render(self.text, True, self.fontColor)
        window.blit(textToRender, (self.x, self.y))


# BUTTONS

restart = button(400, 600, 100, 50, 'Restart')


buttons = [restart]

# BOXES
# 10x8 on easy mode
box11 = box(1, 1, 1)
box12 = box(1, 2, 2)
box13 = box(1, 3, 3)
box14 = box(1, 4, 4)
box15 = box(1, 5, 5)
box16 = box(1, 6, 6)
box17 = box(1, 7, 7)
box18 = box(1, 8, 8)

box21 = box(2, 1, 9)
box22 = box(2, 2, 10)
box23 = box(2, 3, 11)
box24 = box(2, 4, 12)
box25 = box(2, 5, 13)
box26 = box(2, 6, 14)
box27 = box(2, 7, 15)
box28 = box(2, 8, 16)

box31 = box(3, 1, 17)
box32 = box(3, 2, 18)
box33 = box(3, 3, 19)
box34 = box(3, 4, 20)
box35 = box(3, 5, 21)
box36 = box(3, 6, 22)
box37 = box(3, 7, 23)
box38 = box(3, 8, 24)

box41 = box(4, 1, 25)
box42 = box(4, 2, 26)
box43 = box(4, 3, 27)
box44 = box(4, 4, 28)
box45 = box(4, 5, 29)
box46 = box(4, 6, 30)
box47 = box(4, 7, 31)
box48 = box(4, 8, 32)

box51 = box(5, 1, 33)
box52 = box(5, 2, 34)
box53 = box(5, 3, 35)
box54 = box(5, 4, 36)
box55 = box(5, 5, 37)
box56 = box(5, 6, 38)
box57 = box(5, 7, 39)
box58 = box(5, 8, 40)

box61 = box(6, 1, 41)
box62 = box(6, 2, 42)
box63 = box(6, 3, 43)
box64 = box(6, 4, 44)
box65 = box(6, 5, 45)
box66 = box(6, 6, 46)
box67 = box(6, 7, 47)
box68 = box(6, 8, 48)

box71 = box(7, 1, 49)
box72 = box(7, 2, 50)
box73 = box(7, 3, 51)
box74 = box(7, 4, 52)
box75 = box(7, 5, 53)
box76 = box(7, 6, 54)
box77 = box(7, 7, 55)
box78 = box(7, 8, 56)

box81 = box(8, 1, 57)
box82 = box(8, 2, 58)
box83 = box(8, 3, 59)
box84 = box(8, 4, 60)
box85 = box(8, 5, 61)
box86 = box(8, 6, 62)
box87 = box(8, 7, 63)
box88 = box(8, 8, 64)

box91 = box(9, 1, 65)
box92 = box(9, 2, 66)
box93 = box(9, 3, 67)
box94 = box(9, 4, 68)
box95 = box(9, 5, 69)
box96 = box(9, 6, 70)
box97 = box(9, 7, 71)
box98 = box(9, 8, 72)

box101 = box(10, 1, 73)
box102 = box(10, 2, 74)
box103 = box(10, 3, 75)
box104 = box(10, 4, 76)
box105 = box(10, 5, 77)
box106 = box(10, 6, 78)
box107 = box(10, 7, 79)
box108 = box(10, 8, 80)

boxes = [box11, box12, box13, box14, box15, box16, box17, box18, box21, box22, box23, box24, box25, box26, box27, box28,
        box31, box32, box33, box34, box35, box36, box37, box38, box41, box42, box43, box44, box45, box46, box47, box48, 
        box51, box52, box53, box54, box55, box56, box57, box58, box61, box62, box63, box64, box65, box66, box67, box68, 
        box71, box72, box73, box74, box75, box76, box77, box78, box81, box82, box83, box84, box85, box86, box87, box88, 
        box91, box92, box93, box94, box95, box96, box97, box98, box101, box102, box103, box104, box105, box106, box107, box108]


def playClickSound():
    pygame.mixer.music.load(r'sounds\click.wav')
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play()

def showMenu():
    showText1('Minesweeper', 400, 400)
    

def showText1(text, x, y, color = WHITE):
    gamewon = myfont1.render(text, True, color)
    window.blit(gamewon, (x, y))
    pygame.display.update()

def showText2(text, x, y, color = WHITE):
    gamewon = myfont2.render(text, True, color)
    window.blit(gamewon, (x, y))
    pygame.display.update()


def hideText(x, y, width, height, color):
    cover = pygame.Rect(x, y, width, height)
    pygame.draw.rect(window, color, cover)
    pygame.display.update()

def showWinLossRatio():
    global gamesLost, gamesWon
    showText1('Win/Loss : ' + str(gamesWon) + '/' + str(gamesLost), 400, 700)

def initializeDefaultSettings():                    # RESTORE GAME BOARD TO NEW GAME MODE
    global boardFirst, mines, numbers, uncovered, markedBoxes, inMenu
    for i in boxes:
        i.shown = False
        i.color = LIGHTGREY
        i.isMine = False
        i.isMarked = False
        i.digit = None             # THE ACTUAL NUMBER IN THE BOX
        i.furtherUpdates = True

    boardFirst = True
   # inMenu = False
    mines = []
    numbers = []
    uncovered = []
    markedBoxes = []
    hideText(400, 650, 250, 150, BGCOLOR)
    showWinLossRatio()


def drawBoxes():        # DRAW THE BOARD
    for i in boxes:
        i.draw()

def drawButtons():      # DRAW THE BUTTONS
    for i in buttons:
        i.draw()

    
def chooseMines():          # CHOOSE THE MINES
    global mines
    while len(mines) < 10:
        num = random.randint(1, 80)
        if num not in mines:
            for box1 in boxes:
                if box1.number == num:
                    box1.isMine = True
                    mines.append(num)
                else:
                    pass
        else:
            pass
    

def chooseNumbers():        # CHOOSE NUMBERS FOR ALL BOXES EXCEPT MINES
    global numbers
    for i in boxes:
        for j in mines:
            if i.number != j:
                list_of_neighbors = i.findNeighbors()

                countofmines = 0
                for k in mines:
                    for l in list_of_neighbors:
                        if k == l.number:
                            countofmines += 1
            
            if i.isMine == False:       # DON'T MARK BOXES WHICH HAVE MINES
                i.digit = countofmines
            else:
                pass
    




def flagging():         # CHECK FOR FLAGS
    for i in boxes:
        if i.furtherUpdates == True:
            if i.isMarked:
                i.markFlag()
                #markedBoxes.append(i)

            elif i.isMarked == False:
                i.unmarkFlag()
        else:
            pass


def unmarkAll():            # UNMARK ALL THE FLAGGED BOXES
    for i in markedBoxes:
        i.unmarkFlag()


def showNumbers():          # SHOW THE NUMBERS WHEN CLICKED
    for i in boxes:
        if i.shown and (i in uncovered):
            i.renderNumber()


def zeroClickLogic():       # REVEAL ADJACENT SQUARES WHEN ZERO IS CLICKED
    global lastBoxClicked, list_of_neighbors, fullList
    if lastBoxClicked.digit == 0:
        list_of_neighbors = lastBoxClicked.findNeighbors()
    else:
        pass
    for i in list_of_neighbors:
        if i.isMarked == True or i.shown == True:
            list_of_neighbors.remove(i)
        else:
            pass

            
    '''
    for i in list_of_neighbors:
        if i.doesNeighborHaveZero() != [] and i.digit == 0 and (i not in fullList):
            lastBoxClicked = i
            fullList.append(i)
            zeroClickLogic()

        else:
            pass
    '''
    return list_of_neighbors


def minesLeft():
    cover = pygame.Rect(110, 600, 250, 50)

    pygame.draw.rect(window, BGCOLOR, cover)
    pygame.display.update()

    minesLeft = len(markedBoxes)
    minetext = myfont1.render('Mines Left : ' + str(10 - minesLeft), False, WHITE)
    window.blit(minetext, (110, 600))
    pygame.display.update()


def disableBoxes():         # MAKES ALL BOXES UNRESPONSIVE
    for i in boxes:
        i.furtherUpdates = False


def showAllMines():         # SHOWS ALL MINES WHEN GAME IS LOST
    for i in markedBoxes:
        if i.number in mines:
            i.unmarkFlag()
            continue
        else:
            i.showCross()
            continue

    for i in mines:
        for j in boxes:
            if j.number == i:
                j.showMine()


def isGameWon():            # CHECK WHETHER GAME IS WON OR NOT
    global gamesWon
    if len(uncovered) == 70:
        gamesWon += 1
        showText1('You Won!', 400, 650)
        disableBoxes()

def gameLost():
    showText1('You lost!', 400, 650)



def removeDuplicate(sample):        # REMOVE DUPLICATES FROM LIST
    sample1 = [*set(sample)]
    return sample1


# MAIN LOOP
while not crashed:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
            break

        if event.type == pygame.MOUSEMOTION:            # COLOR CHANGING FOR MOUSEMOTION
            pos = pygame.mouse.get_pos()
            for i in boxes:
                if i.hitbox.collidepoint(pos) and i.shown == False:
                    i.color = DARKGREY
                elif i.shown == True:
                    pass
                else:
                    i.color = LIGHTGREY

            for i in buttons:
                if i.hitbox.collidepoint(pos):
                    i.fontColor = RED
                else:
                    i.fontColor = WHITE
                drawButtons()


        
        if event.type == pygame.MOUSEBUTTONDOWN:        # UNCOVERING BOXES
            pos = pygame.mouse.get_pos()
            for i in boxes:
                if i.furtherUpdates == True:
                    if i.hitbox.collidepoint(pos) and i.shown == False:
                        if event.button == LEFTCLICK:       # UNCOVER IF LEFTCLICK
                            if i not in uncovered:
                                lastBoxClicked = i
                                if i.isMarked == True:
                                    pass

                                else:                   # WHEN THE GAME IS LOST
                                    if i.isMine == True:
                                        i.shown = True
                                        uncovered.append(i)

                                        gamesLost += 1
                                        gameLost()
                                        showAllMines()
                                        disableBoxes()
                                    if i.isMine == False:
                                        # zero click logic
                                        i.shown = True
                                        playClickSound()
                                        i.drawUncoveredBox()
                                        uncovered.append(i)
                                        showNumbers()
                                        

                                        if i.digit == 0:            # IMPLEMENTING THE ZERO CLICK LOGIC
                                            neighbors = zeroClickLogic()
                                            for k in neighbors:
                                                k.shown = True
                                                k.drawUncoveredBox()
                                                uncovered.append(k)
                                                showNumbers()
                                        else:
                                            pass

                                        uncovered = removeDuplicate(uncovered)
                                        isGameWon()
                            else:
                                pass
                                
                        if event.button == RIGHTCLICK:      # MARK IF RIGHTCLICK
                            i.isMarked = not i.isMarked
                            if i.isMarked == True:
                                markedBoxes.append(i)
                            else:
                                try:
                                    markedBoxes.remove(i)
                                except ValueError:
                                    pass
                            minesLeft()
            for i in buttons:
                if i.hitbox.collidepoint(pos):
                    if i == restart:
                        defaultSettings = not defaultSettings

                
        
    
    if boardFirst:      # DRAW BOARD ONCE
        window.fill(BGCOLOR)
        showWinLossRatio()
        chooseMines()
        chooseNumbers()
        drawBoxes()
        drawButtons()
        minesLeft()

        boardFirst = not boardFirst
    
    #if inMenu:
     #   disableBoxes()

    #if not inMenu:
     #   flagging()

    flagging()

    if defaultSettings:
        initializeDefaultSettings()
        defaultSettings = not defaultSettings


    pygame.display.update()

pygame.quit()
