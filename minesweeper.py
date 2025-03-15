from math import floor
from random import random
from typing import List

def iterate_adjacent_cells(matrix: List[List[str]], row: int, col: int):
    '''Yields adjacent cells in matrix from position matrix[row][col]'''
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if i == row and j == col:
                continue  # Skip the central cell
            yield i, j, matrix[i][j]

class Board:

    def __init__(self, board_size: list, pct_mines: float):
        self.board_rows, self.board_cols = board_size
        self.pct_mines = pct_mines # like 0.10
        self.n_mines = floor(self.board_rows * self.board_cols * self.pct_mines)
        self.real_board = [[' ' for _ in range(self.board_cols)] for _ in range(self.board_rows)]
        self.player_board = [[' ' for _ in range(self.board_cols)] for _ in range(self.board_rows)]

    def generate_board(self, first_cell: List[List[int]]):
        '''
        Generates the minesweeper board.

        Returns: 
            A Board object.
        '''
        # place mines 
        mines = self.n_mines
        while mines > 0:
            for row in range(self.board_rows):
                for col in range(self.board_cols):
                    if self.real_board[row][col] != 'X' and self.real_board[first_cell[0]][first_cell[1]]:
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
                        for cell in iterate_adjacent_cells(self.real_board, row, col):
                            if cell[2] == 'X':
                                adjacent_mines += 1
                        self.real_board[row][col] = str(adjacent_mines) if adjacent_mines > 0 else ' '

        return self
    
    def show_board(self, mode: str = 'player'):
        '''
        Displays the board to the user.

        Parameters:
            mode (str): Which perspective to show of the player board. 'player' shows only revealed cells, 'full' displays the every cell value. 

        Returns:
            None
        '''
        if mode == 'full':
            for lst in self.real_board:
                print(*lst)
        elif mode == 'player':
            for lst in self.player_board:
                print(*lst)

    def reveal_cell(self, row: int, col: int):
        '''
        Reveals the cell at board[row][col] and updates player_board to reflect the revealed information. 

        Parameters:
            row (int): The row position of the cell to be revealed. 
            col (int): The col position of the cell to be revealed.

        Returns:
            A Board object.
        '''
        revealed_cell_value = self.real_board[row][col]
        self.player_board[row][col] = revealed_cell_value
        if revealed_cell_value == 'X': 
            print('Game over')
            self.show_board('full')
        else:
            if revealed_cell_value == ' ':
                for cell in iterate_adjacent_cells(self.real_board, row, col):
                    self.reveal_cell(cell[0], cell[1])
            self.show_board('player')

        return self

if __name__ == "__main__":
    b = Board([10, 10], .17)
    b.generate_board()
    b.show_board('player')
    