from flask import Flask, render_template,  redirect,  url_for, request, session, make_response
from databaseconnect import Connection
from checkanswers import convert_to_dict, check
import pdfkit
import requests

app = Flask(__name__)

app.secret_key = "FBLA"

connection = Connection() 
questions_answers = None

@app.route('/')
def start():
    return redirect(url_for('login'))

@app.route('/home')
def home():
    
    if 'username' in session.keys():
        user= session['username']
    else:
        user = 'None'
    return render_template('homepage.html', user = user)

@app.route('/login',  methods=["GET", "POST"])
def login():
    if request.method == "POST":
        req = request.form
        print(req)
        user = req['email']

        # if user is None:
        #     return render_template('loginpagefirebase.html', message = "Please enter a valid username and password!")

        session['username'] = user
        

    if 'username' in session.keys():
        return redirect(url_for('dashboard'))

    return render_template('loginpagefirebase.html', message = "")

@app.route('/dashboard',  methods=["GET", "POST"])
def dashboard():
    if request.method == "POST":
        req = request.form
        print(req)
        user = req['email']
        session['username'] = user
        return render_template('dashboard.html', email=user)

    if 'username' in session.keys():
        return render_template('dashboard.html', email=session['username'])
    else:
        return redirect(url_for('login'))
@app.route('/quiz', methods= ["GET", "POST"] )
def quiz():

    global questions_answers
    if request.method != "POST":
        questions_answers = connection.generate_quiz()
       
        
    if request.method == "POST":
        req = request.form
        if questions_answers is not None:
            options = {
                        'title': 'Quiz Results',
                        'page-size': 'Letter',
                        'margin-top': '1in',
                        'margin-right': '1in',
                        'margin-bottom': '1in',
                        'margin-left': '1in',
                        'encoding': "UTF-8",
                        }
            results = check(questions_answers, list(req.items()))
            print(results)
            connection.save_results(session['username'], results)
            rendered = render_template('resultpagetemplate.html', results = results )
            pdf = pdfkit.from_string(rendered, False, options)

            response = make_response(pdf)
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = 'inline; filename=output.pdf'

            return response

    if 'username' in session.keys():    
        return render_template('quizpage.html', questions = questions_answers, enumerate = enumerate)
    else:
        return redirect(url_for('login'))

    
        
@app.route('/register',  methods=["GET", "POST"])
def register():
    if request.method == "POST":
        req = request.form
        #print(req['Username'])
        
        connection.create_account(req['Username'], req['Password'])
    return render_template('register.html', message = "")

@app.route('/logout')
def logout():
    if 'username' in session.keys():
        del session['username'] #deleting 'username' from session
    return redirect(url_for('login'))

@app.route('/settings')
def settings():
    include_in_quiz_checkbox = {
        'q_number' : 'Question numbers',
        'show_name' : 'Your Name',
        'time':'Time submitted',
        'showcorrectanswer': 'Correct Answers',
        'showwronganswer':'Wrong Answers'
    }
    if 'username' in session.keys():
        return render_template('settings.html', prefs = connection.get_prefs(session['username'])['settings'], include_in_quiz_checkbox =include_in_quiz_checkbox)

@app.route('/reports')
def reports():
    return redirect(url_for('quiz'))

@app.route('/updatesettings', methods=['POST'])
def updatesettings():
    if request.method == 'POST':
        prefs = convert_to_dict(request.form.items())
        connection.set_prefs(session['username'], prefs)
        print(prefs)
        
    
    return "Settings updated!"

app.run('localhost')
