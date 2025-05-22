import random
import copy

# Define face colors for a solved cube (6 faces: U, D, F, B, L, R)
face_colors = ['W', 'Y', 'G', 'B', 'O', 'R']  # White, Yellow, Green, Blue, Orange, Red

def create_solved_cube(size=3):
    """
    Create a solved Rubik's cube. Each face has a unique color.
    Cube is represented as a flat list of 6 faces * size * size elements.
    """
    cube = []
    for color in face_colors:
        cube.extend([color] * (size * size))
    return cube

def is_solved(cube, size=3):
    """
    Check if all faces of the cube are uniform in color (solved state).
    """
    for i in range(0, len(cube), size * size):
        face = cube[i:i + size * size]
        if not all(sticker == face[0] for sticker in face):
            return False
    return True

def scramble_cube(cube, depth=10):
    """
    Scrambles the cube using random moves from the move set.
    """
    from solver import all_moves  # Use same move set as the solver

    scrambled_cube = copy.deepcopy(cube)
    scramble_seq = []

    for _ in range(depth):
        move_func, name = random.choice(all_moves)
        scrambled_cube = move_func(scrambled_cube)
        scramble_seq.append(name)

    return scrambled_cube, scramble_seq
