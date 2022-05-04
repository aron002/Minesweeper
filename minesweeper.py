import random


class Minesweeper:
    def __init__(self, width, height, bombs):
        self.bombs = bombs
        self.width = width
        self.height = height
        self.board = []
        self.revealed_board = []
        self.revealed = []
        self.clear = []
        self.flags = []
        setup_board(self.board, '0', self.width, self.height)
        setup_board(self.revealed_board, ' ', self.width, self.height)
        self.place_bombs()
        self.number_board()


    def place_bombs(self):
        bombs_left = self.bombs
        bombs = []
        while bombs_left > 0:
            row = random.randint(0, self.height-1)
            col = random.randint(0, self.width-1)
            if self.board[row][col] == '0':
                self.board[row][col] = 'B'
                bombs_left -= 1
                bombs.append((row, col))

        for i in range(self.height):
            for j in range(self.width):
                if (i, j) not in bombs:
                    self.clear.append((i, j))


    def number_board(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == '0':
                    bomb_count = 0
                    for x in range(-1, 2):
                        for y in range(-1, 2):
                            if x != 0 or y != 0:
                                if 0 <= i+x < self.height and 0 <= j+y < self.width and self.board[i+x][j+y] == 'B':
                                    bomb_count += 1
                    self.board[i][j] = str(bomb_count)


    def click(self, position):
        row, col = position
        if self.revealed_board[row][col] == 'F':
            return True
        if self.board[row][col] == 'B':
            return False
        self._reveal(position)
        return True

    
    def place_flag(self, position):
        row, col = position
        if (row, col) in self.flags:
            self.flags.remove((row, col))
            self.revealed_board[row][col] = ' '
        elif len(self.flags) < self.bombs and self.revealed_board[row][col] == ' ':
            self.revealed_board[row][col] = 'F'
            self.flags.append((row, col))


    def _reveal(self, position):
        i, j = position
        self.revealed_board[i][j] = self.board[i][j]
        self.revealed.append((i, j))
        if self.board[i][j] != '0':
            return
        for x in range(-1, 2):
            for y in range(-1, 2):
                if 0 <= i+x < self.height and 0 <= j+y < self.width and not (i+x, j+y) in self.revealed:
                    # if (x != 0 and y == 0) or (y != 0 and x == 0):
                    self.revealed.append((i+x, j+y))
                    self._reveal([i+x, j+y])


    def check_win(self):
        return set(self.clear) == set(self.revealed)


    def print_board(self):
        board = ''
        for row in self.board:
            board += str(row) + '\n'
        print(board)


    def print_revealed_board(self):
        board = ''
        for row in self.revealed_board:
            board += str(row) + '\n'
        print(board)


def setup_board(board, token, width, height):
    for i in range(height):
        temp = []
        for j in range(width):
            temp.append(token)
        board.append(temp)