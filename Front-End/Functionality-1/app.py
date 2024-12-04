from flask import Flask, request, render_template
from joblib import load
import numpy as np

app = Flask(__name__)


model = load(r'Functionality-1-LR.joblib')

@app.route('/')
def index():
    return render_template('population.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        
        year = int(request.form['year'])
        
        
        input_data = np.array([[year]])
        
        
        prediction = model.predict(input_data)
        
        
        return render_template('population.html', prediction=round(prediction[0]))
    except ValueError:
        return render_template('templates\population.html', error="Invalid input. Please enter a valid year.")

if __name__ == '__main__':
    app.run(debug=True)
