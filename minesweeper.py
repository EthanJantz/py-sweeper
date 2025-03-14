from math import floor
from random import random
from typing import List

class Board:

    def __init__(self, board_size: list, pct_mines: float):
        self.board_rows, self.board_cols = board_size
        self.pct_mines = pct_mines # like 0.10
        self.n_mines = floor(self.board_rows * self.board_cols * self.pct_mines)
        self.real_board = [[' ' for _ in range(self.board_cols)] for _ in range(self.board_rows)]

    def generate_board(self):
        '''
        Generates the minesweeper board.

        Output: 
            A Board object.
        '''

        def iterate_adjacent_cells(matrix: List[List[int]], row: int, col:int ):
            rows = len(matrix)
            cols = len(matrix[0]) if rows > 0 else 0
            for i in range(max(0, row - 1), min(rows, row + 2)):
                for j in range(max(0, col - 1), min(cols, col + 2)):
                    if i == row and j == col:
                        continue  # Skip the current cell
                    yield matrix[i][j]

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
                            self.real_board[row][col] = ' '

        # place number and blank markers
        for row in range(self.board_rows):
                for col in range(self.board_cols):
                    if self.real_board[row][col] == ' ':
                        adjacent_mines = 0
                        for square in iterate_adjacent_cells(self.real_board, row, col):
                            if square == 'X':
                                adjacent_mines += 1
                        self.real_board[row][col] = str(adjacent_mines) if adjacent_mines > 0 else ' '

        return self
    
    def show_real_board(self):
        '''
        Displays the un-masked board to the user.

        Returns:
            None
        '''

        for lst in self.real_board:
            print(*lst)

if __name__ == "__main__":
    b = Board([10, 10], .17)
    b.generate_board()
    b.show_real_board()