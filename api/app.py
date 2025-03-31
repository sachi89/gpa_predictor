from flask import Flask, render_template, request
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from flask_cors import CORS

app = Flask(__name__)

# enables CORS to make requests between domains on allowed routes
# CORS(app, resources={r"/chat": {"origins": "https://gpapredictor.scali-tech.com"}})
CORS(app)

df = pd.read_csv('student_performance_data.csv')

features = [
    'ParentalEducation', 'StudyTimeWeekly', 'Absences',
    'ParentalSupport', 'Tutoring', 'Extracurricular',
    'Sports', 'Music', 'Volunteering'
]
X = df[features]
y = df['GPA']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

lr_model = LinearRegression()
lr_model.fit(X_train_scaled, y_train)

rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

edu_levels = {
    "0": "No High School",
    "1": "High School",
    "2": "Some College",
    "3": "Bachelor's Degree",
    "4": "Graduate Degree"
}
support_levels = {
    "1": "Low",
    "2": "Moderate",
    "3": "High"
}
yes_no = {
    "1": "Yes",
    "0": "No"
}

def predict_gpa(input_data, model='random_forest'):
    input_df = pd.DataFrame([input_data])[features]
    if model == 'linear_regression':
        input_scaled = scaler.transform(input_df)
        return round(lr_model.predict(input_scaled)[0], 2)
    else:
        return round(rf_model.predict(input_df)[0], 2)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()  # Use JSON instead of form data

    if not data:
        return {"error": "Invalid JSON payload"}, 400

    try:
        user_input = {
            'ParentalEducation': int(data.get('ParentalEducation', 0)),  # Provide default value
            'StudyTimeWeekly': float(data.get('StudyTimeWeekly', 0)),
            'Absences': int(data.get('Absences', 0)),
            'ParentalSupport': int(data.get('ParentalSupport', 0)),
            'Tutoring': int(data.get('Tutoring', 0)),
            'Extracurricular': int(data.get('Extracurricular', 0)),
            'Sports': int(data.get('Sports', 0)),
            'Music': int(data.get('Music', 0)),
            'Volunteering': int(data.get('Volunteering', 0))
        }
    except ValueError as e:
        return {"error": f"Invalid data type: {str(e)}"}, 400

    prediction = predict_gpa(user_input)

    return {"response": prediction}

    # prediction = None
    # readable_input = None

    # if request.method == 'POST':
    #     form = request.form
    #     user_input = {
    #         'ParentalEducation': int(form['ParentalEducation']),
    #         'StudyTimeWeekly': float(form['StudyTimeWeekly']),
    #         'Absences': int(form['Absences']),
    #         'ParentalSupport': int(form['ParentalSupport']),
    #         'Tutoring': int(form['Tutoring']),
    #         'Extracurricular': int(form['Extracurricular']),
    #         'Sports': int(form['Sports']),
    #         'Music': int(form['Music']),
    #         'Volunteering': int(form['Volunteering'])
    #     }
    #     prediction = predict_gpa(user_input)
    #     readable_input = {
    #         'Parental Education': edu_levels[form['ParentalEducation']],
    #         'Study Time Weekly': f"{form['StudyTimeWeekly']} hrs",
    #         'Absences': form['Absences'],
    #         'Parental Support': support_levels[form['ParentalSupport']],
    #         'Tutoring': yes_no[form['Tutoring']],
    #         'Extracurricular': yes_no[form['Extracurricular']],
    #         'Sports': yes_no[form['Sports']],
    #         'Music': yes_no[form['Music']],
    #         'Volunteering': yes_no[form['Volunteering']]
    #     }
        # switched from rendering html form to react form
        # return render_template('index.html', prediction=prediction, inputs=readable_input)
        # return prediction

if __name__ == '__main__':
    app.run(debug=True)