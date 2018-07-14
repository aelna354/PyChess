# Rules
Normal Chess board set up.

-Pawns who are in their initial position can move one or two spaces forwards. Afterwards, they can only move one space forwards.
-Rooks can move to the left, right, forward or back any spaces.
-Bishops only move diagonally.
-Knights move in an L shape; two horizontally, than one vertically, OR two vertically, than one horizontally.
-Queen moves diagonally, horizontally, or straight.
-King moves one space in any direction.
-For the sake of this game, we will set aside castling, el passant, and rules that force an opponent to exit check, and the checking/enforcement of checkmate.

The board is represented as an 8x8 array of tiles. Tiles are made white and black.
Each tile has the following variables:
-Row value and column black.
-A piece variable, which may be unfilled (if there is no piece on it).
-A list consisting of all possible moves a certain piece can make from there.
Each piece consists of:
-A name (black pawn, black rook, white queen, etc)
-An image associated with that name
-A direction (downwards for white pieces, upwards for black)
