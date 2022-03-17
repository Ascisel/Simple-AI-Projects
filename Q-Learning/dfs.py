def node_neighbours(labyrinth, node):
    labyrinth_dim = len(labyrinth[0])
    neighbours = []
    check_coord = [node[0], node[1]]
    directions = [-1, 1]
    for i in range(2):
        for j in range(2):
            check_coord[1 - i] += directions[j]
            if is_index_good(check_coord[0], labyrinth_dim) and is_index_good(check_coord[1], labyrinth_dim):
                if labyrinth[check_coord[0]][check_coord[1]] != 'O':
                    neighbours.append(tuple(check_coord))
            check_coord = [node[0], node[1]]

    return neighbours


def is_index_good(index, dimension):
    if index < 0 or index > dimension - 1:
        return False
    return True


def dfs(visited, labyrinth, node):
    if node not in visited:
        visited.add(node)
        for neighbour in node_neighbours(labyrinth, node):
            dfs(visited, labyrinth, neighbour)


def is_route(labyrinth, node):
    visited = set()
    dfs(visited, labyrinth, node)
    for coord in visited:
        if labyrinth[coord[0]][coord[1]] == 'C':
            return True
    return False
