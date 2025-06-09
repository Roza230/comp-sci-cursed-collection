Testing N = 10
-------------------------
Running Optimized DFS...
  DFS: ✓ - 0.0012s - 103 nodes - 0.0MB
Running Hill Climbing...
  Hill Climbing: ✓ - 0.0470s - 0.0MB
Running Simulated Annealing...
  Simulated Annealing: ✓ - 0.0259s - 0.0MB
Running Genetic Algorithm...
  Genetic Algorithm: ✗ - 0.0454s - 0.0MB

Testing N = 30
-------------------------
Running Optimized DFS...
  DFS: TIMEOUT after 60.0s - explored 19,910,000 nodes - 0.0MB
Running Hill Climbing...
  Hill Climbing: ✓ - 5.7823s - 0.0MB
Running Simulated Annealing...
  Simulated Annealing: ✓ - 0.0207s - 0.0MB
Running Genetic Algorithm...
  Genetic Algorithm: ✗ - 0.3557s - 0.0MB

Testing N = 50
-------------------------
Running Optimized DFS...
  DFS: TIMEOUT after 300.0s - explored 70,410,000 nodes - -0.9MB
Running Hill Climbing...
  Hill Climbing: ✗ - 60.5082s - -0.0MB (TIMEOUT)
Running Simulated Annealing...
  Simulated Annealing: ✓ - 0.1041s - 0.0MB
Running Genetic Algorithm...
  Genetic Algorithm: ✗ - 1.0544s - 0.1MB

Testing N = 100
-------------------------
Running Optimized DFS...
  DFS: TIMEOUT after 300.2s - explored 29,980,000 nodes - 0.0MB
Running Hill Climbing...
  Hill Climbing: ✗ - 131.6149s - 0.1MB (TIMEOUT)
Running Simulated Annealing...
  Simulated Annealing: ✓ - 1.4685s - 0.0MB
Running Genetic Algorithm...
  Genetic Algorithm: ✗ - 0.8348s - 0.0MB

Testing N = 200
-------------------------
Running Optimized DFS...
  DFS: TIMEOUT after 600.2s - explored 27,220,000 nodes - -0.0MB
Running Hill Climbing...
  Hill Climbing: ✗ - 186.9846s - 0.1MB (TIMEOUT)
Running Simulated Annealing...
  Simulated Annealing: ✗ - 8.2644s - 0.0MB
Running Genetic Algorithm...
  Genetic Algorithm: ✗ - 5.9261s - 0.3MB

============================================================
PERFORMANCE SUMMARY
============================================================

DFS:
  Success Rate: 20.0%
  Avg Time (successful): 0.0012s
  Avg Memory (successful): 0.0MB
  Max N solved: 10
  Timeouts: 4/5
  Total nodes explored: 147,520,103

Hill Climbing:
  Success Rate: 40.0%
  Avg Time (successful): 2.9147s
  Avg Memory (successful): 0.0MB
  Max N solved: 30
  Timeouts: 3/5

Simulated Annealing:
  Success Rate: 80.0%
  Avg Time (successful): 0.4048s
  Avg Memory (successful): 0.0MB
  Max N solved: 100

Genetic Algorithm:
  Success Rate: 0.0%
