from flask import Flask, render_template,  redirect,  url_for, request

app = Flask(__name__)

@app.route('/')
def start():
    return redirect(url_for("home"))

@app.route('/home')
def home():
    return render_template('homepage.html')

@app.route('/login',  methods=["GET", "POST"])
def login():
    if request.method == "POST":
        req = request.form
        print(req)
        if req['Username'] == '' or req['Password'] == '':
            return render_template('loginpage.html', message = "Please enter a valid username and password!")
        
    return render_template('loginpage.html', message = "")

@app.route('/takequiz', methods= ["GET", "POST"] )
def takequiz():
    if request.method == "POST":
        req = request.form
        print(req)
    return render_template('quizpage.html', Q1name = "Question !1!", Q1type = "text")

@app.route('/register',  methods=["GET", "POST"])
def register():
    if request.method == "POST":
        req = request.form
        print(req)
        if req['Username'] == '' or req['Password'] == '':
            return render_template('register.html', message = "Please enter a valid username and password!")
    return render_template('register.html', message = "")
app.run()