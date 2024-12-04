import random
import re
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os


FAQ_FILE_PATH = r"C:\Users\khushal\Desktop\completenew\chatbot_dataset.txt" 


app = Flask(__name__)
CORS(app)

class Chatbot:
    def __init__(self, faq_file_path):
        
        self.greetings = [
            "hello", "hi", "good morning", "good afternoon", "good evening", "hey", "howdy"
        ]
        self.greeting_responses = [
            "Hello! How can I assist you?",
            "Hi there! What can I do for you today?",
            "Greetings! How can I help?",
            "Howdy! What's on your mind?",
        ]

        self.default_responses = [
            "I'm here to help. What do you need?",
            "What can I assist you with today?",
            "I'm listening. Go ahead.",
            "I'm afraid I don't have a specific answer for that. Could you try a different question?",
        ]

        
        self.faq_responses = {}
        self.vectorizer = None
        self.faq_questions = []

        
        self.load_faqs(faq_file_path)

    def preprocess_text(self, text):
        """
        Preprocess text by removing unnecessary characters and converting to lowercase.
        """
        return re.sub(r"[^\w\s]", "", text.lower().strip())

    def load_faqs(self, faq_file_path):
        """
        Load FAQs from a .txt file in the format 'question:answer'
        """
        try:
            
            if not os.path.exists(faq_file_path):
                print(f"ERROR: File not found at {faq_file_path}")
                return False

            
            self.faq_responses.clear()
            self.faq_questions.clear()

           
            with open(faq_file_path, "r", encoding='utf-8') as file:
                for line in file:
                    
                    parts = line.strip().split(":", 1)
                    if len(parts) == 2:
                        question, answer = parts
                        processed_question = self.preprocess_text(question)
                        self.faq_responses[processed_question] = answer.strip()

            
            if self.faq_responses:
                self.faq_questions = list(self.faq_responses.keys())
                self.vectorizer = TfidfVectorizer().fit(self.faq_questions)
                print(f"Successfully loaded {len(self.faq_questions)} FAQs")
                return True
            else:
                print("No FAQs found in the file")
                return False

        except Exception as e:
            print(f"Error loading FAQs: {str(e)}")
            return False

    def find_best_match(self, user_input):
        """
        Use cosine similarity to find the best matching question from the FAQ.
        """
        if not self.vectorizer or not self.faq_questions:
            return None
        
        
        user_input_vector = self.vectorizer.transform([self.preprocess_text(user_input)])
        faq_vectors = self.vectorizer.transform(self.faq_questions)
        
        
        similarities = cosine_similarity(user_input_vector, faq_vectors)
        max_sim_index = similarities.argmax()
        
        
        if similarities[0, max_sim_index] > 0.2:
            return self.faq_questions[max_sim_index]
        return None

    def get_response(self, user_input):
        """
        Generate a response based on user input.
        """
        user_input_preprocessed = self.preprocess_text(user_input)

        
        if any(greet in user_input_preprocessed for greet in self.greetings):
            return random.choice(self.greeting_responses)

        
        best_match = self.find_best_match(user_input)
        if best_match:
            return self.faq_responses[best_match]

        return random.choice(self.default_responses)

chatbot = Chatbot(FAQ_FILE_PATH)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """
    Chat endpoint to process user messages.
    """
    data = request.get_json()
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({"response": "Please send a message."}), 400
    
    response = chatbot.get_response(user_message)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
