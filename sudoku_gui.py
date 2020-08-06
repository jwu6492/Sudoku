import pygame
import time
pygame.font.init()

class Grid:
    board = [
        [3, 0, 6, 5, 0, 8, 4, 0, 0], 
        [5, 2, 0, 0, 0, 0, 0, 0, 0], 
        [0, 8, 7, 0, 0, 0, 0, 3, 1], 
        [0, 0, 3, 0, 1, 0, 0, 8, 0], 
        [9, 0, 0, 8, 6, 3, 0, 0, 5], 
        [0, 5, 0, 0, 9, 0, 6, 0, 0], 
        [1, 3, 0, 0, 0, 0, 2, 5, 0], 
        [0, 0, 0, 0, 0, 0, 0, 7, 4], 
        [0, 0, 5, 2, 0, 6, 3, 0, 0]
    ]
    
    def __init__(self, rows, cols, width, height, window):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.window = window
        self.squares = [[Square(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.model = None
        self.update_model()
        self.selected = None

    def update_model(self):
        #updates the values in board for algorithm
        self.model = [[self.squares[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def select(self, row, col):
        #reset selected squares
        for i in range(self.rows):
            for j in range(self.cols):
                self.squares[i][j].selected = False
        self.squares[row][col].selected = True
        self.selected = [row, col]       

    def click(self, pos):
        #returns cube of mouseclick
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            #column
            x = pos[0] // gap
            #row
            y = pos[1] // gap
            return [int(y), int(x)]
        else:
            return None
    
    def num_guess(self, val):
        row = self.selected[0]
        col = self.selected[1]
        self.squares[row][col].set_temp(val)

    def insert(self, val):
        row = self.selected[0]
        col = self.selected[1]
        if self.squares[row][col].value == 0:
            self.squares[row][col].set_val(val)
            self.update_model()
            if valid(self.model, row, col, val) and self.solve():
                return True
            else:
                self.squares[row][col].set_val(0)
                self.squares[row][col].set_temp(0)
                self.update_model()
                return False
    
    def clear(self):
        row = self.selected[0]
        col = self.selected[1]
        self.squares[row][col].set_temp(0)
        self.squares[row][col].set_val(0)

    def is_complete(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.squares[i][j].value == 0:
                    return False
        return True

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
        #cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.squares[i][j].draw(self.window)
    
    def solve(self):
        pos = [0,0]
        if not find_empty_space(self.model, pos):
            return True
        row = pos[0]
        col = pos[1]
        for num in range(1, 10):
            if valid(self.model, row, col, num):
                self.model[row][col] = num
                if self.solve():
                    return True
                self.model[row][col] = 0
        #no solution
        return False

    def visualize_solve(self):
        self.update_model()
        pos = [0,0]
        if not find_empty_space(self.model, pos):
            return True
        row = pos[0]
        col = pos[1]
        for num in range(1, 10):
            if valid(self.model, row, col, num):
                self.model[row][col] = num
                self.squares[row][col].set_val(num)
                self.squares[row][col].tracing(self.window, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(100)
                if self.visualize_solve():
                    return True
                self.model[row][col] = 0
                self.squares[row][col].set_val(0)
                self.squares[row][col].tracing(self.window, False)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(100)
        #no solution
        return False       

class Square:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.temp = 0
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False
    
    def set_val(self, val):
        self.value = val
    
    def set_temp(self, val):
        self.temp = val
    
    def draw(self, window):
        text = pygame.font.SysFont('comicsans', size = 35)
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap
        
        if self.temp != 0 and self.value == 0:
            guess = text.render(str(self.temp), 1, (128, 128, 128))
            window.blit(guess, (x + 7, y + 7))
        elif self.value != 0:
            num = text.render(str(self.value), 1, (0, 0, 0))
            window.blit(num, (x + (gap / 2 - num.get_width() / 2), y + (gap / 2 - num.get_height() / 2)))
        if self.selected:
             pygame.draw.rect(window, (0, 0, 255), (x, y, gap, gap), 3)

    def tracing(self, window, correct = True):
        text = pygame.font.SysFont('comicsans', size = 35)
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.value == 0:
            pygame.draw.rect(window, (255, 255, 255), (x, y, gap, gap), 0)
        else:
            num = text.render(str(self.value), 1, (0, 0, 0))
            window.blit(num, (x + (gap / 2 - num.get_width() / 2), y + (gap / 2 - num.get_height() / 2)))
        if correct:
            pygame.draw.rect(window, (0, 255, 0), (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(window, (255, 0, 0), (x, y, gap, gap), 3)

def draw_window(window, board, time, wrong):
    window.fill((255,255,255))
    text = pygame.font.SysFont('comicsans', size = 30)
    time_text = text.render("Time: " + format_time(time), 1, (0,0,0))
    window.blit(time_text, (540 - 130, 565))
    wrong_text = text.render("X " * wrong, 1, (255, 0, 0))
    window.blit(wrong_text, (10, 565))
    board.draw()

def format_time(secs):
    sec = secs % 60
    min = secs // 60
    hour = min // 60
    
    result = str(hour) + ":" + str(min) + ":" + str(sec)
    return result

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

def main():
    win = pygame.display.set_mode((540,600))
    pygame.display.set_caption("Sudoku")
    board = Grid(9, 9, 540, 540, win)
    run = True
    start = time.time()
    wrong = 0
    while run:
        playing_time = round(time.time() - start)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_x:
                    board.clear()
                    key = None
                if event.key == pygame.K_SPACE:
                    board.visualize_solve()
                if event.key == pygame.K_RETURN:
                    row = board.selected[0]
                    col = board.selected[1]
                    if board.squares[row][col].temp != 0:
                        if board.insert(board.squares[row][col].temp):
                            print('Correct')
                        else:
                            print('Wrong')
                            wrong += 1
                        key = None
                        if board.is_complete():
                            print('Game Over') #make game over screen
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                clicked = board.click(position)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None
        if board.selected and key != None:
            board.num_guess(key)
        
        draw_window(win, board, playing_time, wrong)
        pygame.display.update()
main()
pygame.quit()
