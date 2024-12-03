from flask import Flask, render_template, request
import joblib  # For loading the trained model

app = Flask(__name__)

# Load the trained model (assumed it's saved as a .joblib file)
model = joblib.load('5_6230806539179922300.joblib')

# You may need to define how the features are generated from the year
# For example, you might have a mapping of year to features or pre-calculated data
def get_features_from_year(year):
    # This is just an example. Replace this with how you handle year-based features.
    # You may use static values, or calculate them based on year.
    population = 1000000  # Example static value or calculated based on year
    diabetic_patients = 200000  # Example static value or calculated based on year
    male_diabetic_patients = 100000  # Example static value or calculated
    female_diabetic_patients = 100000  # Example static value or calculated
    pollution = 50  # Example static value or calculated
    health_index = 70  # Example static value or calculated
    return [population, diabetic_patients, male_diabetic_patients, female_diabetic_patients, pollution, health_index]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Retrieve year input
    year = int(request.form['year'])

    # Get features based on the year
    features = get_features_from_year(year)

    # Make prediction using the trained model
    prediction = model.predict([features])[0]  # Assuming the model takes in a list of features

    # Return result page with the prediction
    return render_template(
        'result.html',
        prediction=prediction,
        year=year,
        population=features[0],
        diabetic_patients=features[1],
        male_diabetic_patients=features[2],
        female_diabetic_patients=features[3],
        pollution=features[4],
        health_index=features[5]
    )

if __name__ == '__main__':
    app.run(debug=True)
