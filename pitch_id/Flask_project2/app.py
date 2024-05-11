from flask import Flask, render_template, request, redirect, url_for, session
from main_generation import*
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key
@app.route('/')
def index():
    feedback = session.pop('feedback', None)
    # Ensure `image_path` is retrieved from session or set a default if it's not there
    image_path = session.get('image_path', url_for('static', filename='images/cropped_score_f.png'))
    return render_template('index.html', image_path=image_path, note_letters=note_letters, accidentals=accidentals, feedback=feedback)

@app.route('/new_question', methods=['GET'])
def new_question():
    if 'treble_e' not in session:
        session['treble_e'] = 0
    if 'bass_e' not in session:
        session['bass_e'] = 0
    if 'correct_c' not in session:
        session['correct_c'] = 0
        print("correct_c")
    if "idx" not in session:
        session['idx']= 0
        print("start")
    elif session['idx'] != 0 and session['idx'] % 20 ==0:
        session['idx'] =0
        session['treble_e']=0
        session['bass_e']=0
        session['correct_c']=0
    else: 
        session['idx'] += 1
    idx = session['idx']
    treble_e = session.get('treble_e')
    bass_e = session.get('bass_e')
    correct_c = session.get('correct_c')
    image_path = url_for('static', filename=f'images/cropped_score_f.png')
    if os.path.exists(image_path):
        os.remove(image_path)
    clef, note, idx = idx_score_generation(idx, treble_e, bass_e, correct_c)
    current_answer = f"{note} {accidentals[1]}"
    # Store the answer and image_path in the session
    session['current_answer'] = current_answer
      # Assuming you have a naming pattern for the images
    session['image_path'] = image_path
    session.pop('feedback', None)  # Remove feedback from session
    session["clef"] = clef
    
    return render_template('index.html', image_path=image_path, note_letters=note_letters, accidentals=accidentals, clef = clef)

@app.route('/check_answer', methods=['POST'])
def check_answer():
    user_ans = f"{request.form['note_letter']} {request.form['accidental']}"
    current_answer = session.get('current_answer')
    correct_c = session.get('correct_c', 0) # Default to 0 if not set
    treble_e = session.get('treble_e', 0) # Default to 0 if not set
    bass_e = session.get('bass_e', 0) # Default to 0 if not set
    clef = session.get('clef')
    if current_answer is None:
        feedback = 'Error: No current answer available. Please try a new question.'
    elif user_ans.lower() == current_answer.lower():
        feedback = 'Correct!'
        session['correct_c'] += 1
    else:
        feedback = f'Incorrect. The answer should be {current_answer}'
        if clef == "treble":
            session['treble_e'] = treble_e + 1
        elif clef == "bass":
            session['bass_e'] = bass_e + 1
            
    session['feedback'] = feedback
    return redirect(url_for('index'))
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8500)