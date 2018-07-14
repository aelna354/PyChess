# Rules
Normal Chess board set up.

-Pawns who are in their initial position can move one or two spaces forwards. Afterwards, they can only move one space forwards.
-Rooks can move to the left, right, forward or back any spaces.
-Bishops only move diagonally.
-Knights move in an L shape; two horizontally, than one vertically, OR two vertically, than one horizontally.
-Queen moves diagonally, horizontally, or straight.
-King moves one space in any direction.
-For the sake of this game, we will set aside castling, el passant, and rules that force an opponent to exit check, and the checking/enforcement of checkmate.

Objective: Create a functional TKinter chess game.
The board is represented as an 8x8 array of tile.
Each tile is white or black.
Each tile may or may not have a piece on it.
Tiles should have a variable indicating the current piece on it.
Each piece consists of:
-A name (black pawn, black rook, white queen, etc)
-An image associated with that name
-A direction (downwards for white pieces, upwards for black)
Each tile should have:
-A variable indicating the piece that is on it
-A 