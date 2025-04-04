'''
arbitraty decisions: the bot will play X, the player will play O. X will be considered 1 and O will be -1.
X will move first.
'''
from time import sleep
from copy import deepcopy
from random import randint


class State:
    StatesExplored = 0
    def __init__(self, *args):
        if len(args) == 1:
            args = args[0]
        if len(args) == 9:
            self.grid = [args[:3], args[3:6], args[6:9]]
        elif type(args) == list and len(args) != 0 and type(args[0]) == list and all(len(row) == 3 for row in args):
            self.grid = deepcopy(args)
        else:
            self.grid = [[" " for _ in range(3)] for _ in range(3)]
        self.value = self.getStateValue()
        self.failsafe = sum([1 for row in self.grid for square in row if square != " "]) # to ensure infinite looping is impossible
        self.moves = []
        self.WinningFinalStates = 0
        self.bestmove = None

        # calculate who's move it is by counting the number of Xs and Os.
        self.playermove = 1 if sum([1 for row in self.grid for square in row if square == "X"]) <= sum([1 for row in self.grid for square in row if square == "O"]) else -1
        #print("Value:",self.value)
    def __str__(self):
        return "\n".join([" ".join("".join([f"[{square}]"for square in row])) for row in self.grid])+"\n"
    def getStateValue(self):
        value = 0
        def MatchValue(square):
            if square == "X":
                return 1
            if square == "O":
                return -1
            return 0
        for i in range(3):
            if self.grid[i][0] == self.grid[i][1] == self.grid[i][2] != " ":
                value = MatchValue(self.grid[i][0])
            if self.grid[0][i] == self.grid[1][i] == self.grid[2][i] != " ":
                value = MatchValue(self.grid[0][i])
        if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] != " ":
            value = MatchValue(self.grid[0][0])
        if self.grid[0][2] == self.grid[1][1] == self.grid[2][0] != " ":
            value = MatchValue(self.grid[0][2])
        return value
    def calculate(self):
        print(f"Moves Analysed: {State.StatesExplored}\r", end="")
        State.StatesExplored += 1
        # break out if game is over
        if self.value != 0:
            #print(str(self), self.value, "\n")
            return self.value

        # recursively scan every possible move until all ends are found,
        # then minmax the values 
        if self.IsGameOver():
            self.value = self.getStateValue()
            #print(str(self), self.value, "\n")
            return self.value
        if self.failsafe > 9:
            raise Exception("Somewhere be loopin too much cuz we got more than 9 layers.\nHeres the state:" + str(self))
        # find each empty square and create a new state associated to it
        #self.iteration = 0
        for y, row in enumerate(self.grid):
            for x, square in enumerate(row):
                #self.iteration += 1
                if square == " ":
                    #print(self.failsafe, self.iteration,"is valid.")
                    new = State(self.grid)
                    new.failsafe = self.failsafe + 1
                    new.grid[y][x] = "X" if self.playermove == 1 else "O"
                    new.playermove = self.playermove * -1 # other player's turn.
                    new.value = new.getStateValue()               
                    self.moves.append(new) 
        
        values = [state.calculate() for state in self.moves]
        self.WinningFinalStates += sum(move.WinningFinalStates for move in self.moves)
        self.move_and_value = list(zip(self.moves, values))
        # add a tiebreaking weight to "value" to favour moves which set up for a win.
        self.WinningFinalStates += sum(move.value for move in (pair[0] for pair in self.move_and_value) if move.value * self.playermove >= 1)
        # sort first based on value (x[1]) and then descending based on the tiebreaker (-x[0].WinningFinalStates)
        self.move_and_value.sort(key=lambda x: (x[0].value,-x[0].WinningFinalStates),reverse=self.playermove==1)
        self.bestmove, self.value = self.move_and_value[0]
        return self.value
    def IsGameOver(self):
        gridfilled = all(square != " " for row in self.grid for square in row)
        gameover = self.getStateValue() != 0
        return gridfilled or gameover
    def FindMove(self):
        # Can only be used after changing a square in self.grid .
        # Returns the calculated state that corresponds with 
        # the player's move
        PlayedMove = next(move for move in self.moves if move.grid == self.grid)
        #print("\n\n\n\nBot's best move:\n"+str(PlayedMove.bestmove))
        if PlayedMove == None:
            raise ValueError("Invalid move: unable to find move in calculated list.")
        return PlayedMove



def main():
    start = [[" "," "," "],
            [" "," "," "],
            [" "," "," "]]
    start[randint(0,2)][randint(0,2)] = "X"
    grid = State(start)
    grid.calculate()
    playermove = grid.playermove
    spaces = 2 # Spacing for formatting
    print(f"Ready!{' '*30}\n")
    sleep(0.5)
    # game loop
    while not grid.IsGameOver():
        print(str(grid))
        print(f"\r\x1b[6A",end = "")
        if playermove == -1:
            # Loop till valid move inputted

            while True:
                move = input(f"Enter a move (Format: XY): {" "*spaces+"\x1b[1D"*spaces}")
                spaces = len(move)
                try:
                    x,y = int(move[0]) - 1, int(move[1]) - 1
                except:
                    print("Invalid input. Please try again.\r\x1b[2A")
                    continue
                else:
                    print(" "*32+"\r\x1b[1A",end="")
                if grid.grid[y][x] == " ":
                    grid.grid[y][x] = "O"
                    grid = grid.FindMove()
                    break
                else: 
                    print("\x1b[1BInvalid Move. Please try again.\r\x1b[1A",end="")
        else:
            grid = grid.bestmove
        print("\n") 
        playermove *= -1
        sleep(0.5)

    for i in range(3):
        if grid.grid[i][0] == grid.grid[i][1] == grid.grid[i][2] != " ":
            grid.grid[i][0] = grid.grid[i][1] = grid.grid[i][2] = "█"
        if grid.grid[0][i] == grid.grid[1][i] == grid.grid[2][i] != " ":
            grid.grid[0][i] = grid.grid[1][i] = grid.grid[2][i] = "█"
    if grid.grid[0][0] == grid.grid[1][1] == grid.grid[2][2] != " ":
        grid.grid[0][0] = grid.grid[1][1] = grid.grid[2][2] = "█"
    if grid.grid[0][2] == grid.grid[1][1] == grid.grid[2][0] != " ":
        grid.grid[0][2] = grid.grid[1][1] = grid.grid[2][0] = "█"
    print(f"{str(grid)}\n{("No player","X","O")[grid.value]} wins.")
if __name__ == "__main__":
    main()