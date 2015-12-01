#!/usr/bin/env python

import curses, random
from curses import wrapper

class GameTile:
	def __init__(self):
		self.revealed = False
		self.value = 0
	def setValue(self,newValue):
		self.value = newValue
	def setRevealed(self):
		self.revealed = True	
	
class GameBoard:
	def __init__(self,boardY,boardX,maxMines):	
		self.spacesRevealed = 0
		self.spacesLeft = boardX*boardY
		self.board = [[GameTile() for y in range(0,boardY)] for x in range(0,boardX)]
		self.maxY = boardY
		self.maxX = boardX
		
		# add mines and numbers
		count = 0
		while not count == maxMines:
			rx = random.randint(0,boardX-1)
			ry = random.randint(0,boardY-1)
			if not self.board[ry][rx].value == -1:
				self.board[ry][rx].setValue(-1)
				count += 1
				
				for i in [-1,0,1]:
					for j in [-1,0,1]:
						if 0 <= (rx + i) <= boardX-1:
							if 0 <= (ry + j) <= boardY-1:
								if not self.board[ry+j][rx+i].value == -1:
									self.board[ry+j][rx+i].value += 1
							
		
def play(scrn):
		
	info_winX = 30
	beginY, beginX = scrn.getbegyx()
	
	# resize the terminal
	curses.resizeterm(32,62+info_winX)
	scrn.refresh()
	
	# make variable
	gameSizeX = 30
	gameSizeY = 30
	numMines = 100
	smaxY, smaxX = scrn.getmaxyx()
	
	game_win = curses.newpad(gameSizeY+2,(gameSizeX*2)+2)
	
	info_win = scrn.subwin(10,30,0,smaxX-info_winX)
	curses.curs_set(1)
	scrn.clear()
	game_win.box()
	game_win.refresh(0,0,0,0,31,61)
	scrn.refresh()
	info_win.box()
	
	# create the game board
	#gameBoard = createBoard(gameSizeY,gameSizeX)
	gameBoard = GameBoard(gameSizeY,gameSizeX,numMines)
	#gameBoard = BoardObject.board
	#mineBoard(gameBoard,gameSizeY,gameSizeX,10)
	
	# init the display
	for y in range(1,gameSizeY+1):
		for x in range(1,gameSizeX+1):
			game_win.addch(y,(x*2)-1,ord(" "),curses.color_pair(1))
			game_win.addch(y,x*2,ord("'"),curses.color_pair(1))
	
	xoffset = 0
	yoffset = 0
	
	scrn.move(beginY+1,beginX+2)

	pmaxY, pmaxX = game_win.getmaxyx()
	
	if pmaxY > smaxY:
		maxY = smaxY
		yoffsetMax = pmaxY - (smaxY)
	else:
		maxY = pmaxY
		yoffsetMax = 0
		
	if pmaxX > smaxX:
		maxX = smaxX
		xoffsetMax = pmaxX - smaxX
	else:
		maxX = pmaxX
		xoffsetMax = 0
	
	stop = False	
	
	while (not stop) and (not gameBoard.spacesLeft == numMines):
		event = scrn.getch()

		if event == ord("q"):
			break
		elif event == curses.KEY_UP:
			if y != beginY + 1:
				scrn.move(y-1,x)
			elif y == beginY + 1 and yoffset != 0:
				yoffset = yoffset - 1
				game_win.refresh(yoffset,xoffset,0,0,smaxY-1,smaxX-1)		
		elif event == curses.KEY_DOWN:
			if y != maxY - 2:
				scrn.move(y+1,x)
			elif y == maxY - 2 and yoffset != yoffsetMax: 
				yoffset = yoffset + 1
				game_win.refresh(yoffset,xoffset,0,0,smaxY-1,smaxX-1)		
		elif event == curses.KEY_LEFT:
			if x != beginX + 2:
				scrn.move(y,x-2)
			elif x == beginX + 1 and xoffset != 0:
				xoffset = xoffset - 1
				game_win.refresh(yoffset,xoffset,0,0,smaxY-1,smaxX-1)		
		elif event == curses.KEY_RIGHT:
			if x + 1 != maxX - 1:	
				scrn.move(y,x+2)
			elif x + 1 == maxX - 1 and xoffset != xoffsetMax: 
				xoffset = xoffset + 1
				game_win.refresh(yoffset,xoffset,0,0,smaxY-1,smaxX-1)
		elif event == ord("m"):
			y,x = scrn.getyx()
			stop = update(y,x,gameBoard,game_win)
			
		y,x = scrn.getyx()
		# update info window
		game_win.refresh(yoffset,xoffset,0,0,smaxY-1,smaxX-1)	
		info_win.addstr(1,1,"X = " + str((x+1)/2 + xoffset) + " Y = " + str(y + yoffset) + "           ")
		info_win.addstr(2,1,str(gameBoard.spacesLeft) + "    ")
		if stop:
			info_win.addstr(3,1,"Sorry you hit a mine",curses.color_pair(2))
			info_win.addstr(4,1,"Press any key to return",curses.color_pair(2))
			info_win.addstr(5,1,"to the main menu",curses.color_pair(2))
					
		info_win.refresh()
		# move cursor back onto the board
		scrn.move(y,x)
		scrn.refresh()
	
	if not stop:
		info_win.addstr(3,1,"Congradulations you won",curses.color_pair(3))
		info_win.addstr(4,1,"Press any key to return",curses.color_pair(3))
		info_win.addstr(5,1,"to the main menu",curses.color_pair(3))
		info_win.refresh()
		scrn.move(y,x)
		scrn.refresh()
	
	event = scrn.getch()

