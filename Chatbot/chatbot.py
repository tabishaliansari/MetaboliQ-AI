import random

class ChatbotApp:
    def __init__(self):
        # Predefined chatbot responses
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

    def load_faqs(self, file_path):
        """Load FAQ data from a text file."""
        with open(file_path, "r") as file:
            for line in file:
                if ":" in line:
                    question, answer = line.strip().split(":", 1)
                    self.faq_responses[question.strip().lower()] = answer.strip()

    def get_response(self, user_input):
        """Handle user input and respond based on FAQ or random response."""
        user_input_text = user_input.strip().lower()  # Normalize input to lowercase
        if user_input_text in self.faq_responses:
            return self.faq_responses[user_input_text]
        else:
            return random.choice(self.responses)
