from flask import Flask, render_template, request, session
import json

app = Flask(__name__, static_url_path='/static')
app.jinja_env.globals.update(zip=zip)
app.secret_key = 'your_secret_key'

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
    return render_template('index.html', exercises=exercises, tracks=exercises_by_track)

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
