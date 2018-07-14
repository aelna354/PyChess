# aelna354's PyChess Game

A chess game I made in Python 3 using Tkinter. After my successes in creating both my YouTube-DL GUI and the Autoclicker in Tkinter, I thought it'd be fun to do this. Unlike those other projects, this one is made purely for recreation and doesn't have any practical intentions; it's not something I intend to use as I'm honestly not a big fan of chess.

This is a chess game designed to simulate a game of chess.

# Rules

Game plays on a tile of 8x8 boards. No AI, only 2 player mode. One player controls white pieces, other black pieces, white piece player goes first. Game is played in turns; during each turn, the turn player must move exactly one of their pieces. Each piece has rules governing it's movement:

* A Pawn can move forward one space, two if it hasn't moved yet.
* A Rook can move any number of spaces vertically, or any number of spaces horizontally.
* A Bishop can move any number of spaces diagonally.
* A Queen move any number of spaces diagonally, vertically or horizontally.
* A King can move 1 space in any direction.
* A Knight can move in an L-shape (two vertical, one horizontal, or two horizontal, one vertical).

When a piece moves to a tile occupied by another piece, the piece previously on that tile is removed from play. A piece cannot move to a tile occupied by a piece of the same color.

The objective of the game is to remove the opponent's king from play. The game ends when this is acheived, with the remaining king's team winning.

When a pawn reaches the other end of the board, the player who controls it must promote it to, of their choice: a Queen, Bishop, Knight or Rook.

# Installation & Setup

With Python 3 installed, all you have to do is download app.cmd and chess.py, and double click app.cmd to launch the game.

Chess piece images credited to: https://commons.wikimedia.org/wiki/Category:PNG_chess_pieces/Standard_transparent