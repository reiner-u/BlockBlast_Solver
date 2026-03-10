#For streamlit stuff
import streamlit as st
import numpy as np
from solver import core, logic
from solver.pieces import PIECES

BOARD_SIZE = 8
PIECE_GRID_SIZE = 5

# session initialized here
# State for each grid is stored as a flat binary string. one char per cell, row by row.
# e.g. an 8x8 board starts as "0" * 64

def init_state():
    if "board_input" not in st.session_state:
        st.session_state["board_input"] = "0" * (BOARD_SIZE * BOARD_SIZE)
    for i in range(1, 4):
        key = f"piece_{i}_input"
        if key not in st.session_state:
            st.session_state[key] = "0" * (PIECE_GRID_SIZE * PIECE_GRID_SIZE)
    if "result" not in st.session_state:
        st.session_state["result"] = None

# CSS injected once at the top of the page to make all buttons render as compact square cells
GRID_CSS = """
<style>
    .stButton > button {
        width: 40px !important;
        height: 40px !important;
        padding: 0 !important;
        min-width: unset !important;
        border-radius: 4px !important;
        border: none !important;
        background: transparent !important;
        font-size: 20px !important;
        line-height: 1 !important;
    }
</style>
"""

# Input grid helpers
def render_grid(key, size):
    state = list(st.session_state[f"{key}_input"])
    for r in range(size):
        cols = st.columns(size)
        for c in range(size):
            index = r * size + c
            label = "⬛" if state[index] == "1" else "⬜"
            if cols[c].button(label, key=f"{key}_{r}_{c}"):
                state[index] = "0" if state[index] == "1" else "1"
                st.session_state[f"{key}_input"] = "".join(state)
                st.rerun()

def state_to_numpy(key, size):
    #convert the flat binary string back into a 2D numpy int array for the solver
    state_string = st.session_state[f"{key}_input"]
    flat = [int(c) for c in state_string]
    return np.array(flat).reshape(size, size)

def crop_piece(arr): #crops 5x5 grid down to size of entered shape. compares it to known pieces and returns only if valid, otherwise returs nothing
    # arr is a numpy int array. Crop to the tight bounding box of filled cells.
    rows_any = np.any(arr, axis=1)
    cols_any = np.any(arr, axis=0)
    if not rows_any.any():
        return None  # nothing drawn
    rmin, rmax = np.where(rows_any)[0][[0, -1]]
    cmin, cmax = np.where(cols_any)[0][[0, -1]]
    for piece in PIECES.values():
        if np.array_equal(arr[rmin:rmax+1, cmin:cmax+1], piece):
            return arr[rmin:rmax+1, cmin:cmax+1]
    return None

def reset_all():
    # Wipe everything >:)
    st.session_state["board_input"] = "0" * (BOARD_SIZE * BOARD_SIZE)
    for i in range(1, 4):
        st.session_state[f"piece_{i}_input"] = "0" * (PIECE_GRID_SIZE * PIECE_GRID_SIZE)
    st.session_state["result"] = None

def clear_pieces():
    # Keep the current board but clear the piece grids and result, ready for the next turn
    for i in range(1, 4):
        st.session_state[f"piece_{i}_input"] = "0" * (PIECE_GRID_SIZE * PIECE_GRID_SIZE)
    st.session_state["result"] = None


#gui stuff over here
# Cell colours for the solution display
COLOR_EMPTY   = "#2d2d3d"
COLOR_FILLED  = "#1565C0"  # existing filled cells
COLOR_NEW     = "#29B6F6"  # the piece just placed
COLOR_CLEAR   = "#FFC107"  # cells in a line about to be cleared

def render_board_html(grid, new_piece_cells=None, clearing_cells=None, cell_size=34):
    # Renders a static HTML grid — no interactivity needed here.
    # Colour priority: clearing > new piece > filled > empty
    rows, cols = grid.shape
    cells_html = ""
    for r in range(rows):
        for c in range(cols):
            if new_piece_cells and (r, c) in new_piece_cells:
                color = COLOR_NEW
            elif clearing_cells and (r, c) in clearing_cells:
                color = COLOR_CLEAR
            elif grid[r, c] == 1:
                color = COLOR_FILLED
            else:
                color = COLOR_EMPTY
            cells_html += (
                f'<div style="width:{cell_size}px;height:{cell_size}px;'
                f'background:{color};border-radius:4px;"></div>'
            )

    gap = 3
    return (
        f'<div style="display:inline-grid;'
        f'grid-template-columns:repeat({cols},{cell_size}px);'
        f'gap:{gap}px;padding:6px;background:#13131f;border-radius:8px;">'
        f'{cells_html}</div>'
    )

