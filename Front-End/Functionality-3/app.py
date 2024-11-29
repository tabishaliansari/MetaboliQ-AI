from flask import Flask, render_template, request
from joblib import load
import numpy as np

app = Flask(__name__)

# Load the trained model
model = load('random_forest_model.joblib')

# Encoding maps for categorical inputs
encoding_map = {
    'GeneticMarkers': {'Positive': 1, 'Negative': 0},
    'Autoantibodies': {'Positive': 1, 'Negative': 0},
    'FamilyHistory': {'Yes': 1, 'No': 0},
    'EnvironmentalFactors': {'Present': 1, 'Absent': 0},
    'PhysicalActivity': {'low': 0, 'moderate': 1, 'high': 2},
    'DietaryHabits': {'Healthy': 1, 'Unhealthy': 0},
    'Ethnicity': {'high risk': 1, 'low risk': 0},
    'SocioeconomicFactors': {'low': 0, 'moderate': 1, 'high': 2},
    'SmokingStatus': {'smoker': 1, 'non-smoker': 0},
    'AlcoholConsumption': {'low': 0, 'moderate': 1, 'high': 2},
    'GlucoseToleranceTest': {'normal': 0, 'abnormal': 1},
    'HistoryOfPCOS': {'Yes': 1, 'No': 0},
    'PreviousGestationalDiabetes': {'Yes': 1, 'No': 0},
    'PregnancyHistory': {'normal': 0, 'complicated': 1},
    'CysticFibrosisDiagnosis': {'Yes': 1, 'No': 0},
    'SteroidUseHistory': {'Yes': 1, 'No': 0},
    'GeneticTesting': {'Positive': 1, 'Negative': 0},
    'LiverFunctionTests': {'normal': 0, 'abnormal': 1},
    'UrineTest': {
        'Protein Present': 3,
        'Normal': 2,
        'Glucose Present': 1,
        'Ketones Present': 0
    },
    'EarlyOnsetSymptoms': {'Yes': 1, 'No': 0},
}

@app.route('/')
def home():
    return render_template('form.html')

@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        # Retrieve form data
        form_data = request.form.to_dict()

        # Encode categorical inputs
        encoded_data = []
        for key, value in form_data.items():
            if key in encoding_map:
                encoded_value = encoding_map[key][value]
                encoded_data.append(encoded_value)
            else:
                # Directly append numeric fields
                encoded_data.append(float(value))

        # Convert data to numpy array for model prediction
        input_array = np.array([encoded_data])
        prediction = model.predict(input_array)[0]

        # Render prediction result
        return render_template('result.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
