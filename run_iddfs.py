from agent.iddfs import IDDFSAgent
from manual_play import generate_rr_board
from model.model import RRModel, UP, RIGHT, DOWN, LEFT
import time
from utils.puzzle_generator import generate_solvable_puzzle_2robots


def announce_move(move):
    names = {UP: "UP", RIGHT: "RIGHT", DOWN: "DOWN", LEFT: "LEFT"}
    return names.get(move, f"?{move}")


def test_iddfs_game():
    walls, targets = generate_rr_board()

    model = RRModel(16, 16, walls, goal_pos=None)
    start, goal = generate_solvable_puzzle_2robots(
        model,
        targets,
        scramble_steps=40
    )
    model.goal_pos = goal

    state = start

    print("\n=== Ricochet Robots IDDFS Demo ===")
    print("Start:", start, "Goal:", goal)

    agent = IDDFSAgent(model, max_depth=30, max_nodes=100_000)

    print(model.render(state))

    MAX_MOVES = 50
    for move_number in range(1, MAX_MOVES + 1):

        if model.is_terminal(state):
            print(f"Reached the goal in {move_number - 1} moves!")
            return

        print(f"\n--- Move {move_number} ---")
        print("Current state:", state)
        print("Next states:", list(model.successors(state)))

        action = agent.choose_action(state)

        if action is None:
            print("IDDFS returned no action. Stopping.")
            return

        print("Chosen action:", announce_move(action))

        new_state = model.transition(state, action)
        print("New state:", new_state)

        if new_state == state:
            print("WARNING: action did not change state! (wall blocked?)")

        state = new_state
        print(model.render(state))

    print("\nFAILED: Did not reach goal within move limit.")


if __name__ == "__main__":
    test_iddfs_game()
