#For board and solver mechanics, such as placing a piece, checking if a piece can be placed, clearing lines, etc.
import numpy as np
from itertools import permutations


def create_empty_grid():
    return np.zeros((8, 8), dtype=int)


def can_place_piece(grid, piece, row, col):
    # row/col is the top-left corner of the placement
    piece_rows, piece_cols = piece.shape
    grid_rows, grid_cols = grid.shape

    # guard against negative indices — numpy would silently wrap around without this
    if row < 0 or col < 0:
        return False

    if row + piece_rows > grid_rows or col + piece_cols > grid_cols:
        return False

    for r in range(piece_rows):
        for c in range(piece_cols):
            if piece[r, c] == 1 and grid[row + r, col + c] == 1:
                return False

    return True


def place_piece(grid, piece, row, col):
    new_grid = grid.copy()  # never mutate the original — the solver tries many placements per state
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

    for r in range(grid_rows):
        if all(grid[r][c] == 1 for c in range(grid_cols)):
            full_rows.append(r)

    for c in range(grid_cols):
        if all(grid[r][c] == 1 for r in range(grid_rows)):
            full_cols.append(c)

    new_grid = grid.copy()

    for r in full_rows:
        new_grid[r] = 0
    for c in full_cols:
        new_grid[:, c] = 0  # numpy column slice: selects the entire column at once

    cleared_lines = len(full_rows) + len(full_cols)
    return new_grid, cleared_lines


def get_final_board(initial_board, placements, pieces):
    # Replays a solved sequence to return the board state after all pieces are placed and lines cleared.
    # placements is a list of (piece_name, row, col); pieces is the {name: array} dict.
    grid = initial_board.copy()
    for piece_name, row, col in placements:
        grid, _ = clear_lines(place_piece(grid, pieces[piece_name], row, col))
    return grid


def generate_moves(grid, pieces_catalog):
    # Returns every valid single-piece placement as a list of tuples.
    # Each tuple: (piece_name, row, col, resulting_grid, lines_cleared, cells_placed)
    moves = []
    for piece_name, piece in pieces_catalog.items():
        cells_placed = int(np.sum(piece))  # np.sum adds all the 1s to get the cell count
        for row in range(grid.shape[0]):
            for col in range(grid.shape[1]):
                if can_place_piece(grid, piece, row, col):
                    placed = place_piece(grid, piece, row, col)
                    cleared_grid, cleared_lines = clear_lines(placed)
                    moves.append((piece_name, row, col, cleared_grid, cleared_lines, cells_placed))
    return moves


def has_any_move(grid, pieces_catalog):
    # Early-exit check — call this with the current 3 pieces (not the full catalog)
    # to test if the game is over.
    for piece_name, piece in pieces_catalog.items():
        for row in range(grid.shape[0]):
            for col in range(grid.shape[1]):
                if can_place_piece(grid, piece, row, col):
                    return True
    return False


def _can_place_in_order(grid, pieces):
    # Recursive helper for can_play_set.
    # Tries to place pieces[0] somewhere valid, then recurses for pieces[1], pieces[2], etc.
    # Returns True as soon as a full sequence succeeds.
    if not pieces:
        return True  # base case. all pieces placed

    _, piece = pieces[0]
    remaining = pieces[1:]

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if can_place_piece(grid, piece, row, col):
                new_grid, _ = clear_lines(place_piece(grid, piece, row, col))
                if _can_place_in_order(new_grid, remaining):
                    return True

    return False


def can_play_set(grid, three_pieces):
    # Game-over check: returns True if the 3 pieces can all be placed in some order.
    # Ordering matters because placing one piece may clear lines that open space for the next.
    piece_list = list(three_pieces.items())

    for ordering in permutations(piece_list):  # up to 3! = 6 orderings
        if _can_place_in_order(grid, list(ordering)):
            return True

    return False
