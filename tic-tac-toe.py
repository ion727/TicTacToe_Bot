'''
arbitraty decisions: the bot will play X, the player will play O. X will be considered 1 and O will be -1.
X will move first.
'''
from time import sleep, asctime, localtime
from copy import deepcopy
from random import randint, choice

class TerminateProgram(Exception): pass
    
class State:
    TotalStatesExplored = 0
    # Create a cache to ensure no duplicate values are stored 
    StatesExploredID = []
    StatesExplored = []

    def __init__(self, *args, FirstMove = 1, failsafe = 0):
        if len(args) == 1:
            args = args[0]
        if len(args) == 9:
            self.grid = [args[:3], args[3:6], args[6:9]]
        elif type(args) == list and len(args) != 0 and type(args[0]) == list and all(len(row) == 3 for row in args):
            self.grid = deepcopy(args)
        else:
            self.grid = [[" " for _ in range(3)] for _ in range(3)]
        self.failsafe = failsafe # to ensure infinite looping is impossible
        # Prevent infinite looping by checking the failsafe when a new state is created
        if self.failsafe > 9:
            raise Exception("Somewhere be loopin too much cuz we got more than 9 layers.\nHeres the state:\n" + str(self))
        self.value = 0
        self.moves = []
        self.WinningFinalStates = 0
        self.bestmove = None
        self.ID = None
        self.GenerateID()
        self.playermove = FirstMove      
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
                break
            if self.grid[0][i] == self.grid[1][i] == self.grid[2][i] != " ":
                value = MatchValue(self.grid[0][i])
                break
        if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] != " ":
            value = MatchValue(self.grid[0][0])
        if self.grid[0][2] == self.grid[1][1] == self.grid[2][0] != " ":
            value = MatchValue(self.grid[0][2])
        return value
    def calculate(self):
        # recursively scan every possible move until all ends are found,
        # then find best move

        # Ensure this move has not already been checked.
        if self.GenerateID() in State.StatesExploredID:
            Location = State.StatesExploredID.index(self.ID)
            self.__dict__ = State.StatesExplored[Location].__dict__
            return self.value
        else:
            State.StatesExploredID.append(self.ID)
            State.StatesExplored.append(self)
        
        # break out if game is over
        if self.IsGameOver():
            return self.value
        
        # find each empty square and create a new state associated to it
        for y, row in enumerate(self.grid):
            for x, square in enumerate(row):
                if square == " ":
                    print("Moves Analysed: {}\r".format(State.TotalStatesExplored), end="")
                    State.TotalStatesExplored += 1
                    grid = deepcopy(self.grid)
                    grid[y][x] = "X" if self.playermove == 1 else "O"
                    new = State(grid, FirstMove=self.playermove*-1, failsafe=self.failsafe+1)
                    new.value = new.calculate()
                    self.moves.append(new) 
        # if self.moves is empty, exit the function.
        if not self.moves:
            return self.getStateValue()
        # Find value of all child moves
        values = [state.value for state in self.moves]
        
        # add a tiebreaking weight to favour moves which set up for a win.
        self.WinningFinalStates += sum(move.WinningFinalStates for move in self.moves)
        self.move_and_value = list(zip(self.moves, values))
        self.WinningFinalStates += sum(move.value for move in (pair[0] for pair in self.move_and_value) if move.value * self.playermove >= 1)
        # sort first based on value (x[0].value) and then descending based on the tiebreaker (-x[0].WinningFinalStates)
        self.move_and_value.sort(key=lambda x: (x[0].value,-x[0].WinningFinalStates),reverse=self.playermove==1)
        # Unpack best move/value pair
        self.bestmove, self.value = self.move_and_value[0]
        del self.move_and_value
        return self.value
    def IsGameOver(self):
        gridfilled = all(square != " " for row in self.grid for square in row)
        self.value = self.getStateValue()
        return gridfilled or self.value != 0 # return True if no moves left or winning move.
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
    def ResetCache():
        State.TotalStatesExplored = 0
        State.StatesExploredID = []
        State.StatesExplored = []

# ======================================================================================================== #
# ======================================================================================================== #
# ======================================================================================================== #
# ======================================================================================================== #
# ======================================================================================================== #

