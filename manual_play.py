import random
from model.model import RRModel, UP, RIGHT, DOWN, LEFT, W_LEFT, W_RIGHT, W_UP, W_DOWN
from utils.puzzle_generator import generate_solvable_puzzle_2robots

ACTION_NAMES = {
    UP: "UP",
    RIGHT: "RIGHT",
    DOWN: "DOWN",
    LEFT: "LEFT"
}

def action_name(a):
    return ACTION_NAMES.get(a, str(a))

def generate_rr_board(rows=16, cols=16):
    """
    Generate a Ricochet-Robots-style board:
    - perimeter walls
    - internal wall clusters
    - center block
    Returns (walls, targets)
    """

    walls = [[0 for _ in range(cols)] for _ in range(rows)]

    for r in range(rows):
        walls[r][0] |= W_LEFT
        walls[r][cols-1] |= W_RIGHT

    for c in range(cols):
        walls[0][c] |= W_UP
        walls[rows-1][c] |= W_DOWN

    def add_wall(r, c, direction):
        if direction == "UP":
            walls[r][c] |= W_UP
            walls[r-1][c] |= W_DOWN
        elif direction == "DOWN":
            walls[r][c] |= W_DOWN
            walls[r+1][c] |= W_UP
        elif direction == "LEFT":
            walls[r][c] |= W_LEFT
            walls[r][c-1] |= W_RIGHT
        elif direction == "RIGHT":
            walls[r][c] |= W_RIGHT
            walls[r][c+1] |= W_LEFT

    clusters = [
        (1, 4, "LEFT", "UP"),
        (1, 14, "LEFT", "UP"),
        (2, 1, "RIGHT", "UP"),
        (2, 11, "LEFT", "DOWN"),
        (3, 6, "DOWN", "RIGHT"),
        (6, 3, "LEFT", "DOWN"),
        (6, 13, "RIGHT", "DOWN"),
        (8, 5, "UP", "RIGHT"),
        (9, 1, "RIGHT", "DOWN"),
        (9, 13, "LEFT", "DOWN"),
        (11, 9, "RIGHT", "DOWN"),
        (14, 3, "LEFT", "UP"),
        (14, 10, "LEFT", "UP"),
        (13, 5, "RIGHT", "UP"),
        (13, 14, "RIGHT", "UP"),
        (7, 7, "UP", "LEFT"),
        (7, 8, "UP", "RIGHT"),
        (8, 7, "DOWN", "LEFT"),
        (8, 8, "RIGHT", "DOWN"),
    ]

    for r, c, d1, d2 in clusters:
        add_wall(r, c, d1)
        add_wall(r, c, d2)

    single_walls = [
        (0, 1, "RIGHT"),
        (0, 9, "RIGHT"),
        (5, 0, "DOWN"),
        (11, 0, "DOWN"),
        (15, 6, "RIGHT"),
        (15, 11, "RIGHT"),
        (3, 15, "DOWN"),
        (11, 15, "DOWN"),
        (6, 10, "DOWN"),
    ]

    for r, c, d in single_walls:
        add_wall(r, c, d)

    targets = [
        (1, 4),
        (1, 14),
        (2, 1),
        (2, 11),
        (3, 6),
        (6, 3),
        (6, 13),
        (8, 5),
        (9, 1),
        (9, 13),
        (11, 9),
        (14, 3),
        (14, 10),
        (13, 5),
        (13, 14),
    ]

    return walls, targets


def manual_play():
    walls, targets = generate_rr_board()

    model = RRModel(16, 16, walls, goal_pos=None)
    start, goal = generate_solvable_puzzle_2robots(
        model,
        targets,
        scramble_steps=40
    )
    model.goal_pos = goal

    state = start
    step = 0

    print("\n🎮 Ricochet Robots - Manual Play")
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


if __name__ == "__main__":
    manual_play()
