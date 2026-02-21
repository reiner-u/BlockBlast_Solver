#For board and solver mechanics, such as placing a piece, checking if a piece can be placed, clearing lines, etc.
import numpy as np

def create_empty_grid(): 
    return np.zeros((8, 8), dtype=int) #return 8x8 numpy array


def can_place_piece(grid, piece, row, col):
    piece_rows, piece_cols = piece.shape
    grid_rows, grid_cols = grid.shape

    #check if the row or col is negative
    if row < 0 or col < 0:
        return False

    # Check if the piece fits within the grid boundaries
    if row + piece_rows > grid_rows or col + piece_cols > grid_cols:
        return False

    # Check for collisions with existing pieces on the grid
    for r in range(piece_rows):
        for c in range(piece_cols):
            if piece[r, c] == 1 and grid[row + r, col + c] == 1: #numPy indexing
                return False

    return True

def place_piece(grid, piece, row, col):
    new_grid = grid.copy()
    piece_rows, piece_cols = piece.shape
    for r in range(piece_rows):
        for c in range(piece_cols):
            if piece[r][c] == 1:
                new_grid[row + r][col + c] = 1
    return new_grid

def clear_lines(grid):
    full_rows = []
    full_cols = []
    grid_rows, grid_cols = grid.shape
    cleared_lines = 0

    #Check for full rows and columns 
    for r in range(grid_rows):
        if all(grid[r][c] == 1 for c in range(grid_cols)):
            full_rows.append(r)

    for c in range(grid_cols):
        if all(grid[r][c] == 1 for r in range(grid_rows)):
            full_cols.append(c)

    new_grid = grid.copy()

    #In new grid, set full rows and columns to 0
    for r in full_rows:
        new_grid[r] = 0
    for c in full_cols:
        new_grid[:, c] = 0

    cleared_lines = len(full_rows) + len(full_cols) #for scoring purposes
    return new_grid, cleared_lines

def generate_moves(grid, pieces_catalog):
    moves = []
    for piece_name, piece in pieces_catalog.items():
        for row in range(grid.shape[0]):
            for col in range(grid.shape[1]):
                if can_place_piece(grid, piece, row, col): #If the piece can be placed at this position, add it to the list of moves
                    placed =   place_piece(grid, piece, row, col)
                    cleared_grid, cleared_lines = clear_lines(placed)
                    moves.append((piece_name, row, col, cleared_grid, cleared_lines))
    return moves #return a list of tuples, each containing the piece name, row, col, resulting grid after placing the piece and clearing lines, and number of lines cleared.

def has_any_move(grid, pieces_catalog): #Check if there is at least one valid move available for the current grid and pieces catalog. Used to determine if the game is over.
    for piece_name, piece in pieces_catalog.items():
        for row in range(grid.shape[0]):
            for col in range(grid.shape[1]):
                if can_place_piece(grid, piece, row, col):
                    return True
    return False

#def can_play_set(grid, three_pieces): #Check if any combination of the three pieces can be placed on the grid. Used to determine if the game is over.
    #To be implemented, actual solver must be made first.
