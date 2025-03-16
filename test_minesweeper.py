import pytest
from minesweeper import Board
from utility import *

def test_generate_board():
    test_board = Board([10, 10], .1)
    test_board.generate_board([5, 5])

    assert is_2d_array(test_board.real_board), "Expected real_board to be a 2D nested list."
    assert is_2d_array(test_board.player_board), "Expected player_board to be a 2D nested list."
    assert all(i == '?' for i in flatten_list(test_board.player_board)), "Expected all values in player_board to be '?'."

    total_real_mines = 0

    for row in range(test_board.board_rows):
        for col in range(test_board.board_cols):
            if test_board.real_board[row][col] == 'X':
                total_real_mines += 1

    assert total_real_mines == test_board.n_mines, f"Total number of mines on real board ({total_real_mines}) doesn't match expected total ({test_board.n_mines})."

def test_adjacent_cells():
    valid_matrix = [
        ['1', '2', '3'],
        ['4', '5', '6'],
        ['7', '8', '9']
    ]

    invalid_matrix = [
        [
            ['1', '2', '3'],
            ['2', '3', '4'],
        ],
        [
            ['3', '4', '5']
        ],
        ['1', '2', '3']
    ]

    with pytest.raises(AssertionError):
        adjacent_cells(invalid_matrix, 1, 1)

    invalid_matrix = [
        ['1', '2', '3'],
        ['4', int(5), '6'],
        ['7', '8', '9']
    ]

    with pytest.raises(AssertionError):
        adjacent_cells(invalid_matrix, 1, 1)

    with pytest.raises(AssertionError):
        adjacent_cells(valid_matrix, 4, 1)
    
    with pytest.raises(AssertionError):
        adjacent_cells(valid_matrix, 1, 4)

    cells = adjacent_cells(valid_matrix, 1, 1)

    assert len(cells) == 8, f"Expected len(cells) == 8, got {len(cells)}"
    

if __name__ == "__main__":
    pytest.main([__file__, '-s'])