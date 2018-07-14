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
		self.blank = {}
		for i in ["grey", "white", "orange"]:
			self.blank[i] = PhotoImage(file="images/"+i+"blank.png")
		self.row = row
		self.col = col
		self.pieceColor = None
		if (row + col) % 2 == 0:
			self.color = "white"
		else:
			self.color = "grey"
		self.button = Button(command=lambda:clickmethod(self.row, self.col), bg=self.color)
		self.piece = None
		self.highlighted = False
		self.targets = {}
		self.genTargets()

	def genTargets(self):
		verticals = []
		horizontals = []
		diagonals = []
		for i in range(1, 9):
			if i != self.row:
				verticals.append((i, self.col))
			if i != self.col:
				horizontals.append((self.row, i))
			for j in [(self.row-i, self.col-i), (self.row-i, self.col+i),
			(self.row+i, self.col-i), (self.row+i, self.col+i)]:
				if self.goodTile(j[0], j[1]):
					diagonals.append(j)
		self.targets["rook"] = verticals + horizontals
		self.targets["bishop"] = diagonals
		self.targets["queen"] = verticals + horizontals + diagonals

		self.targets["knight"] = []
		for a, b in zip([2, 2, -2, -2, 1, 1, -1, -1],
						[1, -1, 1, -1, 2, -2, 2, -2]):
			a = self.row + a
			b = self.col + b
			if self.goodTile(a, b):
				self.targets["knight"].append((a, b))

		self.targets["bpawn"] = []
		self.targets["bpawnprime"] = []
		self.targets["wpawn"] = []
		self.targets["wpawnprime"] = []
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
		if (a < 1) or (b < 1) or (a > 8) or (b > 8) or (self.row == a and self.col == b):
			return False
		return True

	def getTargets(self):
		if self.piece is not None:
			return self.targets[self.piece.kind]

	def clear(self):
		self.piece = None
		self.piececolor = None
		self.button['image'] = self.blank[self.color]

	def placePiece(self, newPiece):
		self.piece = newPiece
		self.piececolor = newPiece.color
		self.button['image'] = self.piece.image

	def highlight(self):
		if not self.highlighted:
			self.highlighted = True
			if self.piece is not None:
				self.button['bg'] = 'orange'
			else:
				self.button['image'] = self.blank['orange']
		else:
			self.highlighted = False
			if self.piece is not None:
				self.button['image'] = self.piece.image
			else:
				self.button['bg'] = self.blank[self.color]

class Chess(Frame):
	def __init__(self, master):
		self.tiles = {}
		for i in range(1, 9):
			for j in range(1, 9):
				self.tiles[(i, j)] = Tile(i, j, self.click) #reference to cal method
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
			self.tiles[2, i].placePiece(Piece("white", "wpawn"))
			self.tiles[7, i].placePiece(Piece("black", "bpawn"))
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
			for i in p.getTargets():
				if self.tiles[i].piececolor != self.currentcolor:
					self.tiles[i].highlight()
					self.highlighted.append(i)
			if len(self.highlighted) > 0:
				self.state = 3
				self.source = p
		elif self.state == 3:
			if not p.highlighted:
				return
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
			self.highted = []

program = Tk()
program.title("Chess Py")
app = Chess(program)
program.mainloop()