from tkinter import *
import webbrowser

class Tile():
	def __init__(self, row, col, clickmethod):
		self.row = row
		self.col = col
		if (row + col) % 2 == 0:
			self.color = "white"
		else:
			self.color = "grey"
		self.blank = {}
		self.images = {}
		for i in ["grey", "white", "orange"]:
			self.blank[i] = PhotoImage(file="images/"+i+"blank.png")
		for i in ["black", "white"]:
			for j in ["knight", "rook", "pawn", "bishop", "king", "queen"]:
				self.images[i+j] = PhotoImage(file="images/"+i+j+".png")

		self.button = Button(command=lambda:clickmethod(row, col), bg=self.color)
		self.piecekind = None
		self.piececolor = None
		self.highlighted = False

	def clear(self):
		self.piecekind = None
		self.piececolor = None
		self.button['image'] = self.blank[self.color]

	def placePiece(self, color, kind, deprime=True):
		self.piececolor = color
		self.piecekind = kind
		if "pawn" not in kind: self.button['image'] = self.images[color+kind]
		else:
			self.button['image'] = self.images[color+"pawn"]
			if deprime and ("prime" in kind):
				self.piecekind = self.piecekind[:-5]
			
	def highlight(self):
		if not self.highlighted:
			self.highlighted = True
			if self.piecekind is None:
				self.button['image'] = self.blank['orange']
			else:
				self.button['bg'] = 'orange'
		else:
			self.highlighted = False
			if self.piecekind is None:
				self.button['image'] = self.blank[self.color]
			else:
				self.button['bg'] = self.color

