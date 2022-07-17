# JanggiGame

A command line, local vs local Python implementation of [Janggi](https://en.wikipedia.org/wiki/Janggi), also known as Korean chess.

![Board](/README/board.png)

## Running JanggiGame

The Python program has no dependencies, so all that is needed to run the game is a single command line entry:

`python JanggiGame.py` or `python3 JanggiGame.py`

At least Python 3.6 is needed to run the game.

## Playing JanggiGame

Once the program is running, the game will prompt each player to enter their move as from and to positions. If the move is valid, the piece will be moved and it becomes the next player's turn.

The game will print a message at each turn if a player is in check. If a player is in checkmate, the game will print which player won and quit the program.

## Features

This program simulates the board game Janggi (or Korean chess) and allows players to take turns moving their respective pieces until checkmate. 

The program consists of Piece, sub-Piece, and JanggiGame classes with methods for initializing the board with pieces in their starting positions, finding all possible moves for a piece, determining if a player is in check, and determining if a player is in checkmate.

The game will not allow a player to make a move if it is not their turn, if a move is not valid (breaks rules for movement of the piece), if a move would put the current player in check, or if a player is in checkmate.

Once a player is in checkmate, the game_state will be updated to reflect which player won.

## Testing JanggiGame

Included in this repo is a `JanggiGame_tests.py` file that contains tests ranging from a few moves to full game runs that end in checkmate. It can be run with the following command (assuming `JanggiGame.py` is in the same directory):

`python JanggiGame_tests.py` or `python3 JanggiGame_tests.py`
