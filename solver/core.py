#For the brain of the solver, uses stuff from logic.py
import logic
import numpy as np
from itertools import permutations

def try_sequence(grid, remaining_pieces, placements, score):
    if not remaining_pieces: #base case, no more pieces to place
        return placements, score

    piece_name, piece = remaining_pieces[0]  # always work on the first piece; solve() handles ordering via permutations
    remaining = remaining_pieces[1:]  # slice out index 0 so identical pieces aren't both removed

    best_placements = None
    best_score = -1

    for row in range(8):
        for col in range(8):
            if logic.can_place_piece(grid, piece, row, col):
                new_grid = logic.place_piece(grid, piece, row, col)
                cleared_grid, lines_cleared = logic.clear_lines(new_grid)
                new_score = score + int(np.sum(piece)) + lines_cleared #cells placed + lines cleared
                new_placements = placements + [(piece_name, row, col)]
                result = try_sequence(cleared_grid, remaining, new_placements, new_score)

                if result is not None:
                    result_placements, result_score = result
                    if result_score > best_score:
                        best_score = result_score
                        best_placements = result_placements

    if best_placements is None:
        return None  # no valid complete sequence found from this state
    return best_placements, best_score

def solve(grid, three_pieces_dict):
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
