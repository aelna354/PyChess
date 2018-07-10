from tkinter import *

class Chess(Frame):
	def __init__(self, master):
		board = Frame(master)
		self.tiles = []
		index = 1
		for i in range(0, 8):
			self.tiles.append([])
			for j in range(0, 8):
				b = Button(board, command=lambda index=index: self.click(index))
				index += 1
				self.tiles[i].append(b)
				self.tiles[i][-1].grid(row=i,column=j)
		for i in [0, 2, 4, 6]:
			for j in range(0, 8):
				if j % 2 == 0:
					self.tiles[i][j]['bg'] = 'grey'
				else:
					self.tiles[i][j]['bg'] = 'white'
		for i in [1, 3, 5, 7]:
			for j in range(0, 8):
				if j % 2 == 0:
					self.tiles[i][j]['bg'] = 'white'
				else:
					self.tiles[i][j]['bg'] = 'grey'
		self.assignImages()
		Button(text="Start Game", width=10, command=self.begin).grid(row=8,column=3)
		board.grid(row=0, column=0, rowspan=7, columnspan=7)

	def assignImages(self):
		self.pieces = [
		PhotoImage(file="images/whitepawn.png"), PhotoImage(file="images/blackpawn.png"),
		PhotoImage(file="images/whiterook.png"), PhotoImage(file="images/blackrook.png"),
		PhotoImage(file="images/whiteknight.png"), PhotoImage(file="images/blackknight.png"),
		PhotoImage(file="images/whitequeen.png"), PhotoImage(file="images/blackqueen.png"),
		PhotoImage(file="images/whitebishop.png"), PhotoImage(file="images/blackbishop.png"),
		PhotoImage(file="images/whitepawn.png"), PhotoImage(file="images/blackpawn.png"),
		]
		for i in range(0, 8):
			self.tiles[1][i]['image'] = self.pieces[1]
			self.tiles[6][i]['image'] = self.pieces[0]
	def click(self, index):
		print(index)
	def begin(self, index):
		print("B")

program = Tk()
program.title("YouTube-DL Basic GUI")
app = Chess(program)
program.mainloop()