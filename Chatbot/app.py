from flask import Flask, render_template, request
from chatbot import ChatbotApp

app = Flask(__name__)

# Initialize the chatbot logic
chatbot = ChatbotApp()
chatbot.load_faqs("chatbot_dataset.txt")  # Load FAQs from a text file

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_input = request.form["user_input"]  # Get user input from the form
        print(f"User input: {user_input}")  # Debugging line to check user input
        response = chatbot.get_response(user_input)  # Get chatbot response
        print(f"Response: {response}")  # Debugging line to check chatbot response
        return render_template("chatbot.html", response=response, user_input=user_input)
    
    return render_template("chatbot.html", response="Hello! How can I assist you today?", user_input="")

if __name__ == "__main__":
    app.run(debug=True)
