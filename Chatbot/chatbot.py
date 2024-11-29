# -*- coding: utf-8 -*-
#@author: Tabish Ali Ansari

import tkinter as tk
from tkinter import filedialog, scrolledtext
import random

class ChatbotApp:
    def __init__(self, master):
        self.master = master
        master.title("Chatbot")

        self.chat_history = scrolledtext.ScrolledText(master, width=60, height=20)
        self.chat_history.pack(pady=10)

        self.user_input = tk.Entry(master, width=50)
        self.user_input.pack(pady=10)

        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.pack()

        self.responses = [
            "Hello! How can I assist you?",
            "I'm here to help. What do you need?",
            "What can I do for you today?",
            "How can I be of service?",
            "Greetings! What can I do to help you?",
            "Howdy! What's on your mind?",
            "Hi there! What can I assist you with?"
        ]

        self.faq_responses = {}  # Dictionary to store FAQ responses

    def load_faqs(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                for line in file:
                    if ":" in line:
                        question, answer = line.strip().split(":", 1)
                        self.faq_responses[question.strip()] = answer.strip()
            print("FAQs loaded successfully!")
            print("Loaded FAQs:", self.faq_responses)

    def send_message(self):
        user_input_text = self.user_input.get()
        self.chat_history.insert(tk.END, "User: " + user_input_text + "\n")

    # Check if user input matches any FAQ
        if user_input_text.strip() in self.faq_responses:
            response = self.faq_responses[user_input_text.strip()]
        else:
            response = random.choice(self.responses)

        print("User input:", user_input_text)
        #print("FAQ responses:", self.faq_responses)
        print("Response:", response)
    
        self.chat_history.insert(tk.END, "Chatbot: " + response + "\n")
        self.user_input.delete(0, tk.END)


def main():
    root = tk.Tk()
    app = ChatbotApp(root)
    
    # Menu for loading FAQs
    menubar = tk.Menu(root)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Load FAQs", command=app.load_faqs)
    menubar.add_cascade(label="File", menu=filemenu)
    root.config(menu=menubar)
    
    root.mainloop()

if __name__ == "__main__":
    main()