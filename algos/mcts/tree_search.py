import math
import numpy as np
import copy

const_b = math.sqrt(2)  # constant in UCT
M = 1000  # values for nodes that have not been visited
threshold = 1  # threshold of visiting nodes before expanding
max_depth = 50  # depths when nodes are leaves, for FourConnect should be at least the size of gmaeboard: 7x6 =

# dictionary that tracks state - node
state_nodes = {}


def randargmax(b):
    """ a random tie-breaking argmax"""
    return np.argmax(np.random.random(b.shape) * (b == b.max()))


class Node:
    def __init__(self, state, visits=0, move=None, expanded=False, env=None):
        self.visits = visits
        self.move = move  # move that got you to this node
        self.children = {}  # dictionary key: move, value: [visits, reward]
        self.is_expanded = expanded
        self.untried_moves = env.get_moves(state)

    def __repr__(self):
        return u"Node(visits={}, children={}, expanded={})".format(self.visits, self.children, self.is_expanded)

    def select_move(self):
        print("Selecting child or move")
        scores = []
        scored_nodes = []
        for x in self.children:
            scored_nodes.append(x)
            print(self.children[x])

            # assigning big value if child has not been visited at all
            if self.children[x][0] == 0:
                score = M

            # UCT
            else:
                score = self.children[x][1] / self.children[x][0] + const_b * \
                        math.sqrt(math.log(self.visits) / self.children[x][0])

            scores.append(score)

        print("Calculating Scores", scores)
        print("List of Moves", self.children)

        to_explore = randargmax(np.array(scores))
        selected_child = scored_nodes[to_explore]

        print("Selected Child (move)", selected_child)
        return selected_child

    def rollout(self, env, state, path, player):
        print("============ROLLOUT============")
        print("path so far", path)
        rolling_path_length = len(path)

        state = state
        just_played = 3 - copy.copy(player) # making sure the rollout starts with the other player's move

        if rolling_path_length == max_depth:
            return path[-2].children[path][-1][1]
        else:
            while rolling_path_length <= max_depth and env.is_terminal(state, 3 - just_played) is False:
                # have to check for 3 - just_played because I've already updated player at end of loop

                move = np.random.choice(env.get_moves(state))
                state = env.do_move(state, move, just_played)
                just_played = 3 - just_played
                rolling_path_length += 1

            # Reward needs to be for actual player not the one who just made a move in the rollout
        return env.get_reward(state, player)


def expand(node, state, game, player):  # TODO: Should this be in node?
    print("Expanding Node")

    while node.untried_moves:
        # chose move from untried moves from current node
        m = np.random.choice(node.untried_moves)
        print("Chosen Move", m)
        # evaluate move and retrieve new state
        new_state = game.do_move(state, m, player)
        print("New State in Tree Search - Expansion \n", new_state)

        # check whether state already has an existing node
        if new_state not in state_nodes:
            print("Creating new Node for this State")
            state_nodes[new_state] = Node(state=new_state, move=m, env=game)

        # add move that led to expanded node to current node as child
        node.children[m] = [0, 0]
        node.untried_moves.remove(m)
        print("Current Nodes untried moves", node.untried_moves)
        node.is_expanded = True
    print("Expanded Node")


def tree_search(game, budget, start_state, player):
    print("Start State in Tree Search \n", start_state)
    root = Node(start_state, env=game)
    state_nodes[start_state] = root

    for i in range(budget):
        current_node = root
        print("================ ITERATIION {} ================".format(i))
        current_state = start_state
        path = []

        while True:
            if not current_node.is_expanded:
                expand(current_node, current_state, game, player)

            # add pair node-move to the path
            selected_move = current_node.select_move()
            path.append((current_node, selected_move))

            # moving to next state
            current_state = game.do_move(current_state, selected_move, player)
            print("Current State in Tree: ", current_state)
            current_node = state_nodes[current_state]

            print("Length of Current Path: ", len(path))

            # check if node is leaf or terminal
            if (len(path) > max_depth) or (current_node.visits < threshold):
                break

        # calculate reward or rollout
        if len(path) >= max_depth or game.is_terminal(current_state, player):
            reward = game.get_reward(current_state, player)
        else:
            reward = current_node.rollout(game, current_state, path, player)
        print("Reward from Rollout Policy: ", reward)

        # back-up tree
        print("Backing up path of length: ", len(path))
        current_node.visits += 1
        for node, move in path:
            print("current node that I want to back up: ", node, " & move that I took:", move)
            node.visits += 1
            node.children[move][1] += reward
            node.children[move][0] += 1

        print("Path", path)

    # return move with highest value for sum of visits + value --> max/robust child
    return max(root.children.keys(), key=(lambda k: root.children[k]))
