from agent.bfs import BFSAgent
from agent.iddfs import IDDFSAgent
from agent.mcts import MCTSAgent
from manual_play import generate_rr_board
from model.model import RRModel
import time
from utils.puzzle_generator import generate_solvable_puzzle_2robots


def test_agent(agent, model, start_state, agent_name, max_moves=50):
    """Test a single agent and return results"""
    state = start_state
    actions_taken = []
    
    start_time = time.time()
    
    for move_number in range(1, max_moves + 1):
        if model.is_terminal(state):
            elapsed = time.time() - start_time
            return {
                "agent": agent_name,
                "moves": move_number - 1,
                "time": elapsed,
                "success": True
            }
        
        action = agent.choose_action(state)
        
        if action is None:
            elapsed = time.time() - start_time
            return {
                "agent": agent_name,
                "moves": None,
                "time": elapsed,
                "success": False
            }
        
        actions_taken.append(action)
        state = model.transition(state, action)
    
    elapsed = time.time() - start_time
    return {
        "agent": agent_name,
        "moves": None,
        "time": elapsed,
        "success": False
    }


def compare_all_agents(scramble_steps=40, max_moves=50):
    """Compare BFS, IDDFS, and MCTS on the same puzzle"""
    
    print("\n" + "="*70)
    print("AGENT COMPARISON")
    print("="*70)
    
    # Generate puzzle
    walls, targets = generate_rr_board()
    model = RRModel(16, 16, walls, goal_pos=None)
    
    start, goal = generate_solvable_puzzle_2robots(
        model,
        targets,
        scramble_steps=scramble_steps
    )
    model.goal_pos = goal
    
    print(f"\nPuzzle: Start={start}, Goal={goal}")
    print(model.render(start))
    
    # Create agents
    agents = [
        (BFSAgent(model, max_nodes=100_000), "BFS"),
        (IDDFSAgent(model, max_depth=30, max_nodes=100_000), "IDDFS"),
        (MCTSAgent(model, time=0.5, rollout_depth=15), "MCTS")
    ]
    
    # Test each agent
    results = []
    for agent, name in agents:
        print(f"\nTesting {name}...")
        result = test_agent(agent, model, start, name, max_moves)
        results.append(result)
        
        if result["success"]:
            print(f"  ✓ {result['moves']} moves in {result['time']:.3f}s")
        else:
            print(f"  ✗ Failed in {result['time']:.3f}s")
    
    # Print summary
    print("\n" + "="*70)
    print("RESULTS")
    print("="*70)
    print(f"{'Agent':<15} {'Moves':<10} {'Time (s)':<12} {'Status':<10}")
    print("-" * 70)
    
    for result in results:
        moves = result["moves"] if result["moves"] is not None else "FAILED"
        time_val = f"{result['time']:.3f}"
        status = "✓" if result["success"] else "✗"
        
        print(f"{result['agent']:<15} {str(moves):<10} {time_val:<12} {status:<10}")
    
    # Analysis
    successful = [r for r in results if r["success"]]
    
    if successful:
        optimal_moves = min(r["moves"] for r in successful)
        print(f"\nOptimal solution: {optimal_moves} moves")
        
        for result in successful:
            if result["moves"] == optimal_moves:
                print(f"  {result['agent']}: Optimal")
            else:
                extra = result["moves"] - optimal_moves
                print(f"  {result['agent']}: +{extra} moves")
    
    print("\n" + "="*70)
    return results


def run_multiple_tests(num_tests=5, scramble_steps=40):
    """Run multiple tests and aggregate results"""
    
    print(f"\n{'='*70}")
    print(f"RUNNING {num_tests} TESTS")
    print(f"{'='*70}")
    
    all_results = {
        "BFS": {"moves": [], "time": [], "success": 0},
        "IDDFS": {"moves": [], "time": [], "success": 0},
        "MCTS": {"moves": [], "time": [], "success": 0}
    }
    
    for test_num in range(1, num_tests + 1):
        print(f"\n--- Test {test_num}/{num_tests} ---")
        
        results = compare_all_agents(scramble_steps=scramble_steps, max_moves=50)
        
        for result in results:
            agent_name = result["agent"]
            if result["success"]:
                all_results[agent_name]["moves"].append(result["moves"])
                all_results[agent_name]["time"].append(result["time"])
                all_results[agent_name]["success"] += 1
    
    # Print aggregate
    print("\n" + "="*70)
    print(f"AGGREGATE RESULTS ({num_tests} tests)")
    print("="*70)
    print(f"{'Agent':<15} {'Avg Moves':<12} {'Avg Time':<12} {'Success Rate':<15}")
    print("-" * 70)
    
    for agent_name, data in all_results.items():
        if data["moves"]:
            avg_moves = sum(data["moves"]) / len(data["moves"])
            avg_time = sum(data["time"]) / len(data["time"])
            success_rate = (data["success"] / num_tests) * 100
            
            print(f"{agent_name:<15} {avg_moves:<12.1f} {avg_time:<12.3f} {success_rate:<15.0f}%")
        else:
            print(f"{agent_name:<15} {'N/A':<12} {'N/A':<12} {'0%':<15}")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "multiple":
        num = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        run_multiple_tests(num_tests=num)
    else:
        compare_all_agents()
