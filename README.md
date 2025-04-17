# TicTacToe-Bot
Play the classic tic-tac-toe against AI!

This program uses ASCII-art to display a tic-tac-toe board, wherein the player then inputes X;Y coordinates to play.

The bot will automatically play after the player's move.

## Instructions
- run `python3 tic-tac-toe.py` in your command line.
- enter moves following `[column];[row]` considering 1;1 to be the top left square and 3;3 the bottom right.
- the `Enter` key can be pressed instead of a move to play a random move.
- to **end the current game**, type `new` when prompted for a move.
    - **NOTE: RAPIDLY PRESSING THE ENTER KEY WITHOUT AWAITING MOVE UPDATE WILL BREAK THE DISPLAY.**
- to **terminate the entire program**, use a Keyboard Interrupt `ctrl + c`.

## Coming Soon (Well, eventually I guess)
### Optimization
- Alpha-Beta pruning
### Quality of Life (QoL)
- Auto-move for garanteed ties
- Clicking boxes instead of typing moves (TBD)
