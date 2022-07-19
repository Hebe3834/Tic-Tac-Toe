class Board:
    '''Represents a dim-by-dim tic-tac-toe board'''

    def __init__(self, dim):
        '''
        Creates a dim-by-dim tic-tac-toe board
        Assumes dim is a positive int
        '''
        self.dim = dim
        self.lastTok = ""
        self.grid = self.new_grid(dim)

    def new_grid(self, dim):
        self.dim = dim
        return [[" " for i in range(self.dim)] for j in range(self.dim)]

    def row(self, r):
        '''Returns one row of the board, formatted for printing'''
        return " " + " | ".join(self.grid[r]) + " "

    def __str__(self):
        '''Returns the formatted board'''
        hline = "\n"
        for i in range(self.dim):
            hline += "----"
        hline += "\n"
        rows = []
        for i in range(self.dim):
            rows.append(self.row(i))
        b = hline.join(rows)
        return b

    def __repr__(self):
        '''Returns the board as a list'''
        return str(self.grid)

    def play(self, token, coord):
        '''
        Attempts to place token in the position (coord[0], coord[1])
        If it is a valid move updates the board
        Checks if the current player has won the game
        '''
        if not (len(coord) == 2 and coord[0].isdigit() and coord[1].isdigit()):
            print("Please enter two numbers in the format x,y")
            return False
        x = int(coord[0])
        y = int(coord[1])
        if token == self.lastTok:
            print("It is not your turn, " + token + ". Please try again. (Incorrect token)")
        elif not (0 <= x < self.dim and 0 <= y < self.dim and len(coord) == 2):
            print("Coordinates mush be a list of two ints from 0 to " + str(self.dim) + ". Please try again.")
        elif self.grid[y][x] != " ":
            print("This box is already taken. Please try again.")
        else:
            self.lastTok = token
            self.grid[y][x] = token
            # print(self)
            return True
        return False


    def checkList(self, list):
        '''
        Checks if the list generator is full of the same element/token
        '''
        key = next(list)
        for i in list:
            if i != key or i == " ":
                return False
        return True

    def checkWin(self, coord):
        '''
        Checks if the player has won by looking at elements vertically, horizontally, and diagonally
        '''
        x = int(coord[0])
        y = int(coord[1])
        if self.checkList(self.grid[y][c] for c in range(self.dim)): #row
            return True
        if self.checkList(self.grid[r][x] for r in range(self.dim)): #col
            return True
        if x == y and self.checkList(self.grid[j][j] for j in range(self.dim)): # diagonal \
            return True
        if y == self.dim-x-1 and self.checkList(self.grid[j][self.dim - j - 1] for j in range(self.dim)): # diagonal /
            return True
        return False

    def isBoardFull(self):
        '''Checks if there are any spots left on the Board to fill'''
        for i in self.grid:
            for j in i:
                if j == " ":
                    return False
        return True





class Player:

    def __init__(self, name, symbol):
        '''
        Creates a new Player with score 0
        Takes in a name, Board object, and a custom symbol
        '''
        self.score = 0
        self.name = name
        self.symbol = symbol

    def __str__(self):
        '''Prints info about the player's name and score'''
        return "Player " + str(self.name) + " (" + self.symbol + ") with " + str(self.score) + " point(s)."





class GameStateManager:
    '''
    Object that manages the entire tic-tac-toe game, including the board and two players
    To play, create a new GameStateManager 'game' then run 'game.play()''
    '''

    def __init__(self, dim, name1, symb1, name2, symb2):
        '''
        Creates a new game with:
            Board size dim
            Player 1 named name1 with symbol symb1
            Player 2 named name2 with symbol symb2
        '''
        self.dim = dim
        self.b = Board(dim)
        self.player1 = Player(name1, symb1)
        self.player2 = Player(name2, symb2)
        self.p1turn = True

    def __str__(self):
        '''Prints all the info about the game, including the current board and info on each player'''
        return str(self.b) + "\n\n" + str(self.player1) + "\n" + str(self.player2)

    def play(self):
        '''
        Allows two players to play the current tic-tac-toe game.
        Continuously asks for the current player's input
        Ends when either a player has won or the board is full
        '''
        while True:
            print(self.b)
            if self.p1turn:
                coords = input("\n" + self.player1.name + " is up. Please enter coordinates x,y: ")
                print("\n==============================\n")
                if self.b.play(self.player1.symbol, coords.split(",")): # move successful
                    self.p1turn = False
                    if self.b.checkWin(coords.split(",")):
                        print("Congratulations! " + self.player1.name + " has won the game.\n")
                        self.player1.score += 1
                        print(self)
                        break
            elif not self.p1turn:
                coords = input("\n" + self.player2.name + " is up. Please enter coordinates x,y: ")
                print("\n==============================\n")
                if self.b.play(self.player2.symbol, coords.split(",")): # move successful
                    self.p1turn = True
                    if self.b.checkWin(coords.split(",")):
                        print("Congratulations! " + self.player2.name + " has won the game.")
                        self.player2.score += 1
                        print(self)
                        break
            if self.b.isBoardFull():
                print(self.b)
                print("Game Over! Tie")
                reset_board(self.dim) # reset board for new game; losing player goes first next round
                break

    def reset_board(self, dim):
        '''Changes the board to an empty board with size dim'''
        self.b.grid = self.b.new_grid(dim)





def main():
    '''
    Main function: sets up the game
                   displays rules and prompts
                   allows for new game after one has finished
    '''
    print("\n\n\n\n\nWelcome to Tic-Tac-Toe!\n\nFill up an entire row, column, or diagonal to win.\ny equals row (distance from top row)\nx equals column (distance from leftmost row)\n")
    p1_name = input("Name of Player 1: ")
    p1_symbol = input("Player 1 symbol: ")
    while len(p1_symbol) != 1:
        print("Symbols must be a single character")
        p1_symbol = input("Player 1 symbol: ")
    p2_name = input("Name of Player 2: ")
    p2_symbol = input("Player 2 symbol: ")
    while len(p2_symbol) != 1 or p2_symbol == p1_symbol:
        print("Symbols must be a single character, different from Player 1's symbol")
        p2_symbol = input("Player 2 symbol: ")

    game = GameStateManager(3, p1_name, p1_symbol, p2_name, p2_symbol)

    while True:
        dim = int(input("Length/Width of board: "))
        while dim < 2:
            print("Size must be at least 2")
            dim = int(input("Length/Width of board: "))
        game.reset_board(dim)
        print("\n\nNow Playing: " + str(dim) + "x" + str(dim) + " Tic-Tac-Toe with " + p1_name + " and " + p2_name + "\n")
        game.play()
        response = input("\nPlay again? (Y/N) ")
        if response == "N" or response == "n":
            print("Thank you for playing!\n")
            break
        # Any other response continues to a new game



if __name__ == "__main__":
    main()
