#For the brain of the solver, uses stuff from logic.py
from solver import logic
import numpy as np
from itertools import permutations


def try_sequence(grid, remaining_pieces, placements, score):
    # Recursive: places remaining_pieces[0], then calls itself for [1], [2], etc.
    # Returns the (placements, score) that achieves the best total, or None if
    # no complete sequence is possible from this board state.
    if not remaining_pieces:
        return placements, score  # base case — all pieces placed successfully

    piece_name, piece = remaining_pieces[0]
    remaining = remaining_pieces[1:]  # [1:] instead of filtering by value, so identical pieces stay independent

    best_placements = None
    best_score = -1

    for row in range(8):
        for col in range(8):
            if logic.can_place_piece(grid, piece, row, col):
                new_grid = logic.place_piece(grid, piece, row, col)
                cleared_grid, lines_cleared = logic.clear_lines(new_grid)
                new_score = score + int(np.sum(piece)) + lines_cleared  # np.sum counts the filled cells
                new_placements = placements + [(piece_name, row, col)]
                result = try_sequence(cleared_grid, remaining, new_placements, new_score)

                # None means the remaining pieces couldn't all fit from this position — skip it
                if result is not None:
                    result_placements, result_score = result
                    if result_score > best_score:
                        best_score = result_score
                        best_placements = result_placements

    if best_placements is None:
        return None  # no valid complete sequence from this state
    return best_placements, best_score


def solve(grid, three_pieces_dict):
    # Try every ordering of the 3 pieces and return the highest-scoring complete sequence.
    # Ordering matters because placing piece A first may clear a line that lets piece B fit.
    best_score = -1
    best_placements = None

    for permutation in permutations(three_pieces_dict.items()):
        result = try_sequence(grid, list(permutation), [], 0)
        if result is not None:
            placements, score = result
            if score > best_score:
                best_score = score
                best_placements = placements

    if best_placements is None:
        return [], 0
    return best_placements, best_score
