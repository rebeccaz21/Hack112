# PACMAN

from tkinter import *
import random
import math
#import openCV

 ############## GHOSTS ############
 
class Ghost(object):
    def __init__(self, row, col,TA):
        self.w = 60
        self.row = row
        self.col = col
        self.TA=TA
         
    def move(self,data):
        direction = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
        self.row += direction[0]
        self.col += direction[1]
        if self.row < 0 or self.row > data.rows-1:
            self.row -= direction[0]
        if self.col < 0 or self.col > data.cols-1:
            self.col -= direction[1]
        
    def draw(self,canvas,data):
        for row in range(data.rows):
            for col in range(data.cols):
                if row == self.row and col == self.col:
                    canvas.create_image(((col+1)-.25)*self.w-15, ((row+1)-.25)*self.w-15,image=self.TA)
    
    def collidesWithPacman(self,data):
        if self.row == data.playerSpot[0] and self.col == data.playerSpot[1]:
            return True
        return False

def makeGhosts(data):
    ghosts = []
    TAs = [data.abhi,data.eugene,data.tara,data.arman,data.chaya]
    for i in range(5):
        row = random.randint(0,data.rows-1)
        col = random.randint(0,data.cols-1)
        ghosts.append(Ghost(row,col,TAs[len(ghosts)]))
    return ghosts

NORTH = (-1,0)
SOUTH = (1,0)
EAST  = (0,1)
WEST  = (0,-1)

def keyPressed(event, data):
    row,col = data.playerSpot
    if data.inStartScreen:
        data.inStartScreen = False
    elif event.keysym == "Up" and isValid(data, row,col,NORTH):
        data.direction=NORTH
    elif event.keysym == "Down" and isValid(data, row,col,SOUTH):
        data.direction=SOUTH
    elif event.keysym == "Left" and isValid(data, row,col,WEST):
        data.direction=WEST
    elif event.keysym == "Right" and isValid(data, row,col,EAST):
        data.direction=EAST

def doMove(data,row,col,direction):
    (drow,dcol) = direction
    maze,path = data.maze,data.path
    rows,cols = len(maze),len(maze[0])
    if not (0<=row<rows and 0<=col<cols): return False
    data.playerSpot = (row+drow,col+dcol)

def isValid(data, row,col,direction):
    maze = data.maze
    rows,cols = len(maze),len(maze[0])
    if not (0<=row<rows and 0<=col<cols): return False
    if direction==EAST: return maze[row][col].east
    if direction==SOUTH: return maze[row][col].south
    if direction==WEST: return maze[row][col-1].east
    if direction==NORTH: return maze[row-1][col].south
    assert False

##################################### draw #####################################

def redrawAll(canvas, data):
    if data.inStartScreen: return drawStartScreen(canvas, data)
    canvas.create_rectangle(0,0,data.width,data.height,fill = "black")
    drawBridges(canvas, data)
    drawIslands(canvas, data)
    drawBoard(canvas,data)
    drawFood(canvas,data)
    drawPlayerPath(canvas, data)
    for ghost in data.ghosts:
        ghost.draw(canvas,data)
    drawLives(canvas,data)
    drawScoreBoard(canvas,data)
    if data.lives <= 0:
        drawEnd(canvas,data)
    if data.bigFood:
        canvas.create_text(300,300,text='EAT TAS',font="Helvetica 32 bold",fill='yellow')
    if len(data.ghosts)<= 0:
        win(canvas,data)
        
