#!/usr/bin/env python

import curses
from curses import wrapper

class GameTile:
	def __init__(self):
		self.revealed = False
		self.value = 0
	def setValue(self,newValue):
		self.value = newValue
	def setRevealed(self):
		self.revealed = True	
	
def main(scrn):
	# Initialize the screen object
	scrn = curses.initscr()
	# Display message
	init(scrn)
		
	
	beginLoc = scrn.getbegyx()
	beginX = beginLoc[1]
	beginY = beginLoc[0]
	# resize the terminal
	curses.resizeterm(35,60)
	scrn.refresh()
	# make variable
	gameSizeX = 15
	gameSizeY = 15
	
	game_win = curses.newpad(gameSizeY+2,(gameSizeX*2)+2)
	info_win = scrn.subwin(5,60,30,0)
	curses.curs_set(1)
	scrn.clear()
	game_win.box()
	game_win.refresh(0,0,0,0,29,59)
	scrn.refresh()
	info_win.box()
	
	xoffset = 0
	yoffset = 0
	
	scrn.move(beginY+1,beginX+1)
	smaxY, smaxX = scrn.getmaxyx()
	pmaxY, pmaxX = game_win.getmaxyx()
	
	if pmaxY > smaxY:
		maxY = smaxY - 5
		yoffsetMax = pmaxY - (smaxY - 5)
	else:
		maxY = pmaxY
		yoffsetMax = 0
		
	if pmaxX > smaxX:
		maxX = smaxX
		xoffsetMax = pmaxX - smaxX
	else:
		maxX = pmaxX
		xoffsetMax = 0
		
	while True:
		event = scrn.getch()

		if event == ord("q"):
			break
		elif event == curses.KEY_UP:
			if y != beginY + 1:
				scrn.move(y-1,x)
			elif y == beginY + 1 and yoffset != 0:
				yoffset = yoffset - 1
				game_win.refresh(yoffset,xoffset,0,0,smaxY-6,smaxX-1)		
		elif event == curses.KEY_DOWN:
			if y != maxY - 2:
				scrn.move(y+1,x)
			elif y == maxY - 2 and yoffset != yoffsetMax: 
				yoffset = yoffset + 1
				game_win.refresh(yoffset,xoffset,0,0,smaxY-6,smaxX-1)		
		elif event == curses.KEY_LEFT:
			if x != beginX + 1:
				scrn.move(y,x-2)
			elif x == beginX + 1 and xoffset != 0:
				xoffset = xoffset - 1
				game_win.refresh(yoffset,xoffset,0,0,smaxY-6,smaxX-1)		
		elif event == curses.KEY_RIGHT:
			if x + 1 != maxX - 2:	
				scrn.move(y,x+2)
			elif x + 1 == maxX - 2 and xoffset != xoffsetMax: 
				xoffset = xoffset + 1
				game_win.refresh(yoffset,xoffset,0,0,smaxY-6,smaxX-1)		
		y,x = scrn.getyx()
		# update info window
		game_win.refresh(yoffset,xoffset,0,0,smaxY-6,smaxX-1)	
		info_win.addstr(1,1,"X = " + str((x+1)/2 + xoffset) + " Y = " + str(y + yoffset) + "           ")
		info_win.addstr(2,1,str(smaxX))
		info_win.refresh()
		# move cursor back into game window
		scrn.move(y,x)
		scrn.refresh()
		

def init(scrn):
	scrn.addstr("For best results maximize/fullscreen the terminal.\n\n Press Any Arrow Key to continue.");
	c = scrn.getch()
	while c not in (curses.KEY_UP, curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_DOWN):
		c = scrn.getch()

def mainmenu(scrdn, key):
	pass
	
# wrapper function that controls error handling
wrapper(main)      	
