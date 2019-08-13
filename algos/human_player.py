def get_valid_move(prompt, pos_moves):
    value = None
    while value is None:
        try:
            value = int(input(prompt))

        except ValueError:
            print("Sorry I did not understand that")

        if value not in pos_moves:
            print("Please choose a valid move")

        else:
            break

    return value


def human(game, state):
    print("============= HUMAN =============")
    print("Current Actual Game State", "\n", state)
    pos_moves = game.get_moves(state)
    print("Possible Moves", pos_moves)
    move = get_valid_move("What move do you choose? ", pos_moves)
    return int(move)