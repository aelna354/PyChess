from tkinter import *


class Piece():
	def __init__(self, color, kind):
		self.color = color
		self.kind = kind
		self.image = PhotoImage(file="images/"+color+kind+".png")
		if color == "black":
			self.direction = "up"
		else:
			self.direction = "black"

class Tile():
	def __init__(self, row, column, color):
		self.row = row
		self.column = column
		self.color = color
		self.index = (row-1)*8 + column
		self.button = Button(command=lambda:self.click(self.index), bg=color)
		self.piece = None

	def clear(self):
		if self.piece is not None:
			self.piece = None
			self.button['image'] = None

	def range(self):
		neighbors = []
		return neighbors

	def blank(self):
		print(self.color)
		self.button['image'] = PhotoImage(file="images/"+self.color+"blank.png")

	def placePiece(self, newPiece):
		if self.piece is not None:
			self.piece = None
		self.piece = newPiece
		self.button['image'] = self.piece.image

	def click(self, index):
		print(index)

class Chess(Frame):
	def __init__(self, master):
		board = Frame(master)
		self.tiles = {}
		for i in range(1, 9):
			for j in range(1, 9):
				print(i + j)
				if (i + j) % 2 == 0:
					self.tiles[(i, j)] = Tile(i, j, "white")
				else:
					self.tiles[(i, j)] = Tile(i, j, "grey")
			self.tiles[(i, j)].button.grid(row=i, column=j)
		self.initBoard()
		for key, val in self.tiles.items():
			self.tiles[key].button.grid(row=key[0], column=key[1])


	def initBoard(self):
		for i in range(1, 9):
			self.tiles[2, i].placePiece(Piece("white", "pawn"))
			self.tiles[7, i].placePiece(Piece("black", "pawn"))
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
				self.tiles[i, j].blank()

program = Tk()
program.title("YouTube-DL Basic GUI")
app = Chess(program)
program.mainloop()