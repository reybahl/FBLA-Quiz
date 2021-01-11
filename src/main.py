"""FBLA Main
.. moduleauthor:: Reyansh Bahl <https://github.com/reybahl>
"""

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


@app.route('/')
def start():
    """Main route -- Invoked when user visits domain
    When this function is invoked, the user is redirected to a login
    screen where users can login via email/password or Google sign-in.
    Users can also reset their password on login page.

    :return: Response object as a result of redirecting to the login page
    """
    return redirect(url_for('login'))  # Redirecting to login on start


@app.route('/login', methods=["GET", "POST"])
def login():
    """Login page, redirected from main. If the user is already logged in
    it redirects them straight to the dashboard, otherwise show the login page.
    At login screen, users first need to register (if not already registered)
    and then enter their email and password. Alternatively they can also
    use their Google Account to sign-in. They can also reset their password
    in case they forget. For reset, they will need to enter the email id
    that was used to register and on clicking reset, an email will be sent
    to the user where they can click on a link and reset their password.

    :return: Response object as a result of redirecting to the dashboard if 
             user is already logged in, other response object for loginpagefirebase.html
    """
    # Checks if it got a post request
    if request.method == "POST":
        # Gets form data
        req = request.form
        # Gets email from the form
        user = req['email']
        # Creates a session
        session['username'] = user
        return "Logged in"
        
    if 'username' in session.keys():
        return redirect(url_for('dashboard'))

    return render_template('loginpagefirebase.html')  # Shows the login html page


@app.route('/dashboard', methods=["GET", "POST"])
def dashboard():
    """Dashboard page, redirected from login screen. This page presents options to the 
    user to take a quiz, view reports etc. By default the selection option is to take
    a quiz. If user already has a quiz in progress, user can see buttons to resume
    existing quiz or take a new quiz.

    :return: Response object which contains dashboard html with quiz tab selected.
    """
    # Gets a quiz in progress
    quiz = quiz_ref.get_quiz_in_progress(session['username'])
    # Checks if a quiz in progress exists
    quiz_in_progress = True if quiz is not None else False
    # Shows dashboard and specifies if the user has a quiz in progress
    return render_template('dashboard.html', email=session['username'],
                            quiz_in_progress=quiz_in_progress)

    # If the user comes directly to the dashboard without the login page, it checks the session to check if the user is signed in
    if 'username' in session.keys():
        quiz = quiz_ref.get_quiz_in_progress(session['username'])
        quiz_in_progress = True if quiz is not None else False
        return render_template('dashboard.html', email=session['username'], quiz_in_progress=quiz_in_progress)
    else:  # If the user is not signed in, then redirects them back to the sign in page
        return redirect(url_for('login'))

@app.route('/quiz', methods=["GET", "POST"])
def quiz():
    """Quiz page, redirected from dashboard. Here code first checks to see if the 
    user already has a quiz in progress, if yes, it get the current state of the quiz
    from the database. If the user clicked on start a new quiz, this method generates
    a new quiz.

    :return: Response object of quiz in progress or a new quiz based upon what user selected.
    """
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
    """Generates report when a quiz is submitted or user clicks on generate report
    in the reports tab.
    
    :return: Response object that contains a generated report in PDF file format.
    """
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

@app.route('/logout')
def logout():
    """Logs out a user out of the session and removes the username from the 
    session object and sens them back to the login screen.
    
    :return: Response object that contains main login screen.
    """
    if 'username' in session.keys():
        del session['username']
    return redirect(url_for('login'))  # Sends them back to login screen


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    """Presents users with a settings screen for the purpose of report generation.
    It includes various options like font size, and content to include.
    
    :return: Response object that contains settings screen.
    """
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
    """Show the historical quiz that the user has taken. It also presents
    an option to generate PDF report for each run.
    
    :return: Response object that contains historical reports screen.
    """
    return render_template("reports.html", reports=reports_ref.get_reports(session['username']))


@app.route('/updateCurrentQuizState', methods=['POST'])
def updateCurrentQuizState():
    """Updates user's current quiz in progress as and when user changes 
    anything. This function updates the quiz state in the database.
    """
    try:
        if request.method == 'POST':
            quiz_ref.update_quiz_in_progress(session['username'], request.get_json())
    except TypeError:
        pass


@app.route('/getHelp', methods=['POST'])
def getHelp():
    """Intelligent Q&A feature: This gets called when user types a
    question in get help chat window. It uses Naive Bayes algorithm
    to classify what category the question falls in and based upon that
    it returns the corrresponding help related to that category. The
    categories and corresponding help is stored in the database.
    Example::
            User types in: How can I customize font in reports
            Category: reportgeneration
    
    :return: List of questions and answers corresponding to category of the 
             question that user has asked.
    """
    if request.method == 'POST':
        qa = intelligent_qa_ref.get_help(request.get_json())
        return jsonify(qa)


@app.route('/quizInProgressExists', methods=['GET'])
def quizInProgressExists():
    """Checks if there's a current quiz in progress for the user.
    
    :return: True if the user has a quiz in progress, False otherwise
    """
    quiz = quiz_ref.get_quiz_in_progress(session['username'])
    if quiz is None:
        return "False"
    else:
        return "True"


@app.route('/about', methods=['GET'])
def aboutPage():
    """Shows About Page with the links to this documentation.
    
    :return: Response object that contains about page.
    """
    return render_template('aboutpage.html')


@app.route('/help', methods=['GET'])
def help():
    """Shows FAQs
    
    :return: Response object that contains FAQs page.
    """
    return render_template('helppage.html', faqs=intelligent_qa_ref.get_frequently_asked_questions())

@app.route('/getStarted', methods=['GET'])
def getStarted():
    """Shows a list of instructions to get started using FBLA Quiz

    :return: Response object that contains Get Started HTML page
    """

    return render_template("getstarted.html")
connection = Connection.Instance()
questions_answers = None
quiz_ref = Quiz()
settings_ref = Settings()
reports_ref = Reports()
intelligent_qa_ref = IntelligentQA()
app.run('localhost')
