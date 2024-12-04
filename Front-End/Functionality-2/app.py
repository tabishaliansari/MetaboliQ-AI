from flask import Flask, render_template, request
from joblib import load
import sqlite3

app = Flask(__name__)


model = load(r"C:\Users\khushal\Desktop\completenew\joblib models\decision_tree_model (4).joblib")


DB_FILE = 'diabetes_data.db'


def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_data (
            PatientID INTEGER PRIMARY KEY AUTOINCREMENT,
            Age INT CHECK (Age > 0 AND Age <= 13),
            Sex TINYINT(1), 
            BMI FLOAT CHECK (BMI > 0 AND BMI < 60),
            Smoker TINYINT(1),
            HighBP TINYINT(1),
            HighChol TINYINT(1),
            Stroke TINYINT(1),
            HeartDiseaseorAttack TINYINT(1),
            PhysActivity TINYINT(1),
            HvyAlcoholConsump TINYINT(1),
            GenHlth INT CHECK (GenHlth > 0 AND GenHlth <= 5),
            MentHlth INT CHECK (MentHlth >= 0 AND MentHlth <= 30),
            PhysHlth INT CHECK (PhysHlth >= 0 AND PhysHlth <= 30)
        )
    ''')
    conn.commit()
    conn.close()


init_db()


def map_age_to_bucket(age):
    if 18 <= age <= 24:
        return 1
    elif 25 <= age <= 29:
        return 2
    elif 30 <= age <= 34:
        return 3
    elif 35 <= age <= 39:
        return 4
    elif 40 <= age <= 44:
        return 5
    elif 45 <= age <= 49:
        return 6
    elif 50 <= age <= 54:
        return 7
    elif 55 <= age <= 59:
        return 8
    elif 60 <= age <= 64:
        return 9
    elif 65 <= age <= 69:
        return 10
    elif 70 <= age <= 74:
        return 11
    elif 75 <= age <= 79:
        return 12
    elif age >= 80:
        return 13
    else:
        raise ValueError("Age should be above 18")

@app.route('/')
def form_page():
    return render_template('lifestyle_form.html')

@app.route('/result', methods=['POST'])
def result():
    try:
       
        user_data = request.form.to_dict()

       
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
        

        
        user_data['Age'] = map_age_to_bucket(int(user_data['Age']))
        for key, mapping in encoding_map.items():
            user_data[key] = mapping.get(user_data[key], None)

        features = [
            user_data['Age'], 
            user_data['Sex'],  
            float(user_data['BMI']),
            user_data['Smoker'],  
            user_data['HighBP'],  
            user_data['HighChol'], 
            user_data['Stroke'],  
            user_data['HeartDiseaseorAttack'],  
            user_data['PhysActivity'], 
            user_data['HvyAlcoholConsump'],  
            float(user_data['GenHlth']),
            float(user_data['MentHlth']),
            float(user_data['PhysHlth'])
        ]

        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO user_data (
                Age, Sex, BMI, Smoker, HighBP, HighChol, Stroke,
                HeartDiseaseorAttack, PhysActivity, HvyAlcoholConsump,
                GenHlth, MentHlth, PhysHlth
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', features)
        conn.commit()
        conn.close()

        
        prediction = model.predict([features])

        
        result = "Diabetic" if prediction[0] == 1 else "Non-Diabetic"
        return render_template('lifestyle_result.html', result=result)
    except (ValueError, KeyError) as e:
        return f"Error in processing input data: {e}", 400
    except Exception as e:
        return f"Unexpected error: {e}", 500


if __name__ == '__main__':
    app.run(debug=True)
