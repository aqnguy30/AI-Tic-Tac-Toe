# Anh (Tony) Nguyen - 1596895

import numpy as np
import random
from math import inf as infinity

# Initializing the game state and players
game_state = [[' ', ' ', ' '],
              [' ', ' ', ' '],
              [' ', ' ', ' ']]
players = ['X', 'O']


def possible_move(state, player, block_num):
    if state[int((block_num - 1) / 3)][(block_num - 1) % 3] is ' ':
        state[int((block_num - 1) / 3)][(block_num - 1) % 3] = player
    else:
        block_num = int(input("This block is not empty! Please choose again: "))
        possible_move(state, player, block_num)


def copy_game_state(state):
    new_state = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    for i in range(3):
        for j in range(3):
            new_state[i][j] = state[i][j]
    return new_state


def check_current_state(game_state):
    # Checking if the match is draw or not
    draw_flag = 0
    for i in range(3):
        for j in range(3):
            if game_state[i][j] is ' ':
                draw_flag = 1
    if draw_flag is 0:
        return None, "Draw"

    # Checking horizontals
    if (game_state[0][0] == game_state[0][1] and game_state[0][1] == game_state[0][2] and game_state[0][0] is not ' '):
        return game_state[0][0], "Done"
    if (game_state[1][0] == game_state[1][1] and game_state[1][1] == game_state[1][2] and game_state[1][0] is not ' '):
        return game_state[1][0], "Done"
    if (game_state[2][0] == game_state[2][1] and game_state[2][1] == game_state[2][2] and game_state[2][0] is not ' '):
        return game_state[2][0], "Done"

    # Checking verticals
    if (game_state[0][0] == game_state[1][0] and game_state[1][0] == game_state[2][0] and game_state[0][0] is not ' '):
        return game_state[0][0], "Done"
    if (game_state[0][1] == game_state[1][1] and game_state[1][1] == game_state[2][1] and game_state[0][1] is not ' '):
        return game_state[0][1], "Done"
    if (game_state[0][2] == game_state[1][2] and game_state[1][2] == game_state[2][2] and game_state[0][2] is not ' '):
        return game_state[0][2], "Done"

    # Checking diagonals
    if (game_state[0][0] == game_state[1][1] and game_state[1][1] == game_state[2][2] and game_state[0][0] is not ' '):
        return game_state[1][1], "Done"
    if (game_state[2][0] == game_state[1][1] and game_state[1][1] == game_state[0][2] and game_state[2][0] is not ' '):
        return game_state[1][1], "Done"

    return None, "Not Done"


def print_board(game_state):
    print('----------------')
    print('| ' + str(game_state[0][0]) + ' || ' + str(game_state[0][1]) + ' || ' + str(game_state[0][2]) + ' |')
    print('----------------')
    print('| ' + str(game_state[1][0]) + ' || ' + str(game_state[1][1]) + ' || ' + str(game_state[1][2]) + ' |')
    print('----------------')
    print('| ' + str(game_state[2][0]) + ' || ' + str(game_state[2][1]) + ' || ' + str(game_state[2][2]) + ' |')
    print('----------------')


def getBestMove(state, player):
    # Using Minimax Algorithm
    winner_loser, done = check_current_state(state)
    if done == "Done" and winner_loser == 'O':  # If Agent won
        return 1
    elif done == "Done" and winner_loser == 'X':  # If Human won
        return -1
    elif done == "Draw":  # Draw condition
        return 0

    moves = []
    empty_cells = []
    for i in range(3):
        for j in range(3):
            if state[i][j] is ' ':
                empty_cells.append(i * 3 + (j + 1))

    for empty_cell in empty_cells:
        move = {}
        move['index'] = empty_cell
        new_state = copy_game_state(state)
        possible_move(new_state, player, empty_cell)

        if player == 'O':  # If AI
            result = getBestMove(new_state, 'X')  # make more depth tree for human
            move['score'] = result
        else:
            result = getBestMove(new_state, 'O')  # make more depth tree for Agent
            move['score'] = result

        moves.append(move)

    # Finding the best move
    best_move = None
    if player == 'O':  # If it is Agent player
        best = -infinity
        for move in moves:
            if move['score'] > best:
                best = move['score']
                best_move = move['index']
    else:
        best = infinity
        for move in moves:
            if move['score'] < best:
                best = move['score']
                best_move = move['index']

    return best_move


# Starting the game
play_again = 'Y'
player_choice = 0
while play_again == 'Y' or play_again == 'y':
    game_state = [[' ', ' ', ' '],
                  [' ', ' ', ' '],
                  [' ', ' ', ' ']]
    current_state = "Not Done"
    print("\nStarting the Game!")
    print_board(game_state)
    print("Randomly select which player goes first (Agent or Human):")
    players = ['X', 'O']
    player_choice = random.choice(players)
    winner = None

    if player_choice == 'X' or player_choice == 'x':
        print("Human goes first as X!")
        current_player_idx = 0
    else:
        print("Agent goes first as O!")
        current_player_idx = 1

    while current_state == "Not Done":
        if current_player_idx == 0:  # Human's turn
            block_choice = int(input("Dear Human, your turn! Choose where to place (1 to 9): "))
            possible_move(game_state, players[current_player_idx], block_choice)
        else:  # Agent's turn
            block_choice = getBestMove(game_state, players[current_player_idx])
            possible_move(game_state, players[current_player_idx], block_choice)
            print("Agent plays move: " + str(block_choice))
        print_board(game_state)
        winner, current_state = check_current_state(game_state)
        if winner is not None:
            print(str(winner) + " won!")
        else:
            current_player_idx = (current_player_idx + 1) % 2

        if current_state is "Draw":
            print("Draw!")

    play_again = input('Try again, Human? (Y/N) : ')
    if play_again == 'N':
        print('Better practice more, Human!')

# Thank you!