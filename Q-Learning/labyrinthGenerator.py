import numpy as np
from dfs import is_route


def generate_empty_lab(n):
    labyrinth = []
    for i in range(n):
        line = []
        for j in range(n):
            line.append('-')
        labyrinth.append(line)

    return np.array(labyrinth)


def put_holes(labyrinth):
    coordinates = []
    labyrinth_dim = len(labyrinth[0])
    for i in range(labyrinth_dim):
        for j in range(labyrinth_dim):
            coordinates.append((i, j))
    
    np.random.shuffle(coordinates)
    number_of_holes = np.random.randint(labyrinth_dim**2/2)
    for ii in range(number_of_holes):
        labyrinth[coordinates[ii][0]][coordinates[ii][1]] = 'O'


def put_cheese(labyrinth):
    labyrinth_dim = len(labyrinth[0])
    (x, y) = np.random.randint(labyrinth_dim), np.random.randint(labyrinth_dim)
    while labyrinth[x][y] == 'O':
        (x, y) = np.random.randint(labyrinth_dim), np.random.randint(labyrinth_dim)
    labyrinth[x][y] = 'C'


def choose_starting_point(labyrinth):
    labyrinth_dim = len(labyrinth[0])
    (x, y) = np.random.randint(labyrinth_dim), np.random.randint(labyrinth_dim)
    while labyrinth[x][y] == 'O' or labyrinth[x][y] == 'C':
        (x, y) = np.random.randint(labyrinth_dim), np.random.randint(labyrinth_dim)
    
    return (x, y)


def save_labyrinth(labyrinth, filename):
    labyrinth = list(labyrinth)
    with open(filename, 'w') as f:
        for row in labyrinth:
            row = list(row)
            for sign in row:
                f.write(sign)
            f.write('\n')


def read_labyrinth(path):
    labyrinth = []
    with open(path) as f:
        for line in f:
            row = []
            for sign in line[:len(line)-1]:
                row.append(sign)
            labyrinth.append(row)

    return np.array(labyrinth)


def save_starting_point(point, filename):
    with open(filename, 'w') as f:
        for item in point:
            f.write(str(item))


def read_starting_point(path):
    point = []
    with open(path) as f:
        for item in f:
            for number in item:
                point.append(int(number))

    return tuple(point)


def generate_lab(n):
    route = False
    while route is False:
        lab = generate_empty_lab(n)
        put_holes(lab)
        put_cheese(lab)
        starting_point = choose_starting_point(lab)
        route = is_route(lab, starting_point)

    return lab, starting_point


