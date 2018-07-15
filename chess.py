from tkinter import *
import webbrowser

class Piece():
	def __init__(self, color, kind):
		self.color = color
		self.kind = kind
		if "pawn" not in self.kind:
			self.image = PhotoImage(file="images/"+color+kind+".png")
		else:
			self.image = PhotoImage(file="images/"+color+kind[1:]+".png")
			self.kind = self.kind + "prime"

class Tile():
	def __init__(self, row, col, clickmethod):
		self.row = row
		self.col = col
		self.piececolor = None
		if (row + col) % 2 == 0:
			self.color = "white"
		else:
			self.color = "grey"
		self.blank = {}
		for i in ["grey", "white", "orange"]:
			self.blank[i] = PhotoImage(file="images/"+i+"blank.png")
		self.button = Button(command=lambda:clickmethod(row, col), bg=self.color)
		self.piece = None
		self.highlighted = False
		self.targets = {}
		self.genTargets()

	def genTargets(self):
		for i in ["up", "down", "left", "right", "upleft", "upright", "downleft",
		"downright", "knight", "king", "bpawn", "wpawn", "wpawnprime", "bpawnprime"]:
			self.targets[i] = []

		i = self.row + 1
		while i < 9:
			self.targets["down"].append((i, self.col))
			i += 1

		i = self.row - 1
		while i > 0:
			self.targets["up"].append((i, self.col))
			i -= 1

		i = self.col + 1
		while i < 9:
			self.targets["right"].append((self.row, i))
			i += 1

		i = self.col -1
		while i > 0:
			self.targets["left"].append((self.row, i))
			i -= 1

		for i in range(1, 9):
			for pair, target in zip([(self.row - i, self.col + i), (self.row -i, self.col - i),
			(self.row + i, self.col - i), (self.row + i, self.col + i)],
			["upright", "upleft", "downleft", "downright"]):
				if self.goodTile(pair[0], pair[1]):
					self.targets[target].append(pair)

		for a, b in zip([2, 2, -2, -2, 1, 1, -1, -1],
						[1, -1, 1, -1, 2, -2, 2, -2]):
			a = self.row + a
			b = self.col + b
			if self.goodTile(a, b):
				self.targets["knight"].append((a, b))

		if self.row < 8:
			self.targets["wpawnprime"].append(((self.row+1), (self.col)))
			self.targets["wpawn"].append(((self.row+1), (self.col)))
			if self.row < 7:
				self.targets["wpawnprime"].append(((self.row+2), (self.col)))
		if self.row > 1:
			self.targets["bpawnprime"].append(((self.row-1), (self.col)))
			self.targets["bpawn"].append(((self.row-1), (self.col)))
			if self.row > 2:
				self.targets["bpawnprime"].append(((self.row-2), (self.col)))

		self.targets["king"] = []
		for i in [-1, 0, 1]:
			for j in [-1, 0, 1]:
				a = self.row + i
				b = self.col + j
				if self.goodTile(a, b):
					self.targets["king"].append((a, b))

	def goodTile(self, a, b):
		return (9 > a > 0) and (9 > b > 0) and (self.row != a or self.col != b)

	def clear(self):
		self.piece = None
		self.piececolor = None
		self.button['image'] = self.blank[self.color]

	def placePiece(self, newPiece, deprime=True):
		self.piece = newPiece
		self.piececolor = self.piece.color
		self.button['image'] = self.piece.image
		if deprime:
			if "pawnprime" in self.piece.kind:
				self.piece.kind = self.piece.kind[:-5]

	def highlight(self):
		if not self.highlighted:
			self.highlighted = True
			if self.piece is None:
				self.button['image'] = self.blank['orange']
			else:
				self.button['bg'] = 'orange'
		else:
			self.highlighted = False
			if self.piece is None:
				self.button['image'] = self.blank[self.color]
			else:
				self.button['bg'] = self.color