def init(scrn):
	scrn.addstr("For best results maximize/fullscreen the terminal.\n\n Press Any Arrow Key to continue.");
	c = scrn.getch()
	while c not in (curses.KEY_UP, curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_DOWN):
		c = scrn.getch()

def mainmenu(scrn):
	# create color pairs
	curses.start_color()
	curses.use_default_colors()
	curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
	
	# Initialize the screen object
	scrn = curses.initscr()
	
	# Display message
	init(scrn)
	play(scrn)
	
def update(locY, locX, gameBoard, game_win):
	x = ((locX+1)/2)-1
	y = locY - 1
	board = gameBoard.board
	stop = False
	if not board[y][x].revealed:
		board[y][x].setRevealed()
		
		if board[y][x].value == -1:
			stop = True
		elif board[y][x].value == 0:
			updateRec(y,x,gameBoard, game_win)
		else:
			game_win.addch(locY,((x+1)*2)-1,ord(" "),curses.color_pair(1))
			game_win.addch(locY,(x+1)*2,ord(str(board[y][x].value)),curses.color_pair(1))
			gameBoard.spacesRevealed += 1
			gameBoard.spacesLeft -= 1
	return stop
	
def updateRec(y, x, gameBoard, game_win):
	
	gameBoard.board[y][x].setRevealed()
	game_win.addch(y+1,((x+1)*2)-1,ord(" "))
	game_win.addch(y+1,(x+1)*2,ord(" "))
	gameBoard.spacesRevealed += 1
	gameBoard.spacesLeft -= 1
	for i in [-1,0,1]:
		for j in [-1,0,1]:
			if 0 <= (x + i) <= gameBoard.maxX-1:
				if 0 <= (y + j) <= gameBoard.maxY-1:
					if not gameBoard.board[y+j][x+i].revealed:					
						if gameBoard.board[y+j][x+i].value == 0:
							updateRec(y+j, x+i, gameBoard, game_win)
							game_win.addch(y+j+1,((x+i+1)*2)-1,ord(" "))
							game_win.addch(y+j+1,(x+i+1)*2,ord(" "))
						elif gameBoard.board[y+j][x+i].value > 0:
							game_win.addch(y+j+1,((x+i+1)*2)-1,ord(" "),curses.color_pair(1))
							game_win.addch(y+j+1,(x+i+1)*2,ord(str(gameBoard.board[y+j][x+i].value)),curses.color_pair(1))
							gameBoard.board[y+j][x+i].setRevealed()
							gameBoard.spacesRevealed += 1
							gameBoard.spacesLeft -= 1
	


# wrapper function that controls error handling
wrapper(mainmenu)      	
