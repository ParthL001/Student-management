import mysql.connector
import pandas as pd
from sklearn.linear_model import LinearRegression

# Database connection
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Admin",
        database="studentdb"
    )


# Load data from database
def load_data():
    db = get_db()
    query = "SELECT subject, marks FROM students"
    df = pd.read_sql(query, db)
    db.close()
    return df


# Train ML model
def train_model():

    df = load_data()

    # convert subject text → number
    df["subject"] = df["subject"].astype("category").cat.codes

    X = df[["subject"]]
    y = df["marks"]

    model = LinearRegression()
    model.fit(X, y)

    return model


# Predict marks
def predict_marks(subject):

    df = load_data()

    subjects = list(df["subject"].unique())
    subject_map = {s:i for i,s in enumerate(subjects)}

    if subject not in subject_map:
        return "Not enough data"

    subject_value = subject_map[subject]

    model = train_model()

    prediction = model.predict([[subject_value]])

    return round(prediction[0],2)