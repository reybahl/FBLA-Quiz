from flask import Flask, render_template, redirect, url_for, request, session, make_response, jsonify
from databaseconnect import Connection
from checkanswers import convert_to_dict, check
import pdfkit
from datetime import datetime
from quiz import Quiz

from settings import Settings
from reports import Reports
from intelligentqa import IntelligentQA

app = Flask(__name__)
app.secret_key = "FBLA"


@app.route('/')  # Main route -- Invoked when user visits domain
def start():
    return redirect(url_for('login'))  # Redirecting to login on start


@app.route('/login', methods=["GET", "POST"])
def login():
    if 'username' in session.keys():
        return redirect(url_for('dashboard'))  # If the user is already logged in --> Redirect them to the dashboard

    return render_template('loginpagefirebase.html')  # Shows the login html page


@app.route('/dashboard', methods=["GET", "POST"])  # When this url is called, it invokes the dashboard function
def dashboard():
    if request.method == "POST":  # Checks if it got a post request
        req = request.form  # Gets form data
        user = req['email']  # Gets email from the form
        session['username'] = user  # Creates a session
        quiz = quiz_ref.get_quiz_in_progress(session['username'])  # Gets a quiz in progress
        quiz_in_progress = True if quiz is not None else False  # Checks if a quiz in progress exists
        return render_template('dashboard.html', email=session['username'],
                               quiz_in_progress=quiz_in_progress)  # Shows dashboard and specifies if the user has a quiz in progress

    if 'username' in session.keys():  # If the user comes directly to the dashboard without the login page, it checks the session to check if the user is signed in
        quiz = quiz_ref.get_quiz_in_progress(session['username'])
        quiz_in_progress = True if quiz is not None else False
        return render_template('dashboard.html', email=session['username'], quiz_in_progress=quiz_in_progress)
    else:  # If the user is not signed in, then redirects them back to the sign in page
        return redirect(url_for('login'))


@app.route('/quiz', methods=["GET", "POST"])  # Quiz generation route
def quiz():
    global questions_answers

    if request.method != "POST":

        generate_quiz_in_progress = request.args.get(
            'quiz_in_progress')  # Gets url argument specifying if the user wants a quiz in progress or wants to start a new one.
        if generate_quiz_in_progress == 'true':
            quizqa = quiz_ref.get_quiz_in_progress(session['username'])
            if quizqa is not None:
                # get correct answers of the quiz progress from the database
                questions_answers = quiz_ref.get_correct_answers(quizqa)
                return render_template('quizinprogress.html', quizqa=quizqa['results'], enumerate=enumerate)
        else:  # If the user wants a new quiz
            quiz_ref.delete_quiz_in_progress(session['username'])  # Deletes any existing quiz
            questions_answers = quiz_ref.generate_quiz(session['username'])  # Generates new quiz
        if 'username' in session.keys():
            return render_template('quizpage.html', questions=questions_answers, enumerate=enumerate)

        else:  # If user is not logged in
            return redirect(url_for('login'))  # Redirect them to login

    if request.method == "POST":
        req = request.form
        if questions_answers is not None:
            results, score = check(questions_answers, list(req.items()))
            print(results)
            date_time = quiz_ref.save_results(session['username'], results,
                                              score)  # saves results and returns the datetime
            quiz_ref.delete_quiz_in_progress(session['username'])  # Deletes the quiz in progress

            return redirect(url_for('generate_report',
                                    datetime=date_time))  # Sends them to the report generation page with the date and time the quiz was submitted as the url argument


@app.route('/generateReport', methods=["GET"])
def generate_report():
    date_time = request.args['datetime']
    if request.method == "GET":
        results = reports_ref.get_report_for_date(session['username'], date_time)
        # These are some options for the PDF report generator

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
        rendered = render_template('resultpagetemplate.html', enumerate=enumerate, results=results['results'],
                                   score=results['score'], date=date, time=time,
                                   prefs=settings_ref.get_prefs(session['username'])['settings'])
        pdf = pdfkit.from_string(rendered, False, options)
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=output.pdf'

        return response


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        req = request.form
        connection.create_account(req['Username'], req['Password'])

    return render_template('register.html', message="")


@app.route('/logout')
def logout():
    if 'username' in session.keys():
        del session['username']  # deleting 'username' from session to logout
    return redirect(url_for('login'))  # Sends them back to login screen


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        prefs = convert_to_dict(request.form.items())
        settings_ref.set_prefs(session['username'], prefs)
        print(prefs)
        # return redirect('/dashboard#settings')

    include_in_quiz_checkbox = {
        'q_number': 'Question numbers',
        'show_name': 'Your Name',
        'date': 'Date Submitted',
        'time': 'Time submitted',
        'score': 'Your Score',
        'showcorrectanswer': 'Correct Answers',
        'showwronganswer': 'Wrong Answers'
    }
    if 'username' in session.keys():
        return render_template('settings.html', prefs=settings_ref.get_prefs(session['username'])['settings'],
                               user=session['username'], include_in_quiz_checkbox=include_in_quiz_checkbox)


@app.route('/reports')
def reports():
    return render_template("reports.html", reports=reports_ref.get_reports(session['username']))


@app.route('/updateCurrentQuizState', methods=['POST'])
def updateCurrentQuizState():
    try:
        if request.method == 'POST':
            quiz_ref.update_quiz_in_progress(session['username'], request.get_json())
    except TypeError:
        pass


@app.route('/getHelp', methods=['POST'])
def getHelp():
    if request.method == 'POST':
        qa = intelligent_qa_ref.get_help(request.get_json())
        return jsonify(qa)


@app.route('/quizInProgressExists', methods=['GET'])
def quizInProgressExists():
    quiz = quiz_ref.get_quiz_in_progress(session['username'])
    if quiz is None:
        return "False"
    else:
        return "True"


@app.route('/about', methods=['GET'])
def aboutPage():
    return render_template('aboutpage.html')


@app.route('/help', methods=['GET'])
def help():
    return render_template('helppage.html', faqs=intelligent_qa_ref.get_frequently_asked_questions())


connection = Connection.Instance()
questions_answers = None
quiz_ref = Quiz()
settings_ref = Settings()
reports_ref = Reports()
intelligent_qa_ref = IntelligentQA()
app.run('localhost')
