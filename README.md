# TicTacToe-Bot
Play the classic tic-tac-toe against AI!

This program uses ASCII-art to display a tic-tac-toe board, wherein the player then inputes X;Y coordinates to play.

The bot will automatically play after the player's move.

## Instructions
- run `python3 tic-tac-toe.py` in your command line.
- enter moves following `[column];[row]` considering 1;1 to be the top left square and 3;3 the bottom right.
- the Enter key can be pressed instead of a move to play a random move.
    - **NOTE: RAPIDLY PRESSING THE ENTER KEY OR ANY OTHER NEWLINE METHOD WITHOUT AWAITING MOVE PROCESSING WILL BREAK THE DISPLAY.**
- to **end the current game**, use a Keyboard Interrupt `ctrl + c` 
- to **terminate the entire program**, type `end` when prompted for a move.

## Coming Soon (Well, eventually I guess)
### Optimization
- Alpha-Beta pruning
### Quality of Life (QoL)
- Auto-move for garanteed ties
- Clicking boxes instead of typing moves (TBD)