class Chess(Frame):
	def __init__(self, master):
		self.tiles = {}
		self.initBoard()

		self.turn = IntVar()
		self.currentturn = StringVar()
		self.state = StringVar()
		self.highlighted = [] #list of possible destinations
		self.source = None
		self.startbutton = Button(text="Start Game", bg="green", command=self.initGame)
		self.startbutton.grid(row=9, column=4)
		self.state = 1 #1 for not started, 2 for waiting for target piece, 3 for waiting for destination

		hyperlink = Label(text="Source Code", fg="blue4", cursor="hand2")
		hyperlink.bind("<Button-1>", lambda x: webbrowser.open_new(r"https://github.com/aelna354/PyChess/blob/master/chess.py"))
		hyperlink.grid(row=10,column=8, sticky=W)

	def initBoard(self):
		for i in range(1, 9):
			for j in range(1, 9):
				self.tiles[(i, j)] = Tile(i, j, self.click)
				self.tiles[(i, j)].button.grid(row=i, column=j)
		for i in range(1, 9):
			self.tiles[2, i].placePiece("white", "wpawnprime", deprime=False)
			self.tiles[7, i].placePiece("black", "bpawnprime", deprime=False)
		for i in [2, 7]:
			self.tiles[1, i].placePiece("white", "knight")
			self.tiles[8, i].placePiece("black", "knight")
		for i in [1, 8]:
			self.tiles[1, i].placePiece("white", "rook")
			self.tiles[8, i].placePiece("black", "rook")
		for i in [3, 6]:
			self.tiles[1, i].placePiece("white", "bishop")
			self.tiles[8, i].placePiece("black", "bishop")
		self.tiles[1, 4].placePiece("white", "king")
		self.tiles[1, 5].placePiece("white", "queen")
		self.tiles[8, 4].placePiece("black", "king")
		self.tiles[8, 5].placePiece("black", "queen")
		for i in [3, 4, 5, 6]:
			for j in range(1, 9):
				self.tiles[i, j].clear()

	def initGame(self):
		self.startbutton['text'] = "Reset Game"
		self.startbutton['bg'] = 'blue'
		self.startbutton['command'] = self.reset
		self.turn.set(1)
		Label(text="Turn Count: ").grid(row=9, column=1, sticky=W)
		Label(textvariable=self.turn).grid(row=9,column=2, columnspan=3, sticky=W)
		Label(textvariable=self.currentturn).grid(row=9, column=6, columnspan=3)
		self.currentturn.set("Current Turn: White")
		self.currentcolor = "white"
		self.state = 2

	def reset(self):
		print("H")
		for i in self.highlighted:
			self.tiles[i].highlight()
		self.highlighted = []
		self.tiles = {}
		self.initBoard()

	def click(self, r, c):
		p = self.tiles[(r, c)]

		if self.state == 2:
			if p.piececolor != self.currentcolor:
				return
			for i in self.accessible(p):
				self.tiles[i].highlight()
				self.highlighted.append(i)
			if len(self.highlighted) > 0:
				self.state = 3
				self.source = p
		
		elif self.state == 3:

			if p.highlighted:
				p.placePiece(self.source.piececolor, self.source.piecekind)
				self.source.clear()
				self.source = None
				self.state = 2
				self.turn.set(self.turn.get() + 1)
				if self.currentcolor == "white":
					self.currentcolor = "black"
					self.currentturn.set("Current Turn: Black")
				else:
					self.currentcolor = "white"
					self.currentturn.set("Current Turn: White")
				for i in self.highlighted:
					self.tiles[i].highlight()
				self.highlighted = []

			elif p.piececolor == self.currentcolor:
				for i in self.highlighted:
					self.tiles[i].highlight()
				self.highlighted = []
				for i in self.accessible(p):
					self.tiles[i].highlight()
					self.highlighted.append(i)
				if len(self.highlighted) > 0:
					self.source = p
				else:
					self.state = 2

	def accessible(self, p):
		r = p.row
		c = p.col
		targets = []
		if p.piecekind == "king":
			for i in [-1, 0, 1]:
				for j in [-1, 0, 1]:
					if i == 0 and j == 0:
						continue
					a = r +i
					b = c + j
					s = self.good(a, b)
					if s > 1:
						targets.append((a, b))
			return targets
		
		if p.piecekind == "knight":
			for a, b in zip([2, 2, -2, -2, 1, 1, -1, -1],
							[1, -1, 1, -1, 2, -2, 2, -2]):
				a = r + a
				b = c + b
				if self.good(a, b) > 1:
					targets.append((a, b))
			return targets
		
		if "pawn" in p.piecekind:
			if "wp" in p.piecekind: #white pawn
				s = self.good(r+1, c)
				if s > 1:
					targets.append((r+1, c))
				if s == 2 and "prime" in p.piecekind:
					if self.good(r+2, c) > 1:
						targets.append((r+2, c))
			else: #black pawn
				s = self.good(r-1, c)
				if s > 1:
					targets.append((r-1, c))
				if s == 2 and "prime" in p.piecekind:
					if self.good(r-2, c) > 1:
						targets.append((r-2, c))
			return targets
		
		if p.piecekind in "rook queen":
			dirs = [True, True, True, True] #up, down, left, right
			for i in range(1, 9):
				for pair, index in zip([(r-i, c), (r+i, c), (r, c-i), (r, c+i)],
				[0, 1, 2, 3]):
					if not dirs[index]:
						continue
					s = self.good(pair[0], pair[1])
					if s < 2:
						dirs[index] = False
					elif s == 2:
						targets.append(pair)
					else:
						targets.append(pair)
						dirs[index] = False

		if p.piecekind in "bishop queen":
			dirs = [True, True, True, True]
			for i in range(1, 9):
				#upleft = lower row and column
				#upright = lower row, raise column
				#downleft = raise row, lower column
				#downright = raise row and column
				for pair, index in zip([(r-i, c-i), (r-i, c+i), (r+i, c-i), (r+i, c+i)],
										[0, 1, 2, 3]):
					if not dirs[index]:
						continue
					s = self.good(pair[0], pair[1])
					if s < 2:
						dirs[index] = False
					elif s == 2:
						targets.append(pair)
					else:
						targets.append(pair)
						dirs[index] = False
		return targets
	
	def good(self, r, c):
		if not (9 > r > 0 and 9 > c > 0):
			return 0
		if self.tiles[(r, c)].piececolor == self.currentcolor:
			return 1
		elif self.tiles[(r, c)].piececolor is None:
			return 2
		else:
			return 3

program = Tk()
program.title("Chess Py")
app = Chess(program)
program.mainloop()