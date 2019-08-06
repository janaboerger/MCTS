import numpy as np


def four_check(board, player):
    four_in_a_row = False
    for row in board:
        counter = 0
        for j in row:
            if j == player:
                counter += 1
                if counter == 4:
                    four_in_a_row = True
            else:
                counter = 0
    return four_in_a_row


def positive_diagonals(board):
    rows, cols = board.shape

    for st in ([(j, i - cols - j + 7) for j in range(cols)] for i in range(cols + rows - 1)):
        yield ([board[i][j] for i, j in st if 0 <= i < rows and 0 <= j < cols])


def negative_diagonals(board):
    rows, cols = board.shape

    for st in ([(j, i - cols + j + 2) for j in range(cols)] for i in range(cols + rows - 1)):
        yield ([board[i][j] for i, j in st if 0 <= i < rows and 0 <= j < cols])


class State:
    def __init__(self, array):
        self.__board = array

    def __hash__(self):
        return hash(self.__board.data.tobytes())

    def __eq__(self, other):
        return (self.__board == other.__board).all()

    def __repr__(self):
        return "Game State={}".format(self.__board)

    def get_board(self):
        return np.copy(self.__board)


class ConnectFour:
    def __init__(self):
        self.initial_state = State(np.zeros([6, 7]))

    @staticmethod
    def do_move(state, move, player):
        print("Doing Move")
        # look at current state, make move and return new state
        board = state.get_board()
        print("New Game State BEFORE making move", board)

        # looping through columns that player wants to play starting with bottom slot
        for i in range(len(board[:, move][::-1])):
            # print("i", i)
            if board[:, move][::-1][i] == 0:
                # print("Stop")
                board[:, move][::-1][i] = player
                break
        new_board = board
        print("New Game State after making move", new_board)

        return State(new_board)

    @staticmethod
    def get_moves(state):
        print("Getting Moves")
        # check what columns have not been filled up yet
        board = state.get_board()
        return list(np.where(board[0] == 0)[0])

    # returns reward based on the current state
    @staticmethod
    def get_reward(state, player):
        print("Getting Reward")
        # return 1 for win, -1 for loss, 0 for tie
        board = state.get_board()
        reward = -1

        winner = four_check(board, player) \
                 or four_check(board.T, player) \
                 or four_check(negative_diagonals(board), player) \
                 or four_check(positive_diagonals(board), player)

        if winner:
            reward = 1
        # TODO: include case of tie
        return reward

    @staticmethod
    def is_terminal(state, player): # board = state
        # row check, col check, diagonal down, diagonal up

        board = state.get_board()

        return four_check(board, player) \
               or four_check(board.T, player) \
               or four_check(negative_diagonals(board), player) \
               or four_check(positive_diagonals(board), player)
        # TODO: or terminal because no moves left --> tie

