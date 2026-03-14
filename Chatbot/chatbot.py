import tkinter as tk
from tkinter import scrolledtext
import random
from datetime import datetime


# ----------------------------
# CHATBOT KNOWLEDGE
# ----------------------------

INTENTS = [
    {
        "keywords": ["hello", "hi", "hey"],
        "responses": [
            "Hello! 👋 How can I help you?",
            "Hi there! Nice to see you.",
            "Hey! What would you like to talk about?"
        ]
    },
    {
        "keywords": ["who are you", "your name"],
        "responses": [
            "I'm SmartBot 🤖 — a rule-based AI chatbot built with Python.",
            "My name is SmartBot. I was created as an AI internship project."
        ]
    },
    {
        "keywords": ["joke", "funny"],
        "responses": [
            "Why do programmers prefer dark mode? Because light attracts bugs 🐛",
            "Why do Python developers wear glasses? Because they can't C 😂"
        ]
    },
    {
        "keywords": ["help"],
        "responses": [
            "You can ask me about:\n• Python\n• AI\n• Time\n• Date\n• Jokes"
        ]
    }
]


# ----------------------------
# BOT RESPONSE LOGIC
# ----------------------------

def get_response(text):
    text = text.lower()

    for intent in INTENTS:
        for keyword in intent["keywords"]:
            if keyword in text:
                return random.choice(intent["responses"])

    if "time" in text:
        return "Current time: " + datetime.now().strftime("%H:%M:%S")

    if "date" in text:
        return "Today's date: " + datetime.now().strftime("%d %B %Y")

    if "python" in text:
        return "Python is widely used for AI, automation and data science."

    if "ai" in text:
        return "Artificial Intelligence allows computers to learn patterns and make decisions."

    return "Sorry, I didn't understand that."


# ----------------------------
# MAIN PROGRAM
# ----------------------------

def main():

    def add_message(sender, message):
        chat_area.config(state="normal")

        time_now = datetime.now().strftime("%H:%M")

        if sender == "user":
            chat_area.insert(tk.END, f"\nYou ({time_now}): {message}\n")
        else:
            chat_area.insert(tk.END, f"\nSmartBot ({time_now}): {message}\n")

        chat_area.config(state="disabled")
        chat_area.yview(tk.END)


    def send_message(event=None):

        user_text = entry.get().strip()

        if user_text == "":
            return

        add_message("user", user_text)
        entry.delete(0, tk.END)

        response = get_response(user_text)
        add_message("bot", response)


    def clear_chat():
        chat_area.config(state="normal")
        chat_area.delete("1.0", tk.END)
        chat_area.config(state="disabled")


    root = tk.Tk()
    root.title("SmartBot AI Assistant")
    root.geometry("550x650")
    root.configure(bg="#0f172a")


    header = tk.Label(
        root,
        text="🤖 SmartBot AI Assistant",
        font=("Arial", 18, "bold"),
        bg="#0f172a",
        fg="white"
    )
    header.pack(pady=10)


    global chat_area
    chat_area = scrolledtext.ScrolledText(
        root,
        wrap=tk.WORD,
        font=("Arial", 12),
        bg="#1e293b",
        fg="white",
        height=25
    )
    chat_area.pack(padx=10, pady=10)
    chat_area.config(state="disabled")


    input_frame = tk.Frame(root, bg="#0f172a")
    input_frame.pack(pady=10)


    global entry
    entry = tk.Entry(input_frame, font=("Arial", 12), width=30)
    entry.grid(row=0, column=0, padx=10)


    send_btn = tk.Button(
        input_frame,
        text="Send",
        command=send_message,
        bg="#22c55e",
        fg="white",
        font=("Arial", 11, "bold"),
        width=8
    )
    send_btn.grid(row=0, column=1)


    clear_btn = tk.Button(
        input_frame,
        text="Clear",
        command=clear_chat,
        bg="#ef4444",
        fg="white",
        font=("Arial", 11, "bold"),
        width=8
    )
    clear_btn.grid(row=0, column=2)


    entry.bind("<Return>", send_message)
    entry.focus()


    add_message("bot", "Hello 👋 I'm SmartBot. Ask me about Python, AI, time, or jokes!")

    root.mainloop()


# ----------------------------
# PROGRAM ENTRY
# ----------------------------

if __name__ == "__main__":
    main()