from flask import Flask, render_template, request, session, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os

app = Flask(__name__, static_url_path='/static')
app.jinja_env.globals.update(zip=zip)
app.secret_key = 'asdf123'

# Create login database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'tmp/test.db')
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

# Instantiate the new database
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Fetch the user from the database

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user is None or not user.check_password(password):
            return "Invalid username or password"

        login_user(user)  # Log in the user
        return redirect(url_for('home'))

    else:
        return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User(username=username)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))
    else:
        return render_template('register.html')


# Load exercise questions and correct answers from JSON
with open('exercises.json', 'r') as file:
    exercise_data = json.load(file)
    exercises = {str(i+1): ex["ExerciseName"] for i, ex in enumerate(exercise_data)}
    exercise_track = {str(i+1): ex["Track"] for i, ex in enumerate(exercise_data)}
    exercise_questions = {str(i+1): list(ex["Questions"].keys()) for i, ex in enumerate(exercise_data)}
    exercise_answers = {str(i+1): list(ex["Questions"].values()) for i, ex in enumerate(exercise_data)}

# create a dict where each key is a track name and each value is a list of exercises for that track
exercises_by_track = {}
for id, track_name in exercise_track.items():
    if track_name not in exercises_by_track:
        exercises_by_track[track_name] = []
    exercises_by_track[track_name].append((id, exercises[id]))

@app.route('/')
def home():
    return render_template('index.html', exercises=exercises, tracks=exercises_by_track, current_user=current_user)

@app.route('/exercise', methods=['GET', 'POST'])
def exercise():
    if request.method == 'POST':
        exercise_id = request.form['exercise_id']
        student_answer = request.form['answer']
        
        correct_answer = exercise_answers.get(exercise_id)
        
        if student_answer.lower() == correct_answer.lower():
            result_text = 'Correct!'
        else:
            result_text = 'Incorrect!'
        
        # Store the submitted answer in the session
        session[exercise_id] = student_answer
        
        # Get all questions and previously submitted answers for this exercise
        questions = exercise_questions.get(exercise_id)
        answers = [session.get(f'{exercise_id}_{i}', '') for i in range(len(questions))]
        
        return render_template('exercise.html', id=exercise_id, questions=questions, answers=answers)
    else:
        exercise_id = request.args.get('id')
        questions = exercise_questions.get(exercise_id)

        # Get all previously submitted answers for this exercise
        answers = [session.get(f'{exercise_id}_{i}', '') for i in range(len(questions))]

        return render_template('exercise.html', id=exercise_id, questions=questions, answers=answers, exercises=exercises)


@app.route('/exercise/<int:id>', methods=['GET'])
def exercise_with_id(id):
    exercise_id = request.form['exercise_id']
    student_answers = request.form.getlist('answer')
    
    correct_answers = exercise_answers.get(exercise_id)
    result_text = []

    for student_answer, correct_answer in zip(student_answers, correct_answers):
        if student_answer.lower() == correct_answer.lower():
            result_text.append('Correct!')
        else:
            result_text.append('Incorrect!')
    
    # Store the submitted answers in the session
    for i, answer in enumerate(student_answers):
        session[f'{exercise_id}_{i}'] = answer

    return render_template('result.html', result=result_text, id=exercise_id, answers=student_answers, exercises=exercises)


@app.route('/result/<int:id>', methods=['POST'])
def result(id):
    exercise_id = request.form['exercise_id']
    student_answers = request.form.getlist('answer')
    exercise_name = exercises.get(exercise_id)
    questions = exercise_questions.get(exercise_id)
    
    correct_answers = exercise_answers.get(exercise_id)
    result_text = []

    for student_answer, correct_answer in zip(student_answers, correct_answers):
        if student_answer.lower() == correct_answer.lower():
            result_text.append('Correct!')
        else:
            result_text.append('Incorrect!')
    
    # Store the submitted answers in the session
    for i, answer in enumerate(student_answers):
        session[f'{exercise_id}_{i}'] = answer

    return render_template('result.html', result=result_text, id=exercise_id, answers=student_answers, exercise_name=exercise_name, questions=questions)

if __name__ == '__main__':
    app.run(debug=True)
