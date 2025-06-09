import time
import random
import math
import psutil
import os
from typing import List, Tuple, Optional
import numpy as np

class OptimizedNQueensSolver:
  
      # Optimized N-Queens solver with improved algorithms and performance
    
    
    def __init__(self, n: int):
        self.n = n
        self.solutions_found = 0
        self.nodes_explored = 0
        
    def conflicts_fast(self, board: List[int]) -> int:
        # Optimized conflict counting using numpy-like operations
        conflicts = 0
        n = len(board)
        
        # Count column conflicts
        seen_cols = set()
        for col in board:
            if col in seen_cols:
                conflicts += 1
            seen_cols.add(col)
        
        # Count diagonal conflicts efficiently
        diag1 = {}  # row - col
        diag2 = {}  # row + col
        
        for row, col in enumerate(board):
            d1, d2 = row - col, row + col
            
            if d1 in diag1:
                conflicts += diag1[d1]
                diag1[d1] += 1
            else:
                diag1[d1] = 1
                
            if d2 in diag2:
                conflicts += diag2[d2]
                diag2[d2] += 1
            else:
                diag2[d2] = 1
        
        return conflicts
    
    def is_safe_fast(self, board: List[int], row: int, col: int) -> bool:
        # Optimized safety check
        for i in range(row):
            if (board[i] == col or 
                board[i] - i == col - row or 
                board[i] + i == col + row):
                return False
        return True
    
    # 1. OPTIMIZED EXHAUSTIVE DFS WITH TIMEOUT
    def solve_exhaustive_dfs(self, timeout_seconds: int = 300) -> Tuple[Optional[List[int]], dict]:
        """Optimized exhaustive DFS with timeout protection"""
        start_time = time.time()
        start_memory = self.get_memory_usage()
        
        self.solutions_found = 0
        self.nodes_explored = 0
        timeout_reached = False
        
        def dfs_optimized(board: List[int], row: int, cols_used: set, 
                         diag1_used: set, diag2_used: set) -> Optional[List[int]]:
            nonlocal timeout_reached
            
            # Check timeout every 10000 nodes to avoid constant time checking
            if self.nodes_explored % 10000 == 0:
                if time.time() - start_time > timeout_seconds:
                    timeout_reached = True
                    return None
            
            self.nodes_explored += 1
            
            if row == self.n:
                self.solutions_found += 1
                return board[:]
            
            for col in range(self.n):
                if timeout_reached:
                    return None
                    
                if col in cols_used:
                    continue
                    
                d1, d2 = row - col, row + col
                if d1 in diag1_used or d2 in diag2_used:
                    continue
                
                # Place queen
                board[row] = col
                cols_used.add(col)
                diag1_used.add(d1)
                diag2_used.add(d2)
                
                result = dfs_optimized(board, row + 1, cols_used, diag1_used, diag2_used)
                if result is not None:
                    return result
                
                # Backtrack
                cols_used.remove(col)
                diag1_used.remove(d1)
                diag2_used.remove(d2)
            
            return None
        
        board = [-1] * self.n
        solution = dfs_optimized(board, 0, set(), set(), set())
        
        end_time = time.time()
        end_memory = self.get_memory_usage()
        
        stats = {
            'time': end_time - start_time,
            'memory': end_memory - start_memory,
            'nodes_explored': self.nodes_explored,
            'solutions_found': self.solutions_found,
            'success': solution is not None and not timeout_reached,
            'timeout': timeout_reached
        }
        
        return solution, stats
    
    # 2. OPTIMIZED HILL CLIMBING WITH RESTARTS
    def solve_greedy_hill_climbing(self, max_restarts: int = 100) -> Tuple[Optional[List[int]], dict]:
        """Hill climbing with random restarts to escape local optima"""
        start_time = time.time()
        start_memory = self.get_memory_usage()
        
        best_solution = None
        best_conflicts = float('inf')
        total_iterations = 0
        
        for restart in range(max_restarts):
            # Random restart
            board = list(range(self.n))
            random.shuffle(board)
            
            current_conflicts = self.conflicts_fast(board)
            if current_conflicts == 0:
                best_solution = board[:]
                break
            
            iterations = 0
            max_iterations = self.n * 10  # Limit iterations per restart
            
            while current_conflicts > 0 and iterations < max_iterations:
                iterations += 1
                total_iterations += 1
                
                best_move = None
                best_move_conflicts = current_conflicts
                
                # Try moving each queen
                for col in range(self.n):
                    original_row = board[col]
                    
                    # Try each position in this column
                    for new_row in range(self.n):
                        if new_row != original_row:
                            board[col] = new_row
                            conflicts = self.conflicts_fast(board)
                            
                            if conflicts < best_move_conflicts:
                                best_move_conflicts = conflicts
                                best_move = (col, new_row, conflicts)
                            
                            board[col] = original_row  # Restore
                
                # Make the best move if it improves
                if best_move and best_move[2] < current_conflicts:
                    board[best_move[0]] = best_move[1]
                    current_conflicts = best_move[2]
                    
                    if current_conflicts == 0:
                        best_solution = board[:]
                        break
                else:
                    # No improvement, restart
                    break
            
            if current_conflicts < best_conflicts:
                best_conflicts = current_conflicts
                if current_conflicts == 0:
                    best_solution = board[:]
                    break
        
        end_time = time.time()
        end_memory = self.get_memory_usage()
        
        stats = {
            'time': end_time - start_time,
            'memory': end_memory - start_memory,
            'iterations': total_iterations,
            'restarts': restart + 1,
            'final_conflicts': best_conflicts,
            'success': best_conflicts == 0
        }
        
        return best_solution, stats
    
    # 3. OPTIMIZED SIMULATED ANNEALING
    def solve_simulated_annealing(self, max_iterations: int = None) -> Tuple[Optional[List[int]], dict]:
        """Optimized simulated annealing with adaptive parameters"""
        start_time = time.time()
        start_memory = self.get_memory_usage()
        
        if max_iterations is None:
            max_iterations = self.n * 1000  # Adaptive based on problem size
        
        # Initialize with random permutation
        current_board = list(range(self.n))
        random.shuffle(current_board)
        current_conflicts = self.conflicts_fast(current_board)
        
        best_board = current_board[:]
        best_conflicts = current_conflicts
        
        # Adaptive temperature
        initial_temp = self.n * 10.0
        temperature = initial_temp
        cooling_rate = 0.99
        
        for iteration in range(max_iterations):
            if current_conflicts == 0:
                break
            
            # Generate neighbor efficiently
            new_board = current_board[:]
            
            # Swap two random positions (maintains permutation)
            i, j = random.sample(range(self.n), 2)
            new_board[i], new_board[j] = new_board[j], new_board[i]
            
            new_conflicts = self.conflicts_fast(new_board)
            
            # Accept or reject
            delta = current_conflicts - new_conflicts
            if delta > 0 or (temperature > 0.01 and random.random() < math.exp(delta / temperature)):
                current_board = new_board
                current_conflicts = new_conflicts
                
                if current_conflicts < best_conflicts:
                    best_board = current_board[:]
                    best_conflicts = current_conflicts
            
            # Cool down
            temperature *= cooling_rate
            
            # Reheat if stuck
            if iteration % (max_iterations // 10) == 0 and temperature < 1.0:
                temperature = initial_temp * 0.1
        
        end_time = time.time()
        end_memory = self.get_memory_usage()
        
        stats = {
            'time': end_time - start_time,
            'memory': end_memory - start_memory,
            'iterations': iteration + 1,
            'final_conflicts': best_conflicts,
            'success': best_conflicts == 0
        }
        
        return best_board if best_conflicts == 0 else None, stats
    
    # 4. OPTIMIZED GENETIC ALGORITHM
    def solve_genetic_algorithm(self, population_size: int = None, 
                              max_generations: int = None) -> Tuple[Optional[List[int]], dict]:
        """Optimized genetic algorithm with better operators"""
        start_time = time.time()
        start_memory = self.get_memory_usage()
        
        # Adaptive parameters
        if population_size is None:
            population_size = min(100, max(50, self.n * 2))
        if max_generations is None:
            max_generations = min(1000, max(100, self.n * 10))
        
        def create_individual() -> List[int]:
            """Create random permutation"""
            individual = list(range(self.n))
            random.shuffle(individual)
            return individual
        
        def fitness(individual: List[int]) -> int:
            """Higher fitness = fewer conflicts"""
            max_conflicts = self.n * (self.n - 1) // 2
            return max_conflicts - self.conflicts_fast(individual)
        
        def tournament_selection(population: List[List[int]], k: int = 3) -> List[int]:
            """Tournament selection"""
            tournament = random.sample(population, min(k, len(population)))
            return max(tournament, key=fitness)
        
        def pmx_crossover(parent1: List[int], parent2: List[int]) -> Tuple[List[int], List[int]]:
            """Partially Mapped Crossover (PMX) - better for permutations"""
            n = len(parent1)
            start, end = sorted(random.sample(range(n), 2))
            
            child1, child2 = [-1] * n, [-1] * n
            
            # Copy segments
            child1[start:end] = parent1[start:end]
            child2[start:end] = parent2[start:end]
            
            # Create mapping
            def complete_child(child, other_parent, parent):
                for i in range(n):
                    if child[i] == -1:
                        val = other_parent[i]
                        while val in child[start:end]:
                            idx = parent.index(val)
                            val = other_parent[idx]
                        child[i] = val
            
            complete_child(child1, parent2, parent1)
            complete_child(child2, parent1, parent2)
            
            return child1, child2
        
        def mutate(individual: List[int], mutation_rate: float = 0.1) -> List[int]:
            """Improved mutation with multiple operators"""
            if random.random() < mutation_rate:
                if random.random() < 0.5:
                    # Swap mutation
                    i, j = random.sample(range(self.n), 2)
                    individual[i], individual[j] = individual[j], individual[i]
                else:
                    # Inversion mutation
                    i, j = sorted(random.sample(range(self.n), 2))
                    individual[i:j+1] = reversed(individual[i:j+1])
            return individual
        
        # Initialize population
        population = [create_individual() for _ in range(population_size)]
        
        best_individual = None
        best_fitness = -1
        generation = 0
        stagnation_count = 0
        
        for generation in range(max_generations):
            # Evaluate fitness
            fitness_scores = [(individual, fitness(individual)) for individual in population]
            fitness_scores.sort(key=lambda x: x[1], reverse=True)
            
            current_best_fitness = fitness_scores[0][1]
            
            # Check for solution
            if current_best_fitness == self.n * (self.n - 1) // 2:
                best_individual = fitness_scores[0][0]
                best_fitness = current_best_fitness
                break
            
            # Update best and check stagnation
            if current_best_fitness > best_fitness:
                best_individual = fitness_scores[0][0][:]
                best_fitness = current_best_fitness
                stagnation_count = 0
            else:
                stagnation_count += 1
            
            # Early termination if stagnant
            if stagnation_count > max_generations // 10:
                break
            
            # Selection and reproduction
            new_population = []
            
            # Elitism - keep top 20%
            elite_size = population_size // 5
            new_population.extend([ind for ind, _ in fitness_scores[:elite_size]])
            
            # Generate offspring
            while len(new_population) < population_size:
                parent1 = tournament_selection(population)
                parent2 = tournament_selection(population)
                
                if random.random() < 0.8:  # Crossover probability
                    child1, child2 = pmx_crossover(parent1, parent2)
                else:
                    child1, child2 = parent1[:], parent2[:]
                
                new_population.extend([mutate(child1), mutate(child2)])
            
            population = new_population[:population_size]
        
        end_time = time.time()
        end_memory = self.get_memory_usage()
        
        is_solution = best_fitness == self.n * (self.n - 1) // 2
        
        stats = {
            'time': end_time - start_time,
            'memory': end_memory - start_memory,
            'generations': generation + 1,
            'best_fitness': best_fitness,
            'final_conflicts': self.n * (self.n - 1) // 2 - best_fitness if best_fitness >= 0 else -1,
            'success': is_solution
        }
        
        return best_individual if is_solution else None, stats
    
    def get_memory_usage(self) -> float:
        """Get current memory usage in MB"""
        try:
            process = psutil.Process(os.getpid())
            return process.memory_info().rss / 1024 / 1024
        except:
            return 0.0
    
    def print_board(self, board: List[int]):
        """Print the board in a readable format"""
        if board is None:
            print("No solution found")
            return
        
        print(f"\nSolution for {self.n}-Queens:")
        if self.n <= 20:  # Only print board for reasonable sizes
            for row in range(self.n):
                line = ""
                for col in range(self.n):
                    if board[row] == col:
                        line += "Q "
                    else:
                        line += ". "
                print(line)
        else:
            print(f"Board representation: {board[:10]}..." if self.n > 10 else f"Board: {board}")
        print()

def run_optimized_analysis():
    """Run optimized analysis with DFS for all N values"""
    problem_sizes = [10, 30, 50, 100, 200]
    
    results = []
    
    print("OPTIMIZED N-Queens Problem Analysis")
    print("=" * 50)
    
    for n in problem_sizes:
        print(f"\nTesting N = {n}")
        print("-" * 25)
        
        solver = OptimizedNQueensSolver(n)
        
        # 1. Exhaustive DFS with timeout (now for all N values)
        print("Running Optimized DFS...")
        try:
            # Set timeout based on problem size
            timeout = 60 if n <= 30 else 300 if n <= 100 else 600  # 1min, 5min, 10min
            solution, stats = solver.solve_exhaustive_dfs(timeout_seconds=timeout)
            
            results.append({
                'N': n, 'Algorithm': 'DFS', 'Time': stats['time'], 
                'Memory': stats['memory'], 'Success': stats['success'],
                'Nodes': stats['nodes_explored'], 'Timeout': stats['timeout']
            })
            
            if stats['timeout']:
                print(f"  DFS: TIMEOUT after {stats['time']:.1f}s - explored {stats['nodes_explored']:,} nodes")
            else:
                print(f"  DFS: {'✓' if stats['success'] else '✗'} - {stats['time']:.4f}s - {stats['nodes_explored']:,} nodes")
        except Exception as e:
            print(f"  DFS: Error - {e}")
        
        # 2. Hill Climbing with Restarts
        print("Running Hill Climbing...")
        solution, stats = solver.solve_greedy_hill_climbing()
        results.append({
            'N': n, 'Algorithm': 'Hill Climbing', 'Time': stats['time'], 
            'Memory': stats['memory'], 'Success': stats['success']
        })
        print(f"  Hill Climbing: {'✓' if stats['success'] else '✗'} - {stats['time']:.4f}s")
        
        # 3. Simulated Annealing
        print("Running Simulated Annealing...")
        solution, stats = solver.solve_simulated_annealing()
        results.append({
            'N': n, 'Algorithm': 'Simulated Annealing', 'Time': stats['time'], 
            'Memory': stats['memory'], 'Success': stats['success']
        })
        print(f"  Simulated Annealing: {'✓' if stats['success'] else '✗'} - {stats['time']:.4f}s")
        
        # 4. Genetic Algorithm
        print("Running Genetic Algorithm...")
        solution, stats = solver.solve_genetic_algorithm()
        results.append({
            'N': n, 'Algorithm': 'Genetic Algorithm', 'Time': stats['time'], 
            'Memory': stats['memory'], 'Success': stats['success']
        })
        print(f"  Genetic Algorithm: {'✓' if stats['success'] else '✗'} - {stats['time']:.4f}s")
    
    return results

def print_summary(results):
    """Print performance summary"""
    print("\n" + "="*60)
    print("PERFORMANCE SUMMARY")
    print("="*60)
    
    algorithms = ['DFS', 'Hill Climbing', 'Simulated Annealing', 'Genetic Algorithm']
    
    for alg in algorithms:
        alg_results = [r for r in results if r['Algorithm'] == alg]
        if alg_results:
            success_rate = sum(1 for r in alg_results if r['Success']) / len(alg_results)
            successful_results = [r for r in alg_results if r['Success']]
            
            print(f"\n{alg}:")
            print(f"  Success Rate: {success_rate:.1%}")
            
            if successful_results:
                avg_time = sum(r['Time'] for r in successful_results) / len(successful_results)
                print(f"  Avg Time (successful): {avg_time:.4f}s")
                successful_sizes = [r['N'] for r in successful_results]
                print(f"  Max N solved: {max(successful_sizes)}")
                
                if alg == 'DFS':
                    # Special handling for DFS timeouts
                    timeout_results = [r for r in alg_results if r.get('Timeout', False)]
                    if timeout_results:
                        print(f"  Timeouts: {len(timeout_results)}/{len(alg_results)}")
                        total_nodes = sum(r.get('Nodes', 0) for r in alg_results)
                        print(f"  Total nodes explored: {total_nodes:,}")

# Quick test function
def quick_test():
    """Quick test for debugging"""
    print("Quick Test - N=8")
    solver = OptimizedNQueensSolver(8)
    
    algorithms = [
        ("DFS", lambda: solver.solve_exhaustive_dfs(timeout_seconds=30)),
        ("Hill Climbing", solver.solve_greedy_hill_climbing),
        ("Simulated Annealing", solver.solve_simulated_annealing),
        ("Genetic Algorithm", solver.solve_genetic_algorithm)
    ]
    
    for name, method in algorithms:
        solution, stats = method()
        timeout_msg = " (TIMEOUT)" if stats.get('timeout', False) else ""
        print(f"{name}: {'✓' if stats['success'] else '✗'} - {stats['time']:.4f}s{timeout_msg}")
        if solution and stats['success']:
            print(f"  Conflicts: {solver.conflicts_fast(solution)}")

if __name__ == "__main__":
    print("Optimized N-Queens Solver")
    print("Choose: 1) Quick Test  2) Full Analysis")
    
    try:
        choice = input("Enter choice (1 or 2): ").strip()
        if choice == "1":
            quick_test()
        else:
            results = run_optimized_analysis()
            print_summary(results)
    except KeyboardInterrupt:
        print("\nAnalysis interrupted by user")
    except Exception as e:
        print(f"Error: {e}")
        # Run quick test as fallback
        print("Running quick test instead...")
        quick_test()
