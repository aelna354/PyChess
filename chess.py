from tkinter import *
from tkinter import messagebox
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
		for i in ["grey", "white", "orange"]:
			self.blank[i] = PhotoImage(file="images/"+i+"blank.png")

		self.images = {}
		for i in ["black", "white"]:
			for j in ["knight", "rook", "pawn", "bishop", "king", "queen"]:
				self.images[i+j] = PhotoImage(file="images/"+i+j+".png")

		self.button = Button(command=lambda:clickmethod(self), bg=self.color)
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
				self.piecekind = kind[:-5]
			
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
		for i in range(1, 9):
			for j in range(1, 9):
				self.tiles[(i, j)] = Tile(i, j, self.click)
				self.tiles[(i, j)].button.grid(row=i, column=j)
		self.initBoard()

		self.turn = IntVar()
		self.turn.set(1)
		self.currentturn = StringVar()
		self.currentturn.set("Waiting to Start")
		self.highlighted = []
		self.source = None
		self.state = 1 #1 for not playing, 2 for waiting for piece to move, 3 for waiting for destination

		turnc = Frame(master)
		Label(turnc, text="Turn Count: ", justify=LEFT).grid(row=0, column=0, sticky=W)
		Label(turnc, textvariable=self.turn).grid(row=0, column=1, sticky=W)
		turnc.grid(row=9, column=1, columnspan=2, sticky=W)

		self.actionbutton = Button(text="Start Game", bg="green", command=self.action)
		self.actionbutton.grid(row=9, column=4, columnspan=2, sticky=W)

		Label(textvariable=self.currentturn).grid(row=9, column=7, columnspan=2, sticky=W)

		hyperlink = Label(text="Source Code", fg="blue4", cursor="hand2")
		hyperlink.bind("<Button-1>", lambda x: webbrowser.open_new(r"https://github.com/aelna354/PyChess/"))
		hyperlink.grid(row=10,column=7,columnspan=2, sticky=W)

	def initBoard(self):
		for i in [3, 4, 5, 6]:
			for j in range(1, 9):
				self.tiles[i, j].clear()
		for i in range(1, 9):
			self.tiles[2, i].placePiece("black", "bpawnprime", deprime=False)
			self.tiles[7, i].placePiece("white", "wpawnprime", deprime=False)
		for i in [1, 8]:
			self.tiles[1, i].placePiece("black", "rook")
			self.tiles[8, i].placePiece("white", "rook")
		for i in [2, 7]:
			self.tiles[1, i].placePiece("black", "knight")
			self.tiles[8, i].placePiece("white", "knight")
		for i in [3, 6]:
			self.tiles[1, i].placePiece("black", "bishop")
			self.tiles[8, i].placePiece("white", "bishop")
		self.tiles[1, 4].placePiece("black", "king")
		self.tiles[1, 5].placePiece("black", "queen")
		self.tiles[8, 4].placePiece("white", "king")
		self.tiles[8, 5].placePiece("white", "queen")

	def initGame(self):
		self.actionbutton['text'] = "Reset Game"
		self.actionbutton['bg'] = 'yellow'
		self.turn.set(1)
		self.currentturn.set("Current Turn: White")
		self.currentcolor = "white"
		self.state = 2

	def action(self):
		if self.state == 1:
			self.initGame()
		else:
			if messagebox.askyesno("Restart Game?", "Are you sure you'd like to restart the game?"):
				self.unhighlight()
				self.initBoard()
				self.initGame()
				print(len(self.highlighted))

	def unhighlight(self):
		for i in self.highlighted:
			self.tiles[i].highlight()
		self.highlighted = []		

	def click(self, p):
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
			victory = False
			if p.highlighted:
				if p.piecekind == "king":
					victory = True
				p.placePiece(self.source.piececolor, self.source.piecekind)

				self.source.clear()
				self.source = None
				self.state = 2
				self.turn.set(self.turn.get() + 1)
				self.unhighlight()
				if self.currentcolor == "white":
					self.currentcolor = "black"
					self.currentturn.set("Current Turn: Black")
				else:
					self.currentcolor = "white"
					self.currentturn.set("Current Turn: White")

				if (not victory) and ("pawn" in p.piecekind) and (not "prime" in p.piecekind) and (not (8 > p.row > 1)):
					p.highlight()
					p.placePiece(p.piececolor, self.promotePawn())
					p.highlight()

				if victory:
					self.state = 4
					self.currentturn.set("Winner: " + p.piececolor.capitalize())
					messagebox.showinfo("Victory!", "The player controlling the " + p.piececolor.capitalize() + " pieces has won the game.")

			elif p.piececolor == self.currentcolor:
				self.unhighlight()
				for i in self.accessible(p):
					self.tiles[i].highlight()
					self.highlighted.append(i)
				if len(self.highlighted) > 0:
					self.source = p
				else:
					self.state = 2

	def promotePawn(self):
		kind = StringVar()
		kind.set("queen") #if popup is closed
		popup = Toplevel()
		popup.resizable(False, False)
		popup.title('Promote Pawn')
		Label(popup, text="Congratulations! You can now promote this pawn to any of the following:").grid(row=0, column=0)
		opts = ["Queen", "Rook", "Bishop", "Knight"]
		optsframe = Frame(popup)
		for i in range(0, 4):
			Button(optsframe, text=opts[i], command=lambda i=i:[kind.set(opts[i].lower()), popup.destroy()]).grid(row=0, column=i)
		optsframe.grid(row=1, column=0)
		popup.grab_set()
		popup.wait_window(popup)
		return kind.get()
		
	def accessible(self, p):
		r = p.row
		c = p.col
		targets = []

		if p.piecekind == "king":
			for i in [-1, 0, 1]:
				for j in [-1, 0, 1]:
					if i == 0 and j == 0:
						continue
					a = r + i
					b = c + j
					if self.good(a, b) > 1:
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
			if "bp" in p.piecekind: #black pawn
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
			dirs = [True, True, True, True] #upleft, upright, downleft, downright
			for i in range(1, 9):
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
		if not (9 > r > 0 and 9 > c > 0) or (self.tiles[(r, c)].piececolor == self.currentcolor):
			return 1
		elif self.tiles[(r, c)].piececolor is None:
			return 2
		else:
			return 3

program = Tk()
program.title("Chess Py")
app = Chess(program)
program.mainloop()