from flask import Flask, render_template,  redirect,  url_for, request, session, make_response, jsonify
from databaseconnect import Connection
from checkanswers import convert_to_dict, check
import pdfkit
import requests
from datetime import datetime
#import fpdf
# class MyPDF(fpdf.FPDF, fpdf.HTMLMixin):
#     pass

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
        #first check if a quiz is in progress, if yes, show that quiz, otherwise show screen to generate a new quiz
        quizqa = connection.get_quiz_in_progress(session['username'])
        if quizqa is not None:
            #get correct answers from database
            questions_answers = connection.get_correct_answers(quizqa)
            return render_template('quizinprogress.html', quizqa = quizqa['results'], enumerate = enumerate)
        questions_answers = connection.generate_quiz(session['username'])
        if 'username' in session.keys():
            return render_template('quizpage.html', questions = questions_answers, enumerate = enumerate)
        else:
            return redirect(url_for('login'))
    if request.method == "POST":
        req = request.form
        if questions_answers is not None:

            results, score = check(questions_answers, list(req.items()))
            print(results)
            date_time = connection.save_results(session['username'], results, score)
            connection.delete_quiz_in_progress(session['username'])

            return redirect(url_for('generate_report', datetime = date_time))

@app.route('/generateReport',methods=["GET"])
def generate_report():
    date_time = request.args['datetime']
    if request.method == "GET":
        results = connection.get_report_for_date(session['username'], date_time)
        options = {
                        'title': 'Quiz Results',
                        'page-size': 'Letter',
                        'margin-top': '1in',
                        'margin-right': '1in',
                        'margin-bottom': '1in',
                        'margin-left': '1in',
                        'encoding': "UTF-8",
                        }
        user_date_time = results['datetimesubmitted']
        user_date_time = datetime.strptime(user_date_time, '%c')
        date = user_date_time.date()
        time = user_date_time.time()
        rendered = render_template('resultpagetemplate.html', enumerate = enumerate, results = results['results'], score= results['score'], date = date, time = time, prefs = connection.get_prefs(session['username'])['settings'])
        pdf = pdfkit.from_string(rendered, False, options)
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=output.pdf'

        return response
        
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

@app.route('/settings', methods = ['GET', 'POST'])
def settings():
    if request.method == 'POST':
        prefs = convert_to_dict(request.form.items())
        connection.set_prefs(session['username'], prefs)
        print(prefs)
        return redirect(url_for('dashboard'))
        
    include_in_quiz_checkbox = {
        'q_number' : 'Question numbers',
        'show_name' : 'Your Name',
        'date' : 'Date Submitted',
        'time':'Time submitted',
        'score' : 'Your Score',
        'showcorrectanswer': 'Correct Answers',
        'showwronganswer':'Wrong Answers'
    }
    if 'username' in session.keys():
        return render_template('settings.html', prefs = connection.get_prefs(session['username'])['settings'], include_in_quiz_checkbox =include_in_quiz_checkbox)
@app.route('/reports')
def reports():
    return render_template("reports.html", reports = connection.get_reports(session['username']))

@app.route('/updateCurrentQuizState', methods=['POST'])
def updateCurrentQuizState():
    if request.method == 'POST':
        connection.update_quiz_in_progress(session['username'], request.get_json())

@app.route('/getHelp', methods=['POST'])
def getHelp():
    if request.method == 'POST':
        qa = connection.get_help(request.get_json())
        return jsonify(qa)
        
app.run('localhost')
