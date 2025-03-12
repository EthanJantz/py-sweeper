from math import floor
from random import random

class Board:

    def __init__(self, board_size: list, pct_mines: float):
        self.board_rows, self.board_cols = board_size
        self.pct_mines = pct_mines # like 0.10
        self.n_mines = floor(self.board_rows * self.board_cols * self.pct_mines)
        self.real_board = [[' ' for _ in range(self.board_cols)] for _ in range(self.board_rows)]
        self.player_board = self.real_board.copy

    def generate_board(self):
        '''
        Generates the minesweeper board.

        Output: 
            A Board object.
        '''

        # place mines 
        mines = self.n_mines
        while mines > 0:
            for row in range(self.board_rows):
                for col in range(self.board_cols):
                    if self.real_board[row][col] != 'X':
                        is_mine = random() <= self.pct_mines
                        if is_mine and mines > 0:
                            self.real_board[row][col] = 'X'
                            mines -= 1
                        else:
                            self.real_board[row][col] = 'E'

        # place number and blank markers
        
        return self
    
    def show_real_board(self):
        '''
        Displays the un-masked board to the user.

        Output:
            A Board object
        '''

        for lst in self.real_board:
            print(*lst)

if __name__ == "__main__":
    b = Board([10, 10], .1)
    b.generate_board()
    b.show_real_board()