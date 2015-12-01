#!/usr/bin/env python

import curses, random
from curses import wrapper

class GameTile:
	def __init__(self):
		self.revealed = False
		self.value = 0
		self.marked = False
		
	def setValue(self,newValue):
		self.value = newValue
		
	def setRevealed(self):
		self.revealed = True	
	
class GameBoard:
	def __init__(self,boardY,boardX,maxMines):	
		self.spacesRevealed = 0
		self.spacesLeft = boardX*boardY
		self.board = [[GameTile() for x in range(0,boardX)] for y in range(0,boardY)]
		self.maxY = boardY
		self.maxX = boardX
		
		# add mines and numbers
		count = 0
		while count != maxMines:
			rx = random.randint(0,boardX-1)
			ry = random.randint(0,boardY-1)
			if self.board[ry][rx].value != -1:
				self.board[ry][rx].setValue(-1)
				count += 1
				
				for i in [-1,0,1]:
					for j in [-1,0,1]:
						if 0 <= (rx + i) <= boardX-1:
							if 0 <= (ry + j) <= boardY-1:
								if self.board[ry+j][rx+i].value != -1:
									self.board[ry+j][rx+i].value += 1
							
		
def play(scrn,gameSizeY,gameSizeX,numMines):
		
	info_winX = 30
	beginY, beginX = scrn.getbegyx()
	
	# resize the terminal
	curses.resizeterm(32,62+info_winX)
	scrn.refresh()
	
	# make variable
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
		
	if pmaxX > smaxX - info_winX:
		maxX = smaxX - info_winX
		xoffsetMax = pmaxX - (smaxX - info_winX)
		
	else:
		maxX = pmaxX
		xoffsetMax = 0
	
	stop = False	
	
	while (not stop) and (not gameBoard.spacesLeft == numMines):
		event = scrn.getch()

		if event == ord("q"):
			return True

		elif event == curses.KEY_UP:
			if y != beginY + 1:
				scrn.move(y-1,x)
				
			elif y == beginY + 1 and yoffset != 0:
				yoffset = yoffset - 1
				game_win.refresh(yoffset,xoffset,0,0,maxY-1,maxX-1)	
					
		elif event == curses.KEY_DOWN:
			if y != maxY - 2:
				scrn.move(y+1,x)
				
			elif y == maxY - 2 and yoffset != yoffsetMax: 
				yoffset = yoffset + 1
				game_win.refresh(yoffset,xoffset,0,0,maxY-1,maxX-1)		
				
		elif event == curses.KEY_LEFT:
			if x != beginX + 2:
				scrn.move(y,x-2)
				
			elif x == beginX + 2 and xoffset != 0:
				xoffset = xoffset - 2
				game_win.refresh(yoffset,xoffset,0,0,maxY-1,maxX-1)
						
		elif event == curses.KEY_RIGHT:
			if x + 1 != maxX - 1:	
				scrn.move(y,x+2)
				
			elif x + 1 == maxX - 1 and xoffset != xoffsetMax: 
				xoffset = xoffset + 2
				game_win.refresh(yoffset,xoffset,0,0,maxY-1,maxX-1)
				
		elif event == ord("m"):
			y,x = scrn.getyx()
			stop = update(y+yoffset,x+xoffset,gameBoard,game_win, True)
			
		elif event == ord("i"):
			y,x = scrn.getyx()
			stop = update(y+yoffset,x+xoffset,gameBoard,game_win, False)
			
		y,x = scrn.getyx()
		
		# update info window
		game_win.refresh(yoffset,xoffset,0,0,maxY-1,maxX-1)	
		info_win.addstr(1,1,"X = " + str(x/2 + xoffset/2) + " Y = " + str(y + yoffset) + "           ")
		info_win.addstr(2,1,"Unrevealed spaces " + str(gameBoard.spacesLeft) + "    ")
		
		if stop:
			info_win.addstr(3,1,"Sorry you hit a mine",curses.color_pair(2))
			info_win.addstr(4,1,"Press any key to return",curses.color_pair(2))
			info_win.addstr(5,1,"to the main menu",curses.color_pair(2))
			
		else:
			info_win.addstr(3,1,"Press 'm' to toggle mark")
			info_win.addstr(4,1,"Press 'i' to inspect")
					
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
	scrn.clear()

	return False


def init(scrn):
	curses.resizeterm(32,62)
	scrn.box()
	scrn.addstr(1,1,"For best results maximize/fullscreen the terminal.")
	scrn.addstr(5,1,"Press Any Arrow Key to continue.")
	scrn.addstr(3,1,"Pressing 'q' at any time will close the game")
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
	scrn.clear()
	scrn.box()
	quit = False
	
	
	curloc=[(9,19),(11,19),(13,19),(15,19),(17,17),(19,27)]
	index = 0;
	
	
	while not quit:
		y,x = curloc[index]
		curses.curs_set(2)
		scrn.addstr(2,24,"MINESWEEPER")
		scrn.addstr(7,28,"Play")
		scrn.addstr(9,20, "10x10 Grid, 15 Mines")
		scrn.addstr(11,20, "20x20 Grid, 70 Mines")
		scrn.addstr(13,20, "30x30 Grid, 125 Mines")
		scrn.addstr(15,20, "40x40 Grid, 200 Mines")
		scrn.addstr(17,18, "Random Grid, Random Mines")
		scrn.addstr(19,28,"Quit")
		scrn.addstr(23,5,"Use the UP and DOWN arrow keys to navigate menus")
		scrn.addstr(25,5,"Press 'm' to select an option")
		scrn.move(y,x-1)
		scrn.refresh()
		
		event = scrn.getch()

		if event == ord("q"):
			quit = True
			
		elif event == curses.KEY_UP:
			if index != 0:
				index -= 1	
						
		elif event == curses.KEY_DOWN:
			if index != 5:
				index += 1
				
		elif event == ord("m"):
			if index == 0:
				quit = play(scrn,10,10,15)
				
			elif index == 1:
				quit = play(scrn,20,20,70)
				
			elif index == 2:
				quit = play(scrn,30,30,125)
				
			elif index == 3:
				quit = play(scrn,40,40,200)
				
			elif index == 4:
				yrand = random.randint(10,50)
				xrand = random.randint(10,50)
				mines = random.randint((yrand*xrand/16),(yrand*xrand/8))
				quit = play(scrn,yrand,xrand,mines)
				
			elif index == 5:
				quit = True
				
			curses.resizeterm(32,62)
			scrn.box()
			scrn.refresh()
	
def update(locY, locX, gameBoard, game_win, mark):
	x = ((locX+1)/2)-1
	y = locY - 1
	board = gameBoard.board
	stop = False
	if mark:
		if not board[y][x].revealed:
			if not board[y][x].marked:
				board[y][x].marked = True
				game_win.addch(locY,((x+1)*2)-1,ord(" "),curses.color_pair(1))
				game_win.addch(locY,(x+1)*2,ord("X"),curses.color_pair(2))
				
			else:
				board[y][x].marked = False
				game_win.addch(locY,((x+1)*2)-1,ord(" "),curses.color_pair(1))
				game_win.addch(locY,(x+1)*2,ord("'"),curses.color_pair(1))
				
	else:
		if not board[y][x].revealed:
			if board[y][x].marked:
				pass
				
			else:
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
					if not gameBoard.board[y+j][x+i].marked:
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
