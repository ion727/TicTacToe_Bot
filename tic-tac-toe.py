'''
arbitraty decisions: the bot will play X, the player will play O. X will be considered 1 and O will be -1.
X will move first.
'''
from time import sleep
from copy import deepcopy
from random import randint


class State:
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
        self.parent = None
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
                    new.parent = self
                    new.failsafe = self.failsafe + 1
                    new.grid[y][x] = "X" if self.playermove == 1 else "O"
                    new.playermove = self.playermove * -1 # other player's turn.
                    
                    # break out of calculate() when a winning move is found
                    new.value = new.getStateValue()
                    if new.value == self.playermove:
                        self.moves.append(new)
                        self.bestmove = new
                        self.value = new.value
                        #print(f"win for {("","X","O")[self.value]}:\n"+str(self),"\n\n")
                        #return self.value
                    
                    self.moves.append(new) 
        
        values = [state.calculate() for state in self.moves]
        self.move_and_value = list(zip(self.moves, values))
        self.move_and_value.sort(key=lambda x: x[1],reverse=self.playermove==1)
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

Xwins = State([[" ", " ", " "],
               [" ", " ", " "],
               [" ", " ", " "]])
#Xwins.calculate()
#print(Xwins.value,"\n\n+\n+\n+\n+\n+\n")


grid = Xwins
grid.calculate()
end = False
playermove = grid.playermove
print(end="\n\n")
while not grid.IsGameOver():
    print(str(grid))
    print(f"\r\x1b[6A",end = "")
    valid = False
    while not valid:
        if playermove == -1:
            move = input("Enter a move (Format: XY):   \x1b[2D")
            print("\x1b[1A",end="")   
            x,y = int(move[0]) - 1, int(move[1]) - 1
            if grid.grid[y][x] == " ":
                grid.grid[y][x] = "O"
                grid = grid.FindMove()
                valid = True
            else: 
                print("\x1b[1BInvalid Move. Please try again.\r\x1b[1A",end="")
                continue
        else:
            grid = grid.bestmove
            valid = True
    print("\n")     
    playermove *= -1
    sleep(0.5)
print(f"{str(grid)}\n{("No player","X","O")[grid.value]} wins.")
