import math
import numpy as np


class NodeCirlce:
    def __init__(self, move, parent):
        self.parent = parent
        self.childs = []
        self.move = move
        self.terminal = False


class NodeCross:
    def __init__(self, move, parent):
        self.parent = parent
        self.childs = []
        self.move = move
        self.terminal = False


class TicTacToeTree:
    def __init__(self):
        self.root = None
        self.moves = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.terminals = []
        self.ties = []

    def build_tree(self, first_move):
        self.root = NodeCirlce(first_move, None)
        self.cascade_builder(self.root)

    def is_state_terminal(self, node):
        terminal_states = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [7, 5, 3]]
        figure_moves = []
        if isinstance(node, NodeCirlce):
            while node is not None:
                if isinstance(node, NodeCirlce):
                    figure_moves.append(node.move)
                node = node.parent
        else:
            while node is not None:
                if isinstance(node, NodeCross):
                    figure_moves.append(node.move)
                node = node.parent
        if len(figure_moves) > 2:
            for state in terminal_states:
                matches = 0
                for move in figure_moves:
                    if move in state:
                        matches += 1
                if matches == 3:
                    return True
        return False

    def cascade_builder(self, node):
        if self.is_state_terminal(node):
            node.terminal = True
            self.terminals.append(node)
            return
        available_moves = self.moves.copy()
        available_moves.remove(node.move)
        parent = node.parent
        while parent is not None:
            available_moves.remove(parent.move)
            parent = parent.parent
        if available_moves == []:
            node.terminal = None
            self.ties.append(node)
            return
        if isinstance(node, NodeCirlce):
            Next_symbol = NodeCross
        else:
            Next_symbol = NodeCirlce
        for move in available_moves:
            next_move = Next_symbol(move, node)
            node.childs.append(next_move)
            self.cascade_builder(next_move)


def h(node, depth):
    if isinstance(node, NodeCirlce):
        return 10 - depth
    return -10 + depth


def Minimax(s, d, max_move):
    if s.terminal is True:
        return h(s, d)
    if s.terminal is None:
        return 0
    if max_move:
        best_score = -math.inf
        for u in s.childs:
            next_score = Minimax(u, d+1, False)
            best_score = max(next_score, best_score)
        return best_score
    else:
        best_score = math.inf
        for u in s.childs:
            next_score = Minimax(u, d+1, True)
            best_score = min(next_score, best_score)
        return best_score


def Best_move(s, isCircle):
    bestScore = math.inf
    max_move = True
    if isCircle:
        bestScore = -math.inf
        max_move = False
    bestMove = None
    for u in s.childs:
        score = Minimax(u, 0, max_move)
        if isCircle:
            if score > bestScore:
                bestScore = score
                bestMove = u
        else:
            if score < bestScore:
                bestScore = score
                bestMove = u
    return bestMove


def find_child_by_move(node, move):
    for child in node.childs:
        if child.move == move:
            return child
    return None


def print_state(node):
    tablica = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    while node is not None:
        if isinstance(node, NodeCirlce):
            tablica[node.move-1] = 'o'
        else:
            tablica[node.move-1] = 'x'
        node = node.parent

    w = 0
    for i in range(3):
        print('|', end=' ')
        for j in range(3):
            print(tablica[w], end=' | ')
            w += 1
        print("\n")
    print('---------------\n')


def RANDOM_VS_MINIMAX():
    available_moves = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    GameTree = TicTacToeTree()
    first_move = np.random.randint(1, 10)
    available_moves.remove(first_move)
    GameTree.build_tree(first_move)
    s = GameTree.root
    print_state(s)
    while available_moves != [] and s.terminal is not True:
        s = Best_move(s, False)
        print_state(s)
        if s.terminal is True:
            return s
        available_moves.remove(s.move)
        np.random.shuffle(available_moves)
        s = find_child_by_move(s, available_moves[0])
        print_state(s)
        available_moves.pop(0)
    return s


def MINIMAX_VS_MINIMAX(first_move):
    if not isinstance(first_move, int) or first_move < 1 or first_move > 9:
        print("podałeś złe pole startowe, kończę grę")
        return
    available_moves = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    GameTree = TicTacToeTree()
    available_moves.remove(first_move)
    GameTree.build_tree(first_move)
    s = GameTree.root
    print_state(s)
    while available_moves != [] and s.terminal is not True:
        s = Best_move(s, False)
        print_state(s)
        if s.terminal is True:
            return s
        available_moves.remove(s.move)
        s = Best_move(s, True)
        print_state(s)
        available_moves.remove(s.move)
    return s


def RANDOM_VS_RANDOM():
    available_moves = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    GameTree = TicTacToeTree()
    first_move = np.random.randint(1, 10)
    available_moves.remove(first_move)
    GameTree.build_tree(first_move)
    s = GameTree.root
    print_state(s)
    while available_moves != [] and s.terminal is not True:
        np.random.shuffle(available_moves)
        s = find_child_by_move(s, available_moves[0])
        print_state(s)
        if s.terminal is True:
            return s
        available_moves.remove(s.move)
        np.random.shuffle(available_moves)
        s = find_child_by_move(s, available_moves[0])
        print_state(s)
        available_moves.pop(0)
    return s



if __name__ == "__main__":
   pass
