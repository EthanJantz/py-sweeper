from math import floor
from random import random
from typing import List
from utility import * 

class Board:

    def __init__(self, board_size: list, pct_mines: float):
        self.board_rows, self.board_cols = board_size
        self.board_size = self.board_rows * self.board_cols
        self.pct_mines = pct_mines # like 0.10
        self.n_mines = floor(self.board_rows * self.board_cols * self.pct_mines)
        self.real_board = [[' ' for _ in range(self.board_cols)] for _ in range(self.board_rows)]
        self.player_board = [['?' for _ in range(self.board_cols)] for _ in range(self.board_rows)]
        self.n_revealed_cells = 0

    def generate_board(self, first_cell: List[int]):
        '''
        Generates the minesweeper board.

        Parameters:
            first_cell (list[int]): The coordinates of the first cell chosen. Note that because this is set before the board is generated that the first_cell is not structured as a cell is elsewhere. 

        Returns: 
            A Board object.
        '''
        # place mines 
        mines = self.n_mines
        while mines > 0:
            for row in range(self.board_rows):
                for col in range(self.board_cols):
                    if self.real_board[row][col] != 'X' and [row, col] != first_cell:
                        if [row, col, self.real_board[row][col]] in adjacent_cells(self.real_board, first_cell[0], first_cell[1]):
                            continue
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
            mode (str): Which perspective to show of the player board. 'player' shows only revealed cells, 'full' displays every cell value. 

        Returns:
            None
        '''
        if mode == 'full':
            board_to_print = self.real_board
        else:
            board_to_print = self.player_board

        pprint_board = []
        for idx, row in enumerate(board_to_print):
            if idx == 0:
                new_row = [str(i) + " | " for i in range(len(row) + 1)]
                pprint_board.append(new_row)
                new_row = ["----" for i in range(len(row) + 1)]
                pprint_board.append(new_row)
            new_row = [str(idx + 1), " | "] + [row[i] + " | " for i in range(len(row))]
            pprint_board.append(new_row)
            new_row = ["----" for i in range(len(row) + 1)]
            pprint_board.append(new_row)
        
        for lst in pprint_board:
            print(*lst, sep = "")

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
        self.n_revealed_cells += 1

        if 'X' in [cell[2] for cell in adj_cells]:
            return
                        
        for cell in adj_cells:
            self.reveal_cell(cell[0], cell[1], visited_cells = visited_cells)

    def flag_cell(self, row: int, col: int):
        '''Flag a given cell as a potential mine.
        
        Parameters:
            row (int): The row position of the cell to be flagged. 
            col (int): The col position of the cell to be flagged.

        Returns:
            None
        '''
        self.player_board[row][col] = '@'

class Player:

    def __init__(self, board: Board):
        self.board = board
        self.game_over = False
        self.win_condition = False

    def get_input(self, message: str = 'Input: '):
        '''
        Gets input from player. Input must evaluate to an int.

        Parameters:
            message (str): The input message. 

        Returns:
            The input value. 
        '''
        value = input(message)
        try:
            return int(value) - 1 # row, col inputs
        except:
            return value 

    def check_game_state(self):
        '''Checks if the current board has a mine revealed and whether all non-mine cells have been revealed.'''
        self.game_over = 'X' in flatten_list(self.board.player_board)
        self.win_condition = self.board.n_revealed_cells == self.board.board_size - self.board.n_mines

        if self.game_over:
            print("That was a mine, game over!")
            self.board.show_board('full')

        if self.win_condition:
            print("Congratulations, you won!")

if __name__ == "__main__":
    # initialize
    board = Board([9, 9], .15)
    player = Player(board)

    # first move
    player.board.show_board('player')
    row, col = player.get_input("Input row: "), player.get_input("Input col: ")
    player.board.generate_board([row, col])
    player.board.reveal_cell(row, col)
    player.board.show_board('player')

    # core gameplay loop
    while not player.game_over and not player.win_condition:
        action_type = ' '
        while action_type not in 'rf':
            action_type = player.get_input("flag or reveal [f/r]: ")

        row, col = player.get_input("Input row: "), player.get_input("Input col: ")
        
        if action_type in 'reveal':
            player.board.reveal_cell(row, col)

        if action_type in 'flag':
            player.board.flag_cell(row, col)
        
        player.board.show_board('player')
        player.check_game_state()
    
    print("Thanks for playing!")
    