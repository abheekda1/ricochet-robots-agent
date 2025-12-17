from agent.bfs import BFSAgent
from agent.iddfs import IDDFSAgent
from agent.mcts import MCTSAgent

from manual_play import generate_rr_board
from model.model import RRModel

from utils.puzzle_generator import (
    generate_solvable_puzzle_2robots,
    generate_solvable_puzzle_3robots,
    generate_solvable_puzzle_4robots,
)

import time
import sys


# ============================================================
# Agent test helper
# ============================================================

def test_agent(agent, model, start_state, agent_name, max_moves=50):
    state = start_state
    start_time = time.time()

    for move_number in range(1, max_moves + 1):
        if model.is_terminal(state):
            return {
                "agent": agent_name,
                "moves": move_number - 1,
                "time": time.time() - start_time,
                "success": True
            }

        action = agent.choose_action(state)
        if action is None:
            break

        state = model.transition(state, action)

    return {
        "agent": agent_name,
        "moves": None,
        "time": time.time() - start_time,
        "success": False
    }


# ============================================================
# Puzzle generation by robot count
# ============================================================

def generate_puzzle(model, targets, robot_count, scramble_steps):
    if robot_count == 2:
        return generate_solvable_puzzle_2robots(model, targets, scramble_steps)
    elif robot_count == 3:
        return generate_solvable_puzzle_3robots(model, targets, scramble_steps)
    elif robot_count == 4:
        return generate_solvable_puzzle_4robots(model, targets, scramble_steps)
    else:
        raise ValueError("Robot count must be 2, 3, or 4")


# ============================================================
# Compare agents for a given robot count
# ============================================================

def compare_agents_for_robot_count(robot_count, scramble_steps=40, max_moves=50):
    print("\n" + "=" * 80)
    print(f"COMPARISON — {robot_count} ROBOTS")
    print("=" * 80)

    walls, targets = generate_rr_board()
    model = RRModel(16, 16, walls, goal_pos=None)

    start, goal = generate_puzzle(model, targets, robot_count, scramble_steps)
    model.goal = goal

    print(f"\nStart: {start}")
    print(f"Goal : {goal}")
    print(model.render(start))

    agents = [
        (BFSAgent(model, max_nodes=100_000), "BFS"),
        (IDDFSAgent(model, max_depth=100, max_nodes=100_000), "IDDFS"),
        (MCTSAgent(model, time=0.5, rollout_depth=100), "MCTS"),
    ]

    results = []
    for agent, name in agents:
        print(f"\nTesting {name}...")
        result = test_agent(agent, model, start, name, max_moves)
        results.append(result)

        if result["success"]:
            print(f"  ✓ {result['moves']} moves in {result['time']:.3f}s")
        else:
            print(f"  ✗ Failed in {result['time']:.3f}s")

    return results


# ============================================================
# Run experiments across robot counts
# ============================================================

def compare_all_agents(robot_counts=(2, 3, 4), scramble_steps=1000, max_moves=50):
    all_results = {}

    for rc in robot_counts:
        results = compare_agents_for_robot_count(
            rc, scramble_steps=scramble_steps, max_moves=max_moves
        )
        all_results[rc] = results

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"{'Robots':<8} {'Agent':<10} {'Moves':<10} {'Time (s)':<12} {'Status'}")
    print("-" * 80)

    for rc, results in all_results.items():
        for r in results:
            moves = r["moves"] if r["moves"] is not None else "FAILED"
            status = "✓" if r["success"] else "✗"
            print(f"{rc:<8} {r['agent']:<10} {str(moves):<10} {r['time']:<12.3f} {status}")

    return all_results


# ============================================================
# Multiple trials (aggregate stats)
# ============================================================

def run_multiple_tests(num_tests=5, robot_counts=(2, 3, 4), scramble_steps=1000):
    stats = {}

    for rc in robot_counts:
        stats[rc] = {
            "BFS": {"success": 0, "moves": [], "time": []},
            "IDDFS": {"success": 0, "moves": [], "time": []},
            "MCTS": {"success": 0, "moves": [], "time": []},
        }

    for i in range(num_tests):
        print(f"\n### Trial {i+1}/{num_tests} ###")
        results = compare_all_agents(
            robot_counts=robot_counts,
            scramble_steps=scramble_steps
        )

        for rc, agent_results in results.items():
            for r in agent_results:
                agent = r["agent"]
                if r["success"]:
                    stats[rc][agent]["success"] += 1
                    stats[rc][agent]["moves"].append(r["moves"])
                    stats[rc][agent]["time"].append(r["time"])

    print("\n" + "=" * 80)
    print("AGGREGATE RESULTS")
    print("=" * 80)

    for rc in robot_counts:
        print(f"\n--- {rc} ROBOTS ---")
        print(f"{'Agent':<10} {'Success %':<10} {'Avg Moves':<12} {'Avg Time (s)'}")
        print("-" * 60)

        for agent, data in stats[rc].items():
            if data["moves"]:
                success_rate = 100 * data["success"] / num_tests
                avg_moves = sum(data["moves"]) / len(data["moves"])
                avg_time = sum(data["time"]) / len(data["time"])
                print(f"{agent:<10} {success_rate:<10.0f} {avg_moves:<12.1f} {avg_time:<.3f}")
            else:
                print(f"{agent:<10} 0%         N/A          N/A")


# ============================================================
# Entry point
# ============================================================

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "multiple":
        run_multiple_tests(num_tests=5)
    else:
        compare_all_agents()
