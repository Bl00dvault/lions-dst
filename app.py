# Author: Thomas "Bl00dvault" Blauvelt
import json
import os
from flask import Flask, render_template
from flask_login import LoginManager, current_user
import keys
from blueprints.admin import admin_blueprint
from blueprints.exercises import (exercises, exercises_blueprint,
                                  exercises_by_track)
from blueprints.models import Assignment, Question, User, db
from blueprints.results import results_blueprint
from blueprints.users import users_blueprint

__version__ = '2.1.1'

app = Flask(__name__, static_url_path='/static')

# Register blueprints
app.register_blueprint(exercises_blueprint, url_prefix='/exercise')
app.register_blueprint(results_blueprint, url_prefix='/results')
app.register_blueprint(users_blueprint, url_prefix='/users')
app.register_blueprint(admin_blueprint, url_prefix='/admin')


app.jinja_env.globals.update(zip=zip)
app.secret_key = keys.secret_key

# Create login database
basedir = os.path.abspath(os.path.dirname(__file__))
if not os.path.exists('db/'):
    os.makedirs('db/')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db/test.db')
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Fetch the user from the database

# Instantiate the new database
def init_db():
    db.create_all()
    
    # check if admin exists
    admin = User.query.filter_by(username='admin').first()
    
    # if admin does not exist, create one
    if admin is None:
        admin = User(username='admin')
        admin.set_password('asdf')
        admin.is_admin = True
        db.session.add(admin)
        db.session.commit()

with app.app_context():
    init_db()
    with open('exercises.json', 'r') as file:
        data = json.load(file)

    for exercise in data:
        assignment = Assignment.query.filter_by(exercise_name=exercise["ExerciseName"]).first()

        if assignment is None:
            assignment = Assignment(exercise_name=exercise["ExerciseName"], track=exercise["Track"])
            db.session.add(assignment)
            db.session.commit()

        for question_text, correct_answer in exercise["Questions"].items():
            question = Question(question_text=question_text, correct_answer=correct_answer, assignment_id=assignment.id)
            db.session.add(question)

    db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Fetch the user from the database

@app.context_processor
def inject_version():
    return dict(version=__version__)

@app.route('/')
def home():
    return render_template('index.html', exercises=exercises, tracks=exercises_by_track, current_user=current_user)

@app.route('/help')
def help():
    return render_template('help.html')

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(host='0.0.0.0', port=5001, debug=True)
