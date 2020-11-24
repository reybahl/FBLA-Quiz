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

    return render_template('loginpage.html')

@app.route('/takequiz', methods= ["GET", "POST"] )
def takequiz():
    if request.method == "POST":
        req = request.form
        print(req)
    return render_template('quizpage.html', Q1name = "Question !1!", Q1type = "text")

app.run()