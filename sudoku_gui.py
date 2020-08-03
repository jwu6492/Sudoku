import pygame
import time
pygame.font.init()

class Grid:
    board = [
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
    
    def __init__(self, rows, cols, width, height, window):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.window = window
        
    def draw(self):
        space = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thickness = 3
            else:
                thickness = 1
            #columns
            pygame.draw.line(self.window, (0, 0, 0), (i * space, 0), (i * space, self.width), thickness)
            #rows
            pygame.draw.line(self.window, (0, 0, 0), (0, i * space), (self.width, i * space), thickness)

def draw_window(win, board):
    win.fill((255,255,255))
    board.draw()


def main():
    win = pygame.display.set_mode((540,600))
    pygame.display.set_caption("Sudoku")
    board = Grid(9, 9, 540, 540, win)
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw_window(win, board)
        pygame.display.update()

def valid(board, row, col, num):
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
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                pos[0] = i
                pos[1] = j
                return True
    return False

def solve(board):
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
main()
pygame.quit()
