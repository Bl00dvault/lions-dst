import json
import os
import time
from flask import (Blueprint, redirect, render_template, request, session,
                   url_for)
from blueprints.models import Assignment

# create a blueprint for exercises
exercises_blueprint = Blueprint('exercises', __name__)

# Load exercise data from a JSON file
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
 
@exercises_blueprint.route('/exercise/<int:id>', methods=['GET'])
def exercise_landing_page(id):
    # Fetch the assignment from the database
    assignment = Assignment.query.get(id)
    exercise_name = assignment.exercise_name

    # If no assignment is found, return a 404 error
    if assignment is None:
        return "PDF file not found", 404

    # Extract just the filenames for academics (remove the directory prefix)
    lab_guide_filenames = sorted([f for f in os.listdir('static/academics') if f.startswith(f'{assignment.exercise_name}-Lab') and f.endswith('.pdf')])

    # Extract just the filenames for labguides (remove the directory prefix)
    academics_filenames = sorted([f for f in os.listdir('static/academics') if f.startswith(f'{assignment.exercise_name}') and f.endswith('Academics.pdf')])

    # If no matching files are found, return an error
    if not lab_guide_filenames:
        return render_template('exercise_landing_page.html', id=id, lab_guide_filenames=lab_guide_filenames)
    
    return render_template('exercise_landing_page.html', id=id, lab_guide_filenames=lab_guide_filenames, academics_filenames=academics_filenames, exercise_name=exercise_name)

@exercises_blueprint.route('/exercise/<int:id>/clear', methods=['GET'])
def exercise_clear(id):
    exercise_id = str(id)
    
    # Loop over the session keys for this exercise and delete them
    for i in range(len(session)):
        session.pop(f'{exercise_id}_{i}', None)
    
    return redirect(url_for('exercises.exercise_assessment', id=exercise_id))

@exercises_blueprint.route('/exercise/<int:id>/assessment', methods=['GET', 'POST'])
def exercise_assessment(id):
    exercise_id = str(id)
    student_answers = request.form.getlist('answer')
    exercise_name = exercises.get(exercise_id)

    if request.method == 'POST':
        student_answers = request.form.getlist('answer')

        # Store the current time as the start time for this exercise
        session['start_time'] = time.time()
        
        correct_answers = exercise_answers.get(id)
        result_text = []

        for student_answer, correct_answer in zip(student_answers, correct_answers):
            if student_answer.lower() == correct_answer.lower():
                result_text.append('Correct!')
            else:
                result_text.append('Incorrect!')
        
        # Store the submitted answers in the session
        for i, answer in enumerate(student_answers):
            session[f'{id}_{i}'] = answer

        return render_template('result.html', result=result_text, id=id, answers=student_answers, exercises=exercises, exercise_name=exercise_name)
    elif request.method == 'GET':
        questions = exercise_questions.get(str(id))

        if questions is None:
            # Provide an appropriate message to the user or redirect to another page
            return "No questions found for this exercise id", 400

        # Get all previously submitted answers for this exercise
        answers = [session.get(f'{id}_{i}', '') for i in range(len(questions))]

        # Store the current time as the start time for this exercise
        session['start_time'] = time.time()

        return render_template('exercise.html', id=id, questions=questions, answers=answers, exercises=exercises, exercise_name=exercise_name)
