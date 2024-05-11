from flask import Flask, render_template, request, redirect, url_for, session
from generation import*
from element import user_quality,user_interval
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key
@app.route('/')
def index():
    feedback = session.pop('feedback', None)
    # Ensure `image_path` is retrieved from session or set a default if it's not there
    image_path = session.get('image_path', url_for('static', filename='images/cropped_score_ans.png'))
    correction_rate = session.get('correction_rate', 0.0)
    return render_template('index.html', 
                           image_path=image_path, 
                           user_quality=user_quality, 
                           user_interval=user_interval, 
                           feedback=feedback, 
                           correction_rate=correction_rate)
@app.route('/set_difficulty', methods=['POST'])
def set_difficulty():
    difficulty = request.form.get('difficulty', '0')
    session['difficulty'] = int(difficulty)  # Store difficulty level in session
    return redirect(url_for('index'))  # Redirect to the main page

@app.route('/new_question', methods=['GET'])
def new_question():
    if 'total_questions' not in session:
        session['total_questions'] = 0
    if 'correct_c' not in session:
        session['correct_c'] = 0
    if "idx" not in session:
        session['idx']= 0
    elif session['idx'] != 0 and session['idx'] % 20 ==0:
        session['idx'] =0
        session['correct_c']=0
    else: 
        session['idx'] += 1
    idx = session['idx']
    session['total_questions'] += 1
    correct_c = session.get('correct_c')
    image_path = url_for('static', filename='images/cropped_score_ans.png')
    difficulty = session.get('difficulty', 0)  # Get the stored difficulty level, default to 0

    selected_clefs = session.get('selected_clefs')
    print("selected_clefs", selected_clefs)
    ans, clef, clef2, fix_octave1, fix_octave2, note, note2 = score_generation(level=difficulty)
    lilypond_generation(clef, clef2,fix_octave1,fix_octave2,note,note2)
    session['current_answer'] = ans
    session['image_path'] = image_path
    session.pop('feedback', None)  # Remove feedback from session
    
    return render_template('index.html', image_path=image_path, user_quality=user_quality, user_interval=user_interval)

@app.route('/check_answer', methods=['POST'])
def check_answer():
    user_ans = f"{request.form['user_quality']} {request.form['user_interval']}"
    current_answer = session.get('current_answer')
    correct_c = session.get('correct_c', 0) # Default to 0 if not set

    if current_answer is None:
        feedback = 'Error: No current answer available. Please try a new question.'
    elif user_ans.lower() == current_answer.lower():
        feedback = 'Correct!'
        session['correct_c'] += 1
    else:
        feedback = f'Incorrect. The answer should be {current_answer}'
    total_questions = session.get('total_questions', 1)  # Avoid division by zero
    correct_c = session.get('correct_c', 0)
    correction_rate = (correct_c / total_questions) *100
    session['correction_rate'] = correction_rate        
    session['feedback'] = feedback
    return redirect(url_for('index'))

@app.route('/set_preferences', methods=['POST'])
def set_preferences():
    selected_clefs = request.form.get('selected_clefs', '').split(',')
    session['selected_clefs'] = selected_clefs
    session['accidental'] = request.form['accidental']
    
    return redirect(url_for('new_question'))
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8500)