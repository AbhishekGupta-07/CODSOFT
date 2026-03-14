import tkinter as tk
from tkinter import scrolledtext
import random

# ==============================
# MOVIE DATASET
# ==============================

movies = [
    {"title":"Interstellar","genre":"sci-fi","rating":4.8},
    {"title":"Inception","genre":"sci-fi","rating":4.7},
    {"title":"The Matrix","genre":"sci-fi","rating":4.6},

    {"title":"Avengers Endgame","genre":"action","rating":4.7},
    {"title":"John Wick","genre":"action","rating":4.6},
    {"title":"Mad Max Fury Road","genre":"action","rating":4.5},

    {"title":"The Hangover","genre":"comedy","rating":4.4},
    {"title":"Superbad","genre":"comedy","rating":4.3},
    {"title":"Rush Hour","genre":"comedy","rating":4.2},

    {"title":"Titanic","genre":"romance","rating":4.8},
    {"title":"The Notebook","genre":"romance","rating":4.5},
    {"title":"La La Land","genre":"romance","rating":4.4},

    {"title":"The Conjuring","genre":"horror","rating":4.4},
    {"title":"Insidious","genre":"horror","rating":4.2},
    {"title":"A Quiet Place","genre":"horror","rating":4.5}
]

user_ratings = {}

genres = ["action","comedy","sci-fi","romance","horror"]


# ==============================
# RECOMMENDATION ENGINE
# ==============================

def recommend_movies(genre):

    results = []

    for m in movies:

        if m["genre"] == genre:

            score = m["rating"]

            if m["title"] in user_ratings:
                score += user_ratings[m["title"]] * 0.3

            results.append((score,m["title"]))

    results.sort(reverse=True)

    return results[:5]


def random_movie():

    movie = random.choice(movies)

    return f"🎲 Surprise Recommendation:\n\n{movie['title']} ({movie['genre']}) ⭐ {movie['rating']}"


# ==============================
# MESSAGE DISPLAY
# ==============================

def add_message(sender,message):

    if sender=="user":

        chat.insert(tk.END,"\nYou:\n","user")
        chat.insert(tk.END,message+"\n","user_msg")

    else:

        chat.insert(tk.END,"\nSystem:\n","bot")
        chat.insert(tk.END,message+"\n","bot_msg")

    chat.yview(tk.END)


# ==============================
# PROCESS TEXT INPUT
# ==============================

def process():

    text = entry.get().lower()

    if text.strip()=="":
        return

    add_message("user",text)

    # RATE MOVIE
    if text.startswith("rate"):

        parts = text.split()

        if len(parts)>=3:

            movie = " ".join(parts[1:-1]).title()
            rating = int(parts[-1])

            user_ratings[movie] = rating

            add_message("bot",f"Thanks! You rated {movie} {rating}/5 ⭐")

    else:

        for g in genres:

            if g in text:

                recs = recommend_movies(g)

                msg=f"🔥 Top {g.title()} Recommendations:\n\n"

                for score,title in recs:

                    msg += f"• {title} ⭐ {round(score,2)}\n"

                add_message("bot",msg)

                break
        else:

            add_message("bot",
            "Try asking:\n• action movies\n• comedy movies\n• sci-fi movies\n\nOr rate a movie:\nrate inception 5")

    entry.delete(0,tk.END)


# ==============================
# DROPDOWN RECOMMENDATION
# ==============================

def recommend_from_dropdown():

    g = genre_var.get()

    recs = recommend_movies(g)

    msg=f"🎬 Recommended {g.title()} Movies:\n\n"

    for score,title in recs:
        msg += f"• {title} ⭐ {round(score,2)}\n"

    add_message("bot",msg)


# ==============================
# CLEAR CHAT
# ==============================

def clear_chat():

    chat.delete("1.0",tk.END)

    add_message("bot","Chat cleared. Ask for recommendations again.")


# ==============================
# GUI
# ==============================

root = tk.Tk()
root.title("🎬 Smart Movie Recommendation System")
root.geometry("560x700")
root.configure(bg="#0f172a")


title = tk.Label(
    root,
    text="🎬 AI Movie Recommendation System",
    font=("Arial",18,"bold"),
    bg="#0f172a",
    fg="white"
)

title.pack(pady=10)


# CHAT AREA
chat = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD,
    font=("Arial",12),
    bg="#1e293b",
    fg="white",
    height=26
)

chat.pack(padx=10,pady=10)


chat.tag_config("user",foreground="#38bdf8",font=("Arial",11,"bold"))
chat.tag_config("bot",foreground="#22c55e",font=("Arial",11,"bold"))

chat.tag_config("user_msg",foreground="white")
chat.tag_config("bot_msg",foreground="#e2e8f0")


# INPUT FRAME
frame = tk.Frame(root,bg="#0f172a")
frame.pack(pady=10)


entry = tk.Entry(frame,font=("Arial",12),width=28)
entry.grid(row=0,column=0,padx=5)


btn = tk.Button(
    frame,
    text="Ask",
    font=("Arial",11,"bold"),
    bg="#22c55e",
    fg="white",
    width=8,
    command=process
)

btn.grid(row=0,column=1,padx=5)


# GENRE DROPDOWN
genre_var = tk.StringVar()
genre_var.set("action")

dropdown = tk.OptionMenu(frame,genre_var,*genres)
dropdown.config(width=8)
dropdown.grid(row=0,column=2,padx=5)


rec_btn = tk.Button(
    frame,
    text="Recommend",
    command=recommend_from_dropdown,
    bg="#6366f1",
    fg="white"
)

rec_btn.grid(row=0,column=3,padx=5)


# SURPRISE BUTTON
surprise = tk.Button(
    root,
    text="🎲 Surprise Me",
    command=lambda:add_message("bot",random_movie()),
    bg="#f59e0b",
    fg="white",
    font=("Arial",11,"bold")
)

surprise.pack(pady=5)


clear = tk.Button(
    root,
    text="Clear Chat",
    command=clear_chat,
    bg="#ef4444",
    fg="white"
)

clear.pack(pady=5)


root.bind("<Return>",lambda event:process())


add_message("bot",
"""Welcome to Smart Movie Recommender 🎬

Ask for genres:
• action movies
• comedy movies
• sci-fi movies
• horror movies

Or rate movies:
rate inception 5

You can also use dropdown or Surprise Me button!
""")


root.mainloop()