import math

EMPTY = "_"
AI_PLAYER = "X"
HUMAN_PLAYER = "O"


def check_winner(board_state):
    winning_positions = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]

    for pos1, pos2, pos3 in winning_positions:
        if board_state[pos1] == board_state[pos2] == board_state[pos3] != EMPTY:
            return board_state[pos1]


def is_terminal(board_state):
    return check_winner(board_state) or EMPTY not in board_state


def evaluate_board(board_state):
    winner = check_winner(board_state)

    if winner == AI_PLAYER:
        return 10
    elif winner == HUMAN_PLAYER:
        return -10
    return 0


def alpha_beta_search(board_state, is_max_turn, alpha=-math.inf, beta=math.inf):

    if is_terminal(board_state):
        return evaluate_board(board_state)

    if is_max_turn:
        best_score = -math.inf

        for position in range(9):
            if board_state[position] == EMPTY:
                board_state[position] = AI_PLAYER

                score = alpha_beta_search(board_state, False, alpha, beta)

                board_state[position] = EMPTY

                best_score = max(best_score, score)
                alpha = max(alpha, best_score)

                if beta <= alpha:
                    break

        return best_score

    else:
        best_score = math.inf

        for position in range(9):
            if board_state[position] == EMPTY:
                board_state[position] = HUMAN_PLAYER

                score = alpha_beta_search(board_state, True, alpha, beta)

                board_state[position] = EMPTY

                best_score = min(best_score, score)
                beta = min(beta, best_score)

                if beta <= alpha:
                    break

        return best_score


def find_best_move(board_state):

    best_position = -1
    best_score = -math.inf

    for position in range(9):
        if board_state[position] == EMPTY:
            board_state[position] = AI_PLAYER

            score = alpha_beta_search(board_state, False)

            board_state[position] = EMPTY

            if score > best_score:
                best_score = score
                best_position = position

    return best_position


def display_board(board_state):
    for i in range(0, 9, 3):
        print(board_state[i], board_state[i+1], board_state[i+2])
    print()


# -------- Game Start --------

game_board = [EMPTY] * 9

print("Positions are numbered 1-9 as:")
print("1 2 3")
print("4 5 6")
print("7 8 9\n")

while not is_terminal(game_board):

    display_board(game_board)

    human_move = int(input("Your move (1-9): ")) - 1

    if game_board[human_move] == EMPTY:
        game_board[human_move] = HUMAN_PLAYER

    if not is_terminal(game_board):
        ai_move = find_best_move(game_board)
        print("AI moves to:", ai_move + 1)
        game_board[ai_move] = AI_PLAYER


display_board(game_board)

winner = check_winner(game_board)

print("Winner:", winner if winner else "Draw")