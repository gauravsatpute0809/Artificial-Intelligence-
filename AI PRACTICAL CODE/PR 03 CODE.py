import math
import time

# Game board
game_board = [" " for _ in range(9)]

def display_board():
    print("\n")
    print(f"{game_board[0]} | {game_board[1]} | {game_board[2]}")
    print("--+---+--")
    print(f"{game_board[3]} | {game_board[4]} | {game_board[5]}")
    print("--+---+--")
    print(f"{game_board[6]} | {game_board[7]} | {game_board[8]}")
    print("\n")

def check_winner(player_symbol):
    winning_patterns = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]

    for pattern in winning_patterns:
        if game_board[pattern[0]] == game_board[pattern[1]] == game_board[pattern[2]] == player_symbol:
            return True
    return False

def board_full():
    return " " not in game_board

def minimax_algorithm(is_computer_turn):
    if check_winner("O"):
        return 1
    if check_winner("X"):
        return -1
    if board_full():
        return 0

    if is_computer_turn:
        best_value = -math.inf
        for position in range(9):
            if game_board[position] == " ":
                game_board[position] = "O"
                score = minimax_algorithm(False)
                game_board[position] = " "
                best_value = max(score, best_value)
        return best_value
    else:
        best_value = math.inf
        for position in range(9):
            if game_board[position] == " ":
                game_board[position] = "X"
                score = minimax_algorithm(True)
                game_board[position] = " "
                best_value = min(score, best_value)
        return best_value

def computer_play():
    best_value = -math.inf
    best_move = 0

    for position in range(9):
        if game_board[position] == " ":
            game_board[position] = "O"
            score = minimax_algorithm(False)
            game_board[position] = " "

            if score > best_value:
                best_value = score
                best_move = position

    print("Computer is thinking...")
    time.sleep(1)

    game_board[best_move] = "O"
    print(f"Computer chose position: {best_move + 1}")

def start_game():
    print("You are X | Computer is O")
    print("Positions are numbered 1 to 9 like this:\n")

    print("1 | 2 | 3")
    print("--+---+--")
    print("4 | 5 | 6")
    print("--+---+--")
    print("7 | 8 | 9\n")

    while True:
        display_board()

        try:
            user_choice = int(input("Choose position (1-9): ")) - 1

            if user_choice not in range(9) or game_board[user_choice] != " ":
                print("Invalid move. Try again.")
                continue

        except:
            print("Please enter a number between 1 and 9.")
            continue

        game_board[user_choice] = "X"

        if check_winner("X"):
            display_board()
            print("You Win!")
            break

        if board_full():
            display_board()
            print("It's a Draw!")
            break

        computer_play()

        if check_winner("O"):
            display_board()
            print("Computer Wins!")
            break

        if board_full():
            display_board()
            print("It's a Draw!")
            break

start_game()