def drawEnd(canvas,data):
    font = "Helvetica 32 bold"
    canvas.create_rectangle(0,0,data.width,data.height,fill='black')
    canvas.create_text(data.width//2,data.height//2,text="GAME OVER",font=font,fill='white')

def drawLives(canvas,data):
    font = "Helvetica " + str(data.width//20)+" bold"
    canvas.create_text(75,data.height-25,text="Lives: "+str(data.lives),font=font,fill = 'yellow')

def drawBoard(canvas,data):
    r = 60
    for row in range(data.rows):
        for col in range(data.cols):
            canvas.create_rectangle(col*r,row*r,(col+1)*r,(row+1)*r,outline='black')
            

def drawStartScreen(canvas, data):
    font = "Helvetica 32 bold"
    canvas.create_text(300, 300, text="WELCOME TO HACK-MAN", font=font)
    font = "Helvetica 24 bold"
    messages = [
                "press any key to start"
                ]
    for i in range(len(messages)):
        canvas.create_text(300, 150+50*i, text=messages[i], font=font)

def drawIslands(canvas, data):
    islands = data.maze
    rows,cols = len(islands),len(islands[0])
    color = data.islandColor
    r = min(data.cW,data.cH)/5
    for row in range(rows):
        for col in range(cols):
            drawCircle(canvas, islandCenter(data, row,col),r,color,color,data)

def drawCircle(canvas, position, r, color, outlineColor,data):
    (cx,cy) = position
    canvas.create_oval(cx-r,cy-r,cx+r,cy+r,\
    fill=color,outline=outlineColor,width=15)

def drawKelly(canvas,position,r,color,outlineColor,data):
    (cx,cy) = position
    if data.kellyCount % 2 == 0:
        image = data.kelly1
    else:
        image = data.kelly2
    canvas.create_image(cx,cy,image = image)

def islandCenter(data, row, col):
    if data.isPolar:
        cx,cy = data.width/2,data.height/2
        rows,cols = len(data.maze),len(data.maze[0])
        maxR = min(cx,cy)
        r = maxR*(row+1)/(rows+1)
        theta = 2*math.pi*col/cols
        return cx+r*math.cos(theta), cy-r*math.sin(theta)
    else:
        cellWidth,cellHeight = data.cW,data.cH
        return (col+0.5)*cellWidth,(row+0.5)*cellHeight

def drawBridges(canvas, data):
    islands = data.maze
    rows,cols = len(islands),len(islands[0])
    color = data.bridgeColor
    width = min(data.cW,data.cH)/1.5
    for r in range(rows):
        for c in range(cols):
            island = islands[r][c]
            if (island.east):
                canvas.create_line(islandCenter(data, r,c),
                                   islandCenter(data, r,c+1),
                                   fill=color, width=width)
            if (island.south):
                canvas.create_line(islandCenter(data, r,c),
                                   islandCenter(data, r+1,c),
                                   fill=color, width=width)

def drawPlayerPath(canvas, data):
    path = data.path
    (pRow,pCol) = data.playerSpot
    color = data.pathColor
    r = min(data.cW,data.cH)/6
    width = min(data.cW,data.cH)/1.5
    for (row,col) in path:
        drawCircle(canvas, islandCenter(data, row,col),r,color,color,data)
        if (row+1,col) in path and isValid(data, row,col,SOUTH):
            canvas.create_line(islandCenter(data, row,col),
                                   islandCenter(data, row+1,col),
                                   fill=color, width=width)
        if (row,col+1) in path and isValid(data, row,col,EAST):
            canvas.create_line(islandCenter(data, row,col),
                                   islandCenter(data, row,col+1),
                                   fill=color, width=width)
    drawKelly(canvas, islandCenter(data, pRow,pCol),r,
    data.playerColor,data.playerColor,data)
    
    
def drawFood(canvas,data):
    food = data.foodList
    w = 60
    for row in range(len(food)):
        for col in range(len(food[0])):
            if food[row][col] == 1:
                canvas.create_oval((col-.15)*w +30 ,(row-.15)*w+30,(col+.15)*w+30 ,(row+.15)*w +30, fill='white')
            if food[row][col] == 2:
                canvas.create_oval((col-.20)*w +30 ,(row-.20)*w+30,(col+.20)*w+30 ,(row+.20)*w +30, fill='white')
                
def drawScoreBoard(canvas,data):
    canvas.create_text(data.width - 120 ,data.height - 30,  text = "Score: %d" %data.score, font = "Helvetica 32 bold", fill = "yellow")

def win(canvas,data):
    canvas.create_rectange(0,0, data.width, data.height, fill = "black")
    canvas.create_text(data.width//2, data.height//2, text="YAS BINCH", font = "Helvitca 24 Bold",fill = "white")
        
##################################### init #####################################

def init(data, rows=10, cols=10, inStartScreen = True):
    if (rows < 1): rows = 1
    if (cols < 1): cols = 1
    data.inStartScreen = True
    data.rows = rows
    data.cols = cols 
    data.islandColor = "blue"
    data.bridgeColor = "blue"
    data.pathColor = "blue"
    data.playerColor = "yellow"
    data.isPolar = False
    data.path = set()
    data.playerSpot = (data.rows//2,data.cols//2-1)
    data.path.add(data.playerSpot)
    margin = 5
    data.cW = (data.width - margin)/cols
    data.cH = (data.height - margin)/rows
    data.margin = margin
    #make the islands
    data.maze = makeBlankMaze(rows,cols)
    data.island = makeLst(data.rows,data.cols,data)
    #connect the islands
    connectIslands(data.maze)
    data.direction=(0,1)
    data.abhi=PhotoImage(file='abhi.gif')
    data.eugene=PhotoImage(file='eugene.gif')
    data.tara=PhotoImage(file='tara.gif')
    data.arman=PhotoImage(file='arman.gif')
    data.chaya=PhotoImage(file='chaya.gif')
    #make ghosts
    data.ghosts = makeGhosts(data)
    data.gR = 60
    data.timerCount = 0
    #lives
    data.lives = 5
    #food
    data.foodList = makeFood(data.rows, data.cols, data)
    data.score = 0
    data.bigFood = False
    data.kelly1 = PhotoImage(file='a.gif')
    data.kelly2 = PhotoImage(file='aa.gif')
    data.kellyCount = 0
    data.foodTimer = 0

class Struct(object): pass

def makeIsland(number):
    island = Struct()
    island.east = island.south = island.north = island.west = False
    island.number = number
    return island

def makeBlankMaze(rows,cols):
    islands = [[0]*cols for row in range(rows)]
    counter = 0
    for row in range(rows):
        for col in range(cols):
            islands[row][col] = makeIsland(counter)
            counter+=1
    return islands

def makeLst(rows,cols,data):
    islands = [[0]*cols for row in range(rows)]
    for row in range(rows):
        for col in range(cols):
            islands[row][col] = (row,col)
    return islands

def connectIslands(islands):
    rows,cols = len(islands),len(islands[0])
    for i in range(rows*cols-1):
        makeBridge(islands)

def makeBridge(islands):
    rows,cols = len(islands),len(islands[0])
    while True:
        row,col = random.randint(0,rows-1),random.randint(0,cols-1)
        start = islands[row][col]
        if flipCoin(): #try to go east
            if col==cols-1: continue
            target = islands[row][col+1]
            if start.number==target.number: continue
            #the bridge is valid, so 1. connect them and 2. rename them
            start.east = True
            renameIslands(start,target,islands)
        else: #try to go south
            if row==rows-1: continue
            target = islands[row+1][col]
            if start.number==target.number: continue
            #the bridge is valid, so 1. connect them and 2. rename them
            start.south = True
            renameIslands(start,target,islands)
        #only got here if a bridge was made
        return

def renameIslands(i1,i2,islands):
    n1,n2 = i1.number,i2.number
    lo,hi = min(n1,n2),max(n1,n2)
    for row in islands:
        for island in row:
            if island.number==hi: island.number=lo

def flipCoin():
    return random.choice([True, False])
    
def makeFood(rows,cols,data):
    food = [[0]*cols for row in range(rows)]
    for row in range(rows):
        for col in range(cols):
            food[row][col] = 1
    food[0][0] = 2
    food[rows -1][0] = 2
    food[0][cols-1] = 2
    food[rows-1][cols-1] = 2
    return food

def mousePressed(event, data): pass

def checkSpot(data,player):
    island = data.maze[player[0]][player[1]]
    if data.direction == (0,1):
        if not island.east:
            return False
    elif data.direction == (0,-1):
        island = data.maze[player[0]][player[1]-1]
        if not island.east:
            return False
    elif data.direction == (1,0):
        if not island.south:
            return False
    elif data.direction == (-1,0):
        island = data.maze[player[0]-1][player[1]]
        if not island.south:
            return False
    return True
    
def eatFood(data):
    pos = data.playerSpot
    if data.foodList[pos[0]][pos[1]] == 1:
        data.foodList[pos[0]][pos[1]] = 0
        data.score += 10
    elif data.foodList[pos[0]][pos[1]] == 2:
        data.foodList[pos[0]][pos[1]] = 0
        data.score += 50
        data.bigFood = True

def timerFired(data):
    data.kellyCount += 1
    eatFood(data)
    if data.bigFood == False:
        for ghost in data.ghosts:
            if ghost.collidesWithPacman(data):
                data.lives -= 1
                data.playerSpot = (data.rows//2,data.cols//2)
    else:
        data.timerCount += 1
        for ghost in data.ghosts:
            if ghost.collidesWithPacman(data):
                data.ghosts.remove(ghost)
                data.score += 100
        if data.timerCount == 30:
            data.timerCount = 0
            data.bigFood = False
            data.ghosts = makeGhosts(data)
    for ghost in data.ghosts:
        ghost.move(data)
    if checkSpot(data,data.playerSpot):
        doMove(data,data.playerSpot[0],data.playerSpot[1],data.direction)
    data.foodTimer += 1
    if data.foodTimer == 60:
        data.foodList = makeFood(data.rows,data.cols,data)
        data.foodTimer = 0

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    #call open cv
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    root = Tk()
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 500 # milliseconds
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(600, 600)
