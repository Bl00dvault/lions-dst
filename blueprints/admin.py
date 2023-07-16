from flask_login import current_user
from blueprints.models import db
from blueprints.models import TestResult, User, Assignment
from flask import Blueprint, request, render_template, redirect, url_for
import csv

admin_blueprint = Blueprint('admin', __name__)


@admin_blueprint.route('/all_results', methods=['GET', 'POST'])
def all_results():
    # Ensure only admin users can access this page
    if not current_user.is_admin:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Fetch all test results
        test_results = db.session.query(TestResult, User, Assignment)\
        .join(User, TestResult.user_id == User.id)\
        .join(Assignment, TestResult.assignment_id == Assignment.id).all()

        # specify the path to your csv file
        csv_file_path = "scores/results.csv"

        # open the file in write mode
        with open(csv_file_path, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            
            # write the header
            writer.writerow(["UserName","ExerciseName", "Score", "Time (seconds)"])
                
            for result, user, assignment in test_results:
                writer.writerow([user.username, assignment.exercise_name, result.score, int(result.time_to_complete)])
        
        return "Results have been written to csv file.", 200

    elif request.method == 'GET':
        # Fetch all test results
        test_results = db.session.query(TestResult, User, Assignment)\
        .join(User, TestResult.user_id == User.id)\
        .join(Assignment, TestResult.assignment_id == Assignment.id).all()

        # Group test results by user
        results_by_user = {}
        for result, user, assignment in test_results:
            if user.username not in results_by_user:
                results_by_user[user.username] = []
            results_by_user[user.username].append({
                'exercise_name': assignment.exercise_name,
                'score': result.score,
                'time_to_complete': int(result.time_to_complete)
            })

        return render_template('all_results.html', results_by_user=results_by_user)