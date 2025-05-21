import random
import copy

# Constants
FACE_COLORS = {
    'U': 'W',  # Up - White
    'D': 'Y',  # Down - Yellow
    'F': 'G',  # Front - Green
    'B': 'B',  # Back - Blue
    'L': 'O',  # Left - Orange
    'R': 'R',  # Right - Red
}

def create_solved_cube(size=3):
    """Create a solved cube of given size"""
    return {face: [[color] * size for _ in range(size)] for face, color in FACE_COLORS.items()}

def rotate_face_clockwise(face):
    """Rotates a 2D face (list of lists) clockwise"""
    return [list(row) for row in zip(*face[::-1])]

def move_R(cube, size=3):
    """Apply a clockwise rotation to the right face"""
    new_cube = copy.deepcopy(cube)
    # Rotates right face clockwise
    new_cube['R'] = rotate_face_clockwise(new_cube['R'])
    
    # Updates adjacent faces
    # Stores the original values of the Upper face that will be replaced
    temp = [row[size-1] for row in new_cube['U']]
    
    # F → U (front to up)
    for i in range(size):
        new_cube['U'][i][size-1] = new_cube['F'][i][size-1]
    
    # D → F (down to front)
    for i in range(size):
        new_cube['F'][i][size-1] = new_cube['D'][i][size-1]
    
    # B → D (back to down, with reversal due to orientation)
    for i in range(size):
        new_cube['D'][i][size-1] = new_cube['B'][size-1-i][0]
    
    # saved U → B (up to back, with reversal due to orientation)
    for i in range(size):
        new_cube['B'][size-1-i][0] = temp[i]
    
    return new_cube

def move_L(cube, size=3):
    """Apply a clockwise rotation to the left face"""
    new_cube = copy.deepcopy(cube)
    # Rotates left face clockwise
    new_cube['L'] = rotate_face_clockwise(new_cube['L'])
    
    # Updates adjacent faces
    # Stores the original values of the U face that will be replaced
    temp = [row[0] for row in new_cube['U']]
    
    # B → U (back to up, with reversal due to orientation)
    for i in range(size):
        new_cube['U'][i][0] = new_cube['B'][size-1-i][size-1]
    
    # F → B (front to back, with reversal due to orientation)
    for i in range(size):
        new_cube['B'][size-1-i][size-1] = new_cube['F'][i][0]
    
    # D → F (down to front)
    for i in range(size):
        new_cube['F'][i][0] = new_cube['D'][i][0]
    
    # saved U → D (up to down)
    for i in range(size):
        new_cube['D'][i][0] = temp[i]
    
    return new_cube

def move_U(cube, size=3):
    """Apply a clockwise rotation to the up face"""
    new_cube = copy.deepcopy(cube)
    # Rotates upper face clockwise
    new_cube['U'] = rotate_face_clockwise(new_cube['U'])
    
    # Updates adjacent faces
    # Stores the original values of the F face that will be replaced
    temp = new_cube['F'][0].copy()
    
    # R → F (right to front)
    new_cube['F'][0] = [new_cube['R'][0][i] for i in range(size)]
    
    # B → R (back to right)
    new_cube['R'][0] = new_cube['B'][0].copy()
    
    # L → B (left to back)
    new_cube['B'][0] = [new_cube['L'][0][i] for i in range(size)]
    
    # saved F → L (front to left)
    new_cube['L'][0] = temp
    
    return new_cube

def move_D(cube, size=3):
    """Apply a clockwise rotation to the down face"""
    new_cube = copy.deepcopy(cube)
    # Rotates down face clockwise
    new_cube['D'] = rotate_face_clockwise(new_cube['D'])
    
    # Updates adjacent faces
    # Stores the original values of the F face that will be replaced
    temp = new_cube['F'][size-1].copy()
    
    # L → F (left to front)
    new_cube['F'][size-1] = [new_cube['L'][size-1][i] for i in range(size)]
    
    # B → L (back to left)
    new_cube['L'][size-1] = new_cube['B'][size-1].copy()
    
    # R → B (right to back)
    new_cube['B'][size-1] = [new_cube['R'][size-1][i] for i in range(size)]
    
    # saved F → R (front to right)
    new_cube['R'][size-1] = temp
    
    return new_cube

def move_F(cube, size=3):
    """Apply a clockwise rotation to the front face"""
    new_cube = copy.deepcopy(cube)
    # Rotates front face clockwise
    new_cube['F'] = rotate_face_clockwise(new_cube['F'])
    
    # Updates adjacent faces
    # Stores the original values of the U face that will be replaced
    temp = [new_cube['U'][size-1][i] for i in range(size)]
    
    # L → U (left to up, with rotation)
    for i in range(size):
        new_cube['U'][size-1][i] = new_cube['L'][size-1-i][size-1]
    
    # D → L (down to left, with rotation)
    for i in range(size):
        new_cube['L'][i][size-1] = new_cube['D'][0][i]
    
    # R → D (right to down, with rotation)
    for i in range(size):
        new_cube['D'][0][size-1-i] = new_cube['R'][i][0]
    
    # saved U → R (up to right, with rotation)
    for i in range(size):
        new_cube['R'][size-1-i][0] = temp[i]
    
    return new_cube

def move_B(cube, size=3):
    """Apply a clockwise rotation to the back face"""
    new_cube = copy.deepcopy(cube)
    # Rotates back face clockwise - only once!
    new_cube['B'] = rotate_face_clockwise(new_cube['B'])
    
    # Updates adjacent faces
    # Stores the original values of the U face that will be replaced
    temp = [new_cube['U'][0][i] for i in range(size)]
    
    # R → U (right to up, with rotation)
    for i in range(size):
        new_cube['U'][0][i] = new_cube['R'][size-1-i][size-1]
    
    # D → R (down to right, with rotation)
    for i in range(size):
        new_cube['R'][i][size-1] = new_cube['D'][size-1][i]
    
    # L → D (left to down, with rotation)
    for i in range(size):
        new_cube['D'][size-1][size-1-i] = new_cube['L'][i][0]
    
    # saved U → L (up to left, with rotation)
    for i in range(size):
        new_cube['L'][size-1-i][0] = temp[i]
    
    return new_cube

# Defines all possible moves
all_moves = [
    (move_R, "R"),
    (move_U, "U"),
    (move_F, "F"),
    (move_L, "L"),
    (move_B, "B"),
    (move_D, "D"),
]

def scramble_cube(cube, num_moves=20):
    """Scramble a cube by applying random moves"""
    scrambled_cube = copy.deepcopy(cube)
    scramble_sequence = []
    
    for _ in range(num_moves):
        move_func, move_name = random.choice(all_moves)
        scrambled_cube = move_func(scrambled_cube)  # Apply the move to update the cube
        scramble_sequence.append(move_name)
    
    return scrambled_cube, scramble_sequence

def cube_to_state(cube):
    """Convert cube dictionary to hashable tuple representation"""
    state = []
    for face in ['U', 'D', 'F', 'B', 'L', 'R']:
        for row in cube[face]:
            for cell in row:
                state.append(cell)
    return tuple(state)

def is_solved(cube):
    """Check if cube is solved (each face has only one color)"""
    for face, color_grid in cube.items():
        color = color_grid[0][0]
        for row in color_grid:
            for cell in row:
                if cell != color:
                    return False
    return True