class Chess(Frame):
	def __init__(self, master):
		self.tiles = {}
		for i in range(1, 9):
			for j in range(1, 9):
				self.tiles[(i, j)] = Tile(i, j, self.click)
				self.tiles[(i, j)].button.grid(row=i, column=j)
		self.initBoard()
		self.turn = IntVar()
		self.turn.set(1)
		self.currentturn = StringVar()
		self.turncount = StringVar()
		self.state = StringVar()
		self.source = StringVar()
		self.dest = StringVar()

		self.startbutton = Button(text="Start Game", bg="green", command=self.begin)
		self.startbutton.grid(row=9, column=4)
		self.state = 1 #1 for not started, 2 for waiting for target piece, 3 for waiting for destination

		hyperlink = Label(text="Source Code", fg="blue4", cursor="hand2")
		hyperlink.bind("<Button-1>", lambda x: webbrowser.open_new(r"https://github.com/aelna354/PyChess/blob/master/chess.py"))
		hyperlink.grid(row=10,column=8, sticky=W)

	def initBoard(self):
		for i in range(1, 9):
			self.tiles[2, i].placePiece(Piece("white", "wpawn"), deprime=False)
			self.tiles[7, i].placePiece(Piece("black", "bpawn"), deprime=False)
		for i in [2, 7]:
			self.tiles[1, i].placePiece(Piece("white", "knight"))
			self.tiles[8, i].placePiece(Piece("black", "knight"))
		for i in [1, 8]:
			self.tiles[1, i].placePiece(Piece("white", "rook"))
			self.tiles[8, i].placePiece(Piece("black", "rook"))
		for i in [3, 6]:
			self.tiles[1, i].placePiece(Piece("white", "bishop"))
			self.tiles[8, i].placePiece(Piece("black", "bishop"))
		self.tiles[1, 4].placePiece(Piece("white", "king"))
		self.tiles[1, 5].placePiece(Piece("white", "queen"))
		self.tiles[8, 4].placePiece(Piece("black", "king"))
		self.tiles[8, 5].placePiece(Piece("black", "queen"))
		for i in [3, 4, 5, 6]:
			for j in range(1, 9):
				self.tiles[i, j].clear()

	def begin(self):
		self.startbutton.grid_remove()
		Label(text="Turn Count: ").grid(row=9, column=1, sticky=W)
		Label(textvariable=self.turn).grid(row=9,column=2, columnspan=3, sticky=W)
		Label(textvariable=self.currentturn).grid(row=9, column=6, columnspan=3)
		self.turncount.set("Turn Count: " + str(self.turn.get()))
		self.currentturn.set("Current Turn: White")
		self.currentcolor = "white"
		self.state = 2
		self.highlighted = [] #list of possible destinations
		self.source = None

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
				p.placePiece(self.source.piece)
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
		if p.piece.kind in "wpawn bpawn king knight": #all of these move only one space and knight jumps, so they don't need deep error checking
			targets = []
			for i in p.targets[p.piece.kind]:
				if self.tiles[(i[0], i[1])].piececolor != p.piececolor:
					targets.append(i)
			return targets

		if p.piece.kind in "wpawnprime bpawnprime":
			targets = []
			possible = p.targets[p.piece.kind]
			if self.tiles[possible[0]].piececolor != p.piececolor:
				targets.append(possible[0])
				if (self.tiles[possible[0]].piececolor is None) and (len(possible) > 1):
					if self.tiles[possible[1]].piececolor != p.piececolor:
						targets.append(possible[1])
			return targets
		
		up = []
		down = []
		left = []
		right = []
		upleft = []
		upright = []
		downleft = []
		downright = []

		for direction, categ in zip(["up", "down", "left",
		"right", "upleft", "upright", "downleft", "downright"],
		[up, down, left, right, upleft, upright, downleft, downright]):
			for i in p.targets[direction]:
				targetcolor = self.tiles[(i[0], i[1])].piececolor
				if targetcolor == p.piececolor:
					break
				elif targetcolor is None:
					categ.append(i)
				else:
					categ.append(i)
					break
		if p.piece.kind == "bishop":
			return upleft + upright + downleft + downright
		elif p.piece.kind == "rook":
			return up + left + down + right
		elif p.piece.kind == "queen":
			return up + left + down + right + upleft + upright + downleft + downright

program = Tk()
program.title("Chess Py")
app = Chess(program)
program.mainloop()