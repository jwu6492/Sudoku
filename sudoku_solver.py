#sudoku solver using the backtracking algorithm assuming 9x9 board
def valid(board, row, col, num):
    """
    This function will validate if the attempted number input at the specific position is correct or not
    @param board - the inputed 9x9 sudoku board
    @param row - int row of the attempted number input
    @param col - int column of the attempted number input
    @param num - the attempted number input
    @return true if number placement is valid and false if it is not
    """
    #check row
    for i in range(0, len(board)):
        if board[row][i] == num:
            return False
    #check column
    for i in range(0, len(board)):
        if board[i][col] == num:
            return False
    #check sub-grid
    row_start = row - row % 3
    col_start = col - col % 3
    for i in range(row_start, row_start + 3):
        for j in range(col_start, col_start + 3):
            if board[i][j] == num:
                return False
    #valid attempted number
    return True

def find_empty_space(board, pos):
    """
    This function will find the next empty space
    @param board - the inputed 9x9 sudoku board
    @param pos - list that records the location of the empty space
    @return true if there is an empty space and false if there is not
    """
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                pos[0] = i
                pos[1] = j
                return True
    return False

def solve(board):
    """
    This function will implement the backtracking algorithm to solve the sudoku board
    @param board - the inputted 9x9 sudoku board
    @return true if the board is solved and false if there is no solution
    """
    pos = [0,0]
    if not find_empty_space(board, pos):
        return True
    row = pos[0]
    col = pos[1]
    for num in range(1, 10):
        if valid(board, row, col, num):
            board[row][col] = num
            if solve(board):
                return True
            else:
                board[row][col] = 0
    #no solution
    return False

def print_board(board):
    """
    This function will print the board
    @param board - the inputted 9x9 sudoku board
    """
    for i in range(len(board)):
        for j in range(len(board[0])):
            print(board[i][j], end = " ")
        print()

grid = [
    [0, 0, 2, 0, 9, 0, 0, 0, 5],
    [0, 0, 0, 8, 3, 0, 6, 0, 4],
    [7, 6, 0, 0, 5, 0, 9, 2, 0],
    [0, 5, 0, 3, 0, 0, 0, 1, 8],
    [0, 0, 0, 0, 0, 4, 0, 0, 7],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 1, 0, 0, 0, 0, 0, 0, 0],
    [8, 0, 0, 6, 0, 0, 0, 0, 0],
    [3, 0, 0, 0, 0, 0, 0, 4, 0]
]
if solve(grid):
    print("The solved board will look like:")
    print()
    print_board(grid)
else:
    print("error")