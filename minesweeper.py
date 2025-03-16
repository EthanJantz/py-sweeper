from math import floor
from random import random
from typing import List
from utility import * 

class Board:

    def __init__(self, board_size: list, pct_mines: float):
        self.board_rows, self.board_cols = board_size
        self.pct_mines = pct_mines # like 0.10
        self.n_mines = floor(self.board_rows * self.board_cols * self.pct_mines)
        self.real_board = [[' ' for _ in range(self.board_cols)] for _ in range(self.board_rows)]
        self.player_board = [['?' for _ in range(self.board_cols)] for _ in range(self.board_rows)]

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
                        # TODO: Ensure first click is surrounded by ' ' cells to avoid a numeric cell opening.
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
                        for cell in adjacent_cells(self.real_board, row, col):
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

    def reveal_cell(self, row: int, col: int, visited_cells: list = []):
        '''
        Reveals the cell at board[row][col] and updates player_board to reflect the revealed information. 
        Recursively checks adjacent cells using a depth first search algorithm and stops if a mine is in an adjacent cell.

        Parameters:
            row (int): The row position of the cell to be revealed. 
            col (int): The col position of the cell to be revealed.
            visited_cells (list): The list of cells already visited during the search. Defaults to an empty list. 

        Returns:
            None
        '''
        current_cell = [row, col, self.real_board[row][col]]

        if current_cell in visited_cells:
            return
        
        visited_cells += [current_cell]
        adj_cells = adjacent_cells(self.real_board, row, col)        
        self.player_board[row][col] = self.real_board[row][col]
                        
        for cell in adj_cells:
            if cell[2] in 'X': 
                return
            self.reveal_cell(cell[0], cell[1], visited_cells = visited_cells)

class Player:

    def __init__(self, board: Board):
        self.board = board
        self.game_over = False

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
        self.game_over = 'X' in flatten_list(self.board.player_board)

if __name__ == "__main__":
    # initialize
    board = Board([10, 10], .08)
    player = Player(board)
    row, col = player.get_input("Input row: "), player.get_input("Input col: ")
    player.board.generate_board([row, col])
    player.board.reveal_cell(row, col)
    player.board.show_board('player')

    while not player.game_over:
        row, col = player.get_input("Input row: "), player.get_input("Input col: ")
        player.board.reveal_cell(row, col)
        player.board.show_board('player')
        player.check_game_over()
    print("Thanks for playing!")
    