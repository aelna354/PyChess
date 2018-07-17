# aelna354's PyChess Game

A chess game I made in Python 3 using Tkinter. After my successes in creating both my YouTube-DL GUI and the Autoclicker in Tkinter, I thought it'd be fun to do this. Unlike those other projects, this one is made purely for recreation and doesn't have any practical intentions; it's not something I intend to use as I'm honestly not a big fan of chess. Still greatly enjoyed making this and am honestly quite proud of my work :)

![](photo1.png?raw=true)
![](photo2.png?raw=true)

## Rules

No AI, only 2 player mode. Game plays on a board of 8x8 tiles. One player controls white pieces, other black pieces, white piece player goes first. Game is played in turns; during each turn, the turn player must move exactly one of their pieces.

To do this, first, click the piece you would like to move; all tiles this piece may travel to will be highlighted. Click any of those highlighted tiles to move that piece to it. (After you click on a piece to move, before you click on a highlighted tile, you can click on a different piece of that color; and the highlighted destinations will change accordingly.)

Pieces can only move to a tile that is unoccupied or is occupied by a piece of the opposite color. In the case of the latter, the previously occuping piece is removed from play. Each piece has rules governing it's movement:

* A Pawn can move forward one space, two if it hasn't moved yet. **(En passant has NOT been implemented!)** When a pawn reaches the other end of the board, the player who controls it must promote it to, of their choice: a Queen, Bishop, Knight or Rook.
* A Rook can move any number of spaces vertically, or any number of spaces horizontally. **(Castling has NOT been implemented!)**
* A Bishop can move any number of spaces diagonally.
* A Queen move any number of spaces diagonally, vertically or horizontally.
* A King can move 1 space in any direction.
* A Knight can move in an L-shape (two vertical, one horizontal, or two horizontal, one vertical). Note that knights are the *only* pieces that can jump over other pieces.

The objective of the game is to "checkmate" the opponent by removing their king from play. The game ends when this is acheived, with the remaining king's team winning.

(Note: normally in chess, a player is not allowed to put themselves in a position where the opponent can checkmate them. This rule is not enforced in this implementation.)

## Installation & Setup

Install Python 3 if it is not already installed. Aftwards, download the [latest release](https://github.com/aelna354/PyChess/blob/master/release.zip?raw=true) and extract it to any folder on your computer. With Windows, simply double click the app.cmd file to start the game; for other OSs, run "python chess.py" in the command line.

Chess piece images credited to: https://commons.wikimedia.org/wiki/Category:PNG_chess_pieces/Standard_transparent