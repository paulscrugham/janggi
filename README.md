# Janggi

A command line, local vs local Python implementation of [Janggi](https://en.wikipedia.org/wiki/Janggi), also known as Korean chess.

## Features

This program simulates the board game Janggi (or Korean chess) and allows players to take turns moving their respective pieces until checkmate. 

The program consists of Piece, sub-Piece, and JanggiGame classes with methods for initializing the board with pieces in their starting positions, finding all possible moves for a piece, determining if a player is in check, and determining if a player is in checkmate.

The game will not allow a player to make a move if it is not their turn, if a move is not valid (breaks rules for movement of the piece), if a move would put the current player in check, or if a player is in checkmate.

Once a player is in checkmate, the game_state will be updated to reflect which player won.
