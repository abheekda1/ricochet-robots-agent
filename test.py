"""
Ricochet Robots - Final Project Test Script (CS 474)
Kashvi Pundir, Daniel Wang, Abheek Dhawan
https://github.com/abheekda1/ricochet-robots-agent

Game Description:
This project models a simplified version of the Ricochet Robots puzzle game.
Robots move on a fixed 16x16 grid with walls. When a robot moves in a direction,
it slides until it hits a wall or another robot. The goal is to move a designated
target robot to a specified goal square.

Research Question:
How do different computational intelligence techniques scale as the number of
robots increases in Ricochet Robots? In particular, how do search algorithms like BFS and IDDFS,
reinforcement learning, and Monte Carlo Tree Search compare in terms of success
rate, solution quality, and runtime?

Algorithms Compared:
- BFS (Breadth-First Search): Optimal but exhaustive search.
- IDDFS (Iterative Deepening DFS): Depth-limited exhaustive search.
- MCTS (Monte Carlo Tree Search): Online stochastic planning with rollouts.
- Value Iteration: Tabular dynamic programming (only feasible for 2 robots).

What This Script Does:
This script generates solvable Ricochet Robots puzzles with 2, 3, and 4 robots
using reverse scrambling. For each puzzle, it runs the above agents and measures:
- whether the agent reaches the goal
- number of moves taken
- total runtime

The script can run a single comparison or multiple randomized trials and
aggregates the results.

Results Summary (from multiple trials):
- BFS and IDDFS solve small instances quickly but scale poorly as robot count grows.
- Value Iteration performs the best for 2 robots after training but becomes infeasible for larger cases.
- MCTS consistently achieves high success rates for 3-4 robots, at the cost of
  longer solutions and higher runtime.

How to Run:
Build:
    make build
This creates a `test` executable that runs the test script with pypy3.

Single run:
    make singletest

Multiple trials (recommended 10 for quick results):
    make test RUNS=[num trials]

The multiple-trial mode reproduces the aggregate results reported in the project.

Here are our results for 100 trials:
================================================================================
AGGREGATE RESULTS
================================================================================

--- 2 ROBOTS ---
Agent      Success %  Avg Moves    Avg Time (s)
------------------------------------------------------------
BFS        100        9.3          0.019
IDDFS      96         9.0          0.079
MCTS       93         15.5         7.760
VIter      100        9.3          3.354

--- 3 ROBOTS ---
Agent      Success %  Avg Moves    Avg Time (s)
------------------------------------------------------------
BFS        100        7.7          0.104
IDDFS      87         7.1          0.065
MCTS       91         14.1         7.057
VIter      0%         N/A          N/A

--- 4 ROBOTS ---
Agent      Success %  Avg Moves    Avg Time (s)
------------------------------------------------------------
BFS        88         6.3          0.140
IDDFS      72         5.8          0.067
MCTS       91         14.0         6.986
VIter      0%         N/A          N/A
"""

from agent.bfs import BFSAgent
from agent.iddfs import IDDFSAgent
from agent.mcts import MCTSAgent

from agent.rl import ValueIterationAgent
from manual_play import generate_rr_board
from model.model import RRModel

from utils.puzzle_generator import (
    generate_solvable_puzzle_2robots,
    generate_solvable_puzzle_3robots,
    generate_solvable_puzzle_4robots,
)

import time
import sys


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


def generate_puzzle(model, targets, robot_count, scramble_steps):
    if robot_count == 2:
        return generate_solvable_puzzle_2robots(model, targets, scramble_steps)
    elif robot_count == 3:
        return generate_solvable_puzzle_3robots(model, targets, scramble_steps)
    elif robot_count == 4:
        return generate_solvable_puzzle_4robots(model, targets, scramble_steps)
    else:
        raise ValueError("Robot count must be 2, 3, or 4")


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
        (ValueIterationAgent(model, num_robots=robot_count, discount=0.9, num_iterations=20), "VIter"),
    ]

    results = []
    for agent, name in agents:
        if name == "VIter" and robot_count > 2:
            print(f"\nSkipping {name} for {robot_count} robots (not supported).")
            continue
        print(f"\nTesting {name}...")
        result = test_agent(agent, model, start, name, max_moves)
        results.append(result)

        if result["success"]:
            print(f"  ✓ {result['moves']} moves in {result['time']:.3f}s")
        else:
            print(f"  ✗ Failed in {result['time']:.3f}s")

    return results


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


def run_multiple_tests(num_tests=5, robot_counts=(2, 3, 4), scramble_steps=1000):
    stats = {}

    for rc in robot_counts:
        stats[rc] = {
            "BFS": {"success": 0, "moves": [], "time": []},
            "IDDFS": {"success": 0, "moves": [], "time": []},
            "MCTS": {"success": 0, "moves": [], "time": []},
            "VIter": {"success": 0, "moves": [], "time": []},
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


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_multiple_tests(num_tests=int(sys.argv[1]))
    else:
        compare_all_agents()
