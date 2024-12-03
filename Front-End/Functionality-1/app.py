from flask import Flask, request, render_template
from joblib import load
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Load the saved model
model = load('Functionality-1-LR.joblib')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get user input from the form
        year = int(request.form['year'])
        
        # Prepare data for the model (reshape as required by the model)
        input_data = np.array([[year]])
        
        # Predict using the model
        prediction = model.predict(input_data)
        
        # Return the prediction result to the frontend
        return render_template('index.html', prediction=round(prediction[0]))
    except ValueError:
        return render_template('index.html', error="Invalid input. Please enter a valid year.")

if __name__ == '__main__':
    app.run(debug=True)
