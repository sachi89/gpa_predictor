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

# load dataset
df = pd.read_csv('student_performance_data.csv')

# define features (independent variables) and target variable
features = [
    'ParentalEducation', 'StudyTimeWeekly', 'Absences',
    'ParentalSupport', 'Tutoring', 'Extracurricular',
    'Sports', 'Music', 'Volunteering'
]
X = df[features] # extracts predictor variables from the dataset
y = df['GPA'] # extracts the target variable GPA

# split data into training and testing sets (80% training data, 20% testing data)
# random_state=42 ensures consistent results across runs
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# normalize the feature data for models like linear regression
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# train machine learning models
# train linear regression model using the scaled data
lr_model = LinearRegression()
lr_model.fit(X_train_scaled, y_train)

# train random forest model with 100 decision trees
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# mapping for categorical variables for reference
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

# define prediction function
# default model used is random forest
# takes input_data from user input and converts it into a Pandas dataframe
# ensures that only the defined features are selected
# if linear regression is selected, normalize the input and predict GPA
# if random forest is selected, predict GPA without scaling
def predict_gpa(input_data, model='random_forest'):
    input_df = pd.DataFrame([input_data])[features]
    if model == 'linear_regression':
        input_scaled = scaler.transform(input_df)
        return round(lr_model.predict(input_scaled)[0], 2)
    else:
        return round(rf_model.predict(input_df)[0], 2)

# define api endpoint
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()  # extracts JSON payload from the request
    # if no data is received, returns a 400 Bad Request error
    if not data:
        return {"error": "Invalid JSON payload"}, 400
    
    # converts user inputs to the expected data types for the prediction model:
    # integers for categorical variables
    # floats for numerical variables
    # default values to prevent missing data errors
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
    # handles invalid input by returning an error
    except ValueError as e:
        return {"error": f"Invalid data type: {str(e)}"}, 400
    
    # calls predict_gpa() with user input
    prediction = predict_gpa(user_input)
    
    # returns the predicted GPA as a JSON response to display on frontend
    return {"response": prediction}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