def display_solution(initial_board, placements, three_pieces):
    grid = initial_board.copy()

    for step_num, (piece_name, row, col) in enumerate(placements):
        piece = three_pieces[piece_name]
        piece_rows, piece_cols = piece.shape

        # Find which cells the new piece occupies on the board
        new_piece_cells = {
            (row + r, col + c)
            for r in range(piece_rows)
            for c in range(piece_cols)
            if piece[r, c] == 1
        }

        placed_grid = logic.place_piece(grid, piece, row, col)

        # Find which rows and columns are full and will clear
        full_rows = [r for r in range(placed_grid.shape[0])
                     if all(placed_grid[r, c] == 1 for c in range(placed_grid.shape[1]))]
        full_cols = [c for c in range(placed_grid.shape[1])
                     if all(placed_grid[r, c] == 1 for r in range(placed_grid.shape[0]))]

        clearing_cells = (
            {(r, c) for r in full_rows for c in range(placed_grid.shape[1])} |
            {(r, c) for c in full_cols for r in range(placed_grid.shape[0])}
        )

        cleared_count = len(full_rows) + len(full_cols)
        clear_note = f" — clears {cleared_count} line{'s' if cleared_count > 1 else ''}" if cleared_count else ""
        st.markdown(f"**Step {step_num + 1}: {piece_name} → row {row}, col {col}{clear_note}**")
        st.markdown(
            render_board_html(placed_grid, new_piece_cells, clearing_cells or None),
            unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)

        grid, _ = logic.clear_lines(placed_grid)

    # Final board after all placements and clears
    st.markdown("**Final board:**")
    st.markdown(render_board_html(grid), unsafe_allow_html=True)
    st.markdown(
        f'<p style="color:#aaa;font-size:13px;margin-top:6px;">'
        f'<span style="background:{COLOR_FILLED};border-radius:3px;padding:2px 6px;">&nbsp;</span> Existing &nbsp;'
        f'<span style="background:{COLOR_NEW};border-radius:3px;padding:2px 6px;">&nbsp;</span> Placed &nbsp;'
        f'<span style="background:{COLOR_CLEAR};border-radius:3px;padding:2px 6px;">&nbsp;</span> Clearing</p>',
        unsafe_allow_html=True
    )

#web app over here

init_state()
st.markdown(GRID_CSS, unsafe_allow_html=True)

st.title("Block Blast Solver")

# Board
st.subheader("Enter Board State here")
render_grid("board", BOARD_SIZE)

# Pieces
st.subheader("Pieces - Enter them here")
col1, col2, col3 = st.columns(3)
with col1:
    with st.container(border=True):
        st.write("Piece 1")
        render_grid("piece_1", PIECE_GRID_SIZE)
with col2:
    with st.container(border=True):
        st.write("Piece 2")
        render_grid("piece_2", PIECE_GRID_SIZE)
with col3:
    with st.container(border=True):
        st.write("Piece 3")
        render_grid("piece_3", PIECE_GRID_SIZE)

# Solve / Reset
solve_col, reset_col = st.columns([3, 1])
if reset_col.button("Reset", use_container_width=True):
    reset_all()
    st.rerun()

if solve_col.button("Solve", use_container_width=True):
    board = state_to_numpy("board", BOARD_SIZE)

    three_pieces = {}
    for i in range(1, 4):
        arr = state_to_numpy(f"piece_{i}", PIECE_GRID_SIZE)
        piece = crop_piece(arr)
        if piece is not None:
            three_pieces[f"piece_{i}"] = piece

    if not three_pieces:
        st.session_state["result"] = ("warning", "Please draw at least one piece.")
    else:
        placements, score = core.solve(board, three_pieces)
        if not placements:
            st.session_state["result"] = ("error", "No valid solution found — the pieces cannot all be placed.")
        else:
            # Store board and pieces alongside placements so display_solution can simulate each step
            st.session_state["result"] = ("success", placements, score, three_pieces, board)

# Result display, stored in session_state so it persists after further cell clicks
if st.session_state["result"] is not None:
    result = st.session_state["result"]
    if result[0] == "warning":
        st.warning(result[1])
    elif result[0] == "error":
        st.error(result[1])
    else:
        _, placements, score, three_pieces, initial_board = result
        st.success(f"Solution found! Score: {score}")
        st.subheader("Step-by-step solution")
        display_solution(initial_board, placements, three_pieces)

        if st.button("Continue", use_container_width=False):
            final_board = logic.get_final_board(initial_board, placements, three_pieces)
            st.session_state["board_input"] = "".join(str(v) for v in final_board.flatten())
            clear_pieces()
            st.rerun()
