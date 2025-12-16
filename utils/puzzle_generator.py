import random
from model.model import UP, RIGHT, DOWN, LEFT

# ------------------------------------------------------------
# Solved state for 2 robots
# ------------------------------------------------------------

def make_solved_state_2robots(model, goal):
    gr, gc = goal

    candidates = [
        (gr, gc-1),
        (gr, gc+1),
        (gr-1, gc),
        (gr+1, gc),
    ]

    for br, bc in candidates:
        if 0 <= br < model.rows and 0 <= bc < model.cols:
            return (
                (gr, gc),    # target robot
                (br, bc),    # blocker robot
            )

    raise RuntimeError("Could not place blocker robot")


# ------------------------------------------------------------
# Reverse scramble
# ------------------------------------------------------------

def scramble_state(model, state, steps=40):
    current = state
    previous = None

    for _ in range(steps):
        successors = list(model.successors(current))

        if previous is not None:
            successors = [
                (s, a) for (s, a) in successors if s != previous
            ]

        if not successors:
            continue

        next_state, _ = random.choice(successors)
        previous = current
        current = next_state

    return current


# ------------------------------------------------------------
# Public API: generate solvable puzzle
# ------------------------------------------------------------

def generate_solvable_puzzle_2robots(model, targets, scramble_steps=40):
    goal = random.choice(targets)
    model.goal = goal

    solved_state = make_solved_state_2robots(model, goal)
    start_state = scramble_state(model, solved_state, scramble_steps)

    return start_state, goal
