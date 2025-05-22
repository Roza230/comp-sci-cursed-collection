import os
import matplotlib.pyplot as plt # type: ignore
import numpy as np # type: ignore

def visualize_results(results):
    """Generate visualizations for the algorithm comparison"""
    # Create the directory if it doesn't exist
    os.makedirs("results", exist_ok=True)
    
    # Prepare data
    sizes = list(results.keys())
    scramble_depths = list(results[sizes[0]].keys())
    alg_names = list(results[sizes[0]][scramble_depths[0]].keys())
    
    # 1. Time comparison by cube size
    plt.figure(figsize=(10, 6))
    for alg_name in alg_names:
        times = []
        for size in sizes:
            # Average across all scramble depths
            avg_time = np.mean([results[size][depth][alg_name]['time_taken'] 
                               for depth in results[size].keys()])
            times.append(avg_time)
        plt.plot(sizes, times, marker='o', label=alg_name)
    
    plt.xlabel('Cube Size')
    plt.ylabel('Average Time (seconds)')
    plt.title('Algorithm Performance by Cube Size')
    plt.legend()
    plt.grid(True)
    plt.savefig('results/time_comparison_by_size.png')
    
    # 2. Time comparison by scramble complexity
    plt.figure(figsize=(10, 6))
    for alg_name in alg_names:
        times = []
        for depth in scramble_depths:
            # Average across all cube sizes
            avg_time = np.mean([results[size][depth][alg_name]['time_taken'] 
                               for size in results.keys()])
            times.append(avg_time)
        plt.plot(scramble_depths, times, marker='o', label=alg_name)
    
    plt.xlabel('Scramble Complexity (number of moves)')
    plt.ylabel('Average Time (seconds)')
    plt.title('Algorithm Performance by Scramble Complexity')
    plt.legend()
    plt.grid(True)
    plt.savefig('results/time_comparison_by_complexity.png')
    
    # 3. Memory comparison
    plt.figure(figsize=(10, 6))
    for alg_name in alg_names:
        memory = []
        for size in sizes:
            # Average across all scramble depths
            avg_memory = np.mean([results[size][depth][alg_name]['max_memory'] 
                                for depth in results[size].keys()])
            memory.append(avg_memory)
        plt.plot(sizes, memory, marker='o', label=alg_name)
    
    plt.xlabel('Cube Size')
    plt.ylabel('Memory Usage (MB)')
    plt.title('Memory Usage by Cube Size')
    plt.legend()
    plt.grid(True)
    plt.savefig('results/memory_comparison.png')
    
    # 4. Nodes expanded comparison
    plt.figure(figsize=(10, 6))
    for alg_name in alg_names:
        nodes = []
        for size in sizes:
            # Average across all scramble depths
            avg_nodes = np.mean([results[size][depth][alg_name]['nodes_expanded'] 
                               for depth in results[size].keys()])
            nodes.append(avg_nodes)
        plt.plot(sizes, nodes, marker='o', label=alg_name)
    
    plt.xlabel('Cube Size')
    plt.ylabel('Nodes Expanded')
    plt.title('Search Space Exploration by Cube Size')
    plt.legend()
    plt.grid(True)
    plt.savefig('results/nodes_comparison.png')
    
    # 5. Success rate
    plt.figure(figsize=(10, 6))
    for alg_name in alg_names:
        success_rates = []
        for size in sizes:
            # Count successful solves across all scramble depths
            successes = sum(1 for depth in results[size].keys() 
                           if results[size][depth][alg_name]['solution'] is not None)
            total = len(results[size].keys())
            success_rates.append(successes / total * 100)
        plt.plot(sizes, success_rates, marker='o', label=alg_name)
    
    plt.xlabel('Cube Size')
    plt.ylabel('Success Rate (%)')
    plt.title('Algorithm Success Rate by Cube Size')
    plt.legend()
    plt.grid(True)
    plt.savefig('results/success_rate.png')
    
    print("Visualizations saved to 'results' folder.")
    
    return [
        'results/time_comparison_by_size.png',
        'results/time_comparison_by_complexity.png',
        'results/memory_comparison.png',
        'results/nodes_comparison.png',
        'results/success_rate.png'
    ]
