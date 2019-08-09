# this is the execution file

from algos.mcts.tree_search import *
from games.TestGame import TestGame
from games.ConnectFour import ConnectFour

max_budget_p1 = 50  # budget for running tree search for Player 1
max_budget_p2 = 10  # budget for running tree search for Player 2


if __name__ == "__main__":
    # mygame = TestGame()
    mygame = ConnectFour()

    winner = False

    state = mygame.initial_state  # gets initial board
    just_played = 1  # player who's turn it is

    while mygame.get_moves(state):
        print("Current Actual Game State", "\n", state)

        # Player 1
        if just_played == 1:
            print("Player {} is making a move".format(just_played))
            move = tree_search(game=mygame, budget=max_budget_p1, start_state=state, player=just_played)
            state = mygame.do_move(state, move, player=just_played)

        # Player 2
        elif just_played == 2:
            print("Player {} is making a move".format(just_played))
            move = tree_search(game=mygame, budget=max_budget_p2, start_state=state, player=just_played)
            state = mygame.do_move(state, move, player=just_played)

        # check for win
        if mygame.is_terminal(state, just_played):
            winner = True
            print("Player {} won!!".format(just_played))
            break

        just_played = 3 - just_played

    if not winner:
        print("The game ended in a tie")
