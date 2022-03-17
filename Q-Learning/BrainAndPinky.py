import numpy as np
from Qlearning import qlearning, availible_actions
from labyrinthGenerator import generate_lab, save_labyrinth, save_starting_point, read_labyrinth, read_starting_point


class Brain:
    def __init__(self):
        self.qmatrix = None

    def learn_lab(self, n, n_of_actions, beta, gamma, epochs, labyrinth, starting_point, T):
        self.qmatrix = qlearning(n, n_of_actions, beta, gamma, epochs, labyrinth, starting_point, T)

    def try_to_solve(self, labyrinth, starting_point):
        actions_dir = {
            0: (0, 1),
            1: (1, 0),
            2: (0, -1),
            3: (-1, 0)
        }
        position = [starting_point[0], starting_point[1]]

        while labyrinth[position[0]][position[1]] != 'C' and labyrinth[position[0]][position[1]] != 'O':
            nr_action = np.argmax(self.qmatrix[position[0]][position[1]])
            action = actions_dir[nr_action]
            new_pos = [position[0]+action[0], position[1]+action[1]]
            labyrinth[position[0]][position[1]] = 'X'
            print(labyrinth)
            position = new_pos


class Pinky:
    def __init__(self):
        pass

    def try_to_solve(self, labyrinth, starting_point):
        actions_dir = {
            'right': (0, 1),
            'down': (1, 0),
            'left': (0, -1),
            'top': (-1, 0)
        }
        dimension = len(labyrinth[0])
        position = [starting_point[0], starting_point[1]]

        while labyrinth[position[0]][position[1]] != 'C' and labyrinth[position[0]][position[1]] != 'O':
            avail_actions = availible_actions(position, dimension)
            choosed_action = np.random.choice(avail_actions)
            action = actions_dir[choosed_action]
            new_pos = [position[0]+action[0], position[1]+action[1]]
            labyrinth[position[0]][position[1]] = 'X'
            print(labyrinth)
            position = new_pos


if __name__ == "__main__":
    lab, starting_point = generate_lab(8)
    save_labyrinth(lab, 'labyrinth.txt')
    save_starting_point(starting_point, 'starting_point.txt')
    lab = read_labyrinth('labyrinth.txt')
    starting = read_starting_point('starting_point.txt')
    agent1 = Brain()
    agent2 = Pinky()
    agent1.learn_lab(8, 4, 0.1, 0.1, 100000, lab, starting, 500)
    
         
