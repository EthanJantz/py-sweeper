from typing import List

def is_2d_array(list_):
    '''Returns true only if the input list_ is a 2D array.'''
    if not isinstance(list_, list):
        return False
    if not list_:  # Empty list
        return False
    row_len = len(list_[0])
    for row in list_:
        if not isinstance(row, list) or len(row) != row_len:
            return False
    return True

def flatten_list(list_):
    '''Returns a flattened list.'''
    return [x for sublist in list_ for x in sublist]

def adjacent_cells(matrix: List[List[str]], row: int, col: int):
    '''
    Returns adjacent cells in matrix from position matrix[row][col]
    
    Parameters:
        matrix (List[List]): The board being accessed.
        row (int): The row value of the cell being viewed.
        col (int): the col value of the cell being viewed.

    Returns:
        A list of cell locations and values belonging to adjacent cells of matrix[row][col].
    '''
    assert is_2d_array(matrix), "Input: matrix must be a 2D nested list."
    assert all(isinstance(i, str) for i in flatten_list(matrix)), "Input: matrix elements must be type(str)"
    
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0
    assert row >= 0 and row <= rows, f"Input: row must be >= 0 and <= {rows}"
    assert col >= 0 and col <= cols, f"Input: col must be >= 0 and <= {cols}"

    cells = []
    for i in range(max(0, row - 1), min(rows, row + 2)): # row + 2 because range(stop) is not inclusive
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if i == row and j == col:
                continue  # Skip the central cell
            cells += [[i, j, matrix[i][j]]]
    return cells