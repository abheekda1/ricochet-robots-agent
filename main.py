from agent.mcts import MCTSAgent
from model.model import RRModel, UP, RIGHT, DOWN, LEFT
import time


# ============================================================
# Pretty printing helpers
# ============================================================

# def pretty_board(state, goal, walls, rows, cols):
#     """
#     Draws an ASCII board showing:
#     - R = robot
#     - G = goal
#     - # = wall edge for demonstration
#     """
#     rR, cR = state
#     rG, cG = goal

#     print("\nBoard state:")
#     for r in range(rows):
#         row = []
#         for c in range(cols):
#             if (r, c) == (rR, cR):
#                 row.append("R")
#             elif (r, c) == (rG, cG):
#                 row.append("G")
#             else:
#                 row.append(".")
#         print(" ".join(row))
#     print()

def pretty_board(state, goal, walls, rows, cols):
    rR, cR = state
    rG, cG = goal

    W_UP, W_RIGHT, W_DOWN, W_LEFT = 1, 2, 4, 8

    print("\nBoard state (with walls):")

    # Each cell will print:
    #   +---+ structure indicating walls
    for r in range(rows):
        # First print top walls for this row
        top_line = ""
        for c in range(cols):
            top_line += "+"
            top_line += "---" if walls[r][c] & W_UP else "   "
        top_line += "+"
        print(top_line)

        # Now print the cell contents and vertical walls
        mid_line = ""
        for c in range(cols):
            mid_line += "|" if (walls[r][c] & W_LEFT) else " "
            if (r, c) == (rR, cR):
                mid_line += " R "
            elif (r, c) == (rG, cG):
                mid_line += " G "
            else:
                mid_line += " . "
        # Rightmost border
        mid_line += "|" if (walls[r][cols-1] & W_RIGHT) else " "
        print(mid_line)

    # Print bottom wall for last row
    bottom_line = ""
    for c in range(cols):
        bottom_line += "+"
        bottom_line += "---" if walls[rows-1][c] & W_DOWN else "   "
    bottom_line += "+"
    print(bottom_line)


def announce_move(move):
    names = {UP: "UP", RIGHT: "RIGHT", DOWN: "DOWN", LEFT: "LEFT"}
    return names.get(move, f"?{move}")


# ============================================================
# Build a sample board with WALLS
# ============================================================

def make_demo_board():
    rows, cols = 8, 8

    # wall bit constants
    W_UP, W_RIGHT, W_DOWN, W_LEFT = 1, 2, 4, 8

    # empty wall grid
    walls = [[0 for _ in range(cols)] for _ in range(rows)]

    # Add some interesting walls to avoid straight-line loops:
    #
    # Vertical wall at column 3
    for r in range(1, 7):
        walls[r][3] |= W_RIGHT     # wall on right side of (r,3)
        walls[r][4] |= W_LEFT      # matching wall on left of (r,4)

    # Horizontal wall at row 4
    for c in range(2, 6):
        walls[4][c] |= W_DOWN      # wall below (4,c)
        walls[5][c] |= W_UP        # matching wall above (5,c)

    # A small block around (2,2)
    walls[2][2] |= (W_RIGHT | W_DOWN)
    walls[2][3] |= W_LEFT
    walls[3][2] |= W_UP

    return walls


# ============================================================
# Full game test loop
# ============================================================

def test_mcts_game():
    walls = make_demo_board()

    # start and goal positions
    start = (6, 1)
    goal = (1, 6)

    print("\n=== Ricochet Robots MCTS Demo ===")
    print("Start:", start, "Goal:", goal)

    model = RRModel(
        rows=8, 
        cols=8, 
        walls=walls, 
        goal_pos=goal
    )

    agent = MCTSAgent(model, time=0.20, rollout_depth=15)

    state = start
    pretty_board(state, goal, walls, 8, 8)

    MAX_MOVES = 30
    for move_number in range(1, MAX_MOVES + 1):

        if model.is_terminal(state):
            print(f"Reached the goal in {move_number - 1} moves!")
            return

        print(f"\n--- Move {move_number} ---")
        print("Current state:", state)
        print("Next states:", list(model.successors(state)))

        action = agent.choose_action(state)

        if action is None:
            print("MCTS returned no action. Stopping.")
            return

        print("Chosen action:", announce_move(action))

        new_state = model.transition(state, action)
        print("New state:", new_state)

        if new_state == state:
            print("WARNING: action did not change state! (wall blocked?)")
            # continue anyway so you can debug

        state = new_state
        pretty_board(state, goal, walls, 8, 8)

    print("\nFAILED: Did not reach goal within move limit.")


# ============================================================
# Main Entry
# ============================================================

if __name__ == "__main__":
    test_mcts_game()
