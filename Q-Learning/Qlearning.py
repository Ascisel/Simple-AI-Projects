import numpy as np
from dfs import is_index_good


def availible_actions(position, dimension):
    availible_actions = []
    pos_to_check = list(position)
    actions_dir = {
        (0, 1): 'right',
        (1, 0): 'down',
        (0, -1): 'left',
        (-1, 0): 'top'
    }
    for action in actions_dir.keys():
        pos_to_check[0] += action[0]
        pos_to_check[1] += action[1]
        if is_index_good(pos_to_check[0], dimension) and is_index_good(pos_to_check[1], dimension):
            availible_actions.append(actions_dir[action])
        pos_to_check = list(position)

    return availible_actions


def choose_action(position, Qmatrix, T):
    dimension = len(Qmatrix[0])
    probabilities = []
    actionsValues = Qmatrix[position[0]][position[1]]
    actions_dir = {
        'right': (0, 1),
        'down': (1, 0),
        'left': (0, -1),
        'top': (-1, 0)
    }
    actions = availible_actions(position, dimension)
    n_of_actions = len(actions)
    denom = 0
    for i in range(n_of_actions):
        denom += np.exp(actionsValues[i]/T)
    for j in range(n_of_actions):
        probability = np.exp(actionsValues[j]/T)/denom
        probabilities.append(probability)
    choice = np.random.choice(actions, p=probabilities)

    return actions_dir[choice]


def create_qmatrix(n, n_of_actions):
    qmatrix = []
    action_values = [0. for ii in range(n_of_actions)]
    for i in range(n):
        line = []
        for j in range(n):
            line.append(action_values)
        qmatrix.append(line)

    return np.array(qmatrix)


def evaluate_reward(labyrinth, position):
    if labyrinth[position[0]][position[1]] == 'C':
        return 1
    if labyrinth[position[0]][position[1]] == 'O':
        return -2
    return 0


def is_done(labyrinth, position):
    if labyrinth[position[0]][position[1]] == 'C' or labyrinth[position[0]][position[1]] == 'O':
        return True
    return False


def make_step(labyrinth, position, action):
    next_state = (position[0]+action[0], position[1]+action[1])
    reward = evaluate_reward(labyrinth, next_state)
    done = is_done(labyrinth, next_state)

    return next_state, reward, done


def qlearning(n, n_of_actions, beta, gamma, epochs, labyrinth, starting_point, T):
    actions_dir = {
        (0, 1): 0,
        (1, 0): 1,
        (0, -1): 2,
        (-1, 0): 3
    }
    Temp = T
    qmatrix = create_qmatrix(n, n_of_actions)
    position = starting_point
    reach_goal = 0
    for i in range(epochs):
        done = False
        while not done:
            action = choose_action(position, qmatrix, Temp)
            next_pos, reward, done = make_step(labyrinth, position, action)
            old_value = qmatrix[position[0]][position[1]][actions_dir[action]]
            next_max_value = np.max(qmatrix[next_pos[0]][next_pos[1]])

            new_value = (1-beta) * old_value + beta * (reward + gamma * next_max_value)

            qmatrix[position[0]][position[1]][actions_dir[action]] = new_value

            position = next_pos

            if reward > 0:
                reach_goal += 1

        Temp = T/(i+2)

    return qmatrix





    


