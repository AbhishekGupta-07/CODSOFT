import tkinter as tk
from tkinter import messagebox
import random
import math

board = [""] * 9
human = "X"
ai = "O"
difficulty = "Hard"


# ==========================
# WIN CHECK
# ==========================

def check_winner(b):

    wins = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]

    for w in wins:
        a,b1,c = w
        if b[a] == b[b1] == b[c] and b[a] != "":
            return b[a]

    if "" not in b:
        return "Draw"

    return None


# ==========================
# MINIMAX (HARD AI)
# ==========================

def minimax(new_board, is_max):

    result = check_winner(new_board)

    if result == ai:
        return 1
    elif result == human:
        return -1
    elif result == "Draw":
        return 0

    if is_max:

        best = -math.inf

        for i in range(9):
            if new_board[i] == "":
                new_board[i] = ai
                score = minimax(new_board, False)
                new_board[i] = ""
                best = max(best, score)

        return best

    else:

        best = math.inf

        for i in range(9):
            if new_board[i] == "":
                new_board[i] = human
                score = minimax(new_board, True)
                new_board[i] = ""
                best = min(best, score)

        return best


def best_move():

    best_score = -math.inf
    move = None

    for i in range(9):
        if board[i] == "":
            board[i] = ai
            score = minimax(board, False)
            board[i] = ""

            if score > best_score:
                best_score = score
                move = i

    return move


# ==========================
# AI MOVE
# ==========================

def ai_move():

    global difficulty

    if difficulty == "Easy":

        moves = [i for i in range(9) if board[i] == ""]
        move = random.choice(moves)

    elif difficulty == "Medium":

        if random.random() < 0.5:
            moves = [i for i in range(9) if board[i] == ""]
            move = random.choice(moves)
        else:
            move = best_move()

    else:
        move = best_move()

    if move is not None:
        board[move] = ai
        buttons[move]["text"] = ai

    check_game()


# ==========================
# PLAYER MOVE
# ==========================

def player_move(i):

    if board[i] != "":
        return

    board[i] = human
    buttons[i]["text"] = human

    result = check_winner(board)

    if result:
        show_result(result)
        return

    root.after(300, ai_move)


# ==========================
# RESULT SCREEN
# ==========================

def show_result(result):

    if result == human:
        messagebox.showinfo("Game Result", "🎉 Congratulations! You Win!")

    elif result == ai:
        messagebox.showinfo("Game Result", "😢 You Lose! AI Wins!")

    else:
        messagebox.showinfo("Game Result", "🤝 It's a Draw!")

    new_game()


# ==========================
# RESET BOARD
# ==========================

def reset_board():

    global board
    board = [""] * 9

    for b in buttons:
        b["text"] = ""


def new_game():

    reset_board()


# ==========================
# SET DIFFICULTY
# ==========================

def set_difficulty(level):

    global difficulty
    difficulty = level

    messagebox.showinfo("Difficulty", f"Difficulty set to {level}")


# ==========================
# GUI
# ==========================

root = tk.Tk()
root.title("🤖 Tic Tac Toe AI")
root.geometry("360x500")
root.configure(bg="#0f172a")


title = tk.Label(
    root,
    text="🤖 Tic Tac Toe AI",
    font=("Arial",20,"bold"),
    bg="#0f172a",
    fg="white"
)

title.pack(pady=10)


# ==========================
# DIFFICULTY BUTTONS
# ==========================

diff_frame = tk.Frame(root,bg="#0f172a")
diff_frame.pack(pady=5)

tk.Button(diff_frame,text="Easy",
          command=lambda:set_difficulty("Easy"),
          bg="#22c55e",fg="white",width=8).grid(row=0,column=0,padx=5)

tk.Button(diff_frame,text="Medium",
          command=lambda:set_difficulty("Medium"),
          bg="#f59e0b",fg="white",width=8).grid(row=0,column=1,padx=5)

tk.Button(diff_frame,text="Hard",
          command=lambda:set_difficulty("Hard"),
          bg="#ef4444",fg="white",width=8).grid(row=0,column=2,padx=5)


# ==========================
# GAME BOARD
# ==========================

frame = tk.Frame(root,bg="#0f172a")
frame.pack(pady=15)

buttons = []

for i in range(9):

    btn = tk.Button(
        frame,
        text="",
        font=("Arial",22,"bold"),
        width=5,
        height=2,
        bg="#1e293b",
        fg="white",
        command=lambda i=i: player_move(i)
    )

    btn.grid(row=i//3,column=i%3,padx=5,pady=5)

    buttons.append(btn)


# ==========================
# NEW GAME BUTTON
# ==========================

new_btn = tk.Button(
    root,
    text="New Game",
    font=("Arial",12,"bold"),
    bg="#3b82f6",
    fg="white",
    command=new_game
)

new_btn.pack(pady=15)


root.mainloop()