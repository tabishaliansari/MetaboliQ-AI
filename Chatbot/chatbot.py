# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 20:20:29 2024

@author: Tabish Ali Ansari
"""

import tkinter as tk
from tkinter import filedialog, scrolledtext
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

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

        self.greetings = [
            "hello", "hi", "good morning", "good afternoon", "good evening", "hey", "howdy"
        ]
        self.greeting_responses = [
            "Hello! How can I assist you?",
            "Hi there! What can I do for you today?",
            "Greetings! How can I help?",
            "Howdy! What's on your mind?",
        ]

        self.responses = [
            "I'm here to help. What do you need?",
            "What can I assist you with today?",
            "I'm listening. Go ahead.",
        ]

        self.faq_responses = {}  # Dictionary to store FAQ questions and answers
        self.vectorizer = None   # Vectorizer for FAQ matching
        self.faq_questions = []  # List of FAQ questions for vectorization

    def preprocess_text(self, text):
        """
        Preprocess text by removing unnecessary characters and converting to lowercase.
        """
        return re.sub(r"[^\w\s]", "", text.lower().strip())

    def load_faqs(self):
        """
        Load FAQs from a .txt file in the format 'question:answer' and prepare vectorizer.
        """
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                for line in file:
                    if ":" in line:
                        question, answer = line.strip().split(":", 1)
                        self.faq_responses[self.preprocess_text(question)] = answer.strip()
            self.faq_questions = list(self.faq_responses.keys())
            self.vectorizer = TfidfVectorizer().fit(self.faq_questions)
            print("FAQs loaded successfully!")
            print("Loaded FAQs:", self.faq_responses)

    def find_best_match(self, user_input):
        """
        Use cosine similarity to find the best matching question from the FAQ.
        """
        if not self.vectorizer or not self.faq_questions:
            return None
        
        # Vectorize user input and FAQ questions
        user_input_vector = self.vectorizer.transform([self.preprocess_text(user_input)])
        faq_vectors = self.vectorizer.transform(self.faq_questions)
        
        # Calculate cosine similarity
        similarities = cosine_similarity(user_input_vector, faq_vectors)
        max_sim_index = similarities.argmax()
        
        # Check if similarity exceeds a threshold (e.g., 0.2)
        if similarities[0, max_sim_index] > 0.2:
            return self.faq_questions[max_sim_index]
        return None

    def send_message(self):
        user_input_text = self.user_input.get()
        self.chat_history.insert(tk.END, "User: " + user_input_text + "\n")

        user_input_preprocessed = self.preprocess_text(user_input_text)

        # Check if the input is a greeting
        if any(greet in user_input_preprocessed for greet in self.greetings):
            response = random.choice(self.greeting_responses)
        else:
            # Check if input matches an FAQ
            best_match = self.find_best_match(user_input_text)
            if best_match:
                response = self.faq_responses[best_match]
            else:
                response = random.choice(self.responses)

        print("User input:", user_input_text)
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