def main(playermove):
    if playermove not in (1,-1):
        raise ValueError("main() takes one positional argument; playermove must be 1 or -1")
    start = [[" "," "," "],
             [" "," "," "],
             [" "," "," "]]
    if playermove == 1:
        start[randint(0,2)][randint(0,2)] = "X"
    grid = State(start, FirstMove=-1)
    grid.calculate()
    print("Ready!{}\n".format(' '*30))
    sleep(0.5)
    playermove = -1
    spaces = 2 # Spacing for formatting
    # game loop
    while not grid.IsGameOver():
        print(str(grid), end="\r\x1b[5A")
        if playermove == -1:
            # Loop till valid move inputted
            while True:
                move = input("Enter a move (Format: X;Y): {}".format(' '*spaces+'\x1b[1D'*spaces))
                if move == "end":
                    raise TerminateProgram()
                spaces = len(move)     
                # validation 
                try:
                    if move != "":
                        if len(move) != 3 or (len(move) > 1 and move[1] != ";"):
                            raise IndexError()
                        move = move.split(";")
                        x,y = int(move[0]) - 1, int(move[1]) - 1
                        if not (-1 < x < 3 and -1 < y < 3):
                            raise ValueError()
                except ValueError:
                    print("Invalid input. Please try again.                      \r\x1b[2A")
                    continue
                except IndexError:
                    print("Invalid input format. Example: 3;2 for column 3 row 2.\r\x1b[2A")
                    continue
                else:
                    print(" "*59+"\r\x1b[1A",end="")
                if move == "":
                    x,y = choice([(x,y) for y in range(3) for x in range(3) if grid.grid[y][x] == " "])
                if grid.grid[y][x] == " ":
                    grid.grid[y][x] = "O"
                    try:
                        grid = grid.FindMove()
                    except ValueError:
                        return grid
                    break
                else: 
                    print("\x1b[1BInvalid move. Please try again.\r\x1b[1A",end="")
        else:
            grid = grid.bestmove
        print("\n") 
        playermove *= -1
        sleep(0.5)

    for i in range(3):
        if grid.grid[i][0] == grid.grid[i][1] == grid.grid[i][2] != " ":
            grid.grid[i][0] = grid.grid[i][1] = grid.grid[i][2] = "█"
            break
        if grid.grid[0][i] == grid.grid[1][i] == grid.grid[2][i] != " ":
            grid.grid[0][i] = grid.grid[1][i] = grid.grid[2][i] = "█"
            break
    if grid.grid[0][0] == grid.grid[1][1] == grid.grid[2][2] != " ":
        grid.grid[0][0] = grid.grid[1][1] = grid.grid[2][2] = "█"
    if grid.grid[0][2] == grid.grid[1][1] == grid.grid[2][0] != " ":
        grid.grid[0][2] = grid.grid[1][1] = grid.grid[2][0] = "█"
    print("{}\n{} wins.".format(str(grid),("No player","X","O")[grid.value]))
    sleep(1)
    print("\x1b[7A" + (" "*54+"\n")*7 + "\x1b[8A")
    return 0

# ======================================================================================================== #
# ======================================================================================================== #
# ======================================================================================================== #
# ======================================================================================================== #
# ======================================================================================================== #


if __name__ == "__main__":
    playermove = 1
    while True:
        try:
            returned = main(playermove)
            State.ResetCache()
        except KeyboardInterrupt:
            print(end="\r"+57*" " + "\r")
            playermove *= -1
            State.ResetCache()
            continue
        except TerminateProgram:
            print(end="\x1b[1A")
            break
        if returned != 0:
            print("An unexpected error occured. Logging...")
            with open("ErrorLogs.txt", "a") as fp:
                fp.write("{}\nBot was unsuccessful in calculating the following move:\n{}\nPlayermove: {}\nFound in cache? {}\nCalculated moves:".format(asctime(localtime()),str(returned),returned.playermove,returned.GenerateID() in State.StatesExploredID))
                fp.writelines(["\n\n" + str(move) for move in returned.moves])
                fp.write("="*60+"\n")
            for i in range(3):
                print("Logging successful. Exiting in {}...".format(3-i), end="\n\x1b[1A")
                sleep(1)
            print(end="\r\x1b[1A")
            quit()
        else:
            playermove *= -1
