# TicTacToe-Bot
Play the classic tic-tac-toe against AI!

This program uses ASCII-art to display a tic-tac-toe board, wherein the player then inputes X;Y coordinates to play.

The bot will automatically play after the player's move.

## Author: ion727

A fun little project to learn about the minimax algorithm and basic optimisation.

Note: this project is completed for now, I doubt I'll come back to it.


## Instructions
- run `python3 tic-tac-toe.py` in your command line.
- enter moves following `[column];[row]` considering 1;1 to be the top left square and 3;3 the bottom right.
- the `Enter` key can be pressed instead of a move to play a random move.
    - **NOTE: RAPIDLY PRESSING THE ENTER KEY WITHOUT AWAITING MOVE UPDATE MAY BREAK THE DISPLAY.**
- to **end the current game**, type `new` when prompted for a move.
- to **terminate the entire program**, use a Keyboard Interrupt `ctrl + c` or enter `new`.

## Special thanks
### Mechanics' suggestions
- **[@isabella-onder](https://github.com/isabella-onder)** : Autoplay.
- **Felix T.** : Randomising bot's first move.

### Playtesting
- **Felix T.** & **Kurt M.** : Keybinds & input Validation.
- **Mattia U.** : Beat the bot by crashing into a winning state.
- **Margherita S.** : (totally intentionally) reaching every single losing position.
- and many more who found creative ways to disect and break the game in far too many ways.
