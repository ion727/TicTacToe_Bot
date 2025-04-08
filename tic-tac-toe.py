'''
arbitraty decisions: the bot will play X, the player will play O. X will be considered 1 and O will be -1.
X will move first.
'''
from time import sleep
from copy import deepcopy
from random import randint, choice

class TerminateProgram(Exception): pass
    
class State:
    TotalStatesExplored = 0
    # Create a set to ensure no duplicate values are stored 
    StatesExploredID = []
    StatesExplored = []

    def __init__(self, *args, playermove = 1):
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
        self.ID = None
        self.GenerateID()

        # calculate who's move it is by counting the number of Xs and Os.
        self.playermove = playermove if sum([1 for row in self.grid for square in row if square == "X"]) <= sum([1 for row in self.grid for square in row if square == "O"]) else -1*playermove
    def __str__(self):
        return "\n".join([" ".join("".join(["[{}]".format(square) for square in row])) for row in self.grid])+"\n"
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
        # Ensure this move has not already been checked.
        if self.GenerateID() in State.StatesExploredID:
            Location = State.StatesExploredID.index(self.ID)
            self.__dict__ = State.StatesExplored[Location].__dict__
            return self.value
        else:
            State.StatesExploredID.append(self.ID)
            State.StatesExplored.append(self)
        
        # recursively scan every possible move until all ends are found,
        # find best move
        print("Moves Analysed: {}\r".format(State.TotalStatesExplored), end="")
        State.TotalStatesExplored += 1
        
        # break out if game is over
        if self.value != 0 or self.IsGameOver():
            return self.value
        
        # Prevent infinite looping
        if self.failsafe > 9:
            raise Exception("Somewhere be loopin too much cuz we got more than 9 layers.\nHeres the state:" + str(self))
        # find each empty square and create a new state associated to it
        for y, row in enumerate(self.grid):
            for x, square in enumerate(row):
                if square == " ":
                    #print(self.failsafe, self.iteration,"is valid.")
                    new = State(self.grid)
                    new.failsafe = self.failsafe + 1
                    new.grid[y][x] = "X" if self.playermove == 1 else "O"
                    new.playermove = self.playermove * -1 # other player's turn.
                    new.value = new.getStateValue()               
                    self.moves.append(new) 
        if len(self.moves) == 0:
            return self.getStateValue()
        # Find value of all child moves
        values = [state.calculate() for state in self.moves]
        
        # add a tiebreaking weight to favour moves which set up for a win.
        self.WinningFinalStates += sum(move.WinningFinalStates for move in self.moves)
        self.move_and_value = list(zip(self.moves, values))
        self.WinningFinalStates += sum(move.value for move in (pair[0] for pair in self.move_and_value) if move.value * self.playermove >= 1)
        # sort first based on value (x[0].value) and then descending based on the tiebreaker (-x[0].WinningFinalStates)
        self.move_and_value.sort(key=lambda x: (x[0].value,-x[0].WinningFinalStates),reverse=self.playermove==1)
        # Select best move and best and use obtain its value.
        self.bestmove, self.value = self.move_and_value[0]
        del self.move_and_value
        return self.value
    def IsGameOver(self):
        gridfilled = all(square != " " for row in self.grid for square in row)
        gameover = self.getStateValue() != 0
        return gridfilled or gameover
    def FindMove(self):
        # Can only be used after changing a square in self.grid .
        # Returns the calculated state that corresponds with 
        # the player's move
        try:
            PlayedMove = next(move for move in self.moves if move.grid == self.grid)
            return PlayedMove
        except StopIteration:
            raise ValueError("Invalid move: unable to find move in calculated list.")
    def GenerateID(self):
        self.ID = "".join("".join([square for square in row]) for row in self.grid)
        return self.ID

# ======================================================================================================== #

def main():
    start = [[" "," "," "],
             [" "," "," "],
             [" "," "," "]]
    playermove = choice([-1,1])
    if playermove == 1:
        start[randint(0,2)][randint(0,2)] = "X"
    grid = State(start, playermove=playermove)
    grid.calculate()
    print("Ready!{}\n".format(' '*30))
    sleep(0.5)
    playermove = -1
    spaces = 2 # Spacing for formatting
    # game loop
    while not grid.IsGameOver():
        print(str(grid))
        print("\r\x1b[6A",end = "")
        if playermove == -1:
            # Loop till valid move inputted
            while True:
                move = input("Enter a move (Format: XY): {}".format(' '*spaces+'\x1b[1D'*spaces))
                if move == "end":
                    raise TerminateProgram()
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
    print("{}\n{} wins.".format(str(grid),("No player","X","O")[grid.value]))
if __name__ == "__main__":
    while True:
        try:
            main()
        except KeyboardInterrupt:
            print(end=57*" " + "\r")
            continue
        except TerminateProgram:
            print(end="\x1b[1A")
            break