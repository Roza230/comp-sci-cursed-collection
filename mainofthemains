import os
import json
import time
import sys

# Import cube and solver functions
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from algorithms.cube import create_solved_cube, scramble_cube
from algorithms.solver import dfs, bfs, a_star

def test_algorithms(cube_sizes=[2, 3], scramble_moves=[5, 10], algorithms=None):
    """Test different algorithms on various cube sizes and scramble complexities"""
    if algorithms is None:
        algorithms = {
            'DFS': dfs,
            'BFS': bfs,
            'A*': a_star
        }
    
    results = {}
    
    for size in cube_sizes:
        results[size] = {}
        for scramble_depth in scramble_moves:
            print(f"Testing cube size {size}x{size}x{size} with {scramble_depth} scramble moves")
            solved_cube = create_solved_cube(size)
            scrambled_cube, scramble_sequence = scramble_cube(solved_cube, scramble_depth)
            
            results[size][scramble_depth] = {}
            
            for alg_name, alg_func in algorithms.items():
                print(f"  Running {alg_name}...")
                
                # For larger cubes and complex scrambles, limit DFS/BFS depth
                max_depth = min(10, scramble_depth + 2)
                if size > 3 and alg_name in ['DFS', 'BFS']:
                    max_depth = min(5, scramble_depth)
                
                result = alg_func(scrambled_cube, max_depth)
                results[size][scramble_depth][alg_name] = result
                
                print(f"    {'Solved' if result['solution'] else 'Not solved'} - "
                      f"Nodes: {result['nodes_expanded']}, "
                      f"Time: {result['time_taken']:.2f}s, "
                      f"Memory: {result['max_memory']:.2f}MB")
    
    return results

def create_time_comparison_table(results):
    """Create a table comparing execution times of algorithms"""
    print("\n=== TIME COMPARISON TABLE (seconds) ===")
    print(f"{'Cube Size':10} {'Scramble':10} {'DFS':10} {'BFS':10} {'A*':10}")
    print("-" * 55)
    
    for size in results:
        for depth in results[size]:
            dfs_time = results[size][depth]['DFS']['time_taken']
            bfs_time = results[size][depth]['BFS']['time_taken']
            astar_time = results[size][depth]['A*']['time_taken']
            
            print(f"{size}x{size}x{size:<10} {depth:<10} {dfs_time:<10.4f} {bfs_time:<10.4f} {astar_time:<10.4f}")

def save_results_to_csv(results, filename="results/time_comparison.csv"):
    """Save detailed results to CSV for report"""
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, "w") as f:
        f.write("Cube Size,Scramble Depth,Algorithm,Time (s),Nodes Expanded,Memory (MB),Solution Found\n")
        
        for size in results:
            for depth in results[size]:
                for alg in results[size][depth]:
                    r = results[size][depth][alg]
                    solution_found = "Yes" if r['solution'] is not None else "No"
                    f.write(f"{size},{depth},{alg},{r['time_taken']:.4f},{r['nodes_expanded']},{r['max_memory']:.4f},{solution_found}\n")

if __name__ == "__main__":
    # Define test parameters - start small for testing
    cube_sizes = [2, 3]  # Add 4, 5, 6 for full testing later
    scramble_depths = [3, 5]  # Start with small values
    
    # Run the tests
    print("Starting Rubik's Cube solver tests...")
    results = test_algorithms(cube_sizes, scramble_depths)
    
    # Save results
    os.makedirs("results", exist_ok=True)
    with open("results/algorithm_comparison.json", "w") as f:
        json.dump(results, f, default=str)  # Use default=str for non-serializable objects
    
    # Display time comparison table
    create_time_comparison_table(results)
    
    # Save detailed results to CSV
    save_results_to_csv(results)
    
    # Generate visualizations
    from visual.display import visualize_results
    visualize_results(results)
    
    print("Testing complete. Results saved to 'results' folder.")
