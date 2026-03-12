from flask import Flask, render_template, request, redirect
import mysql.connector
from ml_model import predict_marks

app = Flask(__name__)

# MySQL connection
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Admin",
        database="studentdb"
    )

@app.route('/')
def index():
    return render_template('index.html')


# ---------------- ADD STUDENT ---------------- #

@app.route('/add', methods=['GET','POST'])
def add():

    if request.method == 'POST':

        name = request.form['name']
        roll_no = request.form['roll_no']
        subject = request.form['subject']
        marks = request.form['marks']

        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            "INSERT INTO students (name,roll_no,subject,marks) VALUES (%s,%s,%s,%s)",
            (name,roll_no,subject,marks)
        )

        db.commit()
        db.close()

        return redirect('/view')

    return render_template('add.html')


# ---------------- VIEW RECORDS ---------------- #

@app.route('/view')
def view():

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM students")

    data = cursor.fetchall()

    db.close()

    return render_template("view.html",students=data)


# ---------------- DELETE ---------------- #

@app.route('/delete/<int:id>')
def delete(id):

    db = get_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM students WHERE id=%s",(id,))

    db.commit()
    db.close()

    return redirect('/view')


# ---------------- EDIT ---------------- #

@app.route('/edit/<int:id>', methods=['GET','POST'])
def edit(id):

    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':

        name = request.form['name']
        roll_no = request.form['roll_no']
        subject = request.form['subject']
        marks = request.form['marks']

        cursor.execute("""
            UPDATE students
            SET name=%s, roll_no=%s, subject=%s, marks=%s
            WHERE id=%s
        """,(name,roll_no,subject,marks,id))

        db.commit()
        db.close()

        return redirect('/view')

    cursor.execute("SELECT * FROM students WHERE id=%s",(id,))
    student = cursor.fetchone()

    db.close()

    return render_template("edit.html",student=student)


# ---------------- SEARCH ---------------- #

@app.route('/search', methods=['GET','POST'])
def search():

    if request.method == 'POST':

        roll_no = request.form['roll_no']

        db = get_db()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM students WHERE roll_no=%s",(roll_no,))

        student = cursor.fetchall()

        db.close()

        return render_template("view.html",students=student)

    return render_template("search.html")


# ---------------- ML PREDICTION ---------------- #

@app.route('/predict', methods=['GET','POST'])
def predict():

    if request.method == 'POST':

        subject = request.form['subject']

        result = predict_marks(subject)

        return render_template("predict.html",prediction=result)

    return render_template("predict.html")


if __name__ == "__main__":
    app.run(debug=True)