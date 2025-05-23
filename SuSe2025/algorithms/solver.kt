import time
import heapq
import psutil
from collections import deque
from cube import is_solved  # Assuming your `cube.py` has is_solved()

# Define dummy move functions (replace with real logic)
def move_R(cube):
    return cube[:]  # Return a shallow copy if cube is a list

def move_U(cube):
    return cube[:]

def move_F(cube):
    return cube[:]

# Define available moves
all_moves = [
    (move_R, "R"),
    (move_U, "U"),
    (move_F, "F"),
]

def dfs(initial_state, max_depth=20):
    print(f"DFS DEBUG: Starting with max_depth={max_depth}")
    print(f"DFS DEBUG: Initial state: {initial_state}")
    print(f"DFS DEBUG: Is initially solved? {is_solved(initial_state)}")
    print(f"DFS DEBUG: Number of available moves: {len(all_moves)}")

    start_time = time.time()
    process = psutil.Process()
    initial_memory = process.memory_info().rss / (1024 * 1024)
    max_memory = initial_memory
    stack = [(initial_state, [], 0)]
    visited = set()
    nodes_expanded = 0

    while stack:
        current_state, moves, depth = stack.pop()
        current_memory = process.memory_info().rss / (1024 * 1024)
        max_memory = max(max_memory, current_memory)

        print(f"DFS DEBUG: Checking state at depth {depth}, moves: {moves}")
        print(f"DFS DEBUG: Is current state solved? {is_solved(current_state)}")

        if is_solved(current_state):
            print(f"DFS DEBUG: SOLUTION FOUND! Moves: {moves}")
            end_time = time.time()
            return {
                'solution': moves,
                'nodes_expanded': nodes_expanded,
                'time_taken': end_time - start_time,
                'max_memory': max_memory - initial_memory
            }

        state_hash = str(current_state)
        if state_hash in visited or depth >= max_depth:
            continue

        visited.add(state_hash)
        nodes_expanded += 1

        for move_func, move_name in reversed(all_moves):
            try:
                new_state = move_func(current_state)
                if new_state is not None:
                    stack.append((new_state, moves + [move_name], depth + 1))
            except Exception as e:
                print(f"DFS DEBUG: Error applying move {move_name}: {e}")

    end_time = time.time()
    return {
        'solution': None,
        'nodes_expanded': nodes_expanded,
        'time_taken': end_time - start_time,
        'max_memory': max_memory - initial_memory
    }

from collections import deque
import time
import psutil

# Example dummy cube operations
def move_R(cube): return cube[:]  # Replace with real transformation
def move_U(cube): return cube[:]
def move_F(cube): return cube[:]

# Sample goal check
def is_solved(cube): return cube == list(range(len(cube)))  # Replace as needed

all_moves = [(move_R, "R"), (move_U, "U"), (move_F, "F")]

def exhaustive_bfs_all_nodes(initial_state, max_depth=5):
    start_time = time.time()
    process = psutil.Process()
    initial_memory = process.memory_info().rss / (1024 * 1024)
    max_memory = initial_memory

    queue = deque([(initial_state, [], 0)])
    visited = set()
    solutions = []
    all_nodes = set()
    nodes_expanded = 0

    while queue:
        current_state, path, depth = queue.popleft()
        current_memory = process.memory_info().rss / (1024 * 1024)
        max_memory = max(max_memory, current_memory)

        state_hash = str(current_state)
        if state_hash in visited or depth > max_depth:
            continue

        visited.add(state_hash)
        all_nodes.add(state_hash)
        nodes_expanded += 1

        if is_solved(current_state):
            solutions.append(path)  # Collect all solutions, not just first

        if depth == max_depth:
            continue

        for move_func, move_name in all_moves:
            try:
                new_state = move_func(current_state)
                if new_state is not None:
                    queue.append((new_state, path + [move_name], depth + 1))
            except Exception as e:
                print(f"DEBUG: Error applying move {move_name}: {e}")

    end_time = time.time()
    return {
        'all_solutions': solutions,
        'nodes_expanded': nodes_expanded,
        'total_unique_nodes': len(all_nodes),
        'time_taken': end_time - start_time,
        'max_memory': max_memory - initial_memory,
        'visited_nodes': all_nodes
    }


def manhattan_distance_heuristic(cube):
    """
    Placeholder heuristic: counts misplaced stickers.
    Adjust this logic based on your cube's internal structure.
    """
    if isinstance(cube, list):
        return sum(1 for i, val in enumerate(cube) if val != i)
    elif isinstance(cube, dict):
        return sum(1 for k, v in cube.items() if k != v)
    return 0

def a_star(initial_state, max_depth=20):
    start_time = time.time()
    process = psutil.Process()
    initial_memory = process.memory_info().rss / (1024 * 1024)
    max_memory = initial_memory

    initial_cost = manhattan_distance_heuristic(initial_state)
    priority_queue = [(initial_cost, 0, 0, initial_state, [])]
    visited = {}
    nodes_expanded = 0
    counter = 1

    while priority_queue:
        f, g, _, current_state, moves = heapq.heappop(priority_queue)
        current_memory = process.memory_info().rss / (1024 * 1024)
        max_memory = max(max_memory, current_memory)

        if is_solved(current_state):
            end_time = time.time()
            return {
                'solution': moves,
                'nodes_expanded': nodes_expanded,
                'time_taken': end_time - start_time,
                'max_memory': max_memory - initial_memory
            }

        if g >= max_depth:
            continue

        state_hash = str(current_state)
        if state_hash in visited and visited[state_hash] <= g:
            continue

        visited[state_hash] = g
        nodes_expanded += 1

        for move_func, move_name in all_moves:
            try:
                new_state = move_func(current_state)
                if new_state is not None:
                    new_g = g + 1
                    new_h = manhattan_distance_heuristic(new_state)
                    new_f = new_g + new_h
                    counter += 1
                    heapq.heappush(priority_queue, (new_f, new_g, counter, new_state, moves + [move_name]))
            except Exception as e:
                print(f"A* DEBUG: Error applying move {move_name}: {e}")

    end_time = time.time()
    return {
        'solution': None,
        'nodes_expanded': nodes_expanded,
        'time_taken': end_time - start_time,
        'max_memory': max_memory - initial_memory
    }
