from flask import Flask, render_template, request
import joblib

app = Flask(__name__)

# Load your model
model = joblib.load(r"gestational.ipynb")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Collect inputs from form
        age = float(request.form['age'])
        pregnancy_no = float(request.form['pregnancy_no'])
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        bmi = float(request.form['bmi'])
        heredity = float(request.form['heredity'])
        
        # Prepare the input for the model
        inputs = [age, pregnancy_no, weight, height, bmi, heredity]
        
        # Predict using the model
        prediction = model.predict([inputs])[0]
        
        # Determine the result
        result = "has gestational diabetes" if prediction == 1 else "does not have gestational diabetes"
        return render_template('result.html', result=result)
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)
