from tkinter import *
import webbrowser, time

program = Tk()
program.title("Chess Py")
selectable = False
selected = StringVar()

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
	def __init__(self, row, col):
		self.blank = {"grey": PhotoImage(file="images/greyblank.png"), "white": PhotoImage(file="images/whiteblank.png")}
		self.row = row
		self.col = col
		if (row + col) % 2 == 0:
			self.color = "white"
		else:
			self.color = "grey"
		self.button = Button(command=self.click, bg=self.color)
		self.piece = None
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
		self.button['image'] = self.blank[self.color]

	def placePiece(self, newPiece):
		self.piece = newPiece
		self.button['image'] = self.piece.image

	def click(self):
		if selectable and (self.piece is not None):
			selected.set(str(self.row) + str(self.column))
		selectable = False
		
class Chess(Frame):
	def __init__(self, master):
		self.master = master
		board = Frame(master)
		self.tiles = {}

		for i in range(1, 9):
			for j in range(1, 9):
				self.tiles[(i, j)] = Tile(i, j)

		self.initBoard()
		for key, val in self.tiles.items():
			val.button.grid(row=key[0], column=key[1])

		self.turn = IntVar()
		self.turn.set(1)
		self.currentturn = StringVar()
		self.turncount = StringVar()
		self.state = StringVar()
		self.source = StringVar()
		self.dest = StringVar()

		Entry(textvariable=self.turncount, state='disabled').grid(row=9, column=1, columnspan=3)
		self.button = Button(text="Start Game", bg="green", command=self.begin)
		self.button.grid(row=9, column=4)
		Entry(textvariable=self.currentturn, state='disabled').grid(row=9, column=5, columnspan=3)

		Label(text="Source").grid(row=10, column=1, columnspan=2)
		Entry(textvariable=self.source, state='disabled').grid(row=10, column=3, columnspan=2)
		Label(text="Destination").grid(row=10, column=5, columnspan=2)
		Entry(textvariable=self.dest, state='disabled').grid(row=10, column=7, columnspan=2)
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
		self.button.grid_remove()
		self.turncount.set("Turn Count: 1")
		self.currentturn.set("Current Turn: White")
		self.state.set("Waiting for White to pick source...")

	def runTurn(self):
			self.turncount.set("Turn Count: " + str(self.turn))
			if turn % 2 == 0:
				self.currentturn.set("Current Turn: Black")
			else:
				self.currentturn.set("Current Turn: White")
			selectable = True
			self.wait()
			finished = True
			targets = self.tiles[(selected[0], selected[1])].getTargets()
			print(targets)

app = Chess(program)
program.mainloop()