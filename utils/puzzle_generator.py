import random
from model.model import UP, RIGHT, DOWN, LEFT


def place_blockers_near_goal(model, goal, count):
    """
    Place `count` blocker robots near the goal, without overlap.
    """
    gr, gc = goal

    candidates = [
        (gr, gc-1),
        (gr, gc+1),
        (gr-1, gc),
        (gr+1, gc),
        (gr-1, gc-1),
        (gr-1, gc+1),
        (gr+1, gc-1),
        (gr+1, gc+1),
    ]

    blockers = []
    for r, c in candidates:
        if len(blockers) == count:
            break
        if 0 <= r < model.rows and 0 <= c < model.cols:
            blockers.append((r, c))

    if len(blockers) < count:
        raise RuntimeError("Could not place enough blocker robots")

    return blockers


# ============================================================
# Solved states
# ============================================================

def make_solved_state_2robots(model, goal):
    blockers = place_blockers_near_goal(model, goal, count=1)
    return (
        goal,          # target robot
        blockers[0],   # blocker
    )


def make_solved_state_3robots(model, goal):
    blockers = place_blockers_near_goal(model, goal, count=2)
    return (
        goal,          # target robot
        blockers[0],
        blockers[1],
    )


def make_solved_state_4robots(model, goal):
    blockers = place_blockers_near_goal(model, goal, count=3)
    return (
        goal,          # target robot
        blockers[0],
        blockers[1],
        blockers[2],
    )


# ============================================================
# Reverse scramble
# ============================================================

def scramble_state(model, state, steps=40):
    """
    Apply random legal moves starting from a solved state.
    Avoid immediate backtracking.
    """
    current = state
    previous = None

    for _ in range(steps):
        successors = list(model.successors(current))

        # Avoid undoing the previous move
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

def generate_solvable_puzzle_2robots(model, targets, scramble_steps=40):
    goal = random.choice(targets)
    model.goal = goal

    solved_state = make_solved_state_2robots(model, goal)
    start_state = scramble_state(model, solved_state, scramble_steps)

    return start_state, goal


def generate_solvable_puzzle_3robots(model, targets, scramble_steps=40):
    goal = random.choice(targets)
    model.goal = goal

    solved_state = make_solved_state_3robots(model, goal)
    start_state = scramble_state(model, solved_state, scramble_steps)

    return start_state, goal


def generate_solvable_puzzle_4robots(model, targets, scramble_steps=40):
    goal = random.choice(targets)
    model.goal = goal

    solved_state = make_solved_state_4robots(model, goal)
    start_state = scramble_state(model, solved_state, scramble_steps)

    return start_state, goal
