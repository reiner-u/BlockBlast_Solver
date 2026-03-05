#For board and solver mechanics, such as placing a piece, checking if a piece can be placed, clearing lines, etc.
import numpy as np
from itertools import permutations

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
        cells_placed = int(np.sum(piece)) #number of filled cells in the piece, for scoring (1 point each)
        for row in range(grid.shape[0]):
            for col in range(grid.shape[1]):
                if can_place_piece(grid, piece, row, col): #If the piece can be placed at this position, add it to the list of moves
                    placed = place_piece(grid, piece, row, col)
                    cleared_grid, cleared_lines = clear_lines(placed)
                    moves.append((piece_name, row, col, cleared_grid, cleared_lines, cells_placed))
    return moves #return a list of tuples, each containing: piece name, row, col, resulting grid after placing and clearing, number of lines cleared, and number of cells placed.

def has_any_move(grid, pieces_catalog): #Check if there is at least one valid move available for the current grid and pieces catalog. Used to determine if the game is over.
    for piece_name, piece in pieces_catalog.items():
        for row in range(grid.shape[0]):
            for col in range(grid.shape[1]):
                if can_place_piece(grid, piece, row, col):
                    return True
    return False

def _can_place_in_order(grid, pieces):
    # Helper for can_play_set. Tries to place each piece in the given order.
    # Returns True if all pieces can be placed successfully.
    if not pieces:
        return True  # All pieces placed, success

    _, piece = pieces[0]
    remaining = pieces[1:]

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if can_place_piece(grid, piece, row, col):
                new_grid, _ = clear_lines(place_piece(grid, piece, row, col))
                if _can_place_in_order(new_grid, remaining):
                    return True

    return False  # No valid position found for this piece in this ordering

def can_play_set(grid, three_pieces): #Check if any ordering of the three pieces can all be placed on the grid. Used to determine if the game is over.
    # Ordering matters because placing one piece clears lines, which may open up space for the next.
    # three_pieces is a dict of {piece_name: piece_array} with up to 3 items.
    piece_list = list(three_pieces.items())

    for ordering in permutations(piece_list):
        if _can_place_in_order(grid, list(ordering)):
            return True

    return False
