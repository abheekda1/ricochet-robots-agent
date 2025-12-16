from model.model import RRModel, UP, RIGHT, DOWN, LEFT

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

ACTION_NAMES = {
    UP: "UP",
    RIGHT: "RIGHT",
    DOWN: "DOWN",
    LEFT: "LEFT"
}

def action_name(a):
    return ACTION_NAMES.get(a, str(a))


# ------------------------------------------------------------
# Demo board (same as before)
# ------------------------------------------------------------

def make_demo_board():
    rows, cols = 8, 8
    W_UP, W_RIGHT, W_DOWN, W_LEFT = 1, 2, 4, 8

    walls = [[0 for _ in range(cols)] for _ in range(rows)]

    # vertical wall
    for r in range(1, 7):
        walls[r][3] |= W_RIGHT
        walls[r][4] |= W_LEFT

    # horizontal wall
    for c in range(2, 6):
        walls[4][c] |= W_DOWN
        walls[5][c] |= W_UP

    # small block
    walls[2][2] |= (W_RIGHT | W_DOWN)
    walls[2][3] |= W_LEFT
    walls[3][2] |= W_UP

    return walls


# ------------------------------------------------------------
# Interactive game loop
# ------------------------------------------------------------

def manual_play():
    walls = make_demo_board()

    start = ((6, 1), (2, 2), (3, 3))  # robot positions
    goal = (1, 6)

    model = RRModel(8, 8, walls, goal)

    state = start
    step = 0

    print("\n🎮 Ricochet Robots – Manual Play")
    print("Controls: enter the index of the move you want")
    print("Type 'q' to quit\n")

    while True:
        print(f"\n=== Step {step} ===")
        print(model.render(state))

        if model.is_terminal(state):
            print("🎉 Goal reached!")
            return

        successors = list(model.successors(state))

        if not successors:
            print("No legal moves available. Game over.")
            return

        print("\nAvailable moves:")
        for i, (next_state, action) in enumerate(successors):
            print(
                f"  [{i}] R{action[0]} moves {action_name(action[1]):5s} → {next_state}"
            )

        choice = input("\nChoose move index (or q): ").strip()

        if choice.lower() == "q":
            print("Exiting game.")
            return

        if not choice.isdigit():
            print("Invalid input.")
            continue

        idx = int(choice)
        if idx < 0 or idx >= len(successors):
            print("Index out of range.")
            continue

        next_state, action = successors[idx]
        print(f"\nYou chose {action_name(action)}")
        state = next_state
        step += 1


# ------------------------------------------------------------
# Entry point
# ------------------------------------------------------------

if __name__ == "__main__":
    manual_play()
