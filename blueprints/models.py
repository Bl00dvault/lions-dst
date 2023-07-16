from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

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

class TestResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    assignment_id = db.Column(db.Integer)
    score = db.Column(db.Integer)
    time_to_complete = db.Column(db.Float, nullable=False)
    answers = db.Column(db.String(500))

    def __repr__(self):
        return f'<TestResult {self.id}>'

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exercise_name = db.Column(db.String(64), unique=True, nullable=False)
    track = db.Column(db.String(64), nullable=False)
    questions = db.relationship('Question', backref='assignment', lazy=True)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(255), nullable=False)
    correct_answer = db.Column(db.String(255), nullable=False)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'), nullable=False)