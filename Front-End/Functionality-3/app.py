from flask import Flask, render_template, request
from joblib import load
import numpy as np

app = Flask(__name__)


model = load(r"C:\Users\khushal\Desktop\completenew\joblib models\random_forest_model.joblib")


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
    return render_template('medical_form.html')

@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        
        form_data = request.form.to_dict()

        
        encoded_data = []
        for key, value in form_data.items():
            if key in encoding_map:
                encoded_value = encoding_map[key][value]
                encoded_data.append(encoded_value)
            else:
                
                encoded_data.append(float(value))

        
        input_array = np.array([encoded_data])
        prediction = model.predict(input_array)[0]

        
        return render_template('medical_result.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
