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
        self.player_board = [['?' for _ in range(self.board_cols)] for _ in range(self.board_rows)]
        self.game_over = False

    def generate_board(self, first_cell: List[int]):
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
                    if self.real_board[row][col] != 'X' and [row, col] != first_cell:
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
        def chain_reveal(cell: List, limit: int):
            '''
            Recursively look from cell to cell and reveal if it is blank. 

            Parameters:
                cell (list): A list containing row, col, and value of a cell.
                limit (int): The total number of adjacent cells to the given cell.

            Returns:
                None
            '''
            for cell in iterate_adjacent_cells(self.real_board, cell[0], cell[1]):
                if cell[2] in ' 12345678':
                    if self.player_board[cell[0]][cell[1]] != '?':
                        limit -= 1
                        if limit <= 0: return
                    else:
                        self.player_board[cell[0]][cell[1]] = self.real_board[cell[0]][cell[1]]
                        lim = sum(1 for x in iterate_adjacent_cells(self.real_board, cell[0], cell[1]))
                        chain_reveal(cell, lim)
            
        revealed_cell_value = self.real_board[row][col]
        self.player_board[row][col] = revealed_cell_value
        if revealed_cell_value == 'X': 
            print('Game over')
            self.show_board('full')
            self.game_over = True
        else:
            if revealed_cell_value in ' 12345678':
                lim = sum(1 for x in iterate_adjacent_cells(self.real_board, row, col))
                chain_reveal([row, col], lim)
            self.show_board('player')

        return self

class Player:

    def __init__(self, board: Board):
        self.board = board
        self.game_over = self.board.game_over

    def get_input(self, message: str = 'Input: '):
        '''
        Gets input from player. Input must evaluate to an int.

        Parameters:
            message (str): The input message. 

        Returns:
            The input value. 
        '''
        value = None
        while not isinstance(value, int):
            value = input(message)
            try:
                value = int(value)
            except:
                continue

        return value
    
    def check_game_over(self):
        '''Checks if the game is over.'''
        self.game_over = self.board.game_over


if __name__ == "__main__":
    board = Board([10, 10], .15)
    player = Player(board)
    row, col = player.get_input("Input row: "), player.get_input("Input col: ")
    player.board.generate_board([row, col])
    player.board.reveal_cell(row, col)
    while not player.game_over:
        row, col = player.get_input("Input row: "), player.get_input("Input col: ")
        player.board.reveal_cell(row, col)
        player.check_game_over()
    print("Thanks for playing!")
    