import csv
import time
from flask import (Blueprint, json, redirect, render_template, request,
                   session, url_for)
from flask_login import current_user
from blueprints.exercises import (exercise_answers, exercise_questions,
                                  exercises)
from blueprints.models import Assignment, TestResult, User, db

results_blueprint = Blueprint('results', __name__)

@results_blueprint.route('/result/<int:id>', methods=['POST'])
def result(id):
    exercise_id = str(id)
    student_answers = request.form.getlist('answer')
    exercise_name = exercises.get(exercise_id)
    questions = exercise_questions.get(exercise_id)
    correct_answers = exercise_answers.get(exercise_id)
    result_text = []
    start_time = session.get('start_time')
    end_time = time.time()  # The current time is the end time of the test

    for student_answer, correct_answer in zip(student_answers, correct_answers):
        if student_answer.lower() == correct_answer.lower():
            result_text.append('Correct!')
        else:
            result_text.append('Incorrect!')
    
    # Calculate the score as the number of correct answers
    score = int(result_text.count('Correct!') / len(questions) * 100)

    # Store the submitted answers in the session
    for i, answer in enumerate(student_answers):
        session[f'{exercise_id}_{i}'] = answer
    
    # Store the test result in the database
    time_to_complete = int(end_time - start_time)
    test_result = TestResult(
        user_id=current_user.id,
        assignment_id=exercise_id,
        score=score,
        time_to_complete=time_to_complete,
        answers=json.dumps(student_answers)  # Store the answers as a JSON string
    )
    db.session.add(test_result)
    db.session.commit()

    return render_template('result.html', result=result_text, id=exercise_id, answers=student_answers, exercise_name=exercise_name, questions=questions, correct_answers=correct_answers, exercises=exercises, test_result=test_result)

@results_blueprint.route('/all_results', methods=['GET', 'POST'])
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