from flask import Flask, render_template,  redirect,  url_for, request, session
from databaseconnect import Connection
app = Flask(__name__)

app.secret_key = "FBLA"

connection = Connection()
@app.route('/')
def start():
    return redirect(url_for('home'))

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
        if req['Username'] == '' or req['Password'] == '':
            return render_template('loginpage.html', message = "Please enter a valid username and password!")


        user = connection.login(req['Username'], req['Password'])
        if user is None:
            return render_template('loginpage.html', message = "Please enter a valid username and password!")
        else:
            session['username'] = user[0]
            return redirect(url_for('home'))

    return render_template('loginpage.html', message = "")

@app.route('/takequiz', methods= ["GET", "POST"] )
def takequiz():
    if request.method == "POST":
        req = request.form
        print(req)
    return render_template('quizpage.html', questions = [{'type': 'fillblank'}, {'type': 'mult_choice'}])

@app.route('/register',  methods=["GET", "POST"])
def register():
    if request.method == "POST":
        req = request.form
        print(req['Username'])
        if req['Username'] == '' or req['Password'] == '':
            return render_template('register.html', message = "Please enter a valid username and password!")

        connection.create_account(req['Username'], req['Password'])
    return render_template('register.html', message = "")

@app.route('/logout')
def logout():
    if 'username' in session.keys():
        del session['username']
    return redirect(url_for('home'))
app.run()