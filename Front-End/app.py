from flask import Flask, render_template, request
from joblib import load

app = Flask(__name__)

# Load the trained DecisionTreeClassifier model
model = load('decision_tree_model.joblib')

# Temporary storage for user inputs
user_data = {}

@app.route('/')
def form_page_1():
    return render_template('form_page_1.html')

@app.route('/form_page_2', methods=['POST'])
def form_page_2():
    global user_data
    user_data.update(request.form.to_dict())  # Save data from Page 1
    return render_template('form_page_2.html')

@app.route('/result', methods=['POST'])
def result():
    global user_data
    user_data.update(request.form.to_dict())  # Save data from Page 2

    # Map categorical values to numerical encoding
    encoding_map = {
        'Sex': {'M': 0, 'F': 1},
        'Smoker': {'No': 0, 'Yes': 1},
        'HighBP': {'No': 0, 'Yes': 1},
        'HighChol': {'No': 0, 'Yes': 1},
        'Stroke': {'No': 0, 'Yes': 1},
        'HeartDiseaseorAttack': {'No': 0, 'Yes': 1},
        'PhysActivity': {'No': 0, 'Yes': 1},
        'HvyAlcoholConsump': {'No': 0, 'Yes': 1}
    }

    # Encode categorical features
    for key, mapping in encoding_map.items():
        user_data[key] = mapping.get(user_data[key], None)

    # Convert user data to a feature list for prediction
    try:
        features = [
            float(user_data['Age']),
            user_data['Sex'],  # Encoded
            float(user_data['BMI']),
            user_data['Smoker'],  # Encoded
            user_data['HighBP'],  # Encoded
            user_data['HighChol'],  # Encoded
            user_data['Stroke'],  # Encoded
            user_data['HeartDiseaseorAttack'],  # Encoded
            user_data['PhysActivity'],  # Encoded
            user_data['HvyAlcoholConsump'],  # Encoded
            float(user_data['GenHlth']),
            float(user_data['MentHlth']),
            float(user_data['PhysHlth'])
        ]
    except (ValueError, KeyError) as e:
        return f"Error in processing input data: {e}", 400

    # Perform prediction
    prediction = model.predict([features])

    # Interpret the prediction
    result = "Diabetic" if prediction[0] == 1 else "Non-Diabetic"

    # Pass the result to the result template
    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
