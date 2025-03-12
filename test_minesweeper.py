import pytest
from minesweeper import Board

def test_generate_board():
    test_board = Board([10, 10], .1)
    test_board.generate_board()

    total_real_mines = 0

    for row in range(test_board.board_rows):
        for col in range(test_board.board_cols):
            if test_board.real_board[row][col] == 'X':
                total_real_mines += 1

    assert total_real_mines == test_board.n_mines, f"Total number of mines on real board ({total_real_mines}) doesn't match expected total ({test_board.n_mines})."


if __name__ == "__main__":
    pytest.main([__file__, '-s'])