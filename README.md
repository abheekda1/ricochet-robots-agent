# Ricochet Robots Agent
*Authors: Kashvi Pundir, Daniel Wang, Abheek Dhawan*

This project evaluates different AI techniques on a simplified version of the **Ricochet Robots** puzzle game.

## Overview
- Grid size: 16×16 with walls
- Robots slide until they hit a wall or another robot
- Goal: move the target robot to a specified goal square
- Robot counts tested: 2, 3, and 4

Algorithms compared:
- BFS (Breadth-First Search)
- IDDFS (Iterative Deepening DFS)
- MCTS (Monte Carlo Tree Search)
- Value Iteration (2 robots only)

## Files
- `makefile`: Builds and runs the test script
- `test.py`: Generates puzzles, runs agents, and reports results

## Requirements
- Python 3
- `pypy3`

## How to Run

### Build
Creates an executable wrapper for the test script.
```bash
make build
```

### Single Run
Runs one comparison for each robot count.
```bash
make singletest
```

### Multiple Trials (100 recommended)
Runs multiple randomized trials and aggregates results.
```bash
make test RUNS=[num trials]
```

## Our Results
```
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
```