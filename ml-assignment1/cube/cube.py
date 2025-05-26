import random
import copy

FACE_COLORS = {
  'U': 'W',
  'D': 'Y',
  'F': 'G',
  'B': 'B',
  'L': 'O',
  'R': 'R',
}

def create_solved_cube(size=3):
    return {face: [[color] * size for _ in range(size)] for face, color in FACE_COLORS.items()}

def rotate_face_clockwise(face):
    # Rotates a 2D face (list of lists) clockwise
    return [list(row) for row in zip(*face[::-1])]

def move_R (cube):
    new_cube = copy.deepcopy(cube)
    new_cube['R'] = rotate_face_clockwise(new_cube['R'])
    return new_cube

def move_U(cube):
    new_cube = copy.deepcopy(cube)
    new_cube['U'] = rotate_face_clockwise(new_cube['U'])
    return new_cube

def move_F(cube):
    new_cube = copy.deepcopy(cube)
    new_cube['F'] = rotate_face_clockwise(new_cube['F'])
    return new_cube

def move_L(cube):
    new_cube = copy.deepcopy(cube)
    new_cube['L'] = rotate_face_clockwise(new_cube['L'])
    return new_cube

def move_B(cube):
    new_cube = copy.deepcopy(cube)
    new_cube['B'] = rotate_face_clockwise(new_cube['B'])
    new_cube['B'] = rotate_face_clockwise(new_cube['B'])
    return new_cube

def move_D(cube):
    new_cube = copy.deepcopy(cube)
    new_cube['D'] = rotate_face_clockwise(new_cube['D'])
    return new_cube

def rotate_face_clockwise(face):
    return [list(row) for row in zip(*face[::-1])]

all_moves = [
    (move_R, "R"),
    (move_U, "U"),
    (move_F, "F"),
    (move_L, "L"),
    (move_B, "B"),
    (move_D, "D"),
]

def scramble_cube(cube, num_moves=20):
    scrambled_cube = copy.deepcopy(cube)
    scramble_sequence = []
    for _ in range(num_moves):
        move_func, move_name = random.choice(all_moves)
        cube = move_func(cube)
        scramble_sequence.append(move_name)
    return cube, scramble_sequence